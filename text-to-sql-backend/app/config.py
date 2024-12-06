import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    DATABASE_PATH = BASE_DIR / 'instance' / 'test_database.db'
    MODEL_PATH = os.environ.get('MODEL_PATH') or '/Users/chandrashakargudipally/Desktop/cs678/assignment4/my_text_to_sql_model'