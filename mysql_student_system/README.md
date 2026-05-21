# 学生管理系统

这是一个基于 Python Flask 和 MySQL 开发的学生管理系统，主要用于练习 Python Web 后端开发、数据库操作、用户登录注册和基础 API 接口设计。

## 一、项目功能

本项目目前实现了以下功能：

- 用户注册
- 用户登录
- 用户退出
- 密码加密存储
- 登录状态保护
- 管理员权限控制
- 学生信息添加
- 学生信息查询
- 学生信息修改
- 学生信息删除
- 学生姓名搜索
- 学生信息 API 接口

## 二、技术栈

- Python
- Flask
- MySQL
- PyMySQL
- HTML
- CSS
- Werkzeug
- python-dotenv

## 三、项目结构

```text
mysql_student_system/
├── app.py              # Flask 主程序
├── dp.py               # 数据库连接配置
├── create_admin.py     # 创建管理员账号
├── init_db.sql         # 数据库初始化文件
├── requirements.txt    # 项目依赖
├── .env.example        # 环境变量示例
├── templates/          # HTML 页面
├── static/             # 静态资源
└── README.md           # 项目说明文档