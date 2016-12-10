from json import dumps

import requests



class ChatraException(Exception):
    pass


class ChatraClient():
    # Initilizing
    def __init__(self, headers):
        self.base_api = "https://app.chatra.io/api"
        self.headers = headers

    @classmethod
    def basic_authentication(cls, username, password):
        return cls({

            "Content-Type": "application/json",
            "Authorization": requests.auth._basic_auth_str(username, password)
        })

    @classmethod
    def token_authentication(cls, api_key, api_secret):
        return cls({
            "Content-Type": "application/json",
            "Authorization": "Chatra.Simple %s:%s" % (api_key, api_secret)

        })

    # Methods
    def send_pushed_message(self, user_token, text, agent_id=None, group_id=None):
        payload = {"clientId": user_token, "text": text}
        if agent_id:
            payload["agentId"] = agent_id
        if group_id:
            payload["groupId"] = group_id

        return self.post("/pushedMessages/", data=payload)

    def get_pushed_message(self, id):
        return self.get("/pushedMessages/%s")

    def delete_pushed_message(self, id):
        return self.delete("/pushedMessages/%s")

    def update_pushed_message(self, id, text):
        payload = {"text": text}
        return self.get("/pushedMessages/%s", data=payload)

    # Request Methods
    def post(self, url, data, **kwargs):
        return self.request("post", url, data=dumps(data), **kwargs)

    def put(self, url, data, **kwargs):
        return self.request("put", url, data=dumps(data), **kwargs)

    def get(self, url, **kwargs):
        return self.request("get", url, **kwargs)

    def delete(self, url, **kwargs):
        return self.request("delete", url, **kwargs)

    # Actual Request call & Headers
    def request(self,method, url,**kwargs):
        kwargs['headers'] = self.headers
        url = "".join([self.base_api, url])
        response = requests.request(method,url, **kwargs)
        if response.status_code == 200:
            return response.json()
        else:
            raise ChatraException(response.content)

# chatra = 
