from flask import Flask, render_template, request
from backend import chat_with_openai, text_to_speech, merge_mp3_files, text_content
import os

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create", methods=["POST", "GET"])
def create():
    if request.method == "POST":
        text = request.form["podcast-topic"]
        length = request.form["podcast-length"]
        language = request.form["podcast-language"]
        token = 0
        words = 0
        # Choose length
        if length == "short":
            token = 300
            words = 400
        elif length == "medium":
            token = 600
            words = 800
        elif length == "long":
            token = 900
            words = 1200
        generated_text = chat_with_openai(text, words, language)
        text_to_speech(generated_text, language)
        merge_mp3_files()
    return render_template("create.html")

@app.route("/podcast-list")
def podcast_list():
    podcast_list = os.listdir(os.path.join(os.getcwd(), "static"))
    podcasts = []
    for podcast in podcast_list:
        if ".mp3" in podcast:
            podcasts.append(podcast)
    return render_template("podcast-list.html", podcasts=podcasts)

@app.route("/sign-in")
def signin():
    return render_template("sign-in.html")