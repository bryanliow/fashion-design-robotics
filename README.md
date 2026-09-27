# Fashion Design & Robotics

An autonomous robot that drafts trouser sewing patterns from body measurements, and the e-commerce site I built to sell the garments I make.

## Why I built this

I taught myself to sew bespoke garments, and I wanted to combine that hobby with my interest in robotics. Drafting a trouser pattern by hand means turning a handful of body measurements into a sequence of precise lines and points on paper. That is repetitive, rule-based work that a robot can do. So I built a small robot that takes measurements and drives out the pattern geometry.

Once I was making garments, I wanted to sell them. I taught myself HTML, CSS, Python and SQL and built the shop in this repo: product listings, Stripe payments, a customisation add-on, customer enquiries and user accounts.

## What's in this repo

| Folder | What it is |
|---|---|
| [`robot/`](robot/) | Arduino firmware for the pattern-drawing robot (early open-loop prototype) |
| [`website/`](website/) | Flask e-commerce site for the garments |

The machine-learning side of the project, which predicts pattern geometry from measurements and digitises physical pattern pieces with computer vision, is in its own repo: [Computer-Vision-and-Machine-Learning-Pipeline---Pattern-Digitisation](https://github.com/bryanliow/Computer-Vision-and-Machine-Learning-Pipeline---Pattern-Digitisation).

## Demo

> **Screenshot placeholder.** Add images to `docs/` and link them here, for example:
>
> `![Shop page](docs/shop.png)` · `![Robot drawing a pattern](docs/robot.gif)`

## Tech stack

- **Robot:** Arduino (C++), two DC motors driven through an H-bridge motor driver. Chassis modelled in SolidWorks (CAD files not included).
- **Website:** Python, Flask, SQLAlchemy, Flask-Login, Flask-WTF, Jinja2 templates, custom CSS on Bootstrap 5.
- **Database:** PostgreSQL in production (via `DATABASE_URL`), SQLite for local development.
- **Payments:** Stripe Payment Links.
- **Deployment:** Gunicorn (`Procfile`), configured through environment variables.

## How it works

### Robot

```
body measurements ─▶ drafting formulas ─▶ segment lengths ─▶ timed motor moves
(waist, seat, rise,    (e.g. seat/4 + 1)                       (length ÷ calibrated speed)
 inside leg, knee)
```

1. The measurements feed standard trouser-block drafting formulas, which give the length of each construction line (rise depth, knee and hem widths, seat and waist points).
2. Each length is converted into a drive time using a speed calibrated from test runs (`velocity`, distance per millisecond).
3. The robot drives each segment, then pauses so the point can be marked. It works through the front panel and then the back panel, and stops permanently once the pattern is complete.

This firmware is the **first, open-loop prototype**: it relies on timing rather than sensing, so accuracy depends on consistent traction. Getting reliable traction was the main hardware challenge. It was caused by a voltage step-down problem that I fixed by re-engineering it with a new motor driver, and I later moved to Mecanum wheels.

### Website

```
browser ─▶ Flask routes ─▶ Jinja templates
              │
              ├── product catalogue (PRODUCTS list in main.py) ─▶ shop, product pages
              ├── Stripe Payment Links ─▶ checkout (£100 per piece)
              ├── contact form ─▶ custom orders (+£50 hand-embroidered pockets)
              └── SQLAlchemy ─▶ users table (hashed passwords via Werkzeug)
```

- **Catalogue as data:** every product is one entry in the `PRODUCTS` list in `main.py`, rendered by a single `product.html` template. Adding a product doesn't need a new route or page.
- **Customisation add-on:** product pages offer hand-embroidered pocket artwork for +£50. The total updates live, and custom orders go to a pre-filled enquiry form so the design can be agreed first.
- **Accounts:** registration and login use Flask-Login sessions. Passwords are stored as salted PBKDF2-SHA256 hashes, never in plain text.
- **Progressive enhancement:** the shop filters, gallery thumbnails and add-on total use a small vanilla JS file. Everything still works without JavaScript.

## Running it

### Website

Requires Python 3.11+.

```bash
cd website
python -m venv .venv
.venv\Scripts\activate          # Windows; on macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env            # then set SECRET_KEY (see below)
flask --app main run
```

Generate a secret key with `python -c "import secrets; print(secrets.token_hex(32))"` and put it in `.env`. Set `DATABASE_URL` to use PostgreSQL; without it the app creates a local SQLite database.

Then open http://127.0.0.1:5000.

### Robot

1. Open `robot/denim_robot/denim_robot.ino` in the Arduino IDE.
2. Set the measurements at the top of `loop()`.
3. Select your Arduino board and port, then upload.

Motor driver inputs are on pins 3–4 (right motor) and 5–6 (left motor).

## Project status and next steps

- Replace timed moves with closed-loop control (wheel encoders) so accuracy no longer depends on traction.
- Restructure the firmware as an explicit state machine (idle → drawing segment → marking → next segment → done), with measurements sent over serial instead of hard-coded.
- Store customer enquiries in the database and send email notifications.

## Author

Bryan Liow · [GitHub](https://github.com/bryanliow)

## License

Code is released under the [MIT License](LICENSE). Product photographs and embroidery designs in `website/static/assets/img/` are not covered by it: all rights reserved.
