import falcon


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
		resp.status = falcon.HTTP_200
		body = '{"result": 1,                             \
						"error_code": 0,                  \
						"error_msg": "",                  \
						"data_list": [{                   \
						"node_code": "core01",            \
						"node_type": "core",              \
						"host_list": [{                   \
						"host_code": "GW001",             \
						"host_type": "core",             \
						"host_work_status": "normal",      \
						"host_ip_address": "127.0.0.1"             \
						}]                                \
						},                                \
						{                                 \
						"node_code": "shanghai01",        \
						"node_type": "edge",              \
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
						"virtual_network_number": "1003"    \
						},                                \
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
							"virtual_network_number": "1001"    \
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
							"virtual_network_number": "1002"    \
						}]                                \
						}]                                \
						}]                                \
		}'
		resp.body = body


# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
things = ThingsResource()

# things will handle all requests to the '/things' URL path
app.add_route('/things', things)
