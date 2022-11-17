import pandas as pd
from flask import Flask, request, jsonify, render_template
import pickle
import pyrebase
app = Flask(__name__)
model = pickle.load(open('linear_regression_model_sc.pkl', 'rb'))
config = {
  "apiKey": "AIzaSyCpueysTCJjIjW8t3-r-gV4NOPrZY2VZbA",
  "authDomain": "university-admit-predictor.firebaseapp.com",
  "databaseURL": "https://university-admit-predictor-default-rtdb.firebaseio.com",
  "projectId": "university-admit-predictor",
  "storageBucket": "university-admit-predictor.appspot.com",
  "messagingSenderId": "471033088541",
  "appId": "1:471033088541:web:2d05bfca07ad298f2cd4f4",
  "measurementId": "G-DCEHDHRG4K"
}

#initialize firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
@app.route("/register", methods = ["POST", "GET"])
def regiter():
    if request.method == "POST": 
        global name       #Only if data has been posted
        name=request.form.get('name')
        email=request.form.get('email')
        password=request.form.get('pass')
        cpassword=request.form.get('cpass')
    try:
        if(password==cpassword):
            user=auth.create_user_with_email_and_password(email,password)
            
            return render_template("login.html")
    #return render_template("login.html")
    except:
        #return "Your passwaord could not be same Please Try Again"
        return render_template("signup.html",cerror="Your passwaord could not be same or Already Exist account")


#Login
@app.route("/")
def login():
    return render_template("login.html")
@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route('/welcome')
def home():
	return render_template('index.html')
@app.route("/result", methods = ["POST", "GET"])
def result():
    """if('user' in session):
        return "Hi {}".format(session["user"])"""
    if request.method == "POST":        #Only if data has been posted
        email=request.form.get('email')
        password=request.form.get('pass')
        try:
            #Try signing in the user with the given information
            user = auth.sign_in_with_email_and_password(email, password)
            return render_template("index.html")
        except:
                return render_template("login.html",error="Your Email and Password Invalid Please Try login again or SignUp")
                
@app.route('/predict', methods=['GET','post'])
def predict():
	
	GRE_Score = int(request.form['GRE Score'])
	TOEFL_Score = int(request.form['TOEFL Score'])
	University_Rating = int(request.form['University Rating'])
	SOP = float(request.form['SOP'])
	LOR = float(request.form['LOR'])
	CGPA = float(request.form['CGPA'])
	Research = int(request.form['Research'])
	
	final_features = pd.DataFrame([[GRE_Score, TOEFL_Score, University_Rating, SOP, LOR, CGPA, Research]])
	
	predict = model.predict(final_features)
	
	output = predict[0]
	if(output>50):
		return render_template('chance.html', prediction_text='Admission chances are {}'.format(output))
	else:
		return render_template('nochance.html', prediction_text='Admission chances are {}'.format(output))
		
if __name__ == "__main__":
	app.run(debug=True)