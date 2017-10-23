import base64
import paramiko

def add_user(username, password, userip, host_name):
	client = paramiko.SSHClient()
	client.connect(host_name, username='root', password='algoblu')
	command = 'touch /etc/openvpn/ccd/' + usernane + '&&' +  'echo ifconfig-push' + user_ip + '255.255.255.0'
	stdin, stdout, stderr = client.exec_command(command)
	command = 'echo' + username + password + '>>' + '/etc/openvpn/psw-file'
	stdin, stdout, stderr = client.exec_command(command)
	client.close()

def delete_user(username, userip, host_name):
	client = paramiko.SSHClient()
	client.connect(host_name, username='root', password='algoblu')
	command = 'sed -i /' + username + '/d' + '/etc/openvpn/psw-file'
	stdin, stdout, stderr = client.exec_command(command)
	client.close()


def configure_vlan(virtual_network_number, pe_vlan_port_ip):
	client = paramiko.SSHClient()
	client.connect(host_name, username='root', password='algoblu')
	command = 'cp /etc/sysconfig/network-scripts/ifcfg-eth1' + '/etc/sysconfig/network-scripts/ifcfg-eth1.' + virtual_network_number
	stdin, stdout, stderr = client.exec_command(command)

	command = '/etc/sysconfig/network-scripts/ifcfg-eth1.' + virtual_network_number
	stdin, stdout, stderr = client.exec_command(command)
	command = 'sed -i -e "/DEVICE/ s/=.*/=eth1.' + virtual_network_number + '/' + ' ' + '/etc/sysconfig/network-scripts/ifcfg-eth1.' + virtual_network_number
	stdin, stdout, stderr = client.exec_command(command)
	#'DEVICE=eth1.1002'

	#TYPE=Ethernet
	command = 'sed -i -e "/ONBOOT/ s/=.*/=yes/' + ' ' + '/etc/sysconfig/network-scripts/ifcfg-eth1.' + virtual_network_number
	stdin, stdout, stderr = client.exec_command(command)
	#ONBOOT=yes
	#BOOTPROTO=static
	command = 'sed -i -e "/BOOTPROTO/ s/=.*/=static/' + ' ' + '/etc/sysconfig/network-scripts/ifcfg-eth1.' + virtual_network_number
	stdin, stdout, stderr = client.exec_command(command)
	#IPADDR=172.30.1.4
	command = 'sed -i -e "/IPADDR/ s/=.*/=' + pe_vlan_port_ip + '/' + ' ' + '/etc/sysconfig/network-scripts/ifcfg-eth1.' + virtual_network_number
	stdin, stdout, stderr = client.exec_command(command)
	#NETMASK=255.255.0.0
	command = 'sed -i -e "/NETMASK/ s/=.*/=' + '255.255.255.0' + '/' + ' ' + '/etc/sysconfig/network-scripts/ifcfg-eth1.' + virtual_network_number
	stdin, stdout, stderr = client.exec_command(command)

	#vconfig add eth1 1002
	command = 'vconfig add eth1 ' + virtual_network_number
	stdin, stdout, stderr = client.exec_command(command)

	# echo "vconfig add eth1 1002" >> /etc/rc.local
	command = 'vconfig add eth1 ' + virtual_network_number + '>> /etc/rc.local'
	stdin, stdout, stderr = client.exec_command(command)
	#ifup eth1.1002
	command = 'if eth1.' + virtual_network_number
	stdin, stdout, stderr = client.exec_command(command)
	client.close()
