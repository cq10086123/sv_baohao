import requests
import os
import time
import warnings
from urllib3.exceptions import InsecureRequestWarning
import paramiko

# 忽略 InsecureRequestWarning
warnings.simplefilter("ignore", InsecureRequestWarning)

# 从环境变量读取 Telegram 的 Bot Token 和 Chat ID
def get_telegram_secrets():
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    if bot_token is None or chat_id is None:
        raise ValueError("Telegram bot token 或 chat id 未设置。请确保在 GitHub Secrets 中配置了它们。")
    
    return bot_token, chat_id

# 设置电报发送消息的函数
def send_telegram_message(message):
    # 获取 Telegram 配置
    bot_token, chat_id = get_telegram_secrets()
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": message
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            print("消息已成功发送到 Telegram")
        else:
            print(f"消息发送失败，状态码: {response.status_code}")
    except Exception as e:
        print(f"发送电报消息时发生错误: {e}")

# 登录面板
def LoginPanel():
    res = requests.get(host, verify=False)
    csrftoken = res.cookies['csrftoken']
    time.sleep(2)
    headers = {
        'Referer' : host,
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'username': username,
        'password': password,
        'csrfmiddlewaretoken': csrftoken,
    }
    res = requests.post(host, data=data, headers=headers, cookies=res.cookies, verify=False)
    if res.text.find('/logout/') != -1:
        print('面板登录成功')
        send_telegram_message("面板登录成功")  # 发送电报通知
    else:
        print('面板登录失败')
        send_telegram_message("面板登录失败")  # 发送电报通知
        os._exit(0)

# 登录ssh
def LoginSsh():
    # 创建ssh对象
    with paramiko.SSHClient() as ssh:
        # 自动添加SSH密钥
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print('开始ssh连接')
        try:
            # 连接服务器
            ssh.connect(hostname=hostname, username=username, password=password)
            print('ssh连接成功')
            print('开始执行查看ip命令')
            
            # 执行命令
            stdin, stdout, stderr = ssh.exec_command("curl ifconfig.me")
            ip = stdout.read().decode()
            print(f"当前IP: {ip}")
            send_telegram_message(f"SSH连接成功，当前IP: {ip}")  # 发送电报通知
        except Exception as e:
            print(f"SSH连接失败: {e}")
            send_telegram_message(f"SSH连接失败: {e}")  # 发送电报通知
            os._exit(0)

if __name__ == '__main__':
    print("启动脚本")
    # 从环境变量中获取服务器信息
    Serv00 = os.getenv("LOGIN_URL")
    if Serv00 is None:
        print('没有找到服务器信息,请重新设置变量Serv00')
        os._exit(0)
    info = Serv00.split(',')
    hostname = info[0]
    username = info[1]
    password = info[2]
    hostname_number = hostname.split('.')[0].replace('s', '')
    host = f'https://panel{hostname_number}.serv00.com/login/'

    LoginPanel()
    LoginSsh()
