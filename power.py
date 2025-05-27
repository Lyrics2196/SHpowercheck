import requests
import smtplib
import logging
import sys
import json
import argparse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# 从外部json读取配置信息
def load_config(config_path="config.json"):
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    return config


# 命令行参数解析
parser = argparse.ArgumentParser(description="宿舍电量监控")
parser.add_argument("-c", "--config", type=str, default="config.json", help="配置文件路径")
parser.add_argument("-o", "--output", type=str, default="power.log", help="日志文件路径")
args = parser.parse_args()

config = load_config(args.config)

url = config["url"]  # 查询电量的API链接
student_id = config["student_id"]  # 学号
receiver_email = config["receiver_email"]  # 收件人邮箱，列表
sender_email = config["sender_email"]  # 发送通知的邮箱
password = config["password"]  # 邮箱的SMTP授权码
smtp_server = config["smtp_server"]  # SMTP服务器地址
smtp_port = config["smtp_port"]  # SMTP端口
threshold = config["threshold"]  # 电量阈值


# 获取电量信息
def get_power():
    headers = {"Content-Type": "application/json; charset=UTF-8"}
    json_data = {"stucode": student_id, "type": 1}
    response = requests.post(url, headers=headers, json=json_data)
    provalue = response.json()["data"]["provalue"]
    balance = int(provalue[:-3])
    return balance


# 发送警告邮件
def send_email(balance):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = ", ".join(receiver_email)
    message["Subject"] = "宿舍电量警告"
    body = f"宿舍可用电费不足，请及时充值。电量余额: {balance} kWh"
    message.attach(MIMEText(body, "plain"))

    smtp = smtplib.SMTP(smtp_server, smtp_port)
    smtp.starttls()
    smtp.login(sender_email, password)
    smtp.sendmail(sender_email, receiver_email, message.as_string())
    smtp.quit()


def main():
    logging.basicConfig(
        filename=args.output,
        level=logging.INFO,
        filemode="a",
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    balance = get_power()
    if balance < threshold:
        send_email(balance)
        logging.info(f"电量余额{balance}kWh，低于阈值{threshold}kWh，发送警告邮件")
    else:
        logging.info(f"电量余额{balance}kWh，高于阈值{threshold}kWh，无需发送警告邮件")


if __name__ == "__main__":
    main()
