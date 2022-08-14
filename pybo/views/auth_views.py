from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import UserCreateForm, UserLoginForm
from pybo.models import User


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/signup/', methods=('GET', 'POST')) # 회원가입
def signup(): # 회원가입 함수
    form = UserCreateForm() # 폼은 유저 생성 폼 사용
    if request.method == 'POST' and form.validate_on_submit(): # POST 요청 -> 계정 저장
        user = User.query.filter_by(username=form.username.data).first() # 폼에 입력된 username으로 데이터를 조회해서 "이미 등록된 사용자"인지 확인
        # filter_by(): 폼으로 들어온 데이터와 데이터베이스에 있는 데이터를 매칭해서, first(): 첫 번째에 매칭되는 인스턴스를 반환
        if not user: # 신규 사용자라면, (이미 등록된 사용자가 아니라면)
            user = User(username=form.username.data,
                        password=generate_password_hash(form.password1.data),
                        email=form.email.data) # 폼에 입력된 데이터로 새로운 객체 user 생성
                        # 비밀번호는 generate_password_hash()함수로 암호화하여 저장
                        # generate_password_hash 함수로 암호화한 데이터는 복호화 불가 -> 로그인할 때 입력받은 비밀번호는 암호화하여 저장된 비밀번호와 비교해야 함.
            db.session.add(user) # 디비에 user 추가
            db.session.commit() # 디비 저장
            return redirect(url_for('main.index')) # 계정 생성 후 질문 목록 페이지로 이동
        else: # 이미 등록된 사용자라면,
            flash('이미 존재하는 사용자입니다.') # 오류 발생(필드 자체의 오류가 아니라 프로그램 논리 오류(컴파일과 실행은 정상작동하는 오류)를 발생시킴)
    return render_template('auth/signup.html', form=form) # GET 요청 -> 계정 등록 화면 출력, 템플릿에 필요한 form도 반환


@bp.route('/login/', methods=('GET', 'POST')) # 로그인
def login(): # 로그인 함수
    form = UserLoginForm() # 폼은 로그인 폼
    if request.method == 'POST' and form.validate_on_submit(): # POST 요청
        error = None # error에 기본값 None 저장
        user = User.query.filter_by(username=form.username.data).first() # 폼으로 들어온 데이터와 데이터베이스 조회 -> 기존에 있는 유저인지 확인
        if not user: # 기존에 없는 유저일 경우
            error = "존재하지 않는 사용자입니다." # error -> 오류 발생
        elif not check_password_hash(user.password, form.password.data): # 기존에 있는 유저지만, 비밀번호가 틀렸을 경우
        # check_password_hash 함수로 폼으로 입력 받은 password와 데이터베이스의 유저 password 비교
            error = "비밀번호가 올바르지 않습니다." # error -> 오류 발생
        if error is None: # 오류가 없을 경우 -> 로그인 가능
            # 플라스크 세션에 사용자 정보 저장
            session.clear() # 세션 초기화
            # 세션: request와 같이 플라스크가 자체적으로 생성하여 제공하는 객체, 서버에 브라우저별로 생성되는 메모리 공간이라고 할수 있다.
            # request의 경우, 브라우저가 플라스크 서버에 요청을 보내면 새로운 request객체가 생성되지만, session은 그 값을 계속 유지하는 특징이 있음.
            # 따라서 세션에 사용자의 id 값을 저장하면 다양한 URL 요청에 이 세션에 저장된 값을 읽을 수 있다. 
            # 예를 들어 세션 정보를 확인하여 현재 요청한 주체가 로그인한 사용자인지 아닌지를 판별할 수 있다
            session['user_id'] = user.id # 키는 'user_id' 문자열, 값은 데이터베이스에서 조회한 사용자의 고유 아이디
            return redirect(url_for('main.index')) # 로그인 후, 메인 페이지(질문 목록 페이지)로 이동
        flash(error) # 오류가 있을 경우 -> flash()함수로 오류 표시
    return render_template('auth/login.html', form=form) # GET 요청 -> 로그인 페이지로 이동, 로그인 페이지에 필요한 form 전송.


@bp.before_app_request # -> 모든 라우팅 함수보다 항상 먼저 실행됨.
def load_logged_in_user(): # 사용자 로그인 여부 확인 함수
    user_id = session.get('user_id') # 세션에 저장된 'user_id'를 가져와 user_id에 저장
    if user_id is None: # 만약 세션에 저장된 'user_id' 값이 없다면
        g.user = None # g.user에 None 저장
        # g: 플라스크의 컨텍스트 변수(global 변수), request 변수와 같이 [요청 -> 응답] 과정에서 유효함.
    else: # session 변수에 user_id값이 있으면 
        g.user = User.query.get(user_id) # 데이터베이스에서 사용자 정보를 조회하여 g.user에 저장
    # -> 이후 사용자 로그인 검사를 할 때 session을 조사할 필요 없이, g.user에 값이 있는지만 확인하면 됨. 
    # g.user에는 사용자 객체가 저장되어 있으므로 여러 가지 사용자 정보(username, email 등)를 추가로 얻어내는 이점이 있음.

    
@bp.route('/logout/') # 로그아웃
def logout(): # 로그아웃 함수
    session.clear() # 세션 초기화 -> 로그인 기록 삭제
    return redirect(url_for('main.index')) # 로그아웃 후 메인 페이지로 이동
