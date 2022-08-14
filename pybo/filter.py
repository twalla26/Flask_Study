def format_datetime(value, fmt='%Y년 %m월 %d일 %p %I:%M'): # 전달 받은 datetime 객체(value)를 날짜포맷형식(fmt)에 맞게 변환하여 반환하는 함수
    return value.strftime(fmt) # 전달 받은 value가 없을 시 디폴트 값인 %Y년 %m월 %d일 %p %I:%M 이 사용됨