# coding: UTF-8
import os
import requests
import logging

from flask import Flask, request, render_template, Response, session
from jinja2 import Environment, BaseLoader

import google.oauth2.id_token
import firebase_admin
from firebase_admin import credentials


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'hogehoge')
#CORS(app)

# ENV
PROJECT_ID = os.environ.get('PROJECT_ID', None)
SERVER_NAME = 'https://'+PROJECT_ID+'.appspot.com' if PROJECT_ID is not None else 'http://localhost:8080'
DEBUG = os.environ.get('DEBUG', True)

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {'projectId': PROJECT_ID})


# log
logging.getLogger().setLevel( logging.DEBUG if DEBUG else logging.INFO )


# session, POST to Firestore, get list and query
@app.route('/', methods=['GET', 'POST'])
def hello():
    user = session.get('user', {})

    from Models import Hoge
    hoge = Hoge.Hoge()

    val = request.form
    err = None
    if request.method == "POST" and val['submit'] == 'regist':
        hoge.user_id = user['user_id']
        hoge.email = val['email']
        hoge.name = val['name']
        hoge.category = [int(s) for s in val['category'].split(",")]
        err = None if hoge.save() else hoge.get_errors()

    q = hoge.query()
    if 'search_cat' in val and type(val['search_cat']) == int:
        q = q.where(u'category', u'array_contains', int(val['search_cat']))
    #rtemplate = Environment(loader=BaseLoader).from_string(str(res))
    #return rtemplate.render()
    return render_template('main.html', res=q.limit(5).stream(), user=user, err=err, SERVER_NAME=SERVER_NAME)

# get Firebase Authentication token and set session
@app.route('/tokn', methods=['POST'])
def tokn():
    id_token = request.headers['Authorization'].split(' ').pop()
    claims = google.oauth2.id_token.verify_firebase_token(id_token, google.auth.transport.requests.Request())
    res = claims
    if not claims:
        res = 'Unauthorized', 401

    session['user'] = claims
    resp = Response(res)
    return resp


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
