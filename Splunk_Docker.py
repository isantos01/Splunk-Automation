#!/usr/bin/python3

# importing os module that way commands can be used
import os

# To get the ip address of the host
import socket
ip_address = socket.gethostbyname(socket.gethostname())

# importing subprocess module so commands can be processed one by one
import subprocess

# This library is to be able to paste the content of a variable and paste it to a file
from click import echo

print ("Installing Libraries, please wait...")
os.system("apt-get update")
subprocess.Popen(["apt-get", "install", "apt-transport-https", "ca-certificates", "curl", "gnupg", "lsb-release", "-y"])
os.system ("curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg")
os.system ('echo \ "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu/ $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null')
os.system ('apt-get update && apt-get install docker-ce docker-ce-cli containerd.io -y')
os.system ('systemctl enable docker && systemctl start docker')
os.system ('curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose')
os.system ('chmod +x /usr/local/bin/docker-compose')
os.system ('touch docker-compose.yml')

docker_yml = """
version: "2"

networks:
  splunknet:
    driver: bridge

volumes:
  splunk-data: {}

services:
  splunk:
    networks:
      splunknet:
        aliases:
          - splunk
    image: splunk/splunk
    restart: always
    container_name: splunk
    environment:
      - SPLUNK_START_ARGS=--accept-license
      - SPLUNK_PASSWORD=adminsplunk
      - DEBUG=true
    ports:
      - 8083:8000
      - 8084:8089
    volumes:
      - splunk-data:/opt/splunk
"""



with open('docker-compose.yml', 'w') as file:
    documents = echo(docker_yml, file)

subprocess.Popen(["docker-compose", "up"])

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.connect(("8.8.8.8", 80))

ip_address = s.getsockname()[0]

s.close()


subprocess.run(["docker", "ps"])
print ("____________________________________________")
print ("Your username is: admin")
print ("Your password is: adminsplunk")
print ("Webconsole URL: "+ip_address+":8083")
print ("WAIT UNTIL IT SAYS HEALTHY TO ACCESS THE WEBCONSOLE TO DO THAT RUN DOCKER PS COMMAND")