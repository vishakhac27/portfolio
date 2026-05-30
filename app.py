from flask import Flask, render_template, request, redirect
from models import db, Contact  
from flask import session
import os
from flask import jsonify
from flask_mail import Mail, Message


app = Flask(__name__)
app.secret_key = "secret123"

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'vishakhachachane@gmail.com'
app.config['MAIL_PASSWORD'] = 'mzbyacpkenpitezx'

mail = Mail(app)


basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
@app.route("/ai", methods=["POST"])
def ai():
    user_message = request.json.get("message")


    if "skills" in user_message.lower():
        reply = "I know Python, Flask, SQL, HTML, CSS, JavaScript and basic AI integration."
    elif "project" in user_message.lower():
        reply = "I have built a Flask portfolio, Pharmacy Management System, and AI chatbot project."
    elif "you" in user_message.lower():
        reply = "I am a full-stack developer skilled in Flask and learning Generative AI."
    else:
        reply = "I am still learning AI, but I can help with portfolio related questions."

    return jsonify({"reply": reply})

@app.route("/admin")
def admin():
    messages = Contact.query.order_by(Contact.id.desc()).all()
    return render_template("admin.html", messages=messages)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/messages")
def messages():
    data = Contact.query.all()
    for d in data:
        print(d.name, d.email, d.message)
    return "Check terminal"
 
@app.route("/delete/<int:id>")
def delete(id):
    msg = Contact.query.get(id)
    db.session.delete(msg)
    db.session.commit()
    return redirect("/admin")

@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    new_contact = Contact(name=name, email=email, message=message)
    db.session.add(new_contact)
    db.session.commit()


    msg = Message(
        subject="New Contact Message",
        sender=app.config['MAIL_USERNAME'],
        recipients=["vishakhachachane@gmail.com"]
    )

    msg.body = f"""
    New message from your portfolio:

    Name: {name}
    Email: {email}
    Message: {message}
    """

    mail.send(msg)


    user_msg = Message(
        subject="Thanks for contacting me!",
        sender=app.config['MAIL_USERNAME'],
        recipients=[email]
    )

    user_msg.body = "Thank you for contacting me. I will get back to you soon!"

    mail.send(user_msg)

    return redirect("/")

if __name__ == "__main__":
    with app.app_context():
        print("Creating database...")
        db.create_all()
    app.run(debug=True)