import decimal
import pandas as pd
import pyhash

from numpy.random import RandomState
from six import string_types


def is_integer(num):
    try:
        int(num)
        return True
    except ValueError:
        return False


def num_decimal_places(number):
    return abs(decimal.Decimal(number).as_tuple().exponent)


def hash_as_int32(thing):
    hasher = pyhash.city_32()
    return hasher(str(thing))


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
        number = row.parsed_answer
        float(number)  # Check the answer is a number.

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
        if is_integer(number):
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
        return [row.parsed_answer, "0", "1", "2"], 0

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
