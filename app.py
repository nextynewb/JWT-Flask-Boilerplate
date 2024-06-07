from flask import Flask, request, session,  jsonify, render_template, redirect, url_for
import datetime
from functools import wraps
import jwt


app = Flask(__name__)
app.config['SECRET_KEY'] = 'LoremIpsum'

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

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(password)

        user_auth = authenticate(username, password)

        if user_auth:
            session['username'] = username
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

@app.route('/logout')
def logout():
    return render_template('logout.html')

@app.route('/protected')
def protected():
    return render_template('protected.html')

# API Fields

@app.route('/api/user')
def user():
    token = request.headers.get('Authorization')
    decode_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')
    print(decode_token)
    return jsonify({'username': decode_token['username']})

if __name__ == '__main__':
    app.run(debug=True)




