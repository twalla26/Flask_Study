import os # os 모듈 import
# os(Operating System)는 운영체제에서 제공되는 여러가지 기능을 파이썬에서 수행할 수 있게 해줌.

BASE_DIR = os.path.dirname(__file__) # BASE_DIR에 현재 파일의 디렉터리 주소 저장
# __file__은 파이썬 내장변수로서, 현재 수행하고 있는 코드를 담고 있는 파일이 위치한 path, 즉 경로를 반환해줌.


SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db')) # SQLALCHEMY_DATABASE_URI에는 데이터베이스 접속 주소가 저장됨.
# SQLALCHEMY_DATABASE_URI 설정으로 SQLite 데이터베이스가 사용되고 데이터베이스 파일은 앞서 언급한 BASE_DIR 바로 밑에 pybo.db파일로 저장됨.
# SQLite는 파이썬 기본 패키지에 포함된 데이터베이스로, 주로 소규모 프로젝트에서 사용하는 가벼운 파일을 기반으로 한 데이터베이스다.
SQLALCHEMY_TRACK_MODIFICATIONS = False 
# SQLALCHEMY_TRACK_MODIFICATIONS는 수정사항을 추적하고 신호를 내보낸다던데, 추가적인 메모리를 필요로 하고 현 프로젝트에서 불필요한 기능이니 비활성화.