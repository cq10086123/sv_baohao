import requests
import os
import time
import warnings
from urllib3.exceptions import InsecureRequestWarning
# 忽略 InsecureRequestWarning
warnings.simplefilter("ignore", InsecureRequestWarning)
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
    res = requests.post(host, data=data,headers=headers,cookies=res.cookies,verify=False)
    if res.text.find('/logout/') != -1:
        print('面板登录成功')
    else:
        print('面板登录失败')
        os._exit(0)
# 登录ssh
def LoginSsh():
    import paramiko
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
            print(stdout.read().decode())
        except Exception as e:
            print(f"SSH连接失败: {e}")
            os._exit(0)
if __name__ == '__main__':
    print("启动脚本")
    # 从环境变量中获取服务器信息
    Serv00 = os.environ.get('LOGIN_URL')
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
