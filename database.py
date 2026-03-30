import sqlite3
from datetime import datetime

DB_NAME = "messages.db"

# Inicializa la base de datos y crea la tabla si no existe
def init_db():
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS mensajes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    contenido TEXT NOT NULL,
                    fecha_envio TEXT NOT NULL,
                    ip_cliente TEXT NOT NULL
                )
            ''')
            conn.commit()
    except sqlite3.Error as e:
        print(f"(!) Error al inicializar la DB: {e}")


# Guarda un mensaje en la base de datos y retorna el timestamp generado
def save_message(content, ip):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO mensajes (contenido, fecha_envio, ip_cliente)
                VALUES (?, ?, ?)
            ''', (content, ts, ip))
            conn.commit()
            return ts
    except sqlite3.Error as e:
        print(f"(!) Error al guardar mensaje en la DB: {e}")
        return None


# Recupera todos los mensajes para testing
def get_all_messages():
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM mensajes")
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"(!) Error al recuperar mensajes: {e}")
        return []