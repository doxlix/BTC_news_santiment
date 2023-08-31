import requests
from bs4 import BeautifulSoup
import re
import json


class Face_Unlim():
    tokens_dict = {}

    def __init__(self, cookie_token, user_agent=''):
        self.headers = {"cookie": f"token={cookie_token};",
                        "user-agent": f"{user_agent}"}

    def get_token(self, token_name):
        if token_name in self.tokens_dict:
            return self.tokens_dict[token_name]
        url = "https://huggingface.co/settings/tokens"
        resp = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(resp.text, "html.parser")
        try:
            base_elem = soup.find("div", attrs={'btc_data-props': re.compile(token_name)})
            if base_elem:
                res_token = json.loads(base_elem.attrs['btc_data-props'])['token']
                self.tokens_dict[token_name] = res_token
                return res_token
        except Exception:
            return None

    def update_token(self, token_name):
        api_token = self.get_token(token_name)
        url = f"https://huggingface.co/settings/tokens/{api_token}/rotate"
        resp = requests.post(url, headers=self.headers)
        self.tokens_dict.pop(token_name)
        if resp.status_code == 200:
            return self.get_token(token_name)
