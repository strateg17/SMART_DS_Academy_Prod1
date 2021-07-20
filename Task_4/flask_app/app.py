from flask import Flask, render_template,request
from utils import f_pos, f_price
app = Flask(__name__)


@app.route('/',methods = ['GET'])
def hello_page():
    return render_template('index.html')


@app.route('/send',methods = ['GET','POST'])
def send():
    age = request.form['age']
    pos = f_pos(age)
    price = f_price(age)
    return render_template('age.html', age=age, pos=pos, price=price)

@app.route('/home')
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run()