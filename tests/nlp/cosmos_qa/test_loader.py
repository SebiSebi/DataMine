import data_mine as dm
import json
import jsonlines
import os
import pandas as pd
import sys
import unittest

from data_mine import Collection
from data_mine.nlp.cosmos_qa import CosmosQAType
from data_mine.nlp.cosmos_qa.utils import type_to_data_file
from data_mine.utils import datamine_cache_dir
from pyfakefs.fake_filesystem_unittest import TestCase
if sys.version_info >= (3, 3):
    from unittest.mock import ANY, patch
else:
    from mock import ANY, patch

# Regular format.
TRAIN_QUESTION = json.loads("""{
    "id": "train_question_1",
    "context": "Go to YouTube . Notice how they show you five videos ",
    "question": "Why are they upset about Sarah Palin being on Youtube ?",
    "answer0": "They are having fun watching Tina Fey as Sarah Palin .",
    "answer1": "None of the above choices .",
    "answer2": "The love watching saturday night live on youtube .",
    "answer3": "Youtube is doing a wonderful job showing Saturday night live",
    "label": "3"
}""")

# Regular format.
DEV_QUESTION = json.loads("""{
    "id": "dev_question_1",
    "context": "Oh no ! I went to Starbucks tonight to meet with a friend",
    "question": "What may be your reason for going to Starbucks ?",
    "answer0": "Someone invited me there .",
    "answer1": "I invited someone there .",
    "answer2": "The kids enjoy quiet time there .",
    "answer3": "My family wanted to go to Starbucks .",
    "label": "0"
}""")

# Corrct answer (label) is missing.
TEST_QUESTION = json.loads("""{
    "id": "test_question_1",
    "context": "They 're a cuddly sort of species . ",
    "question": "What may cause Firefly to get snuggly ?",
    "answer0": "None of the above choices .",
    "answer1": "Firefly is always snuggly .",
    "answer2": "If he 's tired or uncomfortable , he 'll do it .",
    "answer3": "He notices when i 'm tired or uncomfortable ."
}""")

# The correct answer label should be between 0 and 3.
INVALID_CORRECT_ANSWER_QUESTION = json.loads("""{
    "id": "invalid_correct_answer_question1",
    "context": "Go to YouTube . Notice how they show you five videos ",
    "question": "Why are they upset about Sarah Palin being on Youtube ?",
    "answer0": "They are having fun watching Tina Fey as Sarah Palin .",
    "answer1": "None of the above choices .",
    "answer2": "The love watching saturday night live on youtube .",
    "answer3": "Youtube is doing a wonderful job showing Saturday night live",
    "label": "4"
}""")


class TestCosmosQADatasetLoader(TestCase):

    def setUp(self):
        self.setUpPyfakefs()

        dataset_dir = os.path.join(datamine_cache_dir(), "COSMOS_QA")
        os.makedirs(dataset_dir, mode=0o755)

    def write_questions(self, cosmos_qa_type, question_list):
        self.assertIsInstance(cosmos_qa_type, CosmosQAType)
        datafile = type_to_data_file(cosmos_qa_type)
        with jsonlines.open(datafile, "w") as writer:
            writer.write_all(question_list)

    @patch('data_mine.nlp.cosmos_qa.loader.download_dataset')
    def test_empty_dataset(self, mock_download):
        self.write_questions(CosmosQAType.TRAIN, [])
        df = dm.COSMOS_QA(CosmosQAType.TRAIN)
        mock_download.assert_called_once_with(Collection.COSMOS_QA, ANY)
        self.assertEqual(len(df), 0)

    @patch('data_mine.nlp.cosmos_qa.loader.download_dataset')
    def test_load_in_train_and_dev_format(self, mock_download):
        self.write_questions(CosmosQAType.DEV, [
            TRAIN_QUESTION, DEV_QUESTION
        ])
        df = dm.COSMOS_QA(CosmosQAType.DEV)
        self.assertEqual(len(df), 2)
        expected_df = pd.DataFrame(json.loads("""[
            {
                "id": "train_question_1",
                "question": "Why are they upset about Sarah Palin being on Youtube ?",
                "context": "Go to YouTube . Notice how they show you five videos ",
                "answers": [
                    "They are having fun watching Tina Fey as Sarah Palin .",
                    "None of the above choices .",
                    "The love watching saturday night live on youtube .",
                    "Youtube is doing a wonderful job showing Saturday night live"
                ],
                "correct": "D"
            },
            {
                "id": "dev_question_1",
                "question": "What may be your reason for going to Starbucks ?",
                "context": "Oh no ! I went to Starbucks tonight to meet with a friend",
                "answers": [
                    "Someone invited me there .",
                    "I invited someone there .",
                    "The kids enjoy quiet time there .",
                    "My family wanted to go to Starbucks ."
                ],
                "correct": "A"
            }
        ]"""))  # noqa: E501
        pd.testing.assert_frame_equal(df, expected_df)
        mock_download.assert_called_once_with(Collection.COSMOS_QA, ANY)

    @patch('data_mine.nlp.cosmos_qa.loader.download_dataset')
    def test_load_in_test_format(self, mock_download):
        self.write_questions(CosmosQAType.TEST, [TEST_QUESTION])
        df = dm.COSMOS_QA(CosmosQAType.TEST)
        self.assertEqual(len(df), 1)
        expected_df = pd.DataFrame(json.loads("""[
            {
                "id": "test_question_1",
                "question": "What may cause Firefly to get snuggly ?",
                "context": "They 're a cuddly sort of species . ",
                "answers": [
                    "None of the above choices .",
                    "Firefly is always snuggly .",
                    "If he 's tired or uncomfortable , he 'll do it .",
                    "He notices when i 'm tired or uncomfortable ."
                ],
                "correct": null
            }
        ]"""))
        pd.testing.assert_frame_equal(df, expected_df)
        mock_download.assert_called_once_with(Collection.COSMOS_QA, ANY)

    @patch('data_mine.nlp.cosmos_qa.loader.download_dataset')
    def test_invalid_correct_answer(self, mock_download):
        self.write_questions(CosmosQAType.TRAIN, [
            INVALID_CORRECT_ANSWER_QUESTION
        ])
        with self.assertRaises(AssertionError):
            dm.COSMOS_QA(CosmosQAType.TRAIN)
        mock_download.assert_called_once_with(Collection.COSMOS_QA, ANY)


if __name__ == '__main__':
    unittest.main()
