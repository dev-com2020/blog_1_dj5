import sqlite3
from openai import OpenAI

client = OpenAI(api_key="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")

def initialize_database():
    conn = sqlite3.connect('question.db')
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS questions (
                      id INTEGER PRIMARY KEY, key TEXT UNIQUE, value TEXT)""")

    conn.commit()
    conn.close()

def generate_questions(text):
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

    base_key = ' '.join(text.split()[:2])
    key = base_key
    index=1
    while key_exists(cursor, key):
        key = f"{base_key} {index}"
        index += 1

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
