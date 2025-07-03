import sqlite3
from openai import OpenAI

client = OpenAI(api_key="")

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
        Może być jedna lub dwie poprawne odpowiedzi."""
    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[{'role': 'user', 'content': f"{prompt}"}],
        max_tokens=2500,
        stop=None,
        temperature=0.8
    )

    questions = response.choices[0].message.content

    import unicodedata

    base_key = 'historia'
    key = base_key
    index = 1

    def normalize_key(s):
        return ''.join(
            c for c in unicodedata.normalize('NFKD', s)
            if not unicodedata.combining(c)
        ).lower()

    while key_exists(cursor, normalize_key(key)):
        key = f"{base_key} {index}"
        index += 1

    value = questions
    cursor.execute(f"INSERT INTO questions VALUES ({key}, {value})")
    conn.commit()

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
