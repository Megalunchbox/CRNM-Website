from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/note.html')
def home():
    return render_template('note.html')

if __name__ == '__main__':
    app.run()