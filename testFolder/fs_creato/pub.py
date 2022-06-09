def __init__(self, clientID):
    self.client = MyMQTT(clientID, "test.mosquitto.org", 1883, self)
    self.clientID = clientID
    print(f"{self.clientID} created")
    self.start()  
    self.baseTopic = "PoliTo/C4ES/"
    self.pubTopic = self.baseTopic + self.clientID
    self.subTopic = self.baseTopic + "#"
    self.unsubTopics = []
    self.unsubTopics.append(self.pubTopic) 
    self.client.mySubscribe(self.subTopic)
    

def start (self):
    self.client.start()                

def myPublish(self, topic, message):
    print(f"{self.clientID} publishing {message} to topic: {topic}")
    self.client.myPublish(topic, message)
