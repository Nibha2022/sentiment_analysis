
from flask import Flask, request, render_template
#from Model import *

app = Flask(__name__)

@app.route('/')

def home():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def post_review():

    return render_template('home.html', final=rmse, text="")

@app.route('/result', methods=['POST'])
def test():
    user_input=[str(x) for x in request.form.values()]
    user_input=user_input[0]
    return render_template('index.html', final=user_input , text="")

if __name__ == "__app__":
    app.run()

