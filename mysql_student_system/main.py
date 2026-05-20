import pymysql


def get_conn():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="20021210",
        database="student_system",
        charset="utf8mb4"
    )
    return conn


def add_student():
    name = input("请输入学生姓名：")
    age = int(input("请输入学生年龄："))
    score = float(input("请输入学生成绩："))

    conn = get_conn()
    cursor = conn.cursor()

    sql = "INSERT INTO students (id,name, age, score) VALUES (%s,%s, %s, %s)"
    id = int(input("请输入学生id："))
    data = (id, name, age, score)

    cursor.execute(sql, data)
    conn.commit()

    print("添加成功")

    cursor.close()
    conn.close()


def show_students():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    if not students:
        print("暂无学生数据")
    else:
        for student in students:
            print(student)

    cursor.close()
    conn.close()


def search_student():
    student_id = int(input("请输入要查询的学生id："))

    conn = get_conn()
    cursor = conn.cursor()

    sql = "SELECT * FROM students WHERE id = %s"
    data = (student_id,)

    cursor.execute(sql, data)
    student = cursor.fetchone()

    if student:
        print(student)
    else:
        print("没有找到该学生")

    cursor.close()
    conn.close()


def update_student():
    student_id = int(input("请输入要修改的学生id："))
    new_score = float(input("请输入新的成绩："))

    conn = get_conn()
    cursor = conn.cursor()

    sql = "UPDATE students SET score = %s WHERE id = %s"
    data = (new_score, student_id)

    cursor.execute(sql, data)
    conn.commit()

    if cursor.rowcount > 0:
        print("修改成功")
    else:
        print("没有找到该学生")

    cursor.close()
    conn.close()


def delete_student():
    student_id = int(input("请输入要删除的学生id："))

    conn = get_conn()
    cursor = conn.cursor()

    sql = "DELETE FROM students WHERE id = %s"
    data = (student_id,)

    cursor.execute(sql, data)
    conn.commit()

    if cursor.rowcount > 0:
        print("删除成功")
    else:
        print("没有找到该学生")

    cursor.close()
    conn.close()


def menu():
    while True:
        print("\n===== 学生管理系统 =====")
        print("1. 添加学生")
        print("2. 查看所有学生")
        print("3. 根据id查询学生")
        print("4. 修改学生成绩")
        print("5. 删除学生")
        print("6. 退出系统")

        choice = input("请选择功能：")

        if choice == "1":
            add_student()
        elif choice == "2":
            show_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            update_student()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            print("系统已退出")
            break
        else:
            print("输入错误，请重新选择")


menu()