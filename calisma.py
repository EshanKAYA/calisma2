from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2, os

app = Flask(__name__)
CORS(app)

# DİKKAT: Render'da bu değeri ÇEVRESEL DEĞİŞKEN (Environment Variable) olarak ayarlayacağız.
# Kod içindeki bu değer, sadece yerel test için yedektir.
DATABASE_URL = os.getenv("DATABASE_URL","")

def connect_db():
    return psycopg2.connect(DATABASE_URL)

@app.route("/ziyaretciler", methods=["GET", "POST"])
def ziyaretciler():
    conn = connect_db()
    cur = conn.cursor()
    
    # Tabloyu oluştur (eğer yoksa)
    cur.execute("CREATE TABLE IF NOT EXISTS ziyaretciler (id SERIAL PRIMARY KEY, isim TEXT)")
    
    if request.method == "POST":
        isim = request.json.get("isim")
        if isim:
            cur.execute("INSERT INTO ziyaretciler (isim) VALUES (%s)", (isim,))
            conn.commit()
    
    # Son 10 ziyaretçiyi çek
    cur.execute("SELECT isim FROM ziyaretciler ORDER BY id DESC LIMIT 10")
    isimler = [row[0] for row in cur.fetchall()]
    
    cur.close()
    conn.close()
    
    return jsonify(isimler)

if __name__ == "__main__":
    # Render'da çalışırken bu kısım Gunicorn tarafından devralınır.
    app.run(host="0.0.0.0", port=5001)
