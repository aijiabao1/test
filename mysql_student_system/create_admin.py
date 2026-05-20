import pymysql
from werkzeug.security import generate_password_hash


def get_conn():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="20021210",
        database="student_system",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn


conn = get_conn()
cursor = conn.cursor()

username = "admin"
password = "123456"

password_hash = generate_password_hash(password)

sql = "INSERT INTO users (username, password_hash) VALUES (%s, %s)"
data = (username, password_hash)

try:
    cursor.execute(sql, data)
    conn.commit()
    print("管理员账号创建成功")
except pymysql.err.IntegrityError:
    print("管理员账号已经存在")

cursor.close()
conn.close()