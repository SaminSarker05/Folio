import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


@app.route("/")
def index():
    url = os.getenv("URL")
    title = "Marvin Deng and Samin Sarker"
    about = "Hi! I'm Marvin, a self-driven student studying Computer Science at UCLA with a passion for building projects that create meaningful impacts. I've had the privilege of closely engaging with accomplished engineers and researchers, which has fueled my curiosity and drive to innovate. Additionally, my internships and projects have provided me with invaluable experience, allowing me to refine my skills with the best practices. I'm excited to continue exploring the ever-evolving world of technology and contributing to its advancement."

    return render_template("index.html", title=title, about=about, url=url)


@app.route("/work")
def work():
    work = "During my internship experiences, I worked at Pullscription as a Software Engineering Intern, focusing on designing and developing RESTful APIs using Node.js, Express.js, TypeScript, and SQL queries. At Arine, I served as a Full Stack Software Engineering Intern, collaborating on a project that transformed structured JSON templates into PDFs for patient treatment plans using Python. Additionally, I engaged in advanced web development at Codepath WEB103, building full-stack applications with React and PostgreSQL under the mentorship of experienced engineers. At Global Alliance for Medical Innovation, I utilized Python and computer vision models to analyze gait features from pose estimation video data for neurodegenerative disease diagnosis. "
    return render_template("work.html", work=work)


@app.route("/hobbies")
def hobbies():
    return render_template("hobbies.html")


@app.route("/education")
def education():
    return render_template("education.html")


@app.route("/location")
def location():
    return render_template("location.html")
