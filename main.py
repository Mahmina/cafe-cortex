from flask import Flask, render_template, redirect, url_for, current_app
from flask_bootstrap import Bootstrap5
from dotenv import load_dotenv
from flask_wtf import CSRFProtect
from werkzeug.utils import secure_filename
from forms import SignUpForm, CreateCafeForm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("FLASK_KEY", "dev_secret_key")
bootstrap = Bootstrap5(app)


class Base(DeclarativeBase):
    pass


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)
csrf = CSRFProtect(app)


class Cafe(db.Model):
    __tablename__ = "cafes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    location_url: Mapped[str] = mapped_column(String(200), unique=True)
    opening_time: Mapped[str] = mapped_column(String(100))
    closing_time: Mapped[str] = mapped_column(String(100))
    address: Mapped[str] = mapped_column(String(300))
    rating: Mapped[str] = mapped_column(String(100))
    wifi: Mapped[str] = mapped_column(String(100))
    power_outlet: Mapped[str] = mapped_column(String(100))
    image_file: Mapped[str] = mapped_column(String(255), nullable=True)


with app.app_context():
    db.create_all()

# CREATE RECORD
# with app.app_context():
#     new_cafe = Cafe(
#         id=1,
#         name="STAY - BLEIBDOCHNOCH",
#         location_url="https://www.google.com/maps/place//data=!4m2!3m1!1s0x47a6f9844873159f:0x8840f9cb796fa589?sa=X&ved=1t:8290&ictx=111",
#         opening_time="10:00 AM",
#         closing_time="06:00 PM",
#         address= "Dresdner Str. 79, 04317 Leipzig",
#         rating="4.4",
#         wifi="Yes",
#         power_outlet="Yes",
#         image_file="assets/uploads/bleib-doch-noch.jpg"
#     )
#     db.session.add(new_cafe)
#     db.session.commit()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    return render_template("signup.html", form=form)


@app.route("/cafes")
def show_cafes():
    result = db.session.execute(db.select(Cafe))
    cafes = result.scalars().all()
    return render_template("cafes.html", all_cafes=cafes)


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    form = CreateCafeForm()
    if form.validate_on_submit():
        image_filename = None
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            # gives the absolute path to the root folder of our Flask project
            upload_folder = os.path.join(current_app.root_path, 'static/assets/uploads')
            os.makedirs(upload_folder, exist_ok=True)  # ensure folder exists
            upload_path = os.path.join(upload_folder, filename)
            form.image.data.save(upload_path)
            image_filename = f"assets/uploads/{filename}"
        new_cafe = Cafe(
            name=form.name.data.upper(),
            location_url=form.location_url.data,
            opening_time=form.opening_time.data.strftime("%I:%M %p"),
            closing_time=form.closing_time.data.strftime("%I:%M %p"),
            rating=form.rating.data,
            address=form.address.data,
            wifi=form.wifi.data,
            power_outlet=form.power_outlet.data,
            image_file=image_filename
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("show_cafes"))
    return render_template("add-cafe.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)
