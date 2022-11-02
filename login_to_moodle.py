import requests
import re
import config


def login_to_moodle(username, password):
    r = requests.get(config.moodle_session)
    cookie = r.cookies.get_dict()
    pattern = '<input type="hidden" name="logintoken" value="\w{32}">'
    token = re.findall(pattern, r.text)
    token = re.findall("\w{32}", token[0])
    payload = {'username': username, 'password': password, 'anchor': '', 'logintoken': token[0]}
    r1 = requests.post(config.moodle_login, cookies=cookie, data=payload)
    return r1.cookies.get_dict()
