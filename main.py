#!/usr/bin/env python

import os
from flask import Flask, request, Response, abort
from twilio import twiml
from twilio.rest import TwilioRestClient
from raven.contrib.flask import Sentry


app = Flask(__name__)
TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER')
twilio_client = TwilioRestClient(
    os.environ.get('TWILIO_SID'),
    os.environ.get('TWILIO_TOKEN')
)
try:
    sentry_client = Sentry(app, dsn=os.environ.get('SENTRY_DSN'))
except:
    pass
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')


@app.route('/call_me/<access_token>', methods=['POST'])
def call_me(access_token):
    if access_token != ACCESS_TOKEN:
        abort(403)

    try:
        phone_num = request.form['num']
    except KeyError:
        abort(400)

    call = twilio_client.calls.create(
        to=phone_num,
        from_=TWILIO_NUMBER,
        url="http://twimlets.com/holdmusic?Bucket=com.twilio.music.ambient")

    return call.sid


@app.route('/handle_call/<access_token>', methods=['POST'])
def handle_call(access_token):
    if access_token != ACCESS_TOKEN:
        abort(403)

    resp = twiml.Response()
    resp.play('https://api.twilio.com/cowbell.mp3', loop=10)
    return Response(str(resp), mimetype='text/xml')


@app.route('/text_me/<access_token>', methods=['POST'])
def text_me(access_token):
    if access_token != ACCESS_TOKEN:
        abort(403)

    try:
        phone_num = request.form['num']
        text_body = request.form['msg']
    except KeyError:
        abort(400)

    message = twilio_client.messages.create(
        to=phone_num,
        from_=TWILIO_NUMBER,
        body=text_body)

    return message.sid


@app.route('/handle_text/<access_token>', methods=['POST'])
def handle_text(access_token):
    if access_token != ACCESS_TOKEN:
        abort(403)

    try:
        text_content = request.form['Body']
    except KeyError:
        text_content = ''

    resp = twiml.Response()
    resp.message('This is a response for ' + text_content)
    return Response(str(resp), mimetype='text/xml')


if __name__ == '__main__':
    app.run(debug=True)
