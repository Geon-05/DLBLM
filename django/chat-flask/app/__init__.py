from flask import Flask

def create_app(config_filename=None):
    app = Flask(__name__)

    if config_filename:
        app.config.from_pyfile(config_filename)  # 설정 파일 로드

    # 블루프린트나 다른 초기화 코드 등록
    from .routes import main
    app.register_blueprint(main)

    return app