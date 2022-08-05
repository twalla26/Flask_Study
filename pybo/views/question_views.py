from flask import Blueprint # URL과 함수의 매핑을 관리하기 위해 사용하는 클래스
from flask import render_template # 데이터를 render_template 함수의 파라미터로 전달하면 템플릿에서 해당 데이터로 화면을 구성할 수 있음. 
# 템플릿 파일: 파이썬 문법을 사용할 수 있는 html파일 
from pybo.models import Question # models.py파일에서 Question모델 import -> question_list에 질문 목록 저장

bp = Blueprint('question', __name__, url_prefix='/question') 
# 첫 번째 인수 'question'은 블루프린트의 "별칭". -> 이후 url_for 함수에서 사용됨.
# 두 번째 인수 __name__에는 모듈명인 'question_views'가 인수로 __init__.py에 전달됨.
# 세 번쨰로 url_prefix는 라우팅 함수의 에너테이션 URL 앞에 기본으로 붙일 접두어 URL임. 


@bp.route('/list/')
def _list():
    question_list = Question.query.order_by(Question.create_date.desc()) # query: 데이터베이스에게 특정 데이터를 달라는 클라의 요청
    # order_by: 조회 결과를 정렬하는 함수
    # Question 모델의 question 객체들을 작성일시 기준 역순으로 정렬 -> question_list 변수에 저장
    return render_template('question/question_list.html', question_list=question_list) 
    # question_list.html에 question_list 데이터를 넘겨주고 그 데이터로 템플릿 화면을 구성하게 함.


@bp.route('/detail/<int:question_id>/') # ex)question/detail/3 -> question_id가 3인 페이지 요청
def detail(question_id): # 질문 상세 페이지를 요청했을 때 실행되는 함수, 매개변수에는 바로 윗줄에서 매핑 규칙에 사용한 <int:question_id>가 전달됨. int: 숫자값이 매핑됨을 의미
    question = Question.query.get_or_404(question_id) # 파라미터로 받은 아이디로 Question 모델의 question 객체를 가져와서 question 변수에 저장.
    # get_or_404: 해당 데이터를 찾을 수 없는 경우에 404 페이지를 출력
    return render_template('question/question_detail.html', question=question) # question_detail.html에 question 데이터를 넘겨주고 그 데이터로 템플릿 화면을 구성.


