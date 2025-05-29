from flask import Flask, request, render_template, render_template_string
from src import page_rental_state
from datetime import datetime
import os
import json
from oauth2client.service_account import ServiceAccountCredentials
import gspread

SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']

key_json_string = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_JSON')
credentials_info = json.loads(key_json_string)
credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_info, SCOPES)
client = gspread.authorize(credentials)
spreadsheet = client.open_by_key('1871ZjkgBWblqwsxkTxWSDqGy73M18Z27Qx9LPM_AIF0')
ws_SR = spreadsheet.worksheet('supcharger_rental')
ws_UD = spreadsheet.worksheet('user_data')

@application.route("/")
def page_root_login():
  if request.method == 'POST':
    pw_input = request.form['password']
  return render_template('page_root_login.html', message='WRONG PASSWORD')


@application.route("/root_func")
def page_root_function():
  pw_input = request.form['password']
  if pw_input = ws_SR.cell(2,3).value:
    template = render_template('page_root_function.html')
  else:
    template = ''
  return template


@application.route("/root_func/rental_state")
def page_root_rental_state():
  return render_template('')
