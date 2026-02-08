# app.py
from flask import Flask, render_template, request, redirect, url_for
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)

# ================= CONFIGURAZIONE EMAIL =================
MIA_EMAIL = os.environ.get("MIA_EMAIL")          # la tua email Gmail
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")  # la password app Gmail

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/send", methods=["POST"])
def send():
    nome = request.form.get("nome")
    email = request.form.get("email")
    lavoro = request.form.get("lavoro")
    metratura = request.form.get("metratura")
    messaggio = request.form.get("messaggio")

    # Corpo email
    body = f"""
Nuova richiesta preventivo – EdilVision

Nome: {nome}
Email: {email}
Tipo di lavoro: {lavoro}
Metratura: {metratura} m²

Messaggio:
{messaggio}
    """

    # Creazione email
    msg = MIMEText(body)
    msg["Subject"] = "Nuova richiesta preventivo"
    msg["From"] = MIA_EMAIL
    msg["To"] = MIA_EMAIL

    # Invio email
    try:
        print("Provo a inviare email...")
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(MIA_EMAIL, EMAIL_PASSWORD)
            server.send_message(msg)
        print("Email inviata correttamente!")
    except Exception as e:
        print("Errore invio email:", e)
        # opzionale: mostrare messaggio all'utente
        return f"Errore nell'invio della richiesta: {e}"

    # Redirect alla pagina di conferma
    return redirect(url_for("grazie"))

@app.route("/grazie")
def grazie():
    return render_template("grazie.html")

# Entry point per Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
