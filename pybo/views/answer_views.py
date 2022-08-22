from datetime import datetime # 날짜와 시간을 동시에 표현하기 위한 모듈

from flask import Blueprint # bp 생성
from flask import url_for
from flask import request # db에 데이터 요청하기 위함
from flask import render_template
from flask import g # g.user는 세션에 저장된 사용자 정보 데이터
from flask import flash # 강제로 오류를 발생시키는 함수로, 로직에 오류가 있을 경우 사용한다.
from werkzeug.utils import redirect 

from pybo import db 
from ..forms import AnswerForm # forms.py파일에서 AnswerForm 클래스 import 
from pybo.models import Question, Answer # models.py 파일의 Question, Answer 클래스
from pybo.views.auth_views import login_required # @login_required 적용

bp = Blueprint('answer', __name__, url_prefix='/answer') # bp 생성, 별칭: answer


@bp.route('/create/<int:question_id>', methods=('POST', )) # 질문에 대한 답변 생성 (POST 요청만 있음)
# methods 속성은 question_detail.html에서 답변을 저장하는 form 엘리먼트의 메소드 post와 같은 값을 지정.
@login_required # 로그인이 필요한 기능
def create(question_id): # question_id 는 바로 윗줄에서 매핑 규칙으로 전달됨.
    form = AnswerForm() # question_detail.html에서 작성된 데이터
    question = Question.query.get_or_404(question_id) # db에서 question_id(정수형)를 id 값으로 갖고 있는 question 객체를 
    # 찾아서(id는 고윳값이므로 get 함수를 이용해 조회) question에 저장, 여기서 question_id를 Answer모델의 속성 중 하나와 헷갈리지 말자.
    if form.validate_on_submit(): # 폼으로 들어온 데이터가 폼 양식에 맞을 때,
        content = request.form['content'] # request: 템플릿에서 form 엘리먼트로 전달된 데이터들을 얻을 수 있음.
        # request.form['content']: POST 폼 방식으로 전송된 데이터 항목 중 name 속성이 content인 값을 찾아서 content 객체에 저장
        # request: 플라스크에서 생성과정 없이 사용할 수 있는 기본 객체 -> 브라우저의 요청부터 응답까지의 처리 구간에서 request 객체 사용 가능. request를 통해 브라우저에서 요청한 정보를 확인
        # 데이터는 html 파일의 form 태그에서 주소를 정해서 create함수로 보냄.
        answer = Answer(content=content, create_date=datetime.now(), user=g.user) # 폼에서 전송된 데이터로 answer객체 구성, g.user는 세션에 저장된 사용자 정보 데이터
        question.answer_set.append(answer) # 해당 질문에 달린 답변들에 answer 객체 추가
        db.session.commit() # db 저장
        return redirect('{}#answer_{}'.format(url_for('question.detail', question_id=question_id), answer.id)) # 답변 생성 후 화면을 질문 상세 화면으로 이동 
        # question 별칭의 블루프린트의 detail 함수로, question_id는 detail함수의 인자
        # '{}#answer_{}'.format(anser.id) -> 함수 수행 후, 지정해놓은 앵커로 이동 -> 내가 쓴 답변을 보려고 스크롤을 굳이 안내려도 됨.
    return render_template('question/question_detail.html', question=question, form=form) # 폼으로 들어온 데이터가 양식에 맞지 않을 때, 다시 질문 상세 페이지로 이동
    # 질문 상세 페이지에 필요한 해당 question과 오류가 난 form(AnswerForm)전달 -> 에러 표시


@bp.route('/modify/<int:answer_id>', methods=('GET', 'POST')) # 답변 수정 
@login_required # 로그인이 필요한 기능
def modify(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    if g.user != answer.user: # 사용자가 답변 작성자가 아니라면
        flash("수정 권한이 없습니다.") # 권한 없음
        return redirect(url_for('question.detail', question_id=answer.question.id)) # 답변 상세 페이지로 리다이렉트
    if request.method == "POST": # 'POST' 요청
        form = AnswerForm() # 사용자로부터 입력받은 데이터를 폼에 저장
        if form.validate_on_submit(): # 입력된 데이터가 양식에 맞으면
            form.populate_obj(answer) # 폼에 있는 데이터를 answer 객체에 업데이트
            answer.modify_date = datetime.now() # 수정 일시 저장
            db.session.commit() # db 저장
            return redirect('{}#answer_{}'.format(url_for('question.detail', question_id=answer.question.id), answer.id)) # 답변 수정후 질문 상세 페이지로 리다이렉트
    else: # 'GET' 요청
        form = AnswerForm(obj=answer) # 답변 수정할 수 있도록 기존 내용 폼에 저장
    return render_template('answer/answer_form.html', form=form) # 답변 수정 폼으로 이동, 기존 내용도 전송


@bp.route('delete/<int:answer_id>') 
@login_required # 로그인이 필요한 기능
def delete(answer_id): # 답변 삭제 함수
    answer = Answer.query.get_or_404(answer_id)
    question_id = answer.question.id
    if g.user != answer.user: # 사용자가 답변 작성자가 아니라면
        flash("삭제 권한이 없습니다.") # 삭제 권한 없음
    else: # 사용자가 답변 작성자라면
        db.session.delete(answer) # 데이터베이스에서 답변 삭제
        db.session.commit() # db 저장
    return redirect(url_for('question.detail', question_id=question_id)) # 질문 상세 페이지로 리다이렉트


@bp.route('/vote/<int:answer_id>')
@login_required # 로그인이 필요한 기능
def vote(answer_id): # 답변 추천 함수
    _answer = Answer.query.get_or_404(answer_id)
    if g.user == _answer.user: # 사용자가 답변 작성자라면
        flash("본인이 작성한 글을 추천할 수 없습니다.") # 추천 권한 없음
    else: # 사용자가 답변 작성자가 아니라면
        _answer.voter.append(g.user) # 답변 추천인 중에 사용자 추가
        db.session.commit() # db 저장
    return redirect('{}#answer_{}'.format(url_for('question.detail', question_id=_answer.question.id), _answer.id)) # 질문 상세 페이지로 리다이렉트