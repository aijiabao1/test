# Flask + MySQL 学生管理系统

这是一个基于 Flask 和 MySQL 开发的学生信息管理系统，实现了用户注册、登录、学生信息增删改查、搜索、密码加密和登录保护等功能。

## 技术栈

- Python
- Flask
- MySQL
- PyMySQL
- HTML
- CSS
- Werkzeug
- python-dotenv

## 功能介绍

- 用户注册
- 用户登录
- 退出登录
- 密码加密存储
- 学生列表展示
- 添加学生
- 修改学生
- 删除学生
- 搜索学生
- 登录状态保护

## 项目结构

```text
mysql_student_system/
├── app.py
├── db.py
├── create_admin.py
├── init_db.sql
├── requirements.txt
├── README.md
├── .env
├── .gitignore
├── static/
│   └── style.css
└── templates/
    ├── base.html
    ├── login.html
    ├── register.html
    ├── students.html
    ├── add.html
    └── edit.html