from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import pandas as pd
import smtplib
import os
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
Bootstrap(app)

my_email = "kelsey.c.christensen@gmail.com"
password = os.getenv("PASSWORD")

projects = pd.read_csv("api/static/portfolio-projects.csv")

@app.route("/", methods=["GET", "POST"])
def home():
    items = [row[1] for row in projects.iterrows()]
    if request.method == "POST":
        data = request.form
        send_email(data["name"], data["email"], data["phone"], data["message"])
        return render_template("index.html", msg_sent=True)
    return render_template('index.html', items=items)



def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name} \nEmail: {email} \nPhone: {phone} \nMessage: {message} "
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(my_email, my_email, email_message)



@app.route("/<skill>")
def skill_list(skill):
    items = [row[1] for row in projects.iterrows() if skill in row[1]["SKILLS"]]
    return render_template('list.html', items=items, skill=skill)


@app.route("/project/<title>")
def project_item(title):
    item = [row[1] for row in projects.iterrows() if row[1]["TITLE"] == title]
    return render_template('project_item.html', item=item)


@app.route("/resume", methods=["GET"])
def resume():
    return render_template('resume.html')


if __name__ == '__main__':
    app.run(debug=True)
