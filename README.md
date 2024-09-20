# AI Agent for PDF Question Answering and Slack Notification

## Overview
This project implements an AI agent that extracts answers from a PDF document using OpenAI's language models and posts the results to a Slack channel.

## Features
- PDF text extraction
- Question answering using OpenAI's GPT models
- Slack integration for result posting
- Comprehensive error handling and logging

## Requirements
- Python 3.7+
- OpenAI API key
- Slack Bot Token
- PDF document for analysis

## Setup

1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/ai-agent.git
   cd ai-agent
   ```

2. Create a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   Create a `.env` file in the project root and add the following:
   ```
   OPENAI_API_KEY=your_openai_api_key
   SLACK_BOT_TOKEN=your_slack_bot_token
   SLACK_CHANNEL=your_slack_channel_id
   ```

5. Configure the application:
   Update `config/config.yaml` with your desired settings:
   ```yaml
   openai_model: "gpt-4o-mini"
   ```

## Usage

1. Run the main script:
   ```sh
   python src/main.py
   ```

2. Follow the prompts to enter the PDF file path and questions.

## Testing

Run unit tests:
```sh
pytest tests/
```


## Project Structure
- `src/`: Contains the main application code
  - `pdf_processor.py`: Handles PDF text extraction
  - `question_answering.py`: Interacts with OpenAI API
  - `slack_notifier.py`: Posts results to Slack
  - `main.py`: Orchestrates the workflow
- `tests/`: Contains unit tests
- `config/`: Configuration files
- `requirements.txt`: List of Python dependencies

## Error Handling and Logging
The application includes comprehensive error handling and logging. Check the application logs for detailed information about any issues encountered during execution.

## License
This project is licensed under the MIT License.