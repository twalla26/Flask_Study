from flask import Flask # flask 라는 패키지에서 Flask 모듈을 import

# 플라스크 애플리케이션을 생성하는 코드
# __name__이라는 변수는 플라스크 내장변수로서 변수에 모듈명이 담김 -> 이 코드를 실행하면 pybo.py라는 모듈이 실행되는 것. -> __name__ 변수에는 "pybo"라는 문자열이 담김. 
app = Flask(__name__)


# "@app.route"는 URL과 플라스크 코드를 매핑하는 플라스크의 데코레이터. '/' URL이 요청되면 플라스크는 hello_pybo 함수를 실행시킨다.
# 데코레이터(decorator)란 기존 함수를 변경하지 않고 추가 기능을 덧붙일 수 있도록 해주는 함수를 의미한다.
@app.route('/') 
def hello_pybo(): 
    return 'Hello, Pybo!'