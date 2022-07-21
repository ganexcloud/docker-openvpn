#!/usr/bin/python3
import emails
import sys

# Variables
smtp_host = sys.argv[1]
smtp_port = sys.argv[2]
smtp_user = sys.argv[3]
smtp_password = sys.argv[4]
smtp_tls_enabled = sys.argv[5]
openvpn_username = sys.argv[6]
email_from = sys.argv[7]
email_to = sys.argv[8]

# Create message
message = emails.html(
    html = f"Hi {openvpn_username},<br><br>Your VPN credentils was created successfully, please see the attached zip with instructions.<br><br>Regards",
    subject = "VPN Credentials",
    mail_from = f"{email_from}",
)
message.attach(content_disposition="inline",filename=f"{openvpn_username}.zip",data=open(f"download-configs/{openvpn_username}.zip", "rb"))

# Send message
r = message.send(
    to = email_to,
    smtp = { "host": smtp_host.replace('"', ''), "port": smtp_port.replace('"', ''), "user": smtp_user.replace('"', ''), "password": smtp_password.replace('"', ''), "tls": smtp_tls_enabled.replace('"', '') },
)