from datetime import datetime # 날짜와 시각 저장용

from flask import Blueprint # URL과 함수의 매핑을 관리하기 위해 사용하는 클래스
from flask import render_template # 데이터를 render_template 함수의 파라미터로 전달하면 템플릿에서 해당 데이터로 화면을 구성할 수 있음. 
# 템플릿 파일: 파이썬 문법을 사용할 수 있는 html파일 
from flask import request # 플라스크는 요청 데이터를 추출해서 request 전역객체에 저장한다. 이를 통해 데이터에 접근할 수 있다.
from flask import url_for
from flask import g # g 전역변수 사용
from flask import flash # 강제로 오류를 발생시키는 함수로, 로직에 오류가 있을 경우 사용한다.
from werkzeug.utils import redirect

from .. import db # __init__.py 파일의 db 객체 import
from pybo.models import Question # models.py파일에서 Question모델 import -> question_list에 질문 목록 저장
from pybo.models import Answer, User # 검색 함수를 처리할 떄 필요함
from pybo.forms import QuestionForm # forms.py에서 폼 import
from ..forms import AnswerForm # forms.py 파일에서 폼 import
from pybo.views.auth_views import login_required # @login_required 적용

bp = Blueprint('question', __name__, url_prefix='/question') 
# 첫 번째 인수 'question'은 블루프린트의 "별칭". -> 이후 url_for 함수에서 사용됨.
# 두 번째 인수 __name__에는 모듈명인 'question_views'가 인수로 __init__.py에 전달됨.
# 세 번쨰로 url_prefix는 라우팅 함수의 에너테이션 URL 앞에 기본으로 붙일 접두어 URL임. 


@bp.route('/list/') # 질문 목록
def _list():
    page = request.args.get('page', type=int, default=1) # 페이지
    # ex) http://localhost:5000/question/list/?page=5 과 같은 GET 방식으로 요청한 url에서 page값을 가져올 때 사용됨. 
    # type=int: 페이지 값이 정수형, default=1: url에 page값이 없으면 기본값 1이 설정됨.
    kw = request.args.get('kw', type=str, default='') # 화면에서 전달받은 검색어
    question_list = Question.query.order_by(Question.create_date.desc()) # query: 데이터베이스에게 특정 데이터를 달라는 클라의 요청
    # order_by: 조회 결과를 정렬하는 함수
    # Question 모델의 question 객체들을 작성일시 기준 역순으로 정렬 -> question_list 변수에 저장
    if kw: # 화면에서 전달받은 검색어가 있으면
        search = '%%{}%%'.format(kw) # 검색어를 포함하는 내용을 찾기위해 search에 저장
        sub_query = db.session.query(Answer.question_id, Answer.content, User.username).join(User, Answer.user_id == User.id).subquery() # 서브쿼리 생성
        # 답변과 사용자 모델을 조인하여 생성, 검색 조건에 사용할 답변 내용 Answer.content와 답변 작성자 User.username이 쿼리 조회 항목으로 추가됨.
        # 그리고 이 서브쿼리와 기존 모델인 질문 모델을 연결할수 있는 질문 id에 해당하는 Answer.question_id도 조회 항목에 추가
        # -> 서브쿼리를 생성하면 Question 모델과 서브쿼리를 아우터조인할 수 있다.
        question_list = question_list.join(User).outerjoin(sub_query, sub_query.c.question_id == Question.id).filter(Question.subject.ilike(search) | Question.content.ilike(search) | User.username.ilike(search) | sub_query.c.content.ilike(search) | sub_query.c.username.ilike(search)).distinct() 
        # 질문 작성자를 검색하기 위해 User 모델 조인. User 모델은 Question 모델과 1:1 관계이므로 아우터 조인할 필요가 없음. 
        # (Answer모델에는 question_id가 각각 저장되는 만큼 한 질문에 여러 답변이 종속되기에 1:다수 관계라고 볼 수 있음.)
        # sub_query.c.question_id에 사용한 c는 서브쿼리의 조회 항목 -> sub_query.c.question_id는 서브쿼리의 조회 항목 중 question_id를 의미
        # sub_query.c.question_id와 Question.id를 연결해서 모델 연결
        # 이제 sub_query를 아우터조인했으므로 sub_query의 조회 항목을 filter 함수에 조건으로 추가할 수 있다.
        # 검색 조건은 각각 OR조건으로 조회하도록 filter 함수 내에서 | 기호를 사용했다.
    question_list = question_list.paginate(page, per_page=10)
    # 조회한 데이터 question_list에 paginate함수로 페이징 적용
    # 첫 번째 인수 page는 현재 조회할 페이지의 번호, 두 번째 인수 per_page로 전달된 10은 페이지마다 보여 줄 게시물이 10개임을 의미
    return render_template('question/question_list.html', question_list=question_list, page=page, kw=kw)
    # question_list.html에 question_list 데이터를 넘겨주고 그 데이터로 템플릿 화면을 구성하게 함.



@bp.route('/detail/<int:question_id>/') # ex)question/detail/3 -> question_id가 3인 페이지 요청
def detail(question_id): # 질문 상세 페이지를 요청했을 때 실행되는 함수, 매개변수에는 바로 윗줄에서 매핑 규칙에 사용한 <int:question_id>가 전달됨. int: 숫자값이 매핑됨을 의미
    form = AnswerForm() # 답변 form 객체를 읽을 수 있게 함.
    question = Question.query.get_or_404(question_id) # 파라미터로 받은 아이디로 Question 모델의 question 객체를 가져와서 question 변수에 저장.
    # get_or_404: 해당 데이터를 찾을 수 없는 경우에 404 페이지를 출력
    return render_template('question/question_detail.html', question=question, form=form) 
    # question_detail.html에 question 데이터를 넘겨주고 그 데이터로 템플릿 화면을 구성, 답변 form 객체를 전달하여 오류를 표시할 수 있도록 함.


@bp.route('/create/', methods=('GET', 'POST')) # 질문 생성
@login_required # 로그인이 필요한 함수, 다음 데코레이터는 반드시 해당 함수 "바로" 위에 위치 해야함.
def create():
    form = QuestionForm() # GET 요청일 경우 -> 항목이 비어있는 폼, POST 요청일 경우 -> 사용자가 입력한 데이터가 들어간 폼
    if request.method == 'POST' and form.validate_on_submit(): # POST 요청
        # request.method: create 함수로 요청된 전송 방식 post: 데이터를 서버에 전송
        # form.validate_on_submit 함수: 전송된 폼 데이터의 정합성을 점검(QuestionForm 클래스의 각 속성에 지정한 DataRequired() 같은 점검 항목에 이상이 없는지 확인)
        question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now(), user=g.user) # 폼으로 전달된 데이터를 question객체에 저장
        # 폼으로부터 전달 받은 데이터는 form.subject.data 의 형식으로 받고 있음.
        db.session.add(question) # db에 question 객체 추가
        db.session.commit() # db 저장
        return redirect(url_for('main.index')) # 질문 저장 뒤, main 블루프린트의 index 함수로 이동 -> 질문 목록 페이지로 이동
    return render_template('question/question_form.html', form=form) # GET 요청 -> 질문 생성 폼 페이지로 이동 (form은 빈 form일 것.)
    # question_form.html 템플릿에 전달하는 QuestionForm의 객체(form)는 템플릿에서 라벨이나 입력폼 등을 만들때 필요하다.


@bp.route('/modify/<int:question_id>', methods=('GET', 'POST')) 
@login_required # 로그인이 필요한 기능
def modify(question_id): # 질문 수정 함수
    question = Question.query.get_or_404(question_id)
    if g.user != question.user: # 만약 사용자와 글 작성자가 다르다면
        flash('수정 권한이 없습니다.') # 수정 권한 없음 ->
        return redirect(url_for('question.detail', question_id=question_id)) # 질문 상세 페이지로 리다이렉트
    if request.method == 'POST': # 'POST' 요청
        form = QuestionForm() # form으로 사용자가 입력한 내용을 받아옴
        if form.validate_on_submit(): # 입력한 내용이 양식에 맞으면
            form.populate_obj(question) # 폼에 들어있는 데이터를 question 객체에 업데이트
            question.modify_date = datetime.now() # 수정일시 저장
            db.session.commit() # db 저장
            return redirect(url_for('question.detail', question_id=question_id)) # 수정 후, 질문 상세 페이지로 이동
    else: # 'GET' 요청 -> 질문 수정 버튼을 누른 경우
        form = QuestionForm(obj=question) # 기존의 질문 객체를 폼에 저장
    return render_template('question/question_form.html', form=form) # 질문 작성 페이지로 이동 (기존 질문 객체 전송)


@bp.route('/delete/<int:question_id>')
@login_required # 로그인이 필요한 기능
def delete(question_id): # 질문 삭제 함수
    question = Question.query.get_or_404(question_id)
    if g.user != question.user: # 사용자가 글 작성자가 아니라면
        flash("삭제 권한이 없습니다.")
        return redirect(url_for('question.detail', question_id=question_id)) # 질문 상세 페이지로 리다이렉트
    db.session.delete(question) # 사용자가 작성자라면 질문 삭제
    db.session.commit() # db 저장
    return redirect(url_for('question._list')) # 질문 목록 페이지로 리다이렉트


@bp.route('/vote/<int:question_id>/') 
@login_required # 로그인이 필요한 기능
def vote(question_id): # 질문 추천 함수
    _question = Question.query.get_or_404(question_id)
    if g.user == _question.user: # 사용자가 질문 작성자라면
        flash("본인이 작성한 글은 추천할 수 없습니다.") # 추천 불가
    else: # 사용자가 질문 작성자가 아니라면
        _question.voter.append(g.user) # 질문 추천인 중에 사용자 추가
        # Question 모델의 voter는 여러 사람을 추가할 수 있는 다대다 관계이므로 append()함수로 추천인을 추가해야 한다.
        # question_voter 테이블의 구조상 같은 사용자가 같은 질문을 여러 번 추천해도 추천 횟수는 증가하지 않는다. 
        # 동일한 사용자를 append 할때 오류가 날것 같지만 내부적으로 중복되지 않도록 잘 처리된다.
        db.session.commit() # db 저장
    return redirect(url_for('question.detail', question_id=question_id)) # 질문 상세 페이지로 리다이렉트