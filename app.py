from flask import Flask, render_template, request, redirect, url_for
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)

SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
EMAIL_DESTINAZIONE = "edilvision.preventivi@gmail.com"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/send", methods=["POST"])
def send():
    nome = request.form.get("nome")
    email = request.form.get("email")
    numero = request.form.get("numero")
    lavoro = request.form.get("Tipo di lavoro")
    metratura = request.form.get("metratura")
    messaggio = request.form.get("messaggio")

    testo_email = f"""
Nuova richiesta preventivo – EdilVision

Nome: {nome}
Email: {email}
Numeri: {numero}
Tipo di lavoro: {lavoro}
Metratura: {metratura} m²

Messaggio:
{messaggio}
"""

    message = Mail(
        from_email=EMAIL_DESTINAZIONE,
        to_emails=EMAIL_DESTINAZIONE,
        subject="Nuova richiesta preventivo – EdilVision",
        plain_text_content=testo_email
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)
    except Exception as e:
        print("ERRORE SENDGRID:", e)
        return "Errore invio email", 500

    return redirect(url_for("grazie"))

@app.route("/grazie")
def grazie():
    return render_template("grazie.html")
