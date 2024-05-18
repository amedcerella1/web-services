from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
import openai

app = Flask(__name__)
openai.api_key = 'your_openai_api_key_here'

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=user_message,
        max_tokens=150
    )
    return jsonify(response.choices[0].text.strip())

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    send_email(name, email, message)
    return "Message sent successfully!"

def send_email(name, email, message):
    sender = 'your_email@example.com'
    recipient = 'your_email@example.com'
    subject = f"New Contact Form Submission from {name}"
    body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    with smtplib.SMTP('smtp.example.com', 587) as server:
        server.starttls()
        server.login('your_email@example.com', 'your_email_password')
        server.sendmail(sender, recipient, msg.as_string())

if __name__ == '__main__':
    app.run(debug=True)
