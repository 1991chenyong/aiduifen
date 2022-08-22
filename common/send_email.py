import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import time
import os


def send_email(report_file):
    """发送邮件方法"""
    try:
        # 配置邮件信息
        # 接收邮箱 yangjize@idouzi.com,huangliefeng@idouzi.com
        to = "chenyong@idouzi.com"
        # 发送邮件服务器
        smtp_server = "smtp.qq.com"
        port = "25"
        # 发送邮箱账号和密码（授权码）
        username = "775375798@qq.com"
        password = "hifffqldybkgbcgd"
        # 读取测试报告文件
        mail_body = open(report_file, "r+", encoding="utf-8").read()
        # 定义邮件内容
        msg = MIMEMultipart()
        body = MIMEText(mail_body, _subtype='html', _charset='utf-8')
        msg['Subject'] = Header('自动化接口测试报告', "utf-8")
        msg['from'] = username
        msg['to'] = to
        msg["date"] = time.strftime('%a, %d %b %Y %H:%M:%S %z')
        msg.attach(body)
        # 定义附件内容
        att = MIMEText(mail_body, "base64", "utf-8")
        att["Content-Type"] = "application/octet-stream"
        att["Content-Disposition"] = 'attachment; filename= "report.html"'
        msg.attach(att)
        # 连接邮箱服务器
        smtp = smtplib.SMTP(host=smtp_server)
        smtp.connect(host=smtp_server, port=port)
        # tls加密方式
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        # 登录邮箱
        smtp.login(username, password)
        # 发送邮件
        smtp.sendmail(username, to.split(','), msg.as_string())
        # 断开连接
        smtp.quit()
        print("%s 发送成功,查收%s邮箱" % (username, to))
    except Exception as e:
        print(e)


if __name__ == '__main__':
    send_email('../reports/index.html')