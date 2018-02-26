def get_auth_url():
    weibo_auth_url = "https://api.weibo.com/oauth2/authorize"
    redirect_uri = ""
    auth_url = weibo_auth_url + "?client_id={client_id}&redirect_uri={redirect_uri}".format(client_id=123,
                                                                                            redirect_uri=redirect_uri)
    print(auth_url)


# http://open.weibo.com/wiki/Oauth2/access_token
def get_access_token(code="11111"):
    access_token_url = "https://api.weibo.com/oauth2/access_token"
    import requests
    re_dict = requests.post(access_token_url, data={
        "client_id": 2222333,
        "client_secret": "2c60bxxxxx",
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://47.x.x.x/complete/weibo"
    })

    # '{access_token="xxx", uid="yyy"}


def get_user_info(token, uid):
    user_url = "https://api.weibo.com/2/users/show.json?access_token={token}&uid={uid}".format(token=token, uid=uid)
    print(user_url)


if __name__ == "__main__":
    get_auth_url()
    get_access_token(code="11111")
    get_user_info(access_token="xxxxx", uid="yyyyy")
