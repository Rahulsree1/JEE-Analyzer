from flask import Flask, render_template, request
from tensorflow import keras
from keras.models import load_model
import joblib
from sklearn.preprocessing import PolynomialFeatures
import sqlite3
app = Flask(__name__,template_folder="templates",static_folder="static")

def ml(data):
    model=load_model("./rank.h5")
    ans=(model.predict([data])[0]*119)+29
    model2 = joblib.load("./regression.pkl")
    poly = PolynomialFeatures(degree=5)
    soln = model2.predict(poly.fit_transform([ans+5,ans-5]))
    return ans,soln


@app.route('/')
def index():
    return render_template('index.html')
@app.route('/form/')
def form():
    return render_template('form.html')

@app.route('/predict',methods=['POST'])
def predict():
    con = sqlite3.connect("JeeAnlyzer.db")
    cur = con.cursor()
    f = cur.execute("SELECT * FROM Data")
    l = len(f.fetchall())
    data = [float(request.form.get(nam)) for nam in [f"q{nu}" for nu in range(1,14)]]
    data2 = [(data[0]-1)/9,(data[1]-1)/4,(data[2]-1)/4,(data[3]-1)/9,data[4]/5,(data[5])/5,(data[6]-52)/48,(data[7])/5,(data[8])/5,(data[9])/5,(data[10])/5,(data[11])/5,(data[12])/5]
    marks,rank = ml(data2)
    cur.execute(f"INSERT INTO Data VALUES({l+1},{round(marks[0])},{round(rank[0][0])},{round(rank[1][0])},{data[0]},{data[1]},{data[2]},{data[3]},{data[4]},{data[5]},{data[6]},{data[7]},{data[8]},{data[9]},{data[10]},{data[11]},{data[12]})")
    con.commit()
    con.close()
    return render_template('predict.html',marks = round(marks[0]), r1 = round(rank[0][0]), r2 = round(rank[1][0]))

@app.route('/faqs/')
def faqs():
    return render_template('faq.html')
@app.route('/aboutUs')
def aboutUs():
    return render_template('Au.html')
@app.route('/analysis')
def ana():
    return render_template('analysis.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/data',methods=['POST'])
def data():
    user = request.form.get("user")
    passwd = request.form.get("passwd")
    credentials = {"admin":"JeeAnalyzer@IC252","Rahul1122":"Rahul@9676"}
    if user in credentials.keys() and credentials[user] == passwd:
        con = sqlite3.connect("JeeAnlyzer.db")
        cur = con.cursor()
        f = cur.execute("SELECT * FROM Data")
        da = f.fetchall()
        print(da)
        con.close()
        return render_template("details.html",data = da)
    else:
        return "<h1>Enter Correct Credentials</h1>"
        






@app.route('/a1')
def a1():
    return render_template("a1.html")
@app.route('/a2')
def a2():
    return render_template("a2.html")
@app.route('/a3')
def a3():
    return render_template("a3.html")
@app.route('/a4')
def a4():
    return render_template("a4.html")
@app.route('/a5')
def a5():
    return render_template("a5.html")
@app.route('/a6')
def a6():
    return render_template("a6.html")
@app.route('/a7')
def a7():
    return render_template("a7.html")
@app.route('/a8')
def a8():
    return render_template("a8.html")
@app.route('/a9')
def a9():
    return render_template("a9.html")





if __name__=="__main__":
    app.run(debug=True)