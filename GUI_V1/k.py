""" from PyAccessPoint import pyaccesspoint
import time

access_point = pyaccesspoint.AccessPoint()
access_point.start()
time.sleep(10)
access_point.stop()
 """
""" import base64
import paramiko
from paramiko import SSHClient
import time


ssh = paramiko.SSHClient()  # Iniciamos un cliente SSH
ssh.load_system_host_keys()  # Agregamos el listado de host conocidos
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Si no encuentra el host, lo agrega automáticamente
ssh.connect('10.42.0.227', username='jetsonnano', password='Jetson3744')  # Iniciamos la conexión.
ssh.
stdin, stdout, stderr = ssh.exec_command('ls')
while not stdout.channel.exit_status_ready():
    # Print data when available
    if stdout.channel.recv_ready():
        alldata = stdout.channel.recv(1024)
        prevdata = b"1"
        while prevdata:
            prevdata = stdout.channel.recv(1024)
            alldata += prevdata

        print(str(alldata, "utf8"))
#exit_code = stdout.channel.recv_exit_status()

ssh.close() """
""" 
import socket,time
from ssh2.session import Session

host = '10.42.0.227'
user = 'jetsonnano'
password = 'Jetson3744'

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect((host,22))

session = Session()
session.handshake(sock)
session.userauth_password(user,password)

chanel = session.open_session()
chanel.shell()
chanel.write('rostopic list')
time.sleep(1)
size, data = chanel.read()
print(data.decode())
while size > 0:
    print(data.decode())
    size, data = chanel.read()
chanel.close()
print('Exit status: {0}'.format(chanel.get_exit_status())) """

""" import subprocess, time
host = '10.42.0.227'
user = 'jetsonnano'
password = 'Jetson3744'
subprocess.Popen("ssh {user}@{host}".format(user=user, host=host), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
time.sleep(1)
subprocess.Popen("{password}".format(password=password), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
 """
import pexpect

child = pexpect.spawn('ssh jetsonnano@10.42.0.227')
child.expect('password .*:')
child.sendline('Jetson3744')