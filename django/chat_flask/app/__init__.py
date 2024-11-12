import os
from flask import Flask

def create_app(config_class='config.Config'):
    # Flask 애플리케이션 초기화
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), '../templates'),
        static_folder=os.path.join(os.path.dirname(__file__), '../static')
    )
    
    # 설정 클래스 적용
    app.config.from_object(config_class)

    # 블루프린트 등록
    from .routes import main
    app.register_blueprint(main)

    return app