from dotenv import load_dotenv
from os import environ

# Load .env file into the Environment Variables:
load_dotenv()

class AppConfig:

    sender_email = environ.get("SENDER_EMAIL")
    password = environ.get("PASSWORD")