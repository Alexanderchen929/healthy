import os
import sqlalchemy
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import requests
import json
import time
import random
from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("postgres://iektdbycnntmky:97fe466ce684335ca04b94aee646edae13ae762f53faf8b3ca95252cca431486@ec2-52-70-15-120.compute-1.amazonaws.com:5432/dfrnpgrjo4ksac")

@app.route("/")
@login_required
def start():
    return render_template("register.html")

def checking(meal, rec, v):
    numb = 1
    while numb > 0:
        if v:
            num = random.randint(6, 10)
        else:
            num = random.randint(4,7)
        if num> len(meal):
            num = len(meal)
        y = random.sample(range(0,len(meal)), num)
        calories1 = 0
        protein = 0
        carb = 0
        fat = 0
        for b in y:
            if meal[b][0] != "":
                calories1 = calories1 + int(float(meal[b][0].replace("g","")))
                protein = protein + int(float(meal[b][1].replace("g",'')))
                carb = carb + int(float(meal[b][2].replace("g","")))
                fat = fat + int(float(meal[b][3].replace("g","")))
        if calories1 < 0.33 * rec and calories1 > 0.15 * rec:
            if 9*fat < 0.35*0.25*rec and 9*fat > 0.15*0.25*rec:
                if 4*protein < 0.4*0.25*rec and 4*protein > 0.2*0.25*rec:
                    if 4*carb < 0.55*0.25*rec and 4*carb > 0.35*0.25*rec:
                        numb = 0
    final = []
    for c in y:
        final.append([meal[c][4],meal[c][5],meal[c][6]])
    return final, calories1, protein, carb, fat

@app.route("/index")
@login_required
def index():  # Create lists that will store relevant values
    username = db.execute("SELECT username FROM users WHERE id = :session", session=session["user_id"])[0]["username"]
    list3 = db.execute("SELECT dietary, bmr, hall FROM users WHERE username = :who", who=username)
    rec = list3[0]["bmr"]
    diet = list3[0]["dietary"]
    hall = list3[0]["hall"]
    if hall == "Annenberg Hall":
        hallid = "30"
    if hall =="Adams House":
        hallid = "09"
    if hall =="Cabot/Pforzheimer House":
        hallid ="05"
    if hall =="Currier House":
        hallid ="38"
    if hall =="Dunster/Mather House":
        hallid ="07"
    if hall =="Eliot/Kirkland House":
        hallid ="14"
    if hall =="Leverett House":
        hallid ="16"
    if hall =="Lowell/Winthrop House":
        hallid ="15"
    if hall =="Quincy House":
        hallid ="08"

    date = time.strftime("%m/%d/%Y")
    url1 = "https://esb.prod.uds.harvard.edu/api/dining/2.0/recipes"

    querystring1 = {"locationId":""}
    querystring1["locationId"]=hallid
    payload1 = ""
    headers1 = {
    'Authorization': "Basic OTU0NGQyM2ViOWNjNDM4NGFhZGRiY2QxNWMyZjgzNmI6OTVEMGZkYjYwMDVjNDBmZjhmRDM1QWI3MDM2RjNDNzk=",
    'cache-control': "no-cache",
    'Postman-Token': "7f958bad-8857-4cf3-b807-8a924061a9b1"
    }

    response1 = requests.request("GET", url1, data=payload1, headers=headers1, params=querystring1)
    text1=json.loads(response1.text)
    breakfast=[]
    breakfastv =[]
    lunch=[]
    lunchv=[]
    dinner=[]
    dinnerv=[]

    for a in text1:
        if a["Serve_Date"] == date:
            if a["Meal_Name"] == "Breakfast Menu" or "Breakfast":
                breakfast.append([a["Calories"],a["Protein"],a["Total_Carb"],a["Total_Fat"],a["Recipe_Print_As_Name"],a["Serving_Size"],a["Menu_Category_Name"]])
                if "VGT" in a["Recipe_Web_Codes"]:
                    breakfastv.append([a["Calories"],a["Protein"],a["Total_Carb"],a["Total_Fat"],a["Recipe_Print_As_Name"],a["Serving_Size"],a["Menu_Category_Name"]])
            if a["Meal_Name"] == "Lunch Menu" or "Lunch":
                lunch.append([a["Calories"],a["Protein"],a["Total_Carb"],a["Total_Fat"],a["Recipe_Print_As_Name"],a["Serving_Size"],a["Menu_Category_Name"]])
                if "VGT" in a["Recipe_Web_Codes"]:
                    lunchv.append([a["Calories"],a["Protein"],a["Total_Carb"],a["Total_Fat"],a["Recipe_Print_As_Name"],a["Serving_Size"],a["Menu_Category_Name"]])
            if a["Meal_Name"] == "Dinner Menu" or "Dinner":
                dinner.append([a["Calories"],a["Protein"],a["Total_Carb"],a["Total_Fat"],a["Recipe_Print_As_Name"],a["Serving_Size"],a["Menu_Category_Name"]])
                if "VGT" in a["Recipe_Web_Codes"]:
                    dinnerv.append([a["Calories"],a["Protein"],a["Total_Carb"],a["Total_Fat"],a["Recipe_Print_As_Name"],a["Serving_Size"],a["Menu_Category_Name"]])
    if diet == "None":
        finalb, calorieb, proteinb, carbb, fatb = checking(breakfast, rec, False)
        finall, caloriel, proteinl, carbl, fatl = checking(lunch, rec, False)
        finald, caloried, proteind, carbd, fatd = checking(dinner, rec, False)
    elif diet == "Vegetarian":
        finalb, calorieb, proteinb, carbb, fatb = checking(breakfastv, rec, True)
        finall, caloriel, proteinl, carbl, fatl = checking(lunchv, rec, True)
        finald, caloried, proteind, carbd, fatd = checking(dinnerv, rec, True)
    calorie = calorieb + caloriel + caloried
    protein = proteinb + proteinl + proteind
    carb = carbb + carbl + carbd
    fat = fatb + fatl + fatd
    if 9*fat < 0.35 *rec and 9*fat > 0.15 *rec:
        fatyes = "You're getting enough fat! Avoid fatty snacks"
    elif 9*fat > 0.35*rec:
        fatyes = "Bear in mind this is too much fat"
    else:
        fatyes = "Have some more fat through snacks"
    if 4*protein < 0.4 *rec and 4*protein > 0.2 *rec:
        proteinyes = "You're getting enough protein! Avoid protein heavy snacks"
    elif 4*protein > 0.4*rec:
        proteinyes = "Bear in mind this is too much protein"
    else:
        proteinyes = "Have some more protein through snacks"
    if 4*carb < 0.55 *rec and 4*carb > 0.35 *rec:
        carbyes = "You're getting enough carb! Avoid carb heavy snacks"
    elif 4*carb > 0.55*rec:
        carbyes = "Bear in mind this is too much carb"
    else:
        carbyes = "Have some more carbs through snacks"
    snack = rec - calorie
    return render_template("index.html",textb=finalb, textl = finall, textd = finald, fatyes = fatyes, proteinyes =proteinyes, carbyes = carbyes, calorie = calorie, protein = protein, fat = fat, carb = carb, snack = snack, hall = hall)


@app.route("/options", methods=["GET", "POST"])
@login_required
def options():  # Create lists that will store relevant values
    if request.method == "POST":
        db.execute("UPDATE users SET weight = :weight, height = :height, sex= :sex, dietary = :dietary, plan = :plan, activity =:activity, hall =:hall WHERE id = :session", session=session["user_id"], weight=request.form.get("weight"), height=request.form.get("height"), sex=request.form.get("sex"), dietary=request.form.get("dietary"), plan=request.form.get("plan"), activity=request.form.get("activity"), hall=request.form.get("hall"))
        return redirect("/index")
    else:
        username = db.execute("SELECT username FROM users WHERE id = :session", session=session["user_id"])[0]["username"]
        list1 = db.execute("SELECT weight, height, sex, dietary, plan, activity, hall FROM users WHERE username = :who", who=username)
        return render_template("options.html", weight=int(list1[0]["weight"]), height=int(list1[0]["height"]), sex=list1[0]["sex"], dietary=list1[0]["dietary"], plan=list1[0]["plan"], activity=list1[0]["activity"], hall=list1[0]["hall"])

@app.route("/progress")
@login_required
def progress():
    username = db.execute("SELECT username FROM users WHERE id = :session", session=session["user_id"])[0]["username"]
    list1 = db.execute("SELECT weight, height, sex, dietary, plan, age, activity, bmr, hall FROM users WHERE username = :who", who=username)
    weight = int(list1[0]["weight"])
    height=int(list1[0]["height"])
    sex=list1[0]["sex"]
    dietary=list1[0]["dietary"]
    plan=list1[0]["plan"]
    age=int(list1[0]["age"])
    activity=list1[0]["activity"]
    BMR = list1[0]["bmr"]
    hall = list1[0]["hall"]
    return render_template("progress.html", weight=weight, height=height, sex=sex, dietary=dietary, activity=activity, plan=plan, age=age, bmr = BMR, hall=hall)


@app.route("/check", methods=["GET"])
def check():
    users = []
    username = request.args.get('username')
    for a in db.execute("SELECT username FROM users"):
        users.append(a["username"])
    if len(username) > 0 and username not in users:
        return jsonify(True)
    else:
        return jsonify(False)



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/index")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/index")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        list1 = []
        for a in db.execute("SELECT username FROM users"):
            list1.append(a["username"])
        if request.form.get("username") in list1:
            return apology("Username not available")
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords don't match!")
        elif not request.form.get("username"):
            return apology("Must enter Username")
        else:
            db.execute("INSERT INTO users (username, hash, weight, height, sex, dietary, plan, age, activity, hall) VALUES (:username, :hash, :weight, :height, :sex, :dietary, :plan, :age, :activity, :hall)", username=request.form.get(
                "username"), hash=generate_password_hash(request.form.get("password")), weight=request.form.get("weight"), height=request.form.get("height"), sex=request.form.get("sex"), dietary=request.form.get("dietary"), plan=request.form.get("plan"), age=request.form.get('age'), activity=request.form.get("activity"), hall=request.form.get("hall"))
            rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
            session["user_id"] = rows[0]["id"]
            sex = request.form.get("sex")
            weight = float(request.form.get("weight"))
            height=float(request.form.get("height"))
            plan=request.form.get("plan")
            age=int(request.form.get("age"))
            activity=request.form.get("activity")
            if activity == "Sedentary":
                factor = 1.2
            elif activity == "Lightly active (light exercise/sports 1-3 days/week)":
                factor = 1.375
            elif activity == "Moderately active (moderate exercise/sports 3-5 days/week)":
                factor = 1.725
            else:
                factor = 1.9

            if sex == "Male":
                BMR = (66 + (weight*6.23) + 12.7 * (height/2.54) - 6.8* age)*factor
            else:
                BMR = (655+(weight*4.35)+4.7*(height/2.54)-4.7*age)*factor

            if plan == "Diet (Lose Weight)":
                BMR = BMR - 500
            elif plan == "Muscle (Gain Weight)":
                BMR = BMR + 500
            db.execute("UPDATE users SET bmr = :bmr WHERE username = :username", bmr = int(BMR), username = request.form.get("username"))
            return index()
    else:
        return render_template("register.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == "__main__":
	app.debug = True
	port = int(os.environ.get("PORT", 5000))
	app.run(host = "0.0.0.0", port = port)
