# database.py
import sqlite3

DB_PATH = "chatbot.db"  # .db 파일 하나가 곧 전체 데이터베이스

def get_connection():
    # sqlite3.connect(): 지정한 경로의 DB 파일에 연결 (없으면 자동 생성)
    conn = sqlite3.connect(DB_PATH)

    # row_factory 설정: DB 조회 결과를 어떤 형태로 받을지 지정
    # sqlite3.Row로 설정하면 row["content"] 처럼 컬럼 이름으로 접근할 수 있고,
    # dict(row)로 Python 딕셔너리로 변환하는 것도 가능해집니다.
    # (이 설정이 없으면 결과가 일반 튜플로 오기 때문에 컬럼 이름 접근 불가)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """DB에 테이블이 없으면 생성. 서버를 재시작해도 기존 데이터는 유지됨."""
    conn = get_connection()

    # CREATE TABLE IF NOT EXISTS: 테이블이 이미 있으면 아무것도 안 하고, 없을 때만 생성
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            content TEXT    NOT NULL
        )
    """)

    # conn.commit(): 실행한 SQL을 실제로 DB 파일에 저장(확정)합니다.
    # INSERT/UPDATE/DELETE/CREATE 등 변경 작업 후에는 반드시 commit()을 호출해야 합니다.
    # commit() 전까지는 변경사항이 메모리에만 있고 아직 파일에 기록되지 않은 상태입니다.
    conn.commit()

    # conn.close(): DB 연결을 닫습니다.
    # DB 연결은 파일 핸들과 메모리를 사용하므로, 작업이 끝나면 반드시 닫아야 합니다.
    # 닫지 않으면 연결이 계속 열려 있어 리소스 낭비 및 충돌이 발생할 수 있습니다.
    conn.close()