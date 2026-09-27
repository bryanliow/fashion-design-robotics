import os

from dotenv import load_dotenv
from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from werkzeug.security import generate_password_hash, check_password_hash

from forms import RegisterForm, LoginForm

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
Bootstrap5(app)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# DATABASE: PostgreSQL in production (DATABASE_URL), SQLite for local development
class Base(DeclarativeBase):
    pass


database_url = os.environ.get('DATABASE_URL', 'sqlite:///listings.db')
if database_url.startswith('postgres://'):  # some hosts still issue the legacy scheme
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
db = SQLAlchemy(model_class=Base)
db.init_app(app)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))


# PRODUCT CATALOGUE
# Every piece is £100. Images live in static/assets/img/. A product without a
# Stripe link shows an "Order this piece" button that opens the contact form.
PRICE = 100

PRODUCTS = [
    {
        "slug": "black-flared-denim",
        "name": "Black Flared Denim",
        "category": "Denim",
        "summary": "15oz French denim · Made to measure",
        "intro": "A clean black flare in heavyweight French denim, individually made around your measurements.",
        "details": [("Fabric", "15oz cotton denim from Nîmes, France"), ("Construction", "Hand sewn with a button fly"),
                    ("Fit", "Flared leg, five-pocket style"), ("Composition", "100% cotton")],
        "images": ["black front.jpg", "black back.jpg", "black front close.jpg", "black back close.jpg"],
        "stripe": "https://buy.stripe.com/00wdR1blRevsaoaaRG7AI03",
    },
    {
        "slug": "indigo-flared-denim",
        "name": "Indigo Flare Denim",
        "category": "Denim",
        "summary": "12oz French denim · Made to measure",
        "intro": "A deep-indigo flare with a softer 12oz weight, designed to be made uniquely for you.",
        "details": [("Fabric", "12oz cotton denim from Nîmes, France"), ("Construction", "Hand sewn with a button fly"),
                    ("Fit", "Flared leg, five-pocket style"), ("Composition", "100% cotton")],
        "images": ["blue front.jpg", "blue back.jpg", "blue front close.jpg", "blue back close.jpg"],
        "stripe": "https://buy.stripe.com/bJe4grcpVbjgaoa4ti7AI02",
    },
    {
        "slug": "cream-denim",
        "name": "Cream Denim",
        "category": "Denim",
        "summary": "Undyed twill · Contrast pocket stitching",
        "intro": "Five-pocket jeans in natural cream denim, finished with tonal topstitching and curved pocket details.",
        "details": [("Fabric", "Cream cotton denim twill"), ("Construction", "Hand sewn, riveted back pockets"),
                    ("Fit", "High rise, wide straight leg")],
        "images": ["products/ecru-denim-jeans.jpg"],
        "stripe": "https://buy.stripe.com/cNi28jblR5YWcwi6Bq7AI09",
    },
    {
        "slug": "brown-waxed-cotton-trousers",
        "name": "Brown Waxed Cotton Trousers",
        "category": "Trousers",
        "summary": "Waxed cotton · Wrap-around fabric belt",
        "intro": "A relaxed wide-leg trouser in chocolate-brown waxed cotton, with a long self-fabric belt that wraps and ties at the waist.",
        "details": [("Fabric", "Chocolate-brown waxed cotton"), ("Details", "Self-fabric wrap belt, five pockets"),
                    ("Fit", "Relaxed, wide straight leg")],
        "images": ["products/brown-belted-trousers.jpg"],
        "stripe": "https://buy.stripe.com/5kQ6ozblRafcdAme3S7AI06",
    },
    {
        "slug": "ninja-trousers",
        "name": "Ninja Trousers",
        "category": "Trousers",
        "summary": "Balloon leg · Long tie belt",
        "intro": "A full balloon leg gathered in at the hem, fastened with a long self-fabric belt that wraps around the waist.",
        "details": [("Colour", "Black"), ("Details", "Self-fabric tie belt, curved seams"),
                    ("Fit", "High rise, full balloon leg")],
        "images": ["products/black-balloon-trousers-back.jpg"],
        "stripe": "https://buy.stripe.com/6oU28j89F9b82VI2la7AI05",
    },
    {
        "slug": "balloon-stiff-cotton-trousers",
        "name": "Balloon Stiff Cotton Trousers",
        "category": "Trousers",
        "summary": "Structured cotton · Knee seam panels",
        "intro": "A sculptural balloon shape in a stiff black cotton that holds its volume, shaped by seamed panels at the knee.",
        "details": [("Colour", "Black"), ("Details", "Front pleats, panelled knee seams"),
                    ("Fit", "High rise, wide balloon leg")],
        "images": ["products/black-balloon-trousers-front.jpg", "products/black-panelled-wide-trousers.jpg"],
        "stripe": "https://buy.stripe.com/3cIcMXblR5YW1RE8Jy7AI04",
    },
    {
        "slug": "double-pleated-cotton-trousers",
        "name": "Double Pleated Cotton Trousers",
        "category": "Trousers",
        "summary": "Double front pleats · Full leg",
        "intro": "Tailored wide-leg trousers with deep double pleats that fall into a long, fluid line.",
        "details": [("Colour", "Black"), ("Details", "Double front pleats, side pockets"),
                    ("Fit", "High rise, full wide leg")],
        "images": ["products/black-pleated-wide-trousers.jpg"],
        "stripe": "https://buy.stripe.com/fZu8wH9dJdro1RE1h67AI08",
    },
    {
        "slug": "textured-black-cotton-shirt",
        "name": "Textured Black Cotton Shirt",
        "category": "Shirts",
        "summary": "Crinkled cotton · Laced sleeves",
        "intro": "A relaxed black shirt in textured, crinkled cotton, with eyelet lacing running up the sleeves.",
        "details": [("Colour", "Black"), ("Details", "Eyelet lace-up sleeves, button front"),
                    ("Fit", "Relaxed, dropped shoulder")],
        "images": ["products/black-lace-up-shirt.jpg"],
        "stripe": "https://buy.stripe.com/aFa8wH61x0ECeEq3pe7AI07",
    },
]
PRODUCTS_BY_SLUG = {product["slug"]: product for product in PRODUCTS}
CATEGORIES = list(dict.fromkeys(product["category"] for product in PRODUCTS))


# Optional add-on: hand-embroidered pocket art. Drop example photos into
# static/assets/img/custom/ and they appear in the customisation gallery.
CUSTOM_PRICE = 50
CUSTOM_DIR = os.path.join(app.static_folder, "assets", "img", "custom")


def custom_images():
    if not os.path.isdir(CUSTOM_DIR):
        return []
    return sorted(f for f in os.listdir(CUSTOM_DIR) if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")))


@app.context_processor
def inject_prices():
    return {"price": PRICE, "custom_price": CUSTOM_PRICE}


with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template("index.html", featured=PRODUCTS[2:6], custom_images=custom_images()[:4])

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        # Check if user email is already present in the database.
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()
        if user:
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        # This line will authenticate the user with Flask-Login
        login_user(new_user)
        return redirect(url_for("home"))
    return render_template("register.html", form=form, current_user=current_user)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        # Note, email in db is unique so will only have one result.
        user = result.scalar()
        # Email doesn't exist
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('home'))

    return render_template("login.html", form=form, current_user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/about")
def about():
    return render_template("about.html", current_user=current_user)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        flash("Thanks for getting in touch — I'll reply as soon as I can.")
        return redirect(url_for("contact"))
    product = PRODUCTS_BY_SLUG.get(request.args.get("product", ""))
    custom = request.args.get("custom") == "1"
    return render_template("contact.html", product=product, custom=custom, current_user=current_user)


@app.route("/shop")
def shop():
    return render_template("shop.html", products=PRODUCTS, categories=CATEGORIES, current_user=current_user)


@app.route("/customise")
def customise():
    return render_template("customise.html", images=custom_images(), products=PRODUCTS, current_user=current_user)


@app.route("/shop/<slug>")
def product(slug):
    item = PRODUCTS_BY_SLUG.get(slug) or abort(404)
    others = [p for p in PRODUCTS if p["slug"] != slug][:3]
    return render_template("product.html", product=item, others=others, current_user=current_user)


# Old listing URLs, kept so existing links still work.
@app.route("/listing1")
def listing1():
    return redirect(url_for("product", slug="black-flared-denim"), 301)

@app.route("/listing2")
def listing2():
    return redirect(url_for("product", slug="indigo-flared-denim"), 301)


if __name__ == "__main__":
    app.run(debug=False)
