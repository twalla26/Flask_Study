from flask import Flask # flask 라는 패키지에서 Flask를 import


def create_app(): # 애플리케이션 팩토리 -> 쉽게 말해 app 객체를 생성하여 반환하는 함수
    
    # 플라스크 애플리케이션을 생성하는 코드
    app = Flask(__name__) # __name__이라는 변수는 플라스크 내장변수로서 모듈명이 담김 -> 이 코드를 실행하면 pybo.py라는 모듈이 실행되는 것 -> __name__ 변수에는 "pybo"라는 문자열이 담김

    from .views import main_views # 같은 경로에 있는 views폴더에서 main_views를 import
    app.register_blueprint(main_views.bp) # main_views.py에 있던 블루프린트 객체 bp를 플라스크 앱에 등록.

    return app
