from src.models.user import User
import sqlite3
from typing import List


def fetch_users_from_database(database_path: str) -> List[User]:
    
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user")
    rows = cursor.fetchall()

    users = []
    for row in rows:

        user = User(username=row[0], full_name=row[1], email=row[2], hashed_password=row[3])
        users.append(user)
    
    conn.close()

    return users

def save_user_to_database(database_path: str, user: User):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO user (username, full_name, email, hashed_password)
        VALUES (?, ?, ?, ?)
    """, (user.username, user.full_name, user.email, user.hashed_password))

    conn.commit()
    conn.close()




