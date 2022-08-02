from pybo import db # __init__.py 파일에서 db객체 import


class Question(db.Model): # 모델 클래스를 만드려면 db.Model 클래스를 상속하여 만들어야 함. 이때 db는 __init__.py파일에서 생성한 SQLAlchemy 클래스의 객체임.
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    # 질문 데이터의 속성은 id(질문 데이터의 고유 번호), subject(질문 제목), content(질문 내용), create_date(질문 작성일시)로 구성
    # 각 속성은 db.Column으로 생성. 데이터 타입에 대한 정보와 제약 조건을 넣을 수 있음. 기본적으로 변수명이 칼럼의 이름이 됨.
    # db.Column의 첫 번째 인수는 데이터 타입 -> 속성에 저장할 데이터의 종류 결정 
    # (Integer: 정수, String: 제목처럼 글자 수가 제한된 텍스트, Text: 글자 수 제한이 없는 텍스트, DateTime: 날짜와 시각)
    # primary_key: 아이디 속성을 기본 키로 설정 -> 데이터베이스에서 중복된 값을 가질 수 없게 만듦. id는 모델에서 각 데이터를 구분할 수 있는 유일한 값이므로 기본 키로 설정함.
    # 기본 키로 설정한 속성은 값이 1부터 자동으로 증가하여 저장됨.
    # nullabl: 속성에 값을 저장할 때 빈 값을 허용할 지의 여부. nullable을 설정해두지 않으면 기본으로 빈 값을 허용함.

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    question = db.relationship('Question', backref=db.backref('answer_set'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    # question_id: 답변을 달 질문 데이터의 고유 번호. 모델을 서로 연결해야 하므로 db.ForeigKey(외래키)를 사용.
    # db.ForeignKey의 첫 번째 파라미터 'question.id'는 Answer모델의 question_id 속성이 question 테이블의 id 컬럼과 연결됨을 의미. (question 객체의 속성인 id와 다름.) 테이블 != 객체
    # Question모델을 통해 테이블이 생성되면 테이블명은 question이 된다. (대소문자 때문에 헷갈리지 않도록 주의하자.)
    