import gspread

account = gspread.service_account(filename='/content/cloud-storage-426206-0531416cc0fd.json')
f = account.open('cloud_storage')

def pw_change_html(id):
    html = '''
    <br><br><br>
    <form action="/pw_change" method="post">
        비밀번호를 아직 변경하지 않으셨습니다. 초기비밀번호를 변경해주세요.<br>
        <input type="hidden" name="student_id" value="'''+id+'''">
        <input type="submit" value="비밀번호 변경">
    </form>
    '''
    return html

end_html = '''
  </body>
</html>
'''


def rental(subcharger_id):
  # 해당 보조배터리 반납/대여 상태 확인
  rental_state = f.worksheet('subcharger_rental').cell(int(subcharger_id)+1,4).value
  
  # 대여 페이지
  if rental_state == "반납 완료":
    template = '''
    <html>
      <body>
        <p>
            보조배터리 대여 ('''+subcharger_id+'''번 보조배터리)
        </p><br>
        <form action="/subcharger_rental/result" method="post">
            학번 : <input type="text" name="student_id"><br>
            비밀번호 : <input type="password" name="password"><br>
            <input type="hidden" name="supcharger_id" value="'''+subcharger_id+'''">
            <input type="hidden" name="rental_sys" value="대여">
            <input type="submit" value="대여">
        </form>
        <br><br>*초기비밀번호는 학번입니다.
      </body>
    </html>
'''
  
  # 반납 페이지
  else:
    student_id = f.worksheet('subcharger_rental').cell(int(subcharger_id)+1,2).value
    student_name = f.worksheet('subcharger_rental').cell(int(subcharger_id)+1,3).value
    template = '''
    <html>
      <body>
        <p>
            보조배터리 반납 ('''+subcharger_id+'''번 보조배터리)
        </p><br>
        <form action="/subcharger_rental/result" method="post">
            대여자 확인<br>
            이름 : '''+student_name+'''<br>
            학번 : '''+student_id+'''<br>
            비밀번호 : <input type="password" name="password"><br>
            <input type="hidden" name="student_id" value="'''+student_id+'''">
            <input type="hidden" name="supcharger_id" value="'''+subcharger_id+'''">
            <input type="hidden" name="rental_sys" value="반납">
            <input type="submit" value="반납">
        </form>
        <br><br>*대여하려고 하는데 이 페이지가 나왔을 경우, 엄상진(010-9082-9007)에게 연락주세요.
      </body>
    </html>
'''
  return template


def result_rent(id, pw, subcharger_id):
  id_list = f.worksheet('user_data').col_values(1)
  pw_of_id = f.worksheet('user_data').cell(id_list.index(id)+1,3).value
  if pw != pw_of_id:
    template = '''
    <html>
      <body>
        <p>학번이나 비밀번호가 잘못되었습니다.</p><br>
        <a href="/subcharger_rental/'''+subcharger_id+'''">돌아가기<a>
        <br><br>*비밀번호를 잊어버리신 분은 엄상진(010-9082-9007)에게 연락주세요.
      </body>
    </html>
    '''
  else:
    name_of_id = f.worksheet('user_data').cell(id_list.index(id)+1,2).value
    f.worksheet('subcharger_rental').update_cell(int(subcharger_id)+1,2, id)
    f.worksheet('subcharger_rental').update_cell(int(subcharger_id)+1,3, name_of_id)
    f.worksheet('subcharger_rental').update_cell(int(subcharger_id)+1,4,'대여 중')
    template = '''
    <html>
      <body>
        <p>정상적으로 대여처리되었습니다.</p><br>
        *혹시나 파손/분실시에는 학생복지국장 정서윤에게 연락해주세요.<br>
        *반납시에도 꼭 QR을 찍어주셔야 합니다.
        *(기타 추가 규정 있으면 작성)
    '''
    if id == pw:
      template += pw_change_html(id)
    template += end_html
  return template


def result_return(id, pw, subcharger_id):
  id_list = f.worksheet('user_data').col_values(1)
  pw_of_id = f.worksheet('user_data').cell(id_list.index(id)+1,3).value
  
  # 비밀번호를 틀려서 재입력으로 연결
  if pw != pw_of_id:
    template = '''
    <html>
      <body>
        <p>잘못된 비밀번호입니다.</p><br>
        <a href="/subcharger_rental/'''+subcharger_id+'''">돌아가기<a>
        <br><br>*비밀번호를 잊어버리신 분은 엄상진(010-9082-9007)에게 연락주세요.
      </body>
    </html>
    '''
  
  # 비밀번호가 맞아 반납 절차 시행
  else:
    f.worksheet('subcharger_rental').update_cell(int(subcharger_id)+1,4,'반납 완료')
    template = '''
    <html>
      <body>
        <p>정상적으로 반납처리되었습니다.</p><br>
        *실제로 반납하지 않았는데 반납처리만 하시면, 보조배터리 대여에 불이익이 있을 수 있습니다.
    '''
    
    # 초기비밀번호를 변경하지 않은 경우 비밀번호 변경 안내 추가
    if id == pw:
      template += pw_change_html(id)
    
    template += end_html
  return template
