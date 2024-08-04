from flask import Flask, render_template

app = Flask(__name__)

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


if __name__ == '__main__':
    app.run()



