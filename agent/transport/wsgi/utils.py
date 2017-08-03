import base64
import paramiko

def add_user(self, username, password, userip, host_name):
	client = paramiko.SSHClient()
	client.connect(host_name, username='root', password='algoblu')
	command = 'touch /etc/openvpn/ccd/' + usernane + '&&' +  'echo ifconfig-push' + user_ip + '255.255.255.0'
	stdin, stdout, stderr = client.exec_command(command)
	command = 'echo' + username + password + '>>' + '/etc/openvpn/psw-file'
	stdin, stdout, stderr = client.exec_command(command)
	client.close()

def delete_user(self, username, userip, host_name):
	client = paramiko.SSHClient()
	client.connect(host_name, username='root', password='algoblu')
	command = 'sed -i /' + username + '/d' + '/etc/openvpn/psw-file'
	stdin, stdout, stderr = client.exec_command(command)
	client.close()
