import json
import os
import logging
from pdf_processor import extract_text_from_pdf
from question_answering import get_answer_from_openai
from slack_notifier import post_to_slack
import yaml
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config():
    """
    Load configuration from YAML file.
    """
    try:
        with open("config/config.yaml", "r") as file:
            return yaml.safe_load(file)
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise

def main(pdf_path, questions):
    """
    Main function to process PDF, answer questions, and post results to Slack.
    """
    config = load_config()
    
    try:
        # Remove any surrounding quotes from the pdf_path
        pdf_path = pdf_path.strip('"')
        
        # Validate inputs
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        if not questions:
            raise ValueError("No questions provided")
        
        # Extract text from PDF
        context = extract_text_from_pdf(pdf_path)
        
        # Answer questions
        results = {}
        for question in questions:
            answer = get_answer_from_openai(question, context)
            results[question] = answer
        
        # Prepare results for Slack
        results_json = json.dumps(results, indent=2)
        
        # Post results to Slack
        slack_channel = os.getenv("SLACK_CHANNEL")
        slack_response = post_to_slack(slack_channel, f"Results:\n```{results_json}```")
        
        # Log Slack posting result
        if slack_response and slack_response.get("ok"):
            logger.info("Results posted to Slack successfully")
        else:
            logger.warning("Failed to post results to Slack")
        
        # Print results to console
        print("Results:")
        print(results_json)
        
        logger.info("Process completed")
        return results
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        print(f"Error: {e}")
    except ValueError as e:
        logger.error(f"Invalid input: {e}")
        print(f"Error: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        print(f"An unexpected error occurred. Please check the logs for more details.")

if __name__ == "__main__":
    # Get PDF file path from user
    while True:
        pdf_path = input("Enter the path to the PDF file: ").strip()
        if os.path.exists(pdf_path.strip('"')):
            break
        print("Error: File not found. Please enter a valid file path.")

    # Get questions from user
    questions = []
    while True:
        question = input("Enter a question (or press Enter to finish): ")
        if not question:
            break
        questions.append(question)
    
    # Run main process if questions were provided
    if questions:
        main(pdf_path, questions)
    else:
        print("No questions were provided. Exiting.")