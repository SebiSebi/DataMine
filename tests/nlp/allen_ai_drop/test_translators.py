import json
import pandas as pd
import random
import unittest

from data_mine.nlp.allen_ai_drop import DROP2MC
from data_mine.nlp.allen_ai_drop.translators import hash_as_int32
from faker import Faker

MOCK_QUESTIONS_DF = pd.DataFrame([
    {
        "query_id": "qid1",
        "question": "Question 1?",
        "passage": "Passage 1",
        "answer_type": "spans",
        "parsed_answer": "Chaz Schilens",
        "original_answer": None
    },
    {
        "query_id": "qid2",
        "question": "Question 2?",
        "passage": "Passage 1",
        "answer_type": "number",
        "parsed_answer": "-4",
        "original_answer": None
    },
    {
        "query_id": "qid3",
        "question": "Question 3?",
        "passage": "Passage 1",
        "answer_type": "number",
        "parsed_answer": "0",
        "original_answer": None
    },
    {
        "query_id": "qid4",
        "question": "Question 4?",
        "passage": "Passage 1",
        "answer_type": "number",
        "parsed_answer": "20",
        "original_answer": None
    },
    {
        "query_id": "qid5",
        "question": "Question 5?",
        "passage": "Passage 1",
        "answer_type": "number",
        "parsed_answer": "90",
        "original_answer": None
    },
    {
        "query_id": "qid6",
        "question": "Question 6?",
        "passage": "Passage 1",
        "answer_type": "number",
        "parsed_answer": "700",
        "original_answer": None
    },
    {
        "query_id": "qid7",
        "question": "Question 7?",
        "passage": "Passage 1",
        "answer_type": "number",
        "parsed_answer": "1000",
        "original_answer": None
    },
    {
        "query_id": "qid8",
        "question": "Question 8?",
        "passage": "Passage 1",
        "answer_type": "number",
        "parsed_answer": "1000000",
        "original_answer": None
    },
    {
        "query_id": "qid9",
        "question": "Question 9?",
        "passage": "Passage 2",
        "answer_type": "number",
        "parsed_answer": "0.00001",
        "original_answer": None
    },
    {
        "query_id": "qid10",
        "question": "Question 10?",
        "passage": "Passage 2",
        "answer_type": "number",
        "parsed_answer": "1.0",
        "original_answer": None
    },
    {
        "query_id": "qid11",
        "question": "Question 11?",
        "passage": "Passage 2",
        "answer_type": "number",
        "parsed_answer": "3.14",
        "original_answer": None
    },
    {
        "query_id": "qid12",
        "question": "Question 12?",
        "passage": "Passage 2",
        "answer_type": "number",
        "parsed_answer": "45.321",
        "original_answer": None
    },
    {
        "query_id": "qid13",
        "question": "Question 13?",
        "passage": "Passage 2",
        "answer_type": "number",
        "parsed_answer": "87.4152",
        "original_answer": None
    },
    {
        "query_id": "qid14",
        "question": "Question 14?",
        "passage": "Passage 2",
        "answer_type": "number",
        "parsed_answer": "95.2",
        "original_answer": None
    },
    {
        "query_id": "qid15",
        "question": "Question 15?",
        "passage": "Passage 2",
        "answer_type": "number",
        "parsed_answer": "10412.123456",
        "original_answer": None
    },
    {
        "query_id": "qid16",
        "question": "Question 16?",
        "passage": "Passage 2",
        "answer_type": "number",
        "parsed_answer": ".023",
        "original_answer": None
    },
    {
        "query_id": "qid17",
        "question": "Question 17?",
        "passage": "Passage 2",
        "answer_type": "number",
        "parsed_answer": ".323232",
        "original_answer": None
    },
    {
        "query_id": "qid18",
        "question": "Question 18?",
        "passage": "Passage 3",
        "answer_type": "date",
        "parsed_answer": "18 March 1988",
        "original_answer": json.loads("""
            {
                "number": "",
                "date": {
                    "day": "18",
                    "month": "March",
                    "year": "1988"
                },
                "spans": []
            }
        """)
    },
    {
        "query_id": "qid19",
        "question": "Question 19?",
        "passage": "Passage 3",
        "answer_type": "date",
        "parsed_answer": "January 2000",
        "original_answer": json.loads("""
            {
                "number": "",
                "date": {
                    "day": "",
                    "month": "January",
                    "year": "2000"
                },
                "spans": []
            }
        """)
    },
    {
        "query_id": "qid20",
        "question": "Question 20?",
        "passage": "Passage 3",
        "answer_type": "date",
        "parsed_answer": "13 April",
        "original_answer": json.loads("""
            {
                "number": "",
                "date": {
                    "day": "13",
                    "month": "April",
                    "year": ""
                },
                "spans": []
            }
        """)
    },
    {
        "query_id": "qid21",
        "question": "Question 21?",
        "passage": "Passage 3",
        "answer_type": "date",
        "parsed_answer": "30",
        "original_answer": json.loads("""
            {
                "number": "",
                "date": {
                    "day": "30",
                    "month": "",
                    "year": ""
                },
                "spans": []
            }
        """)
    },
    {
        "query_id": "qid22",
        "question": "Question 22?",
        "passage": "Passage 3",
        "answer_type": "date",
        "parsed_answer": "September",
        "original_answer": json.loads("""
            {
                "number": "",
                "date": {
                    "day": "",
                    "month": "September",
                    "year": ""
                },
                "spans": []
            }
        """)
    },
    {
        "query_id": "qid23",
        "question": "Question 23?",
        "passage": "Passage 3",
        "answer_type": "date",
        "parsed_answer": "2020",
        "original_answer": json.loads("""
            {
                "number": "",
                "date": {
                    "day": "",
                    "month": "",
                    "year": "2020"
                },
                "spans": []
            }
        """)
    }
])


class TestAllenAIDropTranslators(unittest.TestCase):

    def test_hash_as_int32(self):
        # Function must be deterministic.
        hash1 = hash_as_int32(12)
        hash2 = hash_as_int32("some msg")
        for _ in range(0, 100):
            self.assertEqual(hash_as_int32(12), hash1)
            self.assertEqual(hash_as_int32("some msg"), hash2)
        self.assertEqual(hash1, 1400566580)
        self.assertEqual(hash2, 3045715110)

        # Function must return values between 0 and 2**32 - 1.
        fake = Faker(['it_IT', 'en_US', 'ja_JP'])  # Generate unicode.
        for _ in range(0, 200):
            thing = None
            choice = random.choice([1, 2, 3, 4, 5])
            if choice == 1:
                thing = fake.pydict(10, False, str, int, bool)
            elif choice == 2:
                thing = fake.address()
            elif choice == 3:
                thing = fake.text()
            elif choice == 4:
                thing = random.randint(0, (2 ** 32) - 1)
            elif choice == 5:
                thing = fake.name()
            self.assertIsNotNone(thing)
            h = hash_as_int32(thing)
            assert(0 <= h <= (2 ** 32) - 1)

    def test_drop_2_multiple_choice(self):
        df = DROP2MC(MOCK_QUESTIONS_DF)
        expected_df = pd.DataFrame(json.loads("""
        [
            {
                "query_id": "qid2",
                "question": "Question 2?",
                "passage": "Passage 1",
                "answers": [
                    "-4",
                    "-2",
                    "-5",
                    "-3"
                ],
                "correct": "A"
            },
            {
                "query_id": "qid3",
                "question": "Question 3?",
                "passage": "Passage 1",
                "answers": [
                    "-1",
                    "0",
                    "2",
                    "1"
                ],
                "correct": "B"
            },
            {
                "query_id": "qid4",
                "question": "Question 4?",
                "passage": "Passage 1",
                "answers": [
                    "20",
                    "18",
                    "19",
                    "17"
                ],
                "correct": "A"
            },
            {
                "query_id": "qid5",
                "question": "Question 5?",
                "passage": "Passage 1",
                "answers": [
                    "91",
                    "90",
                    "87",
                    "92"
                ],
                "correct": "B"
            },
            {
                "query_id": "qid6",
                "question": "Question 6?",
                "passage": "Passage 1",
                "answers": [
                    "700",
                    "696",
                    "703",
                    "690"
                ],
                "correct": "A"
            },
            {
                "query_id": "qid7",
                "question": "Question 7?",
                "passage": "Passage 1",
                "answers": [
                    "1010",
                    "1000",
                    "992",
                    "990"
                ],
                "correct": "B"
            },
            {
                "query_id": "qid8",
                "question": "Question 8?",
                "passage": "Passage 1",
                "answers": [
                    "1000000",
                    "997092",
                    "995317",
                    "1001470"
                ],
                "correct": "A"
            },
            {
                "query_id": "qid9",
                "question": "Question 9?",
                "passage": "Passage 2",
                "answers": [
                    "0.00001",
                    "-0.41032",
                    "0.20077",
                    ".52869"
                ],
                "correct": "A"
            },
            {
                "query_id": "qid10",
                "question": "Question 10?",
                "passage": "Passage 2",
                "answers": [
                    "1.0",
                    "1.5",
                    "0.4",
                    "0.6"
                ],
                "correct": "A"
            },
            {
                "query_id": "qid11",
                "question": "Question 11?",
                "passage": "Passage 2",
                "answers": [
                    "4.13",
                    "3.14",
                    "3.92",
                    "3.64"
                ],
                "correct": "B"
            },
            {
                "query_id": "qid12",
                "question": "Question 12?",
                "passage": "Passage 2",
                "answers": [
                    "45.321",
                    "43.800",
                    "46.042",
                    "47.750"
                ],
                "correct": "A"
            },
            {
                "query_id": "qid13",
                "question": "Question 13?",
                "passage": "Passage 2",
                "answers": [
                    "93.9530",
                    "86.3225",
                    "90.4810",
                    "87.4152"
                ],
                "correct": "D"
            },
            {
                "query_id": "qid14",
                "question": "Question 14?",
                "passage": "Passage 2",
                "answers": [
                    "89.9",
                    "92.2",
                    "95.2",
                    "87.0"
                ],
                "correct": "C"
            },
            {
                "query_id": "qid15",
                "question": "Question 15?",
                "passage": "Passage 2",
                "answers": [
                    "10554.997801",
                    "10166.530374",
                    "10671.832001",
                    "10412.123456"
                ],
                "correct": "D"
            },
            {
                "query_id": "qid16",
                "question": "Question 16?",
                "passage": "Passage 2",
                "answers": [
                    ".256",
                    ".359",
                    ".023",
                    "-0.161"
                ],
                "correct": "C"
            },
            {
                "query_id": "qid17",
                "question": "Question 17?",
                "passage": "Passage 2",
                "answers": [
                    ".139335",
                    ".323232",
                    ".434165",
                    ".674912"
                ],
                "correct": "B"
            },
            {
                "query_id": "qid18",
                "question": "Question 18?",
                "passage": "Passage 3",
                "answers": [
                    "2 March 1988",
                    "18 March 1988",
                    "18 February 1988",
                    "10 March 1986"
                ],
                "correct": "B"
            },
            {
                "query_id": "qid19",
                "question": "Question 19?",
                "passage": "Passage 3",
                "answers": [
                    "January 2000",
                    "January 1997",
                    "July 2002",
                    "January 1999"
                ],
                "correct": "A"
            },
            {
                "query_id": "qid20",
                "question": "Question 20?",
                "passage": "Passage 3",
                "answers": [
                    "29 April",
                    "13 April",
                    "19 April",
                    "13 May"
                ],
                "correct": "B"
            },
            {
                "query_id": "qid21",
                "question": "Question 21?",
                "passage": "Passage 3",
                "answers": [
                    "3",
                    "14",
                    "28",
                    "30"
                ],
                "correct": "D"
            },
            {
                "query_id": "qid22",
                "question": "Question 22?",
                "passage": "Passage 3",
                "answers": [
                    "July",
                    "April",
                    "March",
                    "September"
                ],
                "correct": "D"
            },
            {
                "query_id": "qid23",
                "question": "Question 23?",
                "passage": "Passage 3",
                "answers": [
                    "2020",
                    "2021",
                    "2023",
                    "2022"
                ],
                "correct": "A"
            }
        ]
        """))
        pd.testing.assert_frame_equal(df, expected_df)

        # Function is deterministic.
        for _ in range(0, 10):
            df = DROP2MC(MOCK_QUESTIONS_DF)
            pd.testing.assert_frame_equal(df, expected_df)


if __name__ == '__main__':
    unittest.main()
