import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Enable script loading
os.environ["OPERATOR_APPROVED_TO_RUN"] = "1"
os.environ["OPENAI_API_KEY"] = "dummy"

from script import generate_summary, SYSTEM_PROMPT

class TestGenerateSummary(unittest.TestCase):
    @patch('script.OpenAI')
    def test_generate_summary_success(self, mock_openai_class):
        # Setup mock client and response
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_choice.message.content = "This is a summary."
        mock_response.choices = [mock_choice]

        mock_client.chat.completions.create.return_value = mock_response

        # Call function
        user_message = "Here are my notes."
        model = "gpt-4o"
        api_key = "fake-key"
        result = generate_summary(user_message, model, api_key)

        # Assertions
        self.assertEqual(result, "This is a summary.")
        mock_openai_class.assert_called_once_with(api_key=api_key)
        mock_client.chat.completions.create.assert_called_once_with(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            max_tokens=1024,
        )

    @patch('script.OpenAI')
    def test_generate_summary_empty_response(self, mock_openai_class):
        # Setup mock client and response with empty content
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_choice.message.content = None
        mock_response.choices = [mock_choice]

        mock_client.chat.completions.create.return_value = mock_response

        # Call function
        result = generate_summary("notes", "model", "key")

        # Assertions
        self.assertEqual(result, "")

    @patch('script.OpenAI')
    def test_generate_summary_api_error(self, mock_openai_class):
        # Setup mock to raise an exception
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        mock_client.chat.completions.create.side_effect = Exception("API failure")

        # Call function and expect exception
        with self.assertRaises(Exception) as context:
            generate_summary("notes", "model", "key")

        self.assertTrue("API failure" in str(context.exception))

if __name__ == '__main__':
    unittest.main()
