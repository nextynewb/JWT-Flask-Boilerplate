from flask import Flask, request, session,  jsonify, render_template, redirect, url_for
import datetime
from functools import wraps
import jwt
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'HelloWorld'


dummy_user_password = {
    'admin': 'admin123',
    'rahmanrom': 'password123',
    'john': 'johnpassword',
    'jane_doe': 'janepass',
    'alice': 'alicepass',
    'bob': 'bobpass',
    'charlie': 'charliepass',
    'david': 'davidpass',
    'eve': 'evepass',
    'frank': 'frankpass'
}

def authenticate(username, password):
    print('Username:', username)
    print('Password:' , password)
    if dummy_user_password.get(username) == password:
        payload = {
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            'password': password
        }
        print('Login success')
        return True

    else:
        print('Login failed')
        return False
    

def generate_jwt(username):
    payload = {
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token


# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if 'username' not in session:
#             return jsonify({'error': 'Login required!'}), 403
#         return f(*args, **kwargs)
#     return decorated_function



@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(password)

        user_auth = authenticate(username, password)

        if user_auth:
            token = generate_jwt(username)
            print(token)
            return {
                'status': 'success',
                'message': 'Login success',
                'token': token
            }
        
        else:
            return{
                'status': 'failed',
                'message': 'Login failed'
            }

    elif request.method == 'GET':
        error = request.args.get('error')
        print(error)
        return render_template('login.html', error = error)
    
@app.route('/index')
def index():
    auth_header = request.headers.get('Authorization')
    print(auth_header)

    return render_template('index.html')

@app.route('/decode')
def decode():
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNzE3NjY3NTQ2fQ.gPB0NO4SPUejK2zOICikI-YTolRUIQaDeMMQSWunP80'
    decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    print(decoded)
    return decoded

if __name__ == '__main__':
    app.run(debug=True)




