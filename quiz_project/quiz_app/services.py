import sqlite3
from openai import OpenAI

from . import config

client = OpenAI(api_key=config.API_KEY)

def initialize_database():
    conn = sqlite3.connect('question.db')
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS questions (
                      id INTEGER PRIMARY KEY, key TEXT UNIQUE, value TEXT)""")

    conn.commit()
    conn.close()

def generate_questions(text):
    initialize_database()
    conn = sqlite3.connect('question.db')
    cursor = conn.cursor()
    prompt = f"""Stwórz test składający się z 10 pytań, z wieloma odpowiedziami na temat: {text}.
        Każde pytanie będzie w osobnej linii, oraz ustaw możliwe 4 odpowiedzi.
        Może być jedna lub dwie poprawne odpowiedzi.
        Podaj listę poprwanych odpowiedzi na końcu."""
    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[{'role': 'user', 'content': f"{prompt}"}],
        max_tokens=2500,
        stop=None,
        temperature=0.8
    )

    questions = response.choices[0].message.content

    import unicodedata

    def normalize_key(s):
        return ''.join(
            c for c in unicodedata.normalize('NFKD', s)
            if not unicodedata.combining(c)
        ).lower()

    base_key = normalize_key(text)
    key = base_key
    index = 1

    while key_exists(cursor, normalize_key(key)):
        key = f"{base_key} {index}"
        index += 1

    value = questions
    cursor.execute(
        "INSERT INTO questions (key, value) VALUES (?, ?)",
        (key, value)
    )
    conn.commit()
    conn.close()

    return questions


def key_exists(cursor,key):
    cursor.execute("SELECT COUNT(*) FROM questions WHERE key = ?", (key,))
    count = cursor.fetchone()[0]
    return count > 0

def print_all_questions():
    initialize_database()
    conn = sqlite3.connect('question.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions")
    rows = cursor.fetchall()
    return rows