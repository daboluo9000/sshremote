# -*- coding:utf-8 -*0

import paramiko
from flask import Flask
from flask import request
from flask import render_template
import time
import re

class SSHRemote:

    # Initialize Parameters
    def __init__(self, host='198.13.62.165', username='user1', password='football123!', port=22, timeout=30):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.timeout = timeout
        self.sshClient = None
        self.sftpClient = None


    def __del__(self):
        if self.sshClient:
            self.sshClient.close()
        if self.sftpClient:
            self.sftpClient.close()


    def getSSHConn(self):
        try:
            self.sshClient = paramiko.SSHClient()
            self.sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.sshClient.connect(self.host, self.port, self.username, self.password)
        except Exception as e:
            raise RuntimeError("ssh connected to [host:%s, username:%s, password:%s] failed" %
                               (self.host, self.username, self.password))


    def closeSSHConn(self):
        self.sshClient.close()


    def getFileList(self, remote_path='~'):
        if remote_path != "":
            exec_cmd = "cd "+remote_path
            std_in, std_out, std_err = self.sshClient.exec_command(exec_cmd+";ls -l")
        else:
            std_in, std_out, std_err = self.sshClient.exec_command("pwd")
        return std_out


    def execPerl(self, remote_path, perl_file_name):
        exec_cmd = "cd "+remote_path
        run_perl = "perl "+perl_file_name
        std_in, std_out, std_err = self.sshClient.exec_command(exec_cmd+";"+run_perl)
        return std_out


    def loginUser(self):
        ssh = self.sshClient.invoke_shell()
        time.sleep(0.1)
        ssh.send('su \n')
        buff = ''
        while not buff.endswith('Password: '):
             resp = ssh.recv(9999)
             buff += resp.decode()
        ssh.send('football123!')
        ssh.send('\n')
        buff = ''
        ssh.send('cd /root \n')
        ssh.send('ls -l \n')
        while not buff.endswith('# '):
            resp = ssh.recv(9999)
            # buff += resp.decode('UTF8')
            print((re.compile(r'\x1b.*?m')).sub('',resp.decode('UTF8')))
            buff += (re.compile(r'\x1b.*?m')).sub('',resp.decode('UTF8'))
        return buff

    def loginWAMUser(self):
        ssh = self.sshClient.invoke_shell()
        time.sleep(0.1)
        ssh.send('op u1wam \n')
        buff = ''
        while not buff.endswith('Password: '):
             resp = ssh.recv(9999)
             buff += resp.decode()
        ssh.send('xuxlx')
        ssh.send('\n')
        buff = ''
        ssh.send('cd /root \n')
        ssh.send('ls -l \n')
        while not buff.endswith('# '):
            resp = ssh.recv(9999)
            # buff += resp.decode('UTF8')
            print((re.compile(r'\x1b.*?m')).sub('',resp.decode('UTF8')))
            buff += (re.compile(r'\x1b.*?m')).sub('',resp.decode('UTF8'))
        return buff


    def testFileList(self):
        std_in, std_out, std_err = self.sshClient.exec_command("op u1wam;ni63sLbd;ls -l")
        return std_out


ssh_remote = SSHRemote()
ssh_remote.getSSHConn()

#std_out = execPerl(client, "/root/perl_dev", "perl_test1.pl")


app = Flask(__name__)

@app.route('/test', methods=['GET', 'POST'])
@app.route('/test/<input_dir>', methods=['GET', 'POST'])
def getFileList(input_dir=''):
    # std_out = ssh_remote.getFileList(input_dir)
    # sample_data = []
    # for line in std_out:
    #     sample_data.append(line)
    #     print(line)
    output = ssh_remote.loginUser()
    std_out = ssh_remote.getFileList()
    print(output.encode('UTF-8'))
    return render_template('index.html', output=output)


@app.route('/ssh', methods=['GET', 'POST'])
def testSSH():
    test_remote = SSHRemote(host='', username='xuxlx', password='')
    test_remote.getSSHConn()
    std_out = test_remote.testFileList()
    return 'a'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7077, debug=True)
