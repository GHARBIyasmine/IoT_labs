# EX3 MQTT - TLS configuration

In this tutorial we will configure the mosquitto MQTT broker to use TLS security.

We will be using openssl to create our own Certificate authority (CA), Server keys and certificates.

We will also test the broker by using the Paho Python client to connect to the broker using a SSL connection.

**Note: this tutorial is done on a raspberry pi vm where the broker and clients are on the same local network, specifically the same vm.**

**This lab was done by following the tutorial by Steve's Internet Guide. Link to original article: http://www.steves-internet-guide.com/mosquitto-tls/**

## Step 1: create a key pair for the CA 

Command is:   `openssl genrsa -des3 -out ca.key 2048`

## Step 2: Create a certificate for the CA using the CA key that we created in step 1

Command is:  `openssl req -new -x509 -days 1826 -key ca.key -out ca.crt`

When filling out the form, the common name is very important and it is usually the domain name of the server. You could use the IP address or Full domain name. However, the DNS server must be put into place and can resolve the FQDN of the server. 

In this case, we don't have DNS configuered so we will the internal IP address of the server which is 192.168.64.131.

## Step 3: create a server key pair that will be used by the broker (not password protected because broker can't decode it)

Command is: `openssl genrsa -out server.key 2048`

![Screenshot 2024-10-08 235041](https://github.com/user-attachments/assets/bed547c2-f6b9-47a3-98d8-a911030fb60d)

## Step 4: create a certificate request .csr. 

Command is: `openssl req -new -out server.csr -key server.key`

## Step 5:  Now we use the CA key to verify and sign the server certificate. This creates the server.crt file

Command is: `openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 360`

![Screenshot 2024-10-08 235110](https://github.com/user-attachments/assets/ad670698-a034-4fc7-b9ba-408af433a792)

## Step 6: Move the CA certificate to the ca_certificates and server.crt and server.key to the certs folder under /etc/mosquitto.

Make sure all these 3 files have read permissions on. 

![Screenshot 2024-10-08 235127](https://github.com/user-attachments/assets/2d730e22-7822-428f-95cb-1f3e152b35c5)

## Step 7: Copy the CA certificate file  ca.crt to the client.

Command is: `cp /etc/mosquitto/ca_certificates/ca.crt /`

## Step 8: Edit the mosquitto.conf file.

- Edit the listener to use port 8883
- Allows anonymous connection (for testing purposes)
- Specify the path for the 3 files of the previous step.
- Optional: Specify the minimum* TLS version to use ( starting from versions after mosquitto v1.6, you can specify the minimum TLS version to use. if ommited, it will use either v1.2 or v1.3)


![Screenshot 2024-10-08 235221](https://github.com/user-attachments/assets/ef5ab459-b7de-4661-8d71-6b36c86e942a)

## Step 9: Client configuration 

Edit the client to tell it to use TLS and give it the path of the CA certificate file that you copied over.

I’m using the python client and the client method is tls_set(). Although there are several parameters that you can pass, the only one you must give is the CA file as well as the tls version for mosquitto v1.6 and later.

`client.tls_set(‘/ca.crt’,tls_version=2)`

This the Python script used : 
 
![Screenshot 2024-10-08 180024](https://github.com/user-attachments/assets/77c685f3-a011-4ee9-b908-0937d650d035)

And this is a snipped of my version:

![Screenshot 2024-10-08 235339](https://github.com/user-attachments/assets/6e198b41-d8c3-446a-958f-fe003dc1c8d5)

**Note: To test the python script, you must run it with python 2.7 and not python 3.7 because using the server IP address in CN field of certificate is deprecated and won't work. But python versions lower than 3.7 still allow this even though it is deprecated. Also the paho-mqtt version should be < 2.0.0**

## Testing :

### Testing using publish and subscribe commands: 

![Screenshot 2024-10-08 234957](https://github.com/user-attachments/assets/d008fa63-6a61-4933-9f7e-e63a4c3e8e07)

### Testing the python code:

![Screenshot 2024-10-09 002852](https://github.com/user-attachments/assets/89b112e1-c425-420f-a37e-0834b916a8fa)


The pcapng files capture the traffic for both testing phases.
