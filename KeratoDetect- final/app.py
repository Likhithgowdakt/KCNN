import os
from flask import Flask
from flask import render_template, redirect
from flask import request
import torch
import torch.nn as nn
from PIL import Image
import torch.nn.functional as F
import torchvision.transforms as transforms

import mysql.connector

app = Flask(__name__)

conn = mysql.connector.connect(
    host="localhost", user="root", password="", database="ktc_project")
cursor = conn.cursor(buffered=True)

UPLOAD_FOLDER = "C:/Users/CHETAN/Desktop/ktc_model/Front/static/uploads"


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        # convolutional layer (sees 180x240x3 image tensor)
        self.conv1 = nn.Conv2d(3, 16, 3, padding=1)
        self.bn1 = nn.BatchNorm2d(16)
        # convolutional layer (sees 90x120x16 tensor)
        self.conv2 = nn.Conv2d(16, 32, 3, padding=1)
        self.bn2 = nn.BatchNorm2d(32)
        # convolutional layer (sees 45x60x32 tensor)
        self.conv3 = nn.Conv2d(32, 64, 3, padding=1)
        self.bn3 = nn.BatchNorm2d(64)

        # max pooling layer
        self.pool = nn.MaxPool2d(2, 2)
        # linear layer (64*45*60 -> 10)
        self.fc1 = nn.Linear(64*45*60, 10)
        # linear layer (10 -> 2)
        self.fc2 = nn.Linear(10, 2)

    def forward(self, x):
        # Define forward behavior
        x = self.pool(F.relu(self.bn1(self.conv1(x))))
        #x = self.pool(F.relu(self.bn2(self.conv2(x))))
        x = self.pool(F.relu(self.bn2(self.conv2(x))))
        x = F.relu(self.bn3(self.conv3(x)))
        # flatten image input
        x = x.view(-1, 64 * 45 * 60)
        # linear layer, with relu activation function
        x = F.relu(self.fc1(x))
        # linear output layer
        x = self.fc2(x)
        return x


# load saved model
model = Net()
model.load_state_dict(torch.load("model.pt"))
model.eval()

# image -> transform


def transform_image(image):
    transform_test = transforms.Compose([
        transforms.Resize((180, 240)),
        transforms.ToTensor(),
        transforms.Normalize((0.8629, 0.8765, 0.63575),
                             (0.2921, 0.2525, 0.4618))
    ])
    return transform_test(image)

# prediction


def get_prediction(img, model):
    # Convert to a batch of 1
    xb = img.unsqueeze(0)
    # Get predictions from model
    yb = model(xb)
    # Pick index with highest probability
    _, preds = torch.max(yb, dim=1)
    # Retrieve the class label
    return preds.item()


@app.route('/', methods=["GET", "POST"])
def home():
    return render_template("index.html")


@app.route('/login', methods=['POST', 'GET'])
def login():
    uname = request.form['email']
    pwd = request.form['password']
    admin_check = request.form.get('admin')
    ophthalmologist_check = request.form.get('ophthalmologist')
    if (admin_check and ophthalmologist_check) or (not admin_check and not ophthalmologist_check):
        request.close()
        return render_template('valid.html', info='Either one of the checkboxes should be checked')
    else:
        # cur=mysql.connection.cursor()
        if admin_check:
            cursor.execute(
                """SELECT * FROM `admin` WHERE `a_email` LIKE '{}'""".format(uname))
            result_count = cursor.fetchall()
            if len(result_count) == 0:
                return render_template('valid.html', info='Invalid Username')
            else:
                rc = cursor.execute(
                    """SELECT `a_pass` FROM `admin` WHERE `a_email` LIKE '{}'""".format(uname))
                pwd_from_db = cursor.fetchone()
                pwd_from_db = ''.join(pwd_from_db)
                if pwd != pwd_from_db:
                    # cur.close()
                    return render_template('valid.html', info='Incorrect Password')
                else:
                    cursor.execute(
                        """SELECT `a_name` FROM `admin` WHERE `a_email` LIKE '{}' AND `a_pass` LIKE '{}'"""
                        .format(uname, pwd))
                    name = cursor.fetchone()
                    name = ''.join(name)
                    # cursor.close()
                    return render_template('adminPage.html', info=name)
        else:
            cursor.execute(
                """SELECT * FROM `users` WHERE `email` LIKE '{}'""".format(uname))
            result_count = cursor.fetchall()
            if len(result_count) == 0:
                return render_template('valid.html', info='Invalid Username')
            else:
                rc = cursor.execute(
                    """SELECT `password` FROM `users` WHERE `email` LIKE '{}'""".format(uname))
                pwd_from_db = cursor.fetchone()
                pwd_from_db = ''.join(pwd_from_db)
                if pwd != pwd_from_db:
                    # cur.close()
                    return render_template('valid.html', info='Incorrect Password')
                else:
                    cursor.execute(
                        """SELECT `name` FROM `users` WHERE `email` LIKE '{}'"""
                        .format(uname))
                    name = cursor.fetchone()
                    name = ''.join(name)
                    # cursor.close()
                    return render_template('input.html', info=name)


@app.route('/add', methods=['GET', 'POST'])
def add():
    return render_template('add.html')


@app.route('/input', methods=['GET', 'POST'])
def input():
    return render_template('input.html')


@app.route('/remove', methods=['GET', 'POST'])
def remove():
    return render_template('remove.html')


@app.route('/signup', methods=["GET", "POST"])
def signup():
    return render_template("signup.html")


@app.route('/login_validation', methods=['POST'])
def login_validation():
    username = request.form.get('username')
    password = request.form.get('pass')

    cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}'"""
                   .format(username, password))
    users = cursor.fetchall()
    if len(users) > 0:
        return render_template('input.html')
    else:
        return render_template('valid.html', info='Incorrect Credentials')


@app.route('/add_user', methods=['POST'])
def add_user():
    uname = request.form.get('name')
    uemail = request.form.get('email')
    upass = request.form.get('pass')
    phone = request.form.get('phone')
    dob = request.form.get('dob')

    cursor.execute(
        """SELECT * FROM `users` WHERE `email` LIKE '{}'""".format(uemail))
    result_count = cursor.fetchall()
    if len(result_count) == 1:
        return render_template('valid.html', info='Email ID already exist!')

    cursor.execute("""INSERT INTO `users` (`user_id`,`name`,`email`,`password`,`phone`,`dob`) VALUES
                 (NULL,'{}','{}','{}','{}','{}')""".format(uname, uemail, upass, phone, dob))

    conn.commit()

    return render_template('login.html')


@app.route('/removeDetails', methods=['GET', 'POST'])
def removeDetails():
    d_username = request.form['username']
    cursor.execute(
        """SELECT * FROM `users` WHERE `email` LIKE '{}'""".format(d_username))
    result_count = cursor.fetchall()
    if len(result_count) == 1:
        cursor.execute(
            'delete from users where email=(%s)', (d_username,))
        conn.commit()
        request.close()
        return render_template('re.html')
    else:
        return render_template('valid.html', info='Email does not exist!')


@app.route('/imagePredict', methods=['GET', 'POST'])
def imagePredict():
    if request.method == 'POST':
        p_name = request.form['name']
        p_email = request.form['email']
        p_phone = request.form['phone']
        p_age = request.form['age']
        p_gender = request.form['gender']
        image_file = request.files['image']
        if image_file:
            image_location = os.path.join(UPLOAD_FOLDER, image_file.filename)
            image_file.save(image_location)
            img_open = Image.open(image_location)
            img = transform_image(img_open)
            pred = get_prediction(img, model)
            if pred == 0:
                output = "Keratoconus Eye"
                cursor.execute("""INSERT INTO `patient` (`p_id`,`p_name`,`p_email`,`p_phone`,`p_age`,`p_gender`,`p_image`,`p_result`) VALUES
                 (NULL,'{}','{}','{}','{}','{}','{}','{}')""".format(p_name, p_email, p_phone, p_age, p_gender, image_file.filename, output))
                conn.commit()
                return render_template('prediction.html', name=p_name, phone=p_phone, age=p_age, email=p_email, prediction="Keratoconus Eye")

            if pred == 1:
                output = "Normal Eye"
                cursor.execute("""INSERT INTO `patient` (`p_id`,`p_name`,`p_email`,`p_phone`,`p_age`,`p_gender`,`p_image`,`p_result`) VALUES
                 (NULL,'{}','{}','{}','{}','{}','{}','{}')""".format(p_name, p_email, p_phone, p_age, p_gender, image_file.filename, output))
                conn.commit()
            return render_template('prediction.html', name=p_name, phone=p_phone, age=p_age, email=p_email, prediction="Normal Eye")

    return render_template('prediction.html', prediction=999)


if __name__ == "__main__":
    app.run(debug=True)
