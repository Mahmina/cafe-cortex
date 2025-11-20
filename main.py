from flask import Flask, render_template, redirect, url_for, current_app
from flask_bootstrap import Bootstrap5
from dotenv import load_dotenv
from flask_wtf import CSRFProtect
from werkzeug.utils import secure_filename
from forms import SignUpForm, CreateCafeForm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("FLASK_KEY", "dev_secret_key")
bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)


class Base(DeclarativeBase):
    pass


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)


class City(db.Model):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    city_name: Mapped[str] = mapped_column(String(100))
    cafes: Mapped[list["Cafe"]] = relationship("Cafe", back_populates="city")


class Cafe(db.Model):
    __tablename__ = "cafes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200))

    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"))
    city: Mapped["City"] = relationship("City", back_populates="cafes")

    website_url: Mapped[str] = mapped_column(String(200), unique=True)
    opening_time: Mapped[str] = mapped_column(String(100))
    closing_time: Mapped[str] = mapped_column(String(100))
    address: Mapped[str] = mapped_column(String(300))
    rating: Mapped[str] = mapped_column(String(100))
    wifi: Mapped[str] = mapped_column(String(100))
    power_outlet: Mapped[str] = mapped_column(String(100))
    image_file: Mapped[str] = mapped_column(String(255), nullable=True)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    return render_template("signup.html", form=form)


@app.route("/cafes")
def show_cafes():
    result = db.session.execute(db.select(City))
    cities = result.scalars().all()
    return render_template("cafes.html", cities=cities)


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    form = CreateCafeForm()

    result = db.session.execute(db.select(City).order_by(City.city_name))
    all_cities = result.scalars().all()
    form.city.choices = [(city.id, city.city_name) for city in all_cities]

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
            city_id=form.city.data,
            website_url=form.website_url.data,
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
