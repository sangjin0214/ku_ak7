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
  return template

def login_fail():
  return template

def rental_state():
  template = ""
  return template

def pw_check():
  template = ""
  return template""
