import requests
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def get_balance():
    url = "https://shgy.buaa.edu.cn/ics/rest/wxdev/getlvalue"

    headers = {
        "Content-Type": "application/json; charset=UTF-8",
    }

    json_data = {
        "stucode": "xxxxxxxx",
        "type": 1,
    }

    response = requests.post(
        url=url,
        headers=headers,
        json=json_data,
    )

    data = json.loads(response.text)
    provalue = data["data"]["provalue"]
    balance = int(provalue[:-3])

    return balance


def send_email(balance, receiver_email):
    sender_email = "xxxxxxxxxxxxx"
    password = "xxxxxxxxxxxxxxxxxxxx"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "宿舍可用电量不足提醒"

    message.attach(
        MIMEText(
            "宿舍可用电量不足，请及时充值\n 目前可用电量：" + str(balance) + "度",
            "plain",
        )
    )
    with smtplib.SMTP("smtp.qq.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())


if __name__ == "__main__":
    receiver_email1 = "xxxxxxxxxxx@buaa.edu.cn"
    receiver_email2 = "xxxxxxxxxxxxxx@qq.com"
    balance = get_balance()
    if balance < 5:
        send_email(balance, receiver_email1)
        send_email(balance, receiver_email2)
