import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://polls_db_csp7_user:oMNUwfm95Ki6Gh9YRJ472ExcyD7JUA2c@dpg-d1hbv9qli9vc73bjm6sg-a/polls_db_csp7"
    )
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
