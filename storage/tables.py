from oslo_utils import timeutils
import sqlalchemy as sa

metadata = sa.MetaData()

now = timeutils.utcnow

Node = sa.Table('Node', metadata,
		        sa.Column('node_id', sa.INTEGER, primary_key=True),
				sa.Column('node_code', sa.String(64)),
				sa.Column('isp', sa.String(64)),
				)
Host = sa.Table('Host', metadata,
		        sa.Column('host_id', sa.INTEGER, primary_key=True),
				sa.Column('node_id', sa.ForeignKey('Node.node_id',
						                           ondelete='CASCADE'),
					      nullable=False),
				sa.Column('host_code', sa.String(64), nullable=False),
				sa.Column('host_type', sa.String(64), nullable=False),
				sa.Column('host_work_status', sa.String(64), nullable=False))

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
			  sa.Column('pe_work_mode', sa.String(64), nullable=False),
			  sa.Column('virtual_network_number', sa.INTEGER, nullable=False))

Ce = sa.Table('Ce', metadata,
		      sa.Column('id', sa.INTEGER, primary_key=True))
