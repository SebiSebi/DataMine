import numpy as np
import pandas as pd
import pyhash
import six

from copy import deepcopy
from data_mine.utils import is_integer, num_decimal_places
from numpy.random import RandomState
from six import string_types
from .utils import serialize_date


def hash_as_int32(thing):
    hasher = pyhash.city_32()
    if six.PY2:  # pragma: no cover
        thing = unicode(thing)  # noqa: F821
    else:  # pragma: no cover
        thing = str(thing)
    return hasher(thing)


def DROP2MC(df):
    """
    TODO(sebisebi): add description.
    """

    # Returns true if we can alter the question so as to make it a
    # multiple-choice question. Currently this is possible if and only
    # if the answer is a number or a date.
    def is_good_question(row):
        answer_type = row.answer_type
        assert(answer_type in ["number", "date", "spans"])
        return answer_type in ["number", "date"]

    def alter_number(row):
        assert(row.answer_type == "number")
        number = row.parsed_answer
        float(number)  # Check that the answer is a number.

        # Cases:
        # int and > 20 then generate numbers of the same range.
        # for years: 1948, do not generate 15xx, but only 19xx.

        # Use this random generator (instead of the global state) to get
        # determinstic results. We seed the generator depending on the
        # query_id and the question. Be aware that numpy requires the seed
        # to be an integer between 0 and 2**32 - 1 inclusive.
        seed = hash_as_int32(row.query_id + " - " + row.question)
        assert(0 <= seed <= (2 ** 32) - 1)
        prng = RandomState(seed)
        choices = []
        if is_integer(number) and num_decimal_places(number) == 0:
            number = int(number)
            step_interval = None  # both ends are inclusive.
            if abs(number) <= 20:
                step_interval = (1, 1)
            elif abs(number) <= 99:
                step_interval = (1, 4)
            elif abs(number) <= 999:
                step_interval = (1, 7)
            else:
                step_interval = (1, number // 100)
            upper_bound = number
            lower_bound = number
            for _ in range(0, 3):
                if prng.randint(0, 10000) % 2 == 0:
                    upper_bound += prng.randint(step_interval[0], step_interval[1] + 1)  # noqa: E501
                    choices.append(upper_bound)
                else:
                    lower_bound -= prng.randint(step_interval[0], step_interval[1] + 1)  # noqa: E501
                    choices.append(lower_bound)
            choices.append(row.parsed_answer)
            choices = list(map(str, choices))
        else:
            # Most float numbers are percentages.
            number = float(number)
            step_interval = (number / 100.0, number / 25.0)
            if step_interval[0] < 0.1:
                step_interval = (0.1, 0.5)
            upper_bound = number
            lower_bound = number
            for _ in range(0, 3):
                if prng.randint(0, 10000) % 2 == 0:
                    upper_bound += prng.uniform(step_interval[0], step_interval[1])  # noqa: E501
                    choices.append(upper_bound)
                else:
                    lower_bound -= prng.uniform(step_interval[0], step_interval[1])  # noqa: E501
                    choices.append(lower_bound)

            # Limit to the same number of decimal points.
            precision = num_decimal_places(row.parsed_answer)
            assert(precision >= 1)
            choices = list(map(lambda x: '{:.{prec}f}'.format(x, prec=precision), choices))  # noqa: E501

            # Some answers in DROP are listed as '.1', '.2'. Make sure we have
            # such numbers in the dataset to remove the possibility of
            # guessing the correct answer just by looking if the number starts
            # with '.'.
            if row.parsed_answer[:1] == "." or row.parsed_answer[:2] == "0.":
                for i, choice in enumerate(choices):
                    if choice[:2] == "0.":
                        if prng.randint(0, 10) <= 7:
                            choices[i] = choice[1:]
            choices.append(row.parsed_answer)

        # All choices must be strings.
        for choice in choices:
            assert(isinstance(choice, string_types))
        assert(len(set(choices)) == 4)  # Choices are distinct.
        assert(len(set([float(x) for x in choices])) == 4)  # 0.1 vs .1
        assert(choices[-1] == row.parsed_answer)

        choices.sort(key=lambda choice: hash_as_int32(choice + " ! " + row.query_id))  # noqa: E501
        assert(choices.count(row.parsed_answer) == 1)
        return choices, choices.index(row.parsed_answer)

    def alter_date(row):
        assert(row.answer_type == "date")

        # Use this random generator (instead of the global state) to get
        # determinstic results. We seed the generator depending on the
        # query_id and the question. Be aware that numpy requires the seed
        # to be an integer between 0 and 2**32 - 1 inclusive.
        seed = hash_as_int32(row.query_id + " - " + row.question)
        assert(0 <= seed <= (2 ** 32) - 1)
        prng = RandomState(seed)

        original_date = row.original_answer["date"]
        assert(len(original_date) == 3)
        year_upper_bound = int(str(original_date['year']) or 2020)
        year_lower_bound = year_upper_bound
        choices = [serialize_date(original_date)]
        while len(choices) < 4:
            date = deepcopy(original_date)
            mask = prng.randint(low=1, high=8)  # 8 is exclusive.
            if len(date['day']) > 0 and (mask & 1) != 0:
                day = int(date['day'])
                # Ignore issues with February.
                possible_days = np.arange(1, 31).tolist()  # without 31.
                if day in possible_days:
                    possible_days.remove(day)
                date['day'] = str(prng.choice(possible_days))
            if len(date['month']) > 0 and (mask & 2) != 0:
                month = date['month']
                possible_months = [
                        "January",
                        "February",
                        "March",
                        "April",
                        "May",
                        "June",
                        "July",
                        "August",
                        "September",
                        "October",
                        "November",
                        "December",
                ]
                if month in possible_months:
                    possible_months.remove(month)
                date['month'] = prng.choice(possible_months)
            if len(date['year']) > 0 and (mask & 4) != 0:
                year = None
                if prng.randint(0, 10000) % 2 == 0:
                    year_upper_bound += prng.randint(1, 3)
                    year = year_upper_bound
                else:
                    year_lower_bound -= prng.randint(1, 3)
                    year = year_lower_bound
                date['year'] = str(year)

            # Skip duplicate choices
            date = serialize_date(date)
            if date not in choices:
                choices.append(date)

        assert(len(set(choices)) == 4)  # Unique choices.
        assert(choices[0] == row.parsed_answer)

        choices.sort(key=lambda choice: hash_as_int32(choice + " ! " + row.query_id))  # noqa: E501
        assert(choices.count(row.parsed_answer) == 1)
        return choices, choices.index(row.parsed_answer)

    all_data = []
    df = df[df.apply(is_good_question, axis=1)].reset_index(drop=True)
    for _, row in df.iterrows():
        choices, correct_answer = None, None
        answer_type = row.answer_type
        if answer_type == "number":
            choices, correct_answer = alter_number(row)
        else:
            assert(answer_type == "date")
            choices, correct_answer = alter_date(row)
        assert(choices[correct_answer] == row.parsed_answer)
        correct_answer = chr(ord('A') + correct_answer)
        assert(correct_answer in ['A', 'B', 'C', 'D'])
        all_data.append({
            'query_id': row.query_id,
            'question': row.question,
            'passage': row.passage,
            'answers': choices,
            'correct': correct_answer
        })

    df = pd.DataFrame(all_data)
    return df
