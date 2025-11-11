from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from dotenv import load_dotenv
from forms import SignUpForm
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("FLASK_KEY")
bootstrap = Bootstrap5(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    return render_template("signup.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)
