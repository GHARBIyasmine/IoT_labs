# EX2 MQTT username - password
The following steps to know how to add username and password to mosquitto or MQTT broker : 
1. navigate the mosquitto file and add a password file and a username. You will be prompted to add a password as well.

The password file is named pass and the username is raspi.

We cas see that the file has been created.

![Screenshot 2024-10-08 130420](https://github.com/user-attachments/assets/576d06f1-aa3a-486d-8c69-55fb4639ad36)

2. We then navigate into the configuration file and disable anonymous connection and we point out the localtion of the password file:
   
![Screenshot 2024-10-08 130920](https://github.com/user-attachments/assets/38011be5-5992-4aa1-b198-c47f6fcf12ab)

3. We Stop the mosquitto service and start it agian for the changes to take effect:

![Screenshot 2024-10-08 131232](https://github.com/user-attachments/assets/d014e71b-a8d3-42f2-b49e-b3f3d68587a2)

4. We tested the first time using a simple publish command with the right username and password and there were no erros. We also tried with a different username and we see that it produced an authorization error :
   
![Screenshot 2024-10-08 131443](https://github.com/user-attachments/assets/d26b616c-40dd-4bdb-9104-11d27f7dea5e)
