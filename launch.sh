docker run \
	--env LDAP_ORGANISATION="Test Company" \
	--env LDAP_DOMAIN="test.com" \
	--env LDAP_ADMIN_PASSWORD="JonSn0w" \
	--detach osixia/openldap:1.5.0