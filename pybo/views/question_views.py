from datetime import datetime # 날짜와 시각 저장용

from flask import Blueprint # URL과 함수의 매핑을 관리하기 위해 사용하는 클래스
from flask import render_template # 데이터를 render_template 함수의 파라미터로 전달하면 템플릿에서 해당 데이터로 화면을 구성할 수 있음. 
# 템플릿 파일: 파이썬 문법을 사용할 수 있는 html파일 
from flask import request # 플라스크는 요청 데이터를 추출해서 request 전역객체에 저장한다. 이를 통해 데이터에 접근할 수 있다.
from flask import url_for
from werkzeug.utils import redirect

from .. import db # __init__.py 파일의 db 객체 import
from pybo.models import Question # models.py파일에서 Question모델 import -> question_list에 질문 목록 저장
from pybo.forms import QuestionForm # forms.py에서 폼 import
from ..forms import AnswerForm # forms.py 파일에서 폼 import

bp = Blueprint('question', __name__, url_prefix='/question') 
# 첫 번째 인수 'question'은 블루프린트의 "별칭". -> 이후 url_for 함수에서 사용됨.
# 두 번째 인수 __name__에는 모듈명인 'question_views'가 인수로 __init__.py에 전달됨.
# 세 번쨰로 url_prefix는 라우팅 함수의 에너테이션 URL 앞에 기본으로 붙일 접두어 URL임. 


@bp.route('/list/') # 질문 목록
def _list():
    page = request.args.get('page', type=int, default=1) # 페이지
    # ex) http://localhost:5000/question/list/?page=5 과 같은 GET 방식으로 요청한 url에서 page값을 가져올 때 사용됨. 
    # type=int: 페이지 값이 정수형, default=1: url에 page값이 없으면 기본값 1이 설정됨.
    question_list = Question.query.order_by(Question.create_date.desc()) # query: 데이터베이스에게 특정 데이터를 달라는 클라의 요청
    # order_by: 조회 결과를 정렬하는 함수
    # Question 모델의 question 객체들을 작성일시 기준 역순으로 정렬 -> question_list 변수에 저장
    question_list = question_list.paginate(page, per_page=10)
    # 조회한 데이터 question_list에 paginate함수로 페이징 적용
    # 첫 번째 인수 page는 현재 조회할 페이지의 번호, 두 번째 인수 per_page로 전달된 10은 페이지마다 보여 줄 게시물이 10개임을 의미
    return render_template('question/question_list.html', question_list=question_list)
    # question_list.html에 question_list 데이터를 넘겨주고 그 데이터로 템플릿 화면을 구성하게 함.


@bp.route('/detail/<int:question_id>/') # ex)question/detail/3 -> question_id가 3인 페이지 요청
def detail(question_id): # 질문 상세 페이지를 요청했을 때 실행되는 함수, 매개변수에는 바로 윗줄에서 매핑 규칙에 사용한 <int:question_id>가 전달됨. int: 숫자값이 매핑됨을 의미
    form = AnswerForm() # 답변 form 객체를 읽을 수 있게 함.
    question = Question.query.get_or_404(question_id) # 파라미터로 받은 아이디로 Question 모델의 question 객체를 가져와서 question 변수에 저장.
    # get_or_404: 해당 데이터를 찾을 수 없는 경우에 404 페이지를 출력
    return render_template('question/question_detail.html', question=question, form=form) 
    # question_detail.html에 question 데이터를 넘겨주고 그 데이터로 템플릿 화면을 구성, 답변 form 객체를 전달하여 오류를 표시할 수 있도록 함.


@bp.route('/create/', methods=('GET', 'POST')) # 질문 생성
def create():
    form = QuestionForm() # GET 요청일 경우 -> 항목이 비어있는 폼, POST 요청일 경우 -> 사용자가 입력한 데이터가 들어간 폼
    if request.method == 'POST' and form.validate_on_submit(): # POST 요청
        # request.method: create 함수로 요청된 전송 방식 post: 데이터를 서버에 전송
        # form.validate_on_submit 함수: 전송된 폼 데이터의 정합성을 점검(QuestionForm 클래스의 각 속성에 지정한 DataRequired() 같은 점검 항목에 이상이 없는지 확인)
        question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now()) # 폼으로 전달된 데이터를 question객체에 저장
        # 폼으로부터 전달 받은 데이터는 form.subject.data 의 형식으로 받고 있음.
        db.session.add(question) # db에 question 객체 추가
        db.session.commit() # db 저장
        return redirect(url_for('main.index')) # 질문 저장 뒤, main 블루프린트의 index 함수로 이동 -> 질문 목록 페이지로 이동
    return render_template('question/question_form.html', form=form) # GET 요청 -> 질문 생성 폼 페이지로 이동 (form은 빈 form일 것.)
    # question_form.html 템플릿에 전달하는 QuestionForm의 객체(form)는 템플릿에서 라벨이나 입력폼 등을 만들때 필요하다.