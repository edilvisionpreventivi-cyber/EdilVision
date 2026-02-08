from flask import Flask, render_template, request, redirect, url_for
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)

SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
MIA_EMAIL = "edilvision.preventivi@gmail.com"  # mittente e destinatario

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/send", methods=["POST"])
def send():
    nome = request.form["nome"]
    email = request.form["email"]
    lavoro = request.form["lavoro"]
    metratura = request.form["metratura"]
    messaggio = request.form["messaggio"]

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

    message = Mail(
        from_email=MIA_EMAIL,
        to_emails=MIA_EMAIL,
        subject="Nuova richiesta preventivo",
        plain_text_content=body
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print("Errore invio email:", e)
        return f"Errore nell'invio della richiesta: {e}"

    return redirect(url_for("grazie"))

@app.route("/grazie")
def grazie():
    return render_template("grazie.html")

if __name__ == "__main__":
    app.run(debug=True)
