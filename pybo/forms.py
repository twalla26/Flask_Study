from flask_wtf import FlaskForm # Form을 만들기 위해 flask_wtf를 설치했고 FlaskForm을 import함.
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired


class QuestionForm(FlaskForm): # 플라스크의 폼은 FlaskForm 클래스를 상속하여 만들어야 함.
    subject = StringField('제목', validators=[DataRequired('제목은 필수 입력 항목입니다.')]) # Stringfield: 글자 수의 제한이 있음.
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수 입력 항목입니다.')]) # TextAreaField: 글자 수의 제한이 없음.
    # 첫번째 입력인수인 '제목'은 폼의 라벨 -> 템플릿에서 "제목"이라는 라벨을 출력할 수 있게 함.
    # 두번째 입력인수 validators: 검증을 위해 사용되는 도구, DataRequired: 필수 항목인지 체크
