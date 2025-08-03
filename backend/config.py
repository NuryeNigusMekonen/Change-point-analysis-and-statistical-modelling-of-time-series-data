import os

class Config:
    DEBUG = True
    CORS_HEADERS = "Content-Type"
    DATA_FOLDER = os.path.join(os.path.dirname(__file__), "data")
