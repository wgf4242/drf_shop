import requests


class YunPian(object):

    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://***"

    def send_sms(self, code, mobile):
        params = {
            "apikey": self.apikey,
            "mobile": mobile,
            "text": "填写棋牌内容的内容"
        }

        # 云片网要在设置-系统设置-IP白名单中添加自己的IP
        response = requests.post(self.single_send_url, data=params)
        import json
        re_dict = json.loads(response.text)
        print(re_dict)


if __name__ == "__main__":
    yun_pian = YunPian("apikey_oeifij4v324sa")
    yun_pian.send_sms("2017", "1123479807081")

