# Variables
SHELL:=/bin/bash
OPENVPN_ADDRESS := "XX"
OPENVPN_SERVER_SUBNET := "172.16.255.0/24"
OPENVPN_ROUTE := "172.16.254.0/24"
OPENVPN_PUSH := "route 10.0.0.0 255.255.0.0"
OPENVPN_DNSSERVER := "10.0.0.2"
OPENVPN_ROOTDIR := "/etc/openvpn/"
KEY_EXPIRE := "3650"
KEY_COUNTRY := "XX"
KEY_PROVINCE := "XX"
KEY_CITY := "XX"
KEY_ORG := "XX"
KEY_EMAIL := "XX"
KEY_OU := "XX"
README := "https://ganexcloud.atlassian.net/wiki/spaces/GAN/pages/57278465/OpenVPN+-+Configurar+cliente+VPN"

# Script
.PHONY: help
help:
	@echo Use:
	@echo '  start: To start a OpenVPN server.'
	@echo '  stop: To stop a OpenVPN server.'
	@echo '  init-config: Generate a initial OpenVPN config.'
	@echo '  add-client USERNAME=NAME: Generate a client certificate.'
	@echo '  revoke-client USERNAME=NAME: Revoke keys but maitain files.'
	@echo '  remove-client USERNAME=NAME: List clients.'
	@echo '  list-clients: Generate a client certificate.'
	@echo ''

# Install Docker and docker-compose
.PHONY: install-docker
install-docker:
	@yum install -y docker
	@service docker start
	@systemctl enable docker.service
	@curl -L https://github.com/docker/compose/releases/download/v2.5.0/docker-compose-`uname -s`-`uname -m` | tee /usr/local/bin/docker-compose > /dev/null
	@chmod +x /usr/local/bin/docker-compose
	@ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
	@echo "Docker installed with sucess!"

# Generate initial configs
.PHONY: init-config
init-config:
	@mkdir -p ${OPENVPN_ROOTDIR}; \
	cd ${OPENVPN_ROOTDIR}; \
	if [[ -d "openvpn-data/" ]]; then echo "Directory openvpn-data already exists, impossible to continue."; exit 1; fi
	wget -q https://raw.githubusercontent.com/ganexcloud/docker-openvpn/master/scripts/docker-compose.yml; \
	docker-compose run --rm openvpn ovpn_genconfig -u udp://${OPENVPN_ADDRESS} -s ${OPENVPN_SERVER_SUBNET} -r ${OPENVPN_ROUTE} -p ${OPENVPN_PUSH} -n ${OPENVPN_DNSSERVER}; \
	docker-compose run --rm -e EASYRSA_BATCH=1 -e EASYRSA_REQ_CN=${OPENVPN_ADDRESS} -e EASYRSA_CA_EXPIRE="${KEY_EXPIRE}" -e EASYRSA_CERT_EXPIRE="${KEY_EXPIRE}" -e EASYRSA_REQ_COUNTRY="${KEY_COUNTRY}" -e KEY_PROVINCE="${EASYRSA_REQ_PROVINCE}" -e EASYRSA_REQ_CITY="${KEY_CITY}" -e EASYRSA_REQ_ORG="${KEY_ORG}" -e EASYRSA_REQ_EMAIL="${KEY_EMAIL}" -e EASYRSA_REQ_OU="${KEY_OU}" openvpn ovpn_initpki nopass
	@echo "OpenVPN configurations created with sucess!"

# Start OpenVPN
.PHONY: start
start:
	@cd ${OPENVPN_ROOTDIR}
	@docker-compose up -d
	@echo "OpenVPN started!"

# Stop OpenVPN
.PHONY: stop
stop: 
	@cd ${OPENVPN_ROOTDIR}
	@docker-compose down
	@echo "OpenVPN stopped!"

# Create client configs
.PHONY: add-client
add-client:
	@cd ${OPENVPN_ROOTDIR} ; \
	mkdir -p download-configs; \
	docker-compose run --rm openvpn easyrsa build-client-full ${USERNAME} nopass; \
	docker-compose run --rm openvpn ovpn_getclient ${USERNAME} > download-configs/${USERNAME}.ovpn; \
	echo ${README} > /tmp/README.md; \
	zip -jr download-configs/${USERNAME}.zip download-configs/${USERNAME}.ovpn /tmp/README.md
	@echo "Credentials created with success, the zip file with credentials are on /etc/openvpn/download-configs/${USERNAME}.zip"

# Revoke client
.PHONY: revoke-client
revoke-client:
	@cd ${OPENVPN_ROOTDIR}; \
	docker-compose run --rm openvpn ovpn_revokeclient ${USERNAME}
	@echo "Client ${USERNAME} revoked with success!"

# Remove client
.PHONY: remove-client
remove-client:
	@cd ${OPENVPN_ROOTDIR} ; \
	docker-compose run --rm openvpn ovpn_revokeclient ${USERNAME} remove
	@echo "Client ${USERNAME} removed with success!"

# List clients
.PHONY: list-clients
list-clients:
	@cd ${OPENVPN_ROOTDIR} ; \
	docker-compose run --rm ovpn_listclients