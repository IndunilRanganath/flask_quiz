import sqlite3
from flask import g

def connect_to_database():
    sql = sqlite3.connect("D:/Professional Course/Working/flask_quiz/quizapp.db")
    sql.row_factory = sqlite3.Row
    return sql

def getDatabase():
    if not hasattr(g, "quizapp_db"):
        g.quizapp_db = connect_to_database()
    return g.quizapp_db