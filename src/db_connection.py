import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    return sqlite3.connect(os.getenv("../shaxamv3.sqlite", "shaxamv3.sqlite"))
