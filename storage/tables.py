from oslo_utils import timeutils
import sqlalchemy as sa

metadata = sa.MetaData()

now = timeutils.utcnow

Node = sa.Table('Node', metadata,
		        sa.Column('node_id', sa.INTEGER, primary_key=True),
				sa.Column('node_code', sa.String(64)),
				sa.Column('isp', sa.String(64))
				)
Host = sa.Table('Host', metadata,
		        sa.Column('host_id', sa.INTEGER, primary_key=True),
				sa.Column('node_id', sa.ForeignKey('Node.node_id',
						                           ondelete='CASCADE'),
					      nullable=False),
				sa.Column('host_code', sa.String(64), nullable=False),
				sa.Column('host_type', sa.String(64), nullable=False),
				sa.Column('host_work_status', sa.String(64), nullable=False),
				sa.Column('host_ip_address', sa.String(64), nullable=False)
				)

Pe = sa.Table('Pe', metadata,
		      sa.Column('id', sa.INTEGER, primary_key=True),
			  sa.Column('host_id', sa.ForeignKey('Host.host_id',
					                             ondelete='CASCADE')),
			  sa.Column('pe_code', sa.String(64), nullable=False),
			  sa.Column('pe_type', sa.String(64), nullable=False),
			  sa.Column('pe_work_status', sa.String(64), nullable=False),
			  sa.Column('pe_default_port_ip', sa.String(64), nullable=False),
			  sa.Column('pe_vlan_port_ip', sa.String(64), nullable=False),
			  sa.Column('pe_vpn_server_ip', sa.String(64), nullable=False),
			  sa.Column('pe_vpn_ip_range_start', sa.String(64), nullable=False),
			  sa.Column('pe_vpn_ip_range_end', sa.String(64), nullable=False),
			  sa.Column('pe_vpn_access_port', sa.INTEGER, nullable=False),
			  sa.Column('virtual_network_number', sa.INTEGER, nullable=False)
			  )

Ce = sa.Table('Ce', metadata,
		      sa.Column('id', sa.INTEGER, primary_key=True),
			  sa.Column('virtual_network_number', sa.INTEGER, nullable=False),
			  sa.Column('customer_id', sa.INTEGER, nullable=False),
			  sa.Column('customer_code', sa.String(64), nullable=False),
			  sa.Column('access_instance_id', sa.INTEGER, nullable=False),
			  sa.Column('tunnel_type', sa.String(64), nullable=False),
			  sa.Column('vpn_cli_ip', sa.String(64), nullable=False),
			  sa.Column('username', sa.String(64), nullable=False),
			  sa.Column('password', sa.String(64), nullable=False),
			  sa.Column('work_mode', sa.String(64), nullable=False),
			  sa.Column('pe_id', sa.INTEGER, nullable=False),
			  )

Pe_total = sa.Table('Pe_total', metadata,
			        sa.Column('id', sa.INTEGER, primary_key=True),
					sa.Column('pe_row_md5sum', sa.String(32), nullable=False),
					sa.Column('pe_table_md5sum', sa.String(32), nullable=False),
					sa.Column('host_code', sa.String(64), nullable=False),
					sa.Column('host_type', sa.String(64), nullable=False),
					sa.Column('host_work_status', sa.String(64), nullable=False),
					sa.Column('host_ip_address', sa.String(64), nullable=False),
					sa.Column('node_code', sa.String(64), nullable=False),
					sa.Column('pe_code', sa.String(64), nullable=False),
					sa.Column('pe_type', sa.String(64), nullable=False),
					sa.Column('pe_work_status', sa.String(64), nullable=False),
					sa.Column('pe_default_port_ip', sa.String(64), nullable=False),
					sa.Column('pe_vlan_port_ip', sa.String(64), nullable=False),
					sa.Column('pe_vpn_server_ip', sa.String(64), nullable=False),
					sa.Column('pe_vpn_ip_range_start', sa.String(64), nullable=False),
					sa.Column('pe_vpn_ip_range_end', sa.String(64), nullable=False),
					sa.Column('pe_vpn_access_port', sa.INTEGER, nullable=False),
					sa.Column('virtual_network_number', sa.INTEGER, nullable=False)
					)

Ce_total = sa.Table('Ce_total', metadata,
		            sa.Column('id', sa.INTEGER, primary_key=True),
					sa.Column('ce_row_md5sum', sa.String(32), nullable=False),
					sa.Column('ce_table_md5sum', sa.String(32), nullable=False),
					sa.Column('virtual_network_number', sa.INTEGER, nullable=False),
					sa.Column('customer_id', sa.INTEGER, nullable=False),
					sa.Column('customer_code', sa.String(64), nullable=False),
					sa.Column('access_instance_id', sa.INTEGER, nullable=False),
					sa.Column('tunnel_type', sa.String(64), nullable=False),
					sa.Column('vpn_cli_ip', sa.String(64), nullable=False),
					sa.Column('username', sa.String(64), nullable=False),
					sa.Column('password', sa.String(64), nullable=False),
					sa.Column('work_mode', sa.String(64), nullable=False),
					sa.Column('pe_code', sa.String(64), nullable=False)
					)
