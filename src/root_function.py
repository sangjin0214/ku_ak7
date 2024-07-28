import gspread

account = gspread.service_account(filename='./lib/cloud-storage-426206-0531416cc0fd.json')
f = account.open('cloud_storage')

def root_login():
  template = ""
  try:
    with open("./src/root_login.html", "r") as t:
      template = t.read()
  except FileNotFoundError:
    template += "FileNotFoundError"
  return template

def login_success():
  template = ""
  try:
    with open("./src/root_login_success.html", "r") as t:
      template = t.read()
  except FileNotFoundError:
    template += "FileNotFoundError"
  return template

def login_fail():
  template = """
  <html>
    <body>
      <h1>ROOT account login failed</h1>
      <br>wrong password
      <a href="/root/login">돌아가기</a>
    </body>
  </html>"""
  return template

def rental_state():
  template = """
  <table>
    <tr>
      <th scope="col">charger_id</td>
      <th scope="col">student_id</td>
      <th scope="col">student_name</td>
      <th scope="col">state</td>
    </tr>"""
  
  #보조배터리 렌탈 현황 시트 범위 조정
  for i in range(1,4):
    template += "\n    <tr>"
    for j in range(1,5):
      template += "\n      <td>"+str(f.worksheet('subcharger_rental').cell(i+1,j).value)+"</td>"
    template += "\n    </tr>"
  template += "\n  </table>"
  return template

def pw_check(id):
  id_list = f.worksheet('user_data').col_values(1)
  name_of_id = f.worksheet('user_data').cell(id_list.index(id)+1,2).value
  pw_of_id = f.worksheet('user_data').cell(id_list.index(id)+1,3).value
  message = id + " " + name_of_id + "의 비밀번호는 " + pw_of_id + " 입니다!"
  return message
