import gspread

account = gspread.service_account(filename='/content/cloud-storage-426206-0531416cc0fd.json')
f = account.open('cloud_storage')


def enter_pw(id):
  id_list = f.worksheet('user_data').col_values(1)
  name_of_id = f.worksheet('user_data').cell(id_list.index(id)+1,2).value
  template = '''
  <html>
    <body>
      <p>
          비밀번호 변경
      </p><br>
      <form action="/pw_change/result" method="post">
          이름 : '''+name_of_id+'''<br>
          학번 : '''+id+'''<br>
          새로운 비밀번호 : <input type="password" name="password"><br>
          비밀번호 재입력 : <input type="password" name="password_r"><br>
          <input type="hidden" name="student_id" value="'''+id+'''">
          <input type="submit" value="변경">
      </form>
    </body>
  </html>
  '''
  return template


def fail_not_same(id):
  template = '''
  <html>
    <body>
      <p>입력하신 두 비밀번호가 다릅니다. 다시 입력해주세요.</p><br>
      <form action="/pw_change" method="post">
        <input type="hidden" name="student_id" value="'''+id+'''">
        <input type="submit" value="재입력하기">
      </form>
    </body>
  </html>
  '''
  return template


def success_change(id, pw):
  id_list = f.worksheet('user_data').col_values(1)
  f.worksheet('user_data').update_cell(id_list.index(id)+1,3, pw)
  template = '''
  <html>
    <body>
      <p>정상적으로 비밀번호가 변경되었습니다.</p><br>
      새로운 비밀번호 : '''+pw+'''
    </body>
  </html>
  '''
  return template
