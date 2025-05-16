from flask import Flask, render_template, request, redirect, url_for, session, flash
from DiseaseaPrediction import DiseasesPrediction
from UserEntry import UserEntry
from AddData import AddData
from convertInputToNumerals import InputUserInfo
from datetime import datetime

app = Flask(__name__, template_folder='templates', static_folder="templates/static")
app.secret_key="4ac4285dab04a0616a1e6e35d4a3de3c"
ue = UserEntry()
dp = DiseasesPrediction()
add_data = AddData()


@app.route('/')
def index():
    if 'email' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if ue.login_user(email, password):
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        if ue.register_user(name, phone, email, password):
            return redirect(url_for('login'))
        else:
            return redirect(url_for('register'))
    return render_template('register.html')

@app.route('/Predict', methods=['GET','POST'])
def input():
    age = int(request.form['age'])
    sex = request.form['gender']
    resting_blood_pressure = int(request.form['BP'])
    thalium_stress_test_max_heart_rate = int(request.form['heartrate'])
    major_vessels_colored = int(request.form['Fluoroscopy'])
    chest_pain_type = request.form['Chest Pain Type']
    peak_exercise_st_segment = request.form['Exercise']
    thalium_test = request.form['Thal']
    input_user = InputUserInfo(sex, chest_pain_type, peak_exercise_st_segment, thalium_test)
    sex, chest_pain_type, peak_exercise_st_segment, thalium_test = input_user.convert()
    input_data = [age, sex, resting_blood_pressure, thalium_stress_test_max_heart_rate,
                      major_vessels_colored, chest_pain_type, peak_exercise_st_segment, int(thalium_test)]
    dp = DiseasesPrediction()
    my_prediction = dp.predict_diseases(input_data)
    input_data.append(my_prediction)
    add_data.add_new_data(input_data)
    email = session.get('email')
    name, phone = ue.retrieve(email)
    current_datetime = datetime.now()
    current_date = current_datetime.date()
    date = current_date.strftime("%d/%m/%Y")
    return render_template('after.html', data=my_prediction, input_data=input_data, email=email, phone=phone, name= name, date = date)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)