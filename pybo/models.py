from pybo import db # __init__.py 파일에서 db객체 import


question_voter = db.Table( # ManyToMany 관계를 적용하기 위해서는 db.Table을 통해 N:N 관계를 의미하는 테이블을 먼저 생성
    # question_voter는 사용자 id와 질문 id를 쌍으로 갖는 테이블 객체
    'question_voter', 
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('question_id', db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), primary_key=True)
    # 사용자 id와 질문 id가 모두 PK(primary_key)이므로 ManyToMany관계가 성립된다.
)

answer_voter = db.Table( # ManyToMany 관계를 적용하기 위해서는 db.Table을 통해 N:N 관계를 의미하는 테이블을 먼저 생성
    'answer_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('answer_id', db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), primary_key=True)
    # 사용자 id와 답변 id가 모두 PK(primary_key)이므로 ManyToMany관계가 성립된다.
)


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

    # 질문에 글쓴이를 추가하기
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False) # 글쓴이 고유 아이디 -> 외래키로 테이블 연결
    user = db.relationship('User', backref=db.backref('question_set')) # 글쓴이 모델 참조, question_set으로 역참조 설정도 가능

    modify_date = db.Column(db.DateTime(), nullable=True) # 글 수정날짜 추가, 빈값 허용

    voter = db.relationship('User', secondary=question_voter, backref=db.backref('question_voter_set'))
    # 첫 번쨰 속성 'User': voter는 추천인이므로 기본적으로 User 모델과 연결된 속성임.
    # 두 번째 속성 secondary: 다대다 기능 정의, 연관 테이블인 question_voter 테이블 객체를 참조
    # Question 모델을 통해 추천인을 저장하면 실제 데이터는 question_voter 테이블에 저장되고 저장된 추천인 정보는 Question 모델의 voter 속성을 통해 참조할 수 있게 된다.

class Answer(db.Model): # 질문에 대한 답변 모델
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    question = db.relationship('Question', backref=db.backref('answer_set', cascade='all, delete-orphan'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    # question_id: 답변을 달 질문 데이터의 고유 번호. 모델을 서로 연결해야 하므로 db.ForeigKey(외래키)를 사용.
    # db.ForeignKey의 첫 번째 파라미터 'question.id'는 Answer모델의 question_id 속성이 question 테이블의 id 컬럼과 연결됨을 의미. (question 객체의 속성인 id와 다름.) 테이블 != 객체
    # Question모델을 통해 테이블이 생성되면 테이블명은 question이 된다. (대소문자 때문에 헷갈리지 않도록 주의하자.)
    # 두번째 파라미터 ondelete는 삭제 연동 설정. 질문을 삭제하면 해당 답변들도 함께 삭제됨. (데이터베이스 설정이라, 데이터베이스 툴에서 쿼리로 삭제할 때만 답변들도 삭제된다.) -> 밑에서 보완됨.
    # question: 답변모델에서 질문 모델을 참조하기 위해 추가. db.relationship을 통해 답변 모델에서 연결된 질문 모델의 제목을 answer.question.subject로 참조할 수 있음.
    # db.relationship의 첫 번째 파라미터는 참조할 모델명(Question)이고, 두 번째 backref 파라미터는 역참조 설정임. 
    # 역참조: 질문에서 답변을 거꾸로 참조하는 것. (어떤 질문 객체가 a_question라면 a_question.answer_set로 질문에 달린 답변들을 참조할 수 있음.)
    # cascade='all, delete-orphan'을 통해 파이썬 코드만으로 답변 데이터 삭제가 가능해짐.
    
    # 답변에 답변 작성자 추가하기
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False) # 작성자 고유 아이디
    user = db.relationship('User', backref=db.backref('answer_set')) # 작성자 모델 참조, 역참조 설정

    modify_date = db.Column(db.DateTime(), nullable=True) # 글 수정 날짜, 빈값 허용

    voter = db.relationship('User', secondary=answer_voter, backref=db.backref('answer_voter_set'))
    # 첫 번쨰 속성 'User': voter는 추천인이므로 기본적으로 User 모델과 연결된 속성임.
    # 두 번째 속성 secondary: 다대다 기능 정의, 연관 테이블인 answer_voter 테이블 객체를 참조
    # Answer 모델을 통해 추천인을 저장하면 실제 데이터는 answer_voter 테이블에 저장되고 저장된 추천인 정보는 Answer 모델의 voter 속성을 통해 참조할 수 있게 된다.



class User(db.Model): # 사용자 모델
    id = db.Column(db.Integer, primary_key=True) # id는 자동으로 증가하는 User 모델의 기본 키
    username = db.Column(db.String(150), unique=True, nullable=False) # unique=True: 같은 값을 저장할 수 없다.
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

