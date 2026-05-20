import os
from flask import Flask, render_template, request, redirect,session,jsonify
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash
import pymysql
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

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
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect("/login")
        return func(*args, **kwargs)
    return wrapper

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect("/login")

        if session.get("role") != "admin":
            return "没有权限访问该页面", 403

        return func(*args, **kwargs)

    return wrapper

@app.route("/")
def home():
    return "欢迎来到学生管理系统"

@app.route("/students")
def students():
    keyword = request.args.get("keyword", "")

    conn = get_conn()
    cursor = conn.cursor()

    if keyword:
        sql = "SELECT * FROM students WHERE name LIKE %s"
        data = ("%" + keyword + "%",)
        cursor.execute(sql, data)
    else:
        cursor.execute("SELECT * FROM students")

    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("students.html", students=result, keyword=keyword)


@app.route("/add", methods=["GET", "POST"])
@admin_required
def add_student():
    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        score = request.form.get("score")

        if not name:
            return render_template("add.html", error="姓名不能为空")

        if not age:
            return render_template("add.html", error="年龄不能为空")

        if not score:
            return render_template("add.html", error="成绩不能为空")

        age = int(age)
        score = float(score)

        if age <= 0 or age > 120:
            return render_template("add.html", error="年龄必须在 1 到 120 之间")

        if score < 0 or score > 100:
            return render_template("add.html", error="成绩必须在 0 到 100 之间")

        conn = get_conn()
        cursor = conn.cursor()

        sql = "INSERT INTO students (name, age, score) VALUES (%s, %s, %s)"
        data = (name, age, score)

        cursor.execute(sql, data)
        conn.commit()

        cursor.close()
        conn.close()

        return redirect("/students")

    return render_template("add.html")

@app.route("/delete/<int:student_id>")
@admin_required
def delete_student(student_id):
    conn = get_conn()
    cursor = conn.cursor()

    sql = "DELETE FROM students WHERE id = %s"
    data = (student_id,)

    cursor.execute(sql, data)
    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/students")

@app.route("/edit/<int:student_id>", methods=["GET", "POST"])
@admin_required
def edit_student(student_id):
    conn = get_conn()
    cursor = conn.cursor()

    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        score = request.form.get("score")

        sql = "UPDATE students SET name=%s, age=%s, score=%s WHERE id=%s"
        data = (name, age, score, student_id)

        cursor.execute(sql, data)
        conn.commit()

        cursor.close()
        conn.close()

        return redirect("/students")

    sql = "SELECT * FROM students WHERE id = %s"
    data = (student_id,)

    cursor.execute(sql, data)
    student = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template("edit.html", student=student)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return render_template("login.html", error="用户名和密码不能为空")

        conn = get_conn()
        cursor = conn.cursor()

        sql = "SELECT * FROM users WHERE username = %s"
        data = (username,)

        cursor.execute(sql, data)
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user and check_password_hash(user["password_hash"], password):
            session["logged_in"] = True
            session["username"] = user["username"]
            session["user_id"] = user["id"]
            session["role"] = user["role"]
            return redirect("/students")
        else:
            return render_template("login.html", error="用户名或密码错误")

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if not username or not password or not confirm_password:
            return render_template("register.html", error="所有字段都不能为空")

        if password != confirm_password:
            return render_template("register.html", error="两次输入的密码不一致")

        if len(password) < 6:
            return render_template("register.html", error="密码长度不能少于 6 位")

        password_hash = generate_password_hash(password)

        conn = get_conn()
        cursor = conn.cursor()

        sql = "INSERT INTO users (username, password_hash) VALUES (%s, %s)"
        data = (username, password_hash)

        try:
            cursor.execute(sql, data)
            conn.commit()
        except pymysql.err.IntegrityError:
            cursor.close()
            conn.close()
            return render_template("register.html", error="用户名已存在")

        cursor.close()
        conn.close()

        return redirect("/login")

    return render_template("register.html")

@app.route("/api/students", methods=["GET", "POST"])
def api_students():
    if not session.get("logged_in"):
        return jsonify({
            "code": 401,
            "message": "请先登录",
            "data": None
        }), 401

    conn = get_conn()
    cursor = conn.cursor()

    if request.method == "GET":
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify({
            "code": 200,
            "message": "查询成功",
            "data": students
        })

    if request.method == "POST":
        if session.get("role") != "admin":
            cursor.close()
            conn.close()

            return jsonify({
                "code": 403,
                "message": "没有权限添加学生",
                "data": None
            }), 403

        data = request.get_json(silent=True) or {}

        name = data.get("name")
        age = data.get("age")
        score = data.get("score")

        if not name:
            cursor.close()
            conn.close()
            return jsonify({
                "code": 400,
                "message": "姓名不能为空",
                "data": None
            }), 400

        try:
            age = int(age)
            score = float(score)
        except:
            cursor.close()
            conn.close()
            return jsonify({
                "code": 400,
                "message": "年龄和成绩格式错误",
                "data": None
            }), 400

        if age <= 0 or age > 120:
            cursor.close()
            conn.close()
            return jsonify({
                "code": 400,
                "message": "年龄必须在 1 到 120 之间",
                "data": None
            }), 400

        if score < 0 or score > 100:
            cursor.close()
            conn.close()
            return jsonify({
                "code": 400,
                "message": "成绩必须在 0 到 100 之间",
                "data": None
            }), 400

        sql = "INSERT INTO students (name, age, score) VALUES (%s, %s, %s)"
        cursor.execute(sql, (name, age, score))
        conn.commit()

        new_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return jsonify({
            "code": 201,
            "message": "添加成功",
            "data": {
                "id": new_id,
                "name": name,
                "age": age,
                "score": score
            }
        }), 201

@app.route("/api/students/<int:student_id>")
@login_required
def api_student_detail(student_id):
    conn = get_conn()
    cursor = conn.cursor()

    sql = "SELECT * FROM students WHERE id = %s"
    data = (student_id,)

    cursor.execute(sql, data)
    student = cursor.fetchone()

    cursor.close()
    conn.close()

    if student:
        return jsonify({
            "code": 200,
            "message": "查询成功",
            "data": student
        })
    else:
        return jsonify({
            "code": 404,
            "message": "学生不存在",
            "data": None
        })

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)