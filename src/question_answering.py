import os
from openai import OpenAI
import yaml
import logging
from dotenv import load_dotenv
import time

# Load environment variables from .env file
load_dotenv()

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

# Load configuration
config = load_config()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def clean_text(text):
    """
    Clean and normalize text by removing newlines, asterisks, and extra spaces.
    """
    # Remove newline characters
    text = text.replace('\n', ' ')
    # Remove asterisks
    text = text.replace('*', '')
    # Replace multiple spaces with a single space
    text = ' '.join(text.split())
    return text

def get_answer_from_openai(question, context):
    """
    Get answer from OpenAI API with retry logic and error handling.
    """
    max_retries = 3
    retry_delay = 5  # seconds

    for attempt in range(max_retries):
        try:
            # Make API call to OpenAI
            response = client.chat.completions.create(
                model=config.get("openai_model", "gpt-4o-mini"),
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. Answer the question based on the given context. If you're not confident in the answer or the exact answer is not in the context, respond with 'Data Not Available'."},
                    {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
                ],
                max_tokens=150
            )
            answer = response.choices[0].message.content.strip()
            cleaned_answer = clean_text(answer)
            return cleaned_answer if cleaned_answer != "Data Not Available" else "Data Not Available"
        except Exception as e:
            if "insufficient_quota" in str(e):
                logger.error("OpenAI API quota exceeded. Please check your billing details.")
                return "Error: API quota exceeded"
            elif attempt < max_retries - 1:
                logger.warning(f"Error getting answer from OpenAI (attempt {attempt + 1}/{max_retries}): {e}")
                time.sleep(retry_delay)
            else:
                logger.error(f"Error getting answer from OpenAI after {max_retries} attempts: {e}")
                return "Error: Unable to get answer from OpenAI"

def exact_match(question, context):
    """
    Attempt to find an exact match for the question in the context.
    """
    if question in context:
        start = context.index(question) + len(question)
        end = context.find('.', start)
        return context[start:end].strip() if end != -1 else context[start:].strip()
    return None

def get_answer(question, context):
    """
    Get answer to a question using exact match or OpenAI API.
    """
    exact_answer = exact_match(question, context)
    if exact_answer:
        return exact_answer
    return get_answer_from_openai(question, context)