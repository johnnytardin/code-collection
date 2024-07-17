# yum update -y --exclude=gitlab-ce
# yum clean all

sed -i "s/^Server\=172.31.0.0\/16/Server\=172.16.0.0\/12/" /etc/zabbix/zabbix_agentd.conf && service zabbix-agent restart
