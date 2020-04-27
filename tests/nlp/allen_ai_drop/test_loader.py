import data_mine as dm
import json
import os
import pandas as pd
import sys
import unittest

from data_mine import Collection
from data_mine.nlp.allen_ai_drop import DROPType
from data_mine.utils import datamine_cache_dir
from pyfakefs.fake_filesystem_unittest import TestCase
if sys.version_info >= (3, 3):
    from unittest.mock import ANY, patch
else:
    from mock import ANY, patch

VALID_QUESTIONS = """{
    "nfl_1": {
        "passage": "Passage 1",
        "qa_pairs": [
            {
                "question": "First question?",
                "answer": {
                    "number": "",
                    "date": {
                        "day": "",
                        "month": "",
                        "year": ""
                    },
                    "spans": [
                        "Chaz Schilens"
                    ]
                },
                "query_id": "f37e81fa-ef7b-4583-b671-762fc433faa9",
                "validated_answers": [
                    {
                        "number": "",
                        "date": {
                            "day": "",
                            "month": "",
                            "year": ""
                        },
                        "spans": [
                            "Chaz Schilens"
                        ]
                    },
                    {
                        "number": "",
                        "date": {
                            "day": "",
                            "month": "",
                            "year": ""
                        },
                        "spans": [
                            "Schilens"
                        ]
                    }
                ]
            },
            {
                "question": "Second question?",
                "answer": {
                    "number": "-4",
                    "date": {
                        "day": "",
                        "month": "",
                        "year": ""
                    },
                    "spans": []
                },
                "query_id": "ac6ba235-3024-4f63-a6ab-730a14def4cb",
                "validated_answers": [],
                "highlights": [],
                "question_type": "",
                "expert_answers": [],
                "workerid": "123411241",
                "workerscore": "0.998213",
                "incorrect_options": [],
                "ai_answer": ""
            },
            {
                "question": "Third question?",
                "answer": {
                    "number": "0",
                    "date": {},
                    "spans": []
                },
                "query_id": "ac6ba235-3024-4f63-bbbb-730a14def4cb",
                "highlights": [],
                "workerid": "1234",
                "workerscore": "0.56"
            },
            {
                "question": "Fourth question?",
                "answer": {
                    "number": "98.56",
                    "date": {
                        "day": "",
                        "month": "",
                        "year": ""
                    },
                    "spans": [],
                    "worker_id": ""
                },
                "query_id": "cccba235-3024-4f63-a6ab-730a14defaaa"
            },
            {
                "question": "This question must be skipped!",
                "answer": {
                    "number": "",
                    "date": {
                        "day": "",
                        "month": "",
                        "year": ""
                    },
                    "spans": []
                },
                "query_id": "dbe49a10-9058-4b15-a66d-1aacdcc3998f"
            },
            {
                "question": "This question must also be skipped!",
                "answer": {
                    "number": "",
                    "date": {},
                    "spans": []
                },
                "query_id": "44444444-9058-4b15-a66d-1aacdcc99999"
            },
            {
                "question": "Fifth question?",
                "answer": {
                    "number": "",
                    "date": {
                        "day": "7",
                        "month": "",
                        "year": "1995"
                    },
                    "spans": []
                },
                "query_id": "0f9528f8-d127-458c-b9df-948142ac92c9"
            },
            {
                "question": "Sixth question - special ID",
                "answer": {
                    "number": "4567",
                    "date": {
                        "day": "",
                        "month": "",
                        "year": "1945"
                    },
                    "spans": []
                },
                "query_id": "daf712ed-3849-48a1-b9b5-f7d21b0c0ab7"
            }
        ],
        "wiki_url": "https://en.wikipedia.org/wiki/Earl's_Court"
    },
    "nfl_2": {
        "passage": "Passage 2",
        "qa_pairs": [
            {
                "question": "Seventh question?",
                "answer": {
                    "number": "",
                    "date": {
                        "day": "",
                        "month": "",
                        "year": ""
                    },
                    "spans": [
                        "span 1",
                        "span 2",
                        "span 3"
                    ]
                },
                "query_id": "dbe49a10-9058-4b15-a66d-1aacdcc3998f"
            },
            {
                "question": "First instance of the duplicate question",
                "answer": {
                    "number": "",
                    "date": {
                        "day": "7",
                        "month": "September",
                        "year": "1995"
                    },
                    "spans": []
                },
                "query_id": "28553293-d719-441b-8f00-ce3dc6df5398"
            },
            {
                "question": "Second instance of the duplicate question",
                "answer": {
                    "number": "",
                    "date": {
                        "day": "8",
                        "month": "January",
                        "year": "2002"
                    },
                    "spans": []
                },
                "query_id": "28553293-d719-441b-8f00-ce3dc6df5398"
            },
            {
                "question": "Last question?",
                "answer": {
                    "number": "",
                    "date": {
                        "day": "",
                        "month": "March",
                        "year": "2020"
                    },
                    "spans": []
                },
                "query_id": "26a54193-a600-4ff3-9fd1-b9f3e6121fbf"
            }
        ],
        "wiki_url": "some invalid URL, it does not matter"
    }
}"""

MISSING_QUESTION_TEXT = """{
    "nfl_1": {
        "passage": "Passage 1",
        "qa_pairs": [
            {
                "answer": {
                    "number": "",
                    "date": {
                        "day": "",
                        "month": "",
                        "year": ""
                    },
                    "spans": [
                        "Chaz Schilens"
                    ]
                },
                "query_id": "f37e81fa-ef7b-4583-b671-762fc433faa9"
            }
        ],
        "wiki_url": "https://en.wikipedia.org"
    }
}"""

MISSING_ANSWER = """{
    "nfl_1": {
        "passage": "Passage 1",
        "qa_pairs": [
            {
                "question": "Why?",
                "query_id": "f37e81fa-ef7b-4583-b671-762fc433faa9"
            }
        ],
        "wiki_url": "https://en.wikipedia.org"
    }
}"""

MISSING_QUERY_ID = """{
    "nfl_1": {
        "passage": "Passage 1",
        "qa_pairs": [
            {
                "question": "Why?",
                "answer": {
                    "number": "",
                    "date": {
                        "day": "",
                        "month": "",
                        "year": ""
                    },
                    "spans": [
                        "Chaz Schilens"
                    ]
                }
            }
        ],
        "wiki_url": "https://en.wikipedia.org"
    }
}"""

INVALID_NUMBER = """{
    "nfl_1": {
        "passage": "Passage 1",
        "qa_pairs": [
            {
                "question": "Why?",
                "answer": {
                    "number": "abcd",
                    "date": {
                        "day": "",
                        "month": "",
                        "year": ""
                    },
                    "spans": []
                },
                "query_id": "f37e81fa-ef7b-4583-b671-762fc433faa9"
            }
        ],
        "wiki_url": "https://en.wikipedia.org"
    }
}"""

MULTIPLE_ANSWERS = """{
    "nfl_1": {
        "passage": "Passage 1",
        "qa_pairs": [
            {
                "question": "Why?",
                "answer": {
                    "number": "12",
                    "date": {
                        "day": "",
                        "month": "",
                        "year": ""
                    },
                    "spans": [
                        "Chaz Schilens"
                    ]
                },
                "query_id": "f37e81fa-ef7b-4583-b671-762fc433faa9"
            }
        ],
        "wiki_url": "https://en.wikipedia.org"
    }
}"""

MISSING_WIKI_URL = """{
    "nfl_1": {
        "passage": "Passage 1",
        "qa_pairs": [
            {
                "question": "Why?",
                "answer": {
                    "number": "",
                    "date": {
                        "day": "",
                        "month": "",
                        "year": ""
                    },
                    "spans": [
                        "Chaz Schilens"
                    ]
                },
                "query_id": "f37e81fa-ef7b-4583-b671-762fc433faa9"
            }
        ]
    }
}"""

MISSING_PASSAGE = """{
    "nfl_1": {
        "qa_pairs": [
            {
                "question": "Why?",
                "answer": {
                    "number": "",
                    "date": {
                        "day": "",
                        "month": "",
                        "year": ""
                    },
                    "spans": [
                        "Chaz Schilens"
                    ]
                },
                "query_id": "f37e81fa-ef7b-4583-b671-762fc433faa9"
            }
        ],
        "wiki_url": "https://en.wikipedia.org"
    }
}"""

MISSING_QA_PAIRS = """{
    "nfl_1": {
        "passage": "Passage 1",
        "wiki_url": "https://en.wikipedia.org"
    }
}"""

TOO_MANY_FIELDS_1 = """{
    "nfl_1": {
        "passage": "Passage 1",
        "qa_pairs": [
            {
                "question": "Why?",
                "answer": {
                    "number": "",
                    "date": {
                        "day": "",
                        "month": "",
                        "year": ""
                    },
                    "spans": [
                        "Chaz Schilens"
                    ]
                },
                "query_id": "f37e81fa-ef7b-4583-b671-762fc433faa9"
            }
        ],
        "wiki_url": "https://en.wikipedia.org",
        "this should not be here": "12"
    }
}"""

TOO_MANY_FIELDS_2 = """{
    "nfl_1": {
        "passage": "Passage 1",
        "qa_pairs": [
            {
                "question": "Why?",
                "answer": {
                    "number": "",
                    "date": {
                        "day": "",
                        "month": "",
                        "year": ""
                    },
                    "spans": [
                        "Chaz Schilens"
                    ]
                },
                "query_id": "f37e81fa-ef7b-4583-b671-762fc433faa9",
                "unknown_field_name": 4123
            }
        ],
        "wiki_url": "https://en.wikipedia.org"
    }
}"""


class TestAllenAIDropDatasetLoader(TestCase):

    def setUp(self):
        self.setUpPyfakefs()

        dataset_dir = os.path.join(
                datamine_cache_dir(),
                Collection.ALLEN_AI_DROP.name,
                "drop_dataset"
        )
        os.makedirs(dataset_dir, mode=0o755)
        self.file_path = os.path.join(dataset_dir, "drop_dataset_dev.json")

    @patch('data_mine.nlp.allen_ai_drop.loader.download_dataset')
    def test_parsing_logic(self, mock_download_dataset):
        # Write the mock questions (good format, valid data).
        with open(self.file_path, "wt") as g:
            g.write(VALID_QUESTIONS)
            g.flush()

        # Parse the dataset and test the result.
        df = dm.ALLEN_AI_DROP(DROPType.DEV)
        expected_df = pd.DataFrame([
            {
                "query_id": "f37e81fa-ef7b-4583-b671-762fc433faa9",
                "question": "First question?",
                "passage": "Passage 1",
                "answer_type": "spans",
                "parsed_answer": "Chaz Schilens",
                "original_answer": json.loads("""
                    {
                        "number": "",
                        "date": {
                            "day": "",
                            "month": "",
                            "year": ""
                        },
                        "spans": [
                            "Chaz Schilens"
                        ]
                    }
                """)
            },
            {
                "query_id": "ac6ba235-3024-4f63-a6ab-730a14def4cb",
                "question": "Second question?",
                "passage": "Passage 1",
                "answer_type": "number",
                "parsed_answer": "-4",
                "original_answer": json.loads("""
                    {
                        "number": "-4",
                        "date": {
                            "day": "",
                            "month": "",
                            "year": ""
                        },
                        "spans": []
                    }
                """)
            },
            {
                "query_id": "ac6ba235-3024-4f63-bbbb-730a14def4cb",
                "question": "Third question?",
                "passage": "Passage 1",
                "answer_type": "number",
                "parsed_answer": "0",
                "original_answer": json.loads("""
                    {
                        "number": "0",
                        "date": {},
                        "spans": []
                    }
                """)
            },
            {
                "query_id": "cccba235-3024-4f63-a6ab-730a14defaaa",
                "question": "Fourth question?",
                "passage": "Passage 1",
                "answer_type": "number",
                "parsed_answer": "98.56",
                "original_answer": json.loads("""
                    {
                        "number": "98.56",
                        "date": {
                            "day": "",
                            "month": "",
                            "year": ""
                        },
                        "spans": []
                    }
                """)
            },
            {
                "query_id": "0f9528f8-d127-458c-b9df-948142ac92c9",
                "question": "Fifth question?",
                "passage": "Passage 1",
                "answer_type": "date",
                "parsed_answer": "7 1995",
                "original_answer": json.loads("""
                    {
                        "number": "",
                        "date": {
                            "day": "7",
                            "month": "",
                            "year": "1995"
                        },
                        "spans": []
                    }
                """)
            },
            {
                "query_id": "daf712ed-3849-48a1-b9b5-f7d21b0c0ab7",
                "question": "Sixth question - special ID",
                "passage": "Passage 1",
                "answer_type": "date",
                "parsed_answer": "1945",
                "original_answer": json.loads("""
                    {
                        "number": "",
                        "date": {
                            "day": "",
                            "month": "",
                            "year": "1945"
                        },
                        "spans": []
                    }
                """)
            },
            {
                "query_id": "dbe49a10-9058-4b15-a66d-1aacdcc3998f",
                "question": "Seventh question?",
                "passage": "Passage 2",
                "answer_type": "spans",
                "parsed_answer": "span 1, span 2, span 3",
                "original_answer": json.loads("""
                    {
                        "number": "",
                        "date": {
                            "day": "",
                            "month": "",
                            "year": ""
                        },
                        "spans": [
                            "span 1",
                            "span 2",
                            "span 3"
                        ]
                    }
                """)
            },
            {
                "query_id": "28553293-d719-441b-8f00-ce3dc6df5398",
                "question": "First instance of the duplicate question",
                "passage": "Passage 2",
                "answer_type": "date",
                "parsed_answer": "7 September 1995",
                "original_answer": json.loads("""
                    {
                        "number": "",
                        "date": {
                            "day": "7",
                            "month": "September",
                            "year": "1995"
                        },
                        "spans": []
                    }
                """)
            },
            {
                "query_id": "26a54193-a600-4ff3-9fd1-b9f3e6121fbf",
                "question": "Last question?",
                "passage": "Passage 2",
                "answer_type": "date",
                "parsed_answer": "March 2020",
                "original_answer": json.loads("""
                    {
                        "number": "",
                        "date": {
                            "day": "",
                            "month": "March",
                            "year": "2020"
                        },
                        "spans": []
                    }
                """)
            }
        ])
        pd.testing.assert_frame_equal(df, expected_df)
        mock_download_dataset.assert_called_once_with(Collection.ALLEN_AI_DROP, ANY)  # noqa: E501

    @patch('data_mine.nlp.allen_ai_drop.loader.download_dataset')
    def test_invalid_questions(self, mock_download_dataset):
        invalid_questions = [
                # (example, expected exception to be raised)
                (MISSING_QUESTION_TEXT, AssertionError),
                (MISSING_ANSWER,        AssertionError),
                (MISSING_QUERY_ID,      AssertionError),
                (INVALID_NUMBER,        ValueError),
                (MULTIPLE_ANSWERS,      AssertionError),
                (MISSING_WIKI_URL,      AssertionError),
                (MISSING_PASSAGE,       AssertionError),
                (MISSING_QA_PAIRS,      AssertionError),
                (TOO_MANY_FIELDS_1,     AssertionError),
                (TOO_MANY_FIELDS_2,     AssertionError)
        ]
        for invalid_question, exception in invalid_questions:
            with open(self.file_path, "wt") as g:
                g.write(invalid_question)
                g.flush()
            with self.assertRaises(exception):
                dm.ALLEN_AI_DROP(DROPType.DEV)
        self.assertEqual(
                mock_download_dataset.call_count,
                len(invalid_questions)
        )


if __name__ == '__main__':
    unittest.main()
