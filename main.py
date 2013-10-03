__author__ = 'bozhu'


import os
from flask import Flask, request, Response
from twilio.rest import TwilioRestClient, twiml


app = Flask(__name__)
twilio_client = TwilioRestClient(
    os.environ.get('ACCOUNT_SID'),
    os.environ.get('ACCOUNT_TOKEN')
)


@app.route('/call_me', methods=['POST'])
def call_me():
    return twilio_client, 'OK'


@app.route('/handle_call', methods=['GET'])
def handle_call():
    resp = twiml.Response()
    resp.play('https://api.twilio.com/cowbell.mp3', loop=10)
    return Response(str(resp), mimetype='text/xml')


@app.route('/text_me', methods=['POST'])
def text_me(phone_num, text_content):
    pass


@app.route('/handle_text', methods=['GET'])
def handle_text():
    resp = twiml.Response()
    resp.message('This is a response.')
    return Response(str(resp), mimetype='text/xml')
