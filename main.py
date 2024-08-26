import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 基本信息设置
url = "https://shgy.buaa.edu.cn/ics/rest/wxdev/getlvalue"  # 查询电量的API链接
student_id = "xxxxxxxxxxxx"  # 学号
receiver_email = [
    "email1@qq.com",
    "email2@buaa.edu.cn",
]  # 收件人邮箱，多个邮箱用列表表示
sender_email = "xxxxxx"  # 发送通知的邮箱
password = "xxxxxxxxxxxxxxx"  # 邮箱的SMTP授权码
smtp_server = "smtp.xx.com"  # SMTP服务器地址
smtp_port = 587  # SMTP端口，默认587，163邮箱使用465
threshold = 100  # 电量阈值，低于此值发送警告邮件

# 获取电量信息
headers = {"Content-Type": "application/json; charset=UTF-8"}
json_data = {"stucode": student_id, "type": 1}
response = requests.post(url, headers=headers, json=json_data)
provalue = response.json()["data"]["provalue"]
balance = int(provalue[:-3])

# 发送警告邮件
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = ", ".join(receiver_email)
message["Subject"] = "宿舍电量警告"
body = f"宿舍可用电费不足，请及时充值。电量余额: {balance} kWh"
message.attach(MIMEText(body, "plain"))

smtp = smtplib.SMTP(smtp_server, smtp_port)
smtp.starttls()
smtp.login(sender_email, password)

if balance < threshold:
    smtp.sendmail(sender_email, receiver_email, message.as_string())

smtp.quit()
