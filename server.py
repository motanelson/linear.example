
from flask import Flask, request, redirect
import os
import hashlib

app = Flask(__name__)

lista1 = [
    "off_topic",
    "operation_system",
    "cosmos_os",
    "assembly",
    "programming",
    "hardware"
]

USERS_FILE = "users.txt"


# ---------- UTIL ----------
def sanitize(text):
    return text.replace("<", "").replace(">", "")


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def get_filename(category):
    return f"{category}.txt"


# ---------- USERS ----------
def load_users():
    users = {}

    if not os.path.exists(USERS_FILE):
        open(USERS_FILE, "w").close()

    with open(USERS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("|||")
            if len(parts) == 2:
                users[parts[0]] = parts[1]

    return users


def save_user(url, password_hash):
    with open(USERS_FILE, "a", encoding="utf-8") as f:
        f.write(f"{url}|||{password_hash}\n")


# ---------- POSTS ----------
def load_posts(category):
    posts = []
    filename = get_filename(category)

    if not os.path.exists(filename):
        open(filename, "w").close()

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("|||")
            if len(parts) == 2:
                posts.append((parts[0], parts[1]))

    return posts


def save_post(category, url, message):
    filename = get_filename(category)
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"{url}|||{message}\n")


# ---------- HOME ----------
@app.route("/")
def home():
    html = """
    <html>
    <head>
        <style>
            body { background:black; color:white; font-family:Arial; }
            a { color:#00ffff; display:block; margin:10px 0; }
        </style>
    </head>
    <body>
        <h1>Categorias</h1>
    """

    for cat in lista1:
        html += f'<a href="/{cat}">{cat}</a>'

    html += "</body></html>"
    return html


# ---------- CATEGORY ----------
@app.route("/<category>", methods=["GET", "POST"])
def category_page(category):
    if category not in lista1:
        return "Categoria inválida", 404

    error = ""

    if request.method == "POST":
        url = sanitize(request.form.get("url", ""))
        message = sanitize(request.form.get("message", ""))
        password = request.form.get("password", "")

        users = load_users()

        if url and message and password:
            hashed = hash_password(password)

            if url in users:
                # utilizador existe → validar password
                if users[url] != hashed:
                    error = "❌ Password errada!"
                else:
                    save_post(category, url, message)
                    return redirect(f"/{category}")
            else:
                # novo utilizador → registar
                save_user(url, hashed)
                save_post(category, url, message)
                return redirect(f"/{category}")

    posts = load_posts(category)

    html = f"""
    <html>
    <head>
        <style>
            body {{ background:black; color:white; font-family:Arial; }}
            textarea, input {{
                width:100%;
                background:#111;
                color:white;
                border:1px solid #555;
                padding:10px;
                margin-top:5px;
            }}
            button {{
                margin-top:10px;
                padding:10px;
                background:#333;
                color:white;
                border:none;
            }}
            hr {{ border:1px solid #444; }}
            a {{ color:#00ffff; }}
        </style>
    </head>
    <body>

        <a href="/">⬅ Voltar</a>

        <h2>{category}</h2>

        <form method="POST">
            <label>Endereço (URL):</label>
            <input type="text" name="url" required>

            <label>Password:</label>
            <input type="password" name="password" required>

            <label>Mensagem:</label>
            <textarea name="message" rows="4" required></textarea>

            <button type="submit">Submit</button>
        </form>

        <p style="color:red;">{error}</p>

        <hr>
        <h2>Mensagens</h2>
    """

    for url, msg in reversed(posts):
        html += f"""
        <div>
            <b>{url}</b><br>
            <p>{msg}</p>
        </div>
        <hr>
        """

    html += "</body></html>"
    return html


if __name__ == "__main__":
    app.run(debug=True)