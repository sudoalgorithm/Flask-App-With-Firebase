'''
A simple application performing create operation on firebase realtime database.
'''

from flask import Flask, Response, request ,render_template, url_for
from flask_restful import Resource, Api
import pyrebase
import config

app = Flask(__name__)
api = Api(app)

firebase = pyrebase.initialize_app(config.config)
auth = firebase.auth()
users = auth.sign_in_with_email_and_password(config.auth_user['emailAddress'], config.auth_user['password'])
db = firebase.database()

class Index(Resource):
    def get(self):
        return Response(render_template('index.html', mimetype='text/html'))

@api.resource('/handledata')
class HandleData(Resource):
    def post(self):
        emailaddress = request.form['emailaddress']
        password = request.form['password']
        address = request.form['address']
        addresstwo = request.form['addresstwo']
        city = request.form['city']
        state = request.form['state']
        zipcode = request.form['zipcode']

        data = {
            "emailaddress":emailaddress,
            "password":password,
            "address":address,
            "addresstwo":addresstwo,
            "city":city,
            "state":state,
            "zipcode":zipcode,
        }
        db.child("userdata").push(data, users['idToken'])
        return Response(render_template('dashboard.html'), mimetype='text/html')

api.add_resource(Index, '/')
api.add_resource(HandleData)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
