from flask import Flask, render_template
app = Flask(__name__)

def get_sample_chores():
    sample_chores = [
        {
            "name": "Clean bathroom",
            "description": "scrub the tub, drink from the sink.",
            "lastCompleted": 0
        },
        {
            "name": "Clean bathroom",
            "description": "scrub the tub, drink from the sink.",
            "lastCompleted": 0
        },
        {
            "name": "Clean bathroom",
            "description": "scrub the tub, drink from the sink.",
            "lastCompleted": 0
        }
    ]
    return sample_chores


@app.route('/')
def hello(name=None):
    chores = get_sample_chores()
    return render_template('index.html', chores=chores)
    