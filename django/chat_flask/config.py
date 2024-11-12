import secrets
import os

class Config:
    SECRET_KEY = secrets.token_hex(16)  # 안전한 랜덤 키 생성
    DB_PATH = os.path.join(os.getcwd(), "D:/important/database/database.db")  # 데이터베이스 경로 지정
    API_KEY_PATH = os.path.join(os.getcwd(), "D:/important/APIkey.json")  # API 키 경로 지정
    DEBUG = True

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
