import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict


load_dotenv()
app = Flask(__name__)

# mysql connection
if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase("file:memory?mode=memory&cache=shared", uri=True)
else:
    mydb = MySQLDatabase(
        os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306,
    )


class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb


mydb.connect()
mydb.create_tables([TimelinePost])


# POST endpoint to create a new timeline post
@app.route("/api/timeline_post", methods=["POST"])
def post_time_line_post():
    if "name" not in request.form:
        return "Invalid name", 400
    name = request.form["name"]
    email = request.form["email"]
    content = request.form["content"]
    timeline_post = TimelinePost.create(name=name, email=email, content=content)

    return model_to_dict(timeline_post)


# GET endpoint to retrive all timeline posts
@app.route("/api/timeline_post", methods=["GET"])
def get_time_line_post():
    return {
        "timeline_posts": [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }


@app.route("/api/timeline_post/<int:post_id>", methods=["DELETE"])
def delete_time_line_post(post_id):
    post = TimelinePost.get(TimelinePost.id == post_id)
    post.delete_instance()
    return {"status": "post deleted"}


@app.route("/")
def index():
    url = os.getenv("URL")
    title = "Marvin Deng and Samin Sarker"
    about = "Hi! I'm Marvin, a self-driven student studying Computer Science at UCLA with a passion for building projects that create meaningful impacts. I've had the privilege of closely engaging with accomplished engineers and researchers, which has fueled my curiosity and drive to innovate. Additionally, my internships and projects have provided me with invaluable experience, allowing me to refine my skills with the best practices. I'm excited to continue exploring the ever-evolving world of technology and contributing to its advancement."

    return render_template("index.html", title=title, about=about, url=url)


@app.route("/work")
def work():
    jobs = [
        {
            "disc": "I worked at Pullscription as a Software Engineering Intern, focusing on designing and developing RESTful APIs using Node.js, Express.js, TypeScript, and SQL queries."
        },
        {
            "disc": "At Global Alliance for Medical Innovation, I utilized Python and computer vision models to analyze gait features from pose estimation video data for neurodegenerative disease diagnosis. "
        },
        {
            "disc": "At Arine, I served as a Full Stack Software Engineering Intern, collaborating on a project that transformed structured JSON templates into PDFs for patient treatment plans using Python."
        },
    ]
    return render_template(
        "template.html", pageTitle="Work Experiences", items=jobs, hobbiesPage=False
    )
    # work = "During my internship experiences, "
    # return render_template("work.html", work=work)


@app.route("/hobbies")
def hobbies():
    hobbies = [
        {
            "disc": "I love citibiking and finding new spots in the City (Roosevelt Island is the best)."
        },
        {"disc": "I also love food and will eat anything!"},
        {
            "disc": "I also work out but am not consistent! However, I did do my first muscle up this week!"
        },
        {
            "disc": "Watching movies/tv-shpws reccs: House of the Dragon, The Walking Dead"
        },
    ]

    return render_template(
        "template.html", pageTitle="Hobbies", items=hobbies, hobbiesPage=True
    )


@app.route("/education")
def education():
    schools = [
        {"disc": "Stuyesant High School 2019 -- 2023"},
        {"disc": "New York University BS in Computer Science 2023 -- 2024"},
        {"disc": "Columbia University BA in Computer Science 2024 -- 2027"},
    ]
    return render_template(
        "template.html", pageTitle="Education", items=schools, hobbiesPage=False
    )


@app.route("/location")
def location():
    return render_template("location.html")


# TIMELINE Post Page
@app.route("/timeline")
def timeline():
    posts = get_time_line_post()["timeline_posts"]
    print("endpoint hit", posts)
    return render_template("timeline.html", title="Timeline", posts=posts)
