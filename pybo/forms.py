from flask_wtf import FlaskForm # Form을 만들기 위해 flask_wtf를 설치했고 FlaskForm을 import함.
from wtforms import StringField, TextAreaField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class QuestionForm(FlaskForm): # 플라스크의 폼은 FlaskForm 클래스를 상속하여 만들어야 함.
    subject = StringField('제목', validators=[DataRequired('제목은 필수 입력 항목입니다.')]) # Stringfield: 글자 수의 제한이 있음.
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수 입력 항목입니다.')]) # TextAreaField: 글자 수의 제한이 없음.
    # 첫번째 입력인수인 '제목'은 폼의 라벨 -> 템플릿에서 "제목"이라는 라벨을 출력할 수 있게 함.
    # 두번째 입력인수 validators: 검증을 위해 사용되는 도구, DataRequired: 필수 항목인지 체크

class AnswerForm(FlaskForm): # 답변 등록 폼
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수 입력 항목입니다.')]) # 답변은 내용만 있으면 됨.

class UserCreateForm(FlaskForm): # 계정 생성 폼
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)]) # username은 필수입력항목이며, 길이는 3 ~ 25 사이여야 함
    password1 = PasswordField('비밀번호', validators=[DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    # PasswordField: StringField와 비슷하지만 외부에서는 *******와 같은 형식으로 보임.
    # EqualTo: password1과 password2가 일치해야 한다는 조건
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    email = EmailField('이메일', validators=[DataRequired(), Email()])
    # Email(): 해당 속성의 값이 이메일 형식과 일치하는지를 검증

class UserLoginForm(FlaskForm): # 로그인 폼
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('비밀번호', validators=[DataRequired()])