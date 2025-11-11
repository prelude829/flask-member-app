# Flask 모듈에서 Flask 클래스, render_template(HTML 렌더링),
# request(요청 데이터 처리), redirect(페이지 이동) 함수 가져오기
from flask import Flask, render_template, request, redirect

# MySQL 데이터베이스 연동을 위한 mysql-connector-python 모듈 가져오기
import mysql.connector

# Flask 애플리케이션 객체 생성
app = Flask(__name__)

# --------------------------------------------
# MySQL 데이터베이스 연결 설정
# --------------------------------------------
db = {
    # 'host': ‘192.168.1.15',  <- 이 부분 따옴표(‘)가 잘못되어 있었습니다.
    'host': 'mysql',                  # mysql 서비스(원격에 있음)
    'user': 'flaskuser',
    'password': 'flask1234',
    'database': 'flaskdb',
    'charset': 'utf8mb4',             # ★ 한글 깨짐 방지
    'use_unicode': True,              # ★ 파이썬에서 유니코드로 받기
    'collation': 'utf8mb4_unicode_ci' # (선택) 정렬도 UTF-8로
}

# --------------------------------------------
# 1) 회원 목록 페이지
# --------------------------------------------
@app.route('/')                   # '/' URL 접근 시 실행됨 (홈 화면)
def index():
    conn = mysql.connector.connect(**db)             # DB 연결
    cur = conn.cursor(dictionary=True)               # 컬럼명을 키로 반환
    cur.execute("SELECT * FROM members")             # 전체 회원 조회
    rows = cur.fetchall()                            # 결과 리스트 반환
    conn.close()                                     # 연결 종료
    return render_template('index.html', members=rows)  # 결과 전달

# --------------------------------------------
# 2) 회원 추가 페이지
# --------------------------------------------
@app.route('/add', methods=['GET', 'POST'])          # GET/POST 요청 모두 허용
def add():
    if request.method == 'POST':                     # 폼 제출 시 처리
        name = request.form['name']                  # 입력값 추출
        email = request.form['email']
        city = request.form['city']

        conn = mysql.connector.connect(**db)         # DB 연결
        cur = conn.cursor()                          # 커서 생성
        cur.execute(                                 # INSERT 실행
            "INSERT INTO members (name, email, city) VALUES (%s, %s, %s)",
            (name, email, city)
        )
        conn.commit()                                # 변경사항 저장
        conn.close()                                 # 연결 종료
        return redirect('/')                         # 목록 페이지로 이동

    return render_template('add.html')               # GET 요청 시 입력 폼 표시

# --------------------------------------------
# 3) 회원 수정
# --------------------------------------------
# <int:id> 부분이 빠져있어서 추가했습니다.
@app.route('/edit/<int:id>', methods=['GET', 'POST']) # 회원 id를 URL 파라미터로 받아 GET/POST 요청 모두 허용
def edit(id):
    conn = mysql.connector.connect(**db)                   # DB 연결
    cur = conn.cursor(dictionary=True)                     # 컬럼명을 키로 반환하는 딕셔너리 커서 생성

    if request.method == 'POST':                           # POST 요청(수정 폼 제출 시)
        name = request.form['name']                        # 폼 입력값 추출
        email = request.form['email']
        city = request.form['city']

        cur.execute(                                       # members 테이블의 해당 id 레코드 수정
            "UPDATE members SET name=%s, email=%s, city=%s WHERE id=%s",
            (name, email, city, id)
        )
        conn.commit()                                      # 변경사항 저장
        conn.close()                                       # 연결 종료
        return redirect('/')                               # 수정 후 목록 페이지로 이동

    # GET 요청 시 (수정 폼 표시)
    cur.execute("SELECT * FROM members WHERE id=%s", (id,)) # GET 요청 시 해당 회원 조회
    member = cur.fetchone()                                # 한 건만 가져오기
    conn.close()                                           # 연결 종료
    return render_template('edit.html', member=member)     # edit.html에 회원 데이터 전달

# --------------------------------------------
# 4) 회원 삭제
# --------------------------------------------
# <int:id> 부분이 빠져있어서 추가했습니다.
@app.route('/delete/<int:id>')                    # URL에서 회원 id를 전달받음
def delete(id):
    conn = mysql.connector.connect(**db)          # DB 연결
    cur = conn.cursor()                           # 커서 생성
    cur.execute("DELETE FROM members WHERE id=%s", (id,))  # 해당 id 회원 삭제
    conn.commit()                                 # 변경사항 저장
    conn.close()                                  # 연결 종료
    return redirect('/')                          # 삭제 후 목록 페이지로 이동


# Flask 앱 실행 구문
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # ← 컨테이너 외부에서도 접근 가능