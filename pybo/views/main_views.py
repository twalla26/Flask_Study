from flask import Blueprint # flask 모듈에서 Blueprint 클래스 import

bp = Blueprint('main', __name__, url_prefix='/') # Blueprint 클래스로 bp 객체 생성.
# 첫 번째 인수 'main'은 블루프린트의 "별칭". -> 이후 url_for 함수에서 사용됨.
# 두 번째 인수 __name__에는 모듈명인 'main_views'가 인수로 __init__.py에 전달됨.
# 세 번쨰로 url_prefix는 라우팅 함수의 에너테이션 URL 앞에 기본으로 붙일 접두어 URL임. 
# 만약 url_prefix가 '/'대신 '/main'이었다면, hello_pybo함수를 호출하는 url은 localhost:5000/이 아니라 localhost:5000/main/이 될 것.


@bp.route('/hello') # URL과 플라스크 코드를 매핑하는 플라스크의 데코레이터. "@app.route"같은 에너테이션으로 URL을 매핑해주는 함수를 라우팅 함수라 함.
def hello_pybo(): # '/hello' URL이 요청되면 플라스크는 hello_pybo 함수를 실행시킨다.
    return 'Hello, Pybo!'
# 데코레이터(decorator)란 기존 함수를 변경하지 않고 추가 기능을 덧붙일 수 있도록 해주는 함수를 의미한다.
# __init__에선 app.route였지만 뷰파일에선 bp.route로 바뀌었다. 여기서 bp는 앞에서 생성한 블루프린트 객체다.


@bp.route('/')
def index():
    return 'Pybo index'