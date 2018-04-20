from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Hello, World!</h1>"

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, {}!</h1>'.format(name)

if __name__ == '__main__':
    app.run(debug=True,
            host='0.0.0.0')
