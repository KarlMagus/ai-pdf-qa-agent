import unittest
from unittest.mock import patch, MagicMock
from src.pdf_processor import extract_text_from_pdf
from src.question_answering import get_answer_from_openai
from src.slack_notifier import post_to_slack
from src.main import main

class TestAIWorkflow(unittest.TestCase):

    @patch('src.pdf_processor.fitz.open')
    def test_pdf_extraction(self, mock_fitz_open):
        mock_doc = MagicMock()
        mock_page = MagicMock()
        mock_page.get_text.return_value = "Zania, Inc."
        mock_doc.__enter__.return_value = [mock_page]
        mock_fitz_open.return_value = mock_doc

        text = extract_text_from_pdf("dummy.pdf")
        self.assertIn("Zania, Inc.", text)

    @patch('src.question_answering.client.chat.completions.create')
    def test_question_answering(self, mock_openai):
        mock_openai.return_value.choices[0].message.content = "Shruti Gupta"
        
        context = "Zania, Inc. CEO is Shruti Gupta."
        question = "Who is the CEO of the company?"
        answer = get_answer_from_openai(question, context)
        self.assertEqual(answer, "Shruti Gupta")

    @patch('src.slack_notifier.slack_client.chat_postMessage')
    def test_slack_notification(self, mock_slack):
        mock_slack.return_value = {"ok": True}
        
        response = post_to_slack("#general", "Test message")
        self.assertTrue(response["ok"])

    @patch('src.main.extract_text_from_pdf')
    @patch('src.main.get_answer_from_openai')
    @patch('src.main.post_to_slack')
    def test_main_workflow(self, mock_slack, mock_qa, mock_pdf):
        mock_pdf.return_value = "Sample PDF content"
        mock_qa.return_value = "Sample answer"
        mock_slack.return_value = {"ok": True}

        pdf_path = "dummy.pdf"
        questions = ["Sample question"]
        results = main(pdf_path, questions)

        self.assertEqual(results, {"Sample question": "Sample answer"})
        mock_pdf.assert_called_once_with(pdf_path)
        mock_qa.assert_called_once()
        mock_slack.assert_called_once()

if __name__ == "__main__":
    unittest.main()