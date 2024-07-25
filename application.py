from flask import Flask, request, render_template
from src import subcharger_rental, pw_change, root_function
from dotenv import load_dotenv
import os

application = Flask(__name__)


@application.route("/")
def main_page():
    return "EOM"


@application.route("/subcharger_rental/<subcharger_id>")
def rental_page(subcharger_id):
    template = subcharger_rental.rental(subcharger_id)
    return template


@application.route("/subcharger_rental/result", methods=['POST'])
def rental_result():
    id = request.form['student_id']
    pw = request.form['password']
    subcharger_num = request.form['subcharger_id']
    rental_sys = request.form['rental_sys']
    if rental_sys == '대여':
        template = subcharger_rental.result_rent(id, pw, subcharger_id)
    else:
        template = subcharger_rental.result_return(id, pw, subcharger_id)
    return template


@application.route("/pw_change", methods=['POST'])
def pw_change():
    id = request.form['student_id']
    template = pw_change.enter_pw(id)
    return template


@application.route("/pw_change/result", methods=['POST'])
def pw_change_result():
    id = request.form['student_id']
    pw = request.form['password']
    pw_r = request.form['password_r']
    if pw != pw_r:
        template = pw_change.fail_not_same(id)
    else:
        template = pw_change.success_change(id, pw)
    return template
   

@application.route("/root/login")
def root_login():
    template = root_function.root_login()
    return template


@application.route("/root/login_result", methods=['POST'])
def root_login_result():
    load_dotenv()
    ROOT_PASSWORD = os.getenv('ROOT_PASSWORD')
    pw = request.form['password']
    if pw == ROOT_PASSWORD:
        template = root_funciton.login_success()
    else:
        template = root_function.login_fail()
    return template


@application.route("/root/rental_state", methods=['POST'])
def rental_state():
    root_login = request.form['root_login']
    if root_login == 1:
        template = root_function.rental_state()
    else:
        template = '잘못된 접근입니다.'
    return template


@application.route("/root/login/pw_check", method=['GET', 'POST'])
def pw_check():
    root_login = request.form['root_login']
    user_id = ''
    if root_login == 1:
        if request.method == 'POST':
            user_id = request.form['user_id']
            template = render_template('./src/pw_check.html', message=root_function.pw_check(user_id))
    else:
        template = '<h1>잘못된 접근입니다.</h1>'
    return template
    

if __name__ == '__main__':
    application.run()
