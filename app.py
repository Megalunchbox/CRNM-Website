from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email

import os, stripe


app = Flask(__name__)
app.config.from_object('config.Config')
csrf = CSRFProtect(app)

stripe.api_key = app.config['STRIPE_SECRET_KEY']
app.config['SESSION_COOKIE_SECURE'] = True

@app.after_request
def set_secure_headers(response):
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' https://cdnjs.cloudflare.com https://threejs.org https://js.stripe.com 'unsafe-inline'; "
        "style-src 'self' https://cdnjs.cloudflare.com 'unsafe-inline'; "
        "img-src 'self' data:; "
        "connect-src 'self' https://api.stripe.com"
        )
    return response

@app.route('/')
def index():
    return render_template('note.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/dynamic')
def dynamic():
    content = {
        "title": "Dynamic Page - Computer Repair Near Me LLC",
        "heading": "Welcome to the Dynamic Page",
        "paragraphs": [
            "This is the first paragraph of dynamic content.",
            "Here's another piece of information dynamically loaded.",
            "Feel free to modify the content as you see fit."
        ]
    }
    return render_template('dynamic_content.html', **content)

@app.route('/checkout')
def checkout():
    return render_template('checkout.html', key=app.config['STRIPE_PUBLIC_KEY'])

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    data = request.get_json()
    email = data.get('email')
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Your Product Name',
                },
                'unit_amount': 2000,  # amount in cents
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://localhost:5000/success',
        cancel_url='http://localhost:5000/cancel',
        customer_email=email,
    )
    return jsonify(id=session.id)

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/cancel')
def cancel():
    return render_template('cancel.html')

if __name__ == '__main__':
    app.run()



