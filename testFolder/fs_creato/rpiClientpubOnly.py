from MyMQTT import *
from time import sleep
import paho.mqtt.client as PahoMQTT
import sys

#from pubsub import *
#from NEWNEWpubsub import *

class pubOnly():

    def __init__(self, clientID):
        self.client = MyMQTT(clientID, "test.mosquitto.org", 1883, self)
        self.clientID = clientID
        print(f"{self.clientID} created")
        self.client.start()
        self.client.mySubscribe("PoliTo/C4ES/#")

        topic = "PoliTo/C4ES/" + clientname + "/command"

        message1 = {"src" : clientname, "dest" : "pi0", "command" : "ls -la"}

        sleep(5)

        # self.client.myPublish(topic, message1)
        # print(f"{self.clientID} publishing {message1} to topic: {topic}")

        # sleep(5)

        # message2 = {"src" : clientname, "dest" : "pi0", "command" : "pwd"}

        # self.client.myPublish(topic, message2)

        # sleep(5)

        #message3 = {"src" : clientname, "dest" : "pi0", "command" : "cd A ; ls -la ; rm ./zsamples_B6N.txt"}
        # questo funziona ma dovrei sapere il nome del file

        #self.client.myPublish(topic, message3)

        #sleep(5)

        #message4 = {"src" : clientname, "dest" : "pi0", "command" : "cd A ; ls | tail +3"}
        # funziona per listare tutti i file e directories in dir
        #self.client.myPublish(topic, message4)

        message45 = {"src" : clientname, "dest" : "pi0", "command" : "cd A ; ls | for file in * do if [[ -f $file ]] then echo $file fi done"}
        self.client.myPublish(topic, message45)


        # message5 = {"src" : clientname, "dest" : "pi0", "command" : "cd A ; echo qualcosa > (ls -la | head -n 1)"}

        # self.client.myPublish(topic, message5)

        sleep(5)

    def notify(self, message, topic):
        if topic == f"PoliTo/C4ES/{self.clientID}/command":
            print("loopback")
            return



if __name__ == "__main__":

    clientname = str(sys.argv[1])

    publisher = pubOnly(clientname)
