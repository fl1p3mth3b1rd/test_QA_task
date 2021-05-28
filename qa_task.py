import requests
import re

get_session_token_url = "https://regions-test.2gis.com/v1/auth/tokens"

session_token = requests.post(get_session_token_url)
pattern = r'token=(\w+);'
session_token = re.findall(pattern, session_token.headers['Set-Cookie'])
cookies = {
    'token': session_token[0],
}