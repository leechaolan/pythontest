import falcon
import time

# Falcon follows the REST architectural style, meaning (among
		# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class ThingsResource(object):
	def on_get(self, req, resp):
		"""Handles GET requests"""
		resp.status = falcon.HTTP_200  # This is the default status
		resp.body = ('\nTwo things awe me most, the starry sky '
					'above me and the moral law within me.\n'
					'\n'
					'    ~ Immanuel Kant\n\n')

	def on_post(self, req, resp):
#		time.sleep(5)
		resp.status = falcon.HTTP_200
		body = '{"result": 1,                             \
						"error_code": 0,                  \
						"error_msg": "",                  \
						"data_list": [{                   \
						"node_code": "core01",            \
						"operator_code": "ctcc",           \
						"host_list": [{                   \
						"host_code": "GW001",             \
						"host_type": "core",             \
						"host_work_status": "normal",      \
						"host_ip_address": "127.0.0.1"             \
						}]                                \
						},                                \
						{                                 \
						"node_code": "shanghai01",        \
						"operator_code": "ctcc",            \
						"host_list": [{                   \
						"host_code": "GW002",             \
						"host_type": "core",             \
						"host_work_status": "normal",     \
						"host_ip_address": "127.0.0.1",             \
						"pe_list": [{                     \
						"pe_code": "PE011",               \
						"pe_type": "monitor",             \
						"pe_work_status": "normal",        \
						"pe_vm_ip": "172.31.254.4",    \
						"pe_sdn_ip": "172.22.1.202",   \
						"pe_access_server_ip": "172.31.61.2",    \
						"pe_access_ip_pool_begin_ip": "172.22.1.148",    \
						"pe_access_ip_pool_end_ip": "172.22.1.156",    \
						"pe_access_port": "10003",    \
						"virtual_network_number": "1001" \
						},                             \
						{                                 \
							"pe_code": "PE012",           \
							"pe_type": "public",          \
							"pe_work_status": "normal",    \
							"pe_vm_ip": "172.31.254.2",    \
							"pe_sdn_ip": "172.22.1.200",   \
							"pe_access_server_ip": "172.31.41.2",    \
							"pe_access_ip_pool_begin_ip": "172.22.1.130",    \
							"pe_access_ip_pool_end_ip": "172.22.1.138",    \
							"pe_access_port": "10001",    \
							"virtual_network_number": "1002"    \
						},                                \
						{                                 \
							"pe_code": "PE013",           \
							"pe_type": "private",         \
							"pe_work_status": "normal",    \
							"pe_vm_ip": "172.31.254.3",    \
							"pe_sdn_ip": "172.22.1.201",    \
							"pe_access_server_ip": "172.31.51.2",    \
							"pe_access_ip_pool_begin_ip": "172.22.1.139",    \
							"pe_access_ip_pool_end_ip": "172.22.1.147",    \
							"pe_access_port": "10002",    \
							"virtual_network_number": "1003"    \
						}]                                \
						}]                                \
						}]                                      \
		}'




#		body = '{                    \
#					"result": 1,                                                     \
#						"error_code": 1,                                             \
#						"error_msg": "",                                             \
#						"data_list": [{                                              \
#							"customer_id": 1,                                        \
#							"customer_code": "algoblu",                              \
#							"virtual_network_list": [{                               \
#								"virtual_network_number": "1001",                    \
#								"access_instance_list": [{                           \
#									"site_code": "algoblu_beijing",                  \
#									"access_instance_id": 10,                        \
#									"pe_code": "PE011",                               \
#									"work_mode": "master",                           \
#									"tunnel_type": "openvpn",                        \
#									"openvpn_client_ip": "172.40.10.12",             \
#									"username": "u1499062623",                       \
#									"password": "p37dE9y6"                           \
#								}                                                   \
#								]                                                   \
#							},                                                       \
#							{                                                        \
#								"virtual_network_number": "1002",                    \
#								"access_instance_list": [{                           \
#									"site_code": "algoblu_beijing",                  \
#									"access_instance_id": 1,                         \
#									"pe_code": "PE012",                               \
#									"work_mode": "master",                           \
#									"tunnel_type": "openvpn",                        \
#									"openvpn_client_ip": "172.40.1.12",              \
#									"username": "u1499062623",                       \
#									"password": "p37dE9y6"                           \
#								},                                                   \
#								{                                                    \
#									"site_code": "algoblu_beijing",                  \
#									"access_instance_id": 2,                         \
#									"pe_code": "PE013",                               \
#									"work_mode": "slave",                            \
#									"tunnel_type": "openvpn",                        \
#									"openvpn_client_ip": "172.40.2.12",              \
#									"username": "u1499062623",                       \
#									"password": "p37dE9y6"                           \
#								}                                                   \
#								]                                                   \
#							},
	#						{                                                         \
#								"virtual_network_number": "1003",                    \
#								"access_instance_list": [{                           \
#									"site_code": "algoblu_beijing",                  \
#									"access_instance_id": 1,                         \
#									"pe_code": "PE012",                               \
#									"work_mode": "master",                           \
#									"tunnel_type": "openvpn",                        \
#									"openvpn_client_ip": "172.40.1.12",              \
#									"username": "u1499062623",                       \
#									"password": "p37dE9y6"                           \
#								},                                                   \
#								{                                                    \
#									"site_code": "algoblu_beijing",                  \
#									"access_instance_id": 2,                         \
#									"pe_code": "PE013",                               \
#									"work_mode": "slave",                            \
#									"tunnel_type": "openvpn",                        \
#									"openvpn_client_ip": "172.40.2.12",              \
#									"username": "u1499062623",                       \
#									"password": "p37dE9y6"                           \
#								}
#								]                                                   \
#								}		\
	#							]                                                       \
#						}]                                                           \
#				}'
		resp.body = body


# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
things = ThingsResource()

# things will handle all requests to the '/things' URL path
app.add_route('/things', things)
