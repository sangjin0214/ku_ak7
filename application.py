from flask import Flask, request, send_file
from src import subcharger_rental, pw_change


application = Flask(__name__)


@application.route("/")
def main_page():
    template = '''
    <html>
      <body>
        <p>hello world</p>
      </body>
    </html>
    '''
    return template


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


@applicatoin.route("/pw_change", methods=['POST'])
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


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=int(sys.argv[1]))
