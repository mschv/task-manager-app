import sqlite3

DB_NAME="tasks.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        c=conn.cursor()

        #create users table
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')

        #create tasks table
        c.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                category TEXT,
                deadline TEXT,
                priority TEXT,
                completed INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        conn.commit()

def add_user(username,password):
    with sqlite3.connect(DB_NAME)as conn:
        c=conn.cursor()
        try:
            c.execute("INSERT INTO users(username,password) VALUES(?,?)",(username,password))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False #Username already exists
        
def get_user(username):
    with sqlite3.connect(DB_NAME) as conn:
        c=conn.cursor()
        c.execute("SELECT * FROM users WHERE username =?",(username,))
        return c.fetchone() #returns tupple or None

def add_task(user_id, title, category, deadline, priority):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''INSERT INTO tasks (user_id, title, category, deadline, priority)
                     VALUES (?, ?, ?, ?, ?)''',
                  (user_id, title, category, deadline, priority))
        conn.commit()

def get_tasks_by_user(user_id):
    with sqlite3.connect(DB_NAME) as conn:
        c=conn.cursor()
        c.execute("SELECT * FROM tasks WHERE user_id=?",(user_id,))
        return c.fetchall()

def mark_task_complete(task_id):
    with sqlite3.connect(DB_NAME) as conn:
        c=conn.cursor()
        c.execute("UPDATE tasks SET completed=1 WHERE id=?",(task_id,))
        conn.commit()

def toggle_task_completion(task_id):
    with sqlite3.connect(DB_NAME) as conn:
        c=conn.cursor()
        c.execute('''UPDATE tasks 
                     SET completed = CASE completed WHEN 1 THEN 0 ELSE 1 END 
                     WHERE id = ?''', (task_id,))
        conn.commit()

def delete_task(task_id):
    with sqlite3.connect(DB_NAME) as conn:
        c=conn.cursor()
        c.execute("DELETE FROM tasks WHERE id=?",(task_id,))
        conn.commit()

def get_task_by_id(task_id):
    with sqlite3.connect(DB_NAME) as conn:
        c=conn.cursor()
        c.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        return c.fetchone()

def update_task(task_id,title,category,deadline,priority):
    with sqlite3.connect(DB_NAME)as conn:
        c=conn.cursor()
        c.execute('''UPDATE tasks SET title = ?, category = ?, deadline = ?, priority = ? 
                     WHERE id = ?''',
                  (title, category, deadline, priority, task_id))
        conn.commit()

def get_db_connection():
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row
    return conn

def get_tasks_by_status(user_id, completed):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM tasks WHERE user_id = ? AND completed = ?", (user_id, int(completed)))
    tasks = c.fetchall()
    conn.close()
    return tasks
