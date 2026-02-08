from flask import Flask, render_template, request, redirect, url_for
from threading import Thread
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)

# ================= CONFIGURAZIONE EMAIL =================
MIA_EMAIL = "edilvision.preventivi@gmail.com"
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")  # Password app Gmail impostata su Render

# ================= FUNZIONE PER INVIO EMAIL IN BACKGROUND =================
def invia_email(body):
    try:
        msg = MIMEText(body)
        msg["Subject"] = "Nuova richiesta preventivo – EdilVision"
        msg["From"] = MIA_EMAIL
        msg["To"] = MIA_EMAIL

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(MIA_EMAIL, EMAIL_PASSWORD)
            server.send_message(msg)

        print("Email inviata con successo!")
    except Exception as e:
        print(f"Errore nell'invio dell'email: {e}")

# ================= ROTTE =================
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/send", methods=["POST"])
def send():
    # Prendo i dati dal form
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

    # Invio email in background
    Thread(target=invia_email, args=(body,)).start()

    # Redirect alla pagina di conferma
    return redirect(url_for("grazie"))

@app.route("/grazie")
def grazie():
    return render_template("grazie.html")

# ================= AVVIO SERVER =================
if __name__ == "__main__":
    # debug=True solo in locale
    app.run(debug=True)

