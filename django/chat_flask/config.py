import secrets

class Config:
    SECRET_KEY = secrets.token_hex(16)  # 안전한 랜덤 키 생성
    DEBUG = True

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
