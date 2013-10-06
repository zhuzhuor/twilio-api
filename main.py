#!/usr/bin/env python

import os
from flask import Flask, request, Response, abort
from twilio import twiml
from twilio.rest import TwilioRestClient

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
assert ACCESS_TOKEN  # ACCESS_TOKEN must not be empty

app = Flask(__name__)
TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER')
twilio_client = TwilioRestClient(
    os.environ.get('TWILIO_SID'),
    os.environ.get('TWILIO_TOKEN')
)
sentry_client = None
try:
    from raven.contrib.flask import Sentry
    sentry_client = Sentry(app, dsn=os.environ.get('SENTRY_DSN'))
except:
    pass


@app.route('/<access_token>/call_me', methods=['POST'])
def call_me(access_token):
    if access_token != ACCESS_TOKEN:
        abort(403)

    try:
        phone_num = request.form['num']
    except KeyError:
        if sentry_client:
            sentry_client.captureException()
        abort(400)

    call = twilio_client.calls.create(
        to=phone_num,
        from_=TWILIO_NUMBER,
        url='http://twimlets.com/holdmusic?Bucket=com.twilio.music.ambient')

    return 'OK\n' + call.sid


@app.route('/<access_token>/handle_call', methods=['POST'])
def handle_call(access_token):
    if access_token != ACCESS_TOKEN:
        abort(403)

    resp = twiml.Response()
    resp.play(
        'http://com.twilio.music.classical.s3.amazonaws.com/BusyStrings.mp3',
        loop=1)
    return Response(resp.toxml(), mimetype='text/xml')


@app.route('/<access_token>/text_me', methods=['POST'])
def text_me(access_token):
    if access_token != ACCESS_TOKEN:
        abort(403)

    try:
        phone_num = request.form['num']
        text_body = request.form['msg']
    except KeyError:
        if sentry_client:
            sentry_client.captureException()
        abort(400)

    message = twilio_client.messages.create(
        to=phone_num,
        from_=TWILIO_NUMBER,
        body=text_body)

    return 'OK\n' + message.sid


@app.route('/<access_token>/handle_text', methods=['POST'])
def handle_text(access_token):
    if access_token != ACCESS_TOKEN:
        abort(403)

    try:
        text_content = request.form['Body']
    except KeyError:
        if sentry_client:
            sentry_client.captureException()
        text_content = ''

    resp = twiml.Response()
    resp.message('This is a response for ' + text_content)
    return Response(resp.toxml(), mimetype='text/xml')


if __name__ == '__main__':
    app.run(debug=True)
