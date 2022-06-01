# Cybersecurity Honeypot: fighting ransomware with sentinel files

This is the project of 'Cybersecurity for Embedded Systems' course @PoliTO, A.Y. 2021-2022. <br />
We present a cluster of Raspberry Pi devices. Each raspberry can communicate to the others in the network, according to the principles of a fully connected mesh. <br />
The following picture is a schematic of our proposed solution: 
![Schematic](/images/malwareHoneypot.drawio.png "schematic")


## How to play

1) Launch the command ```python --version```. If the version is below 3.X.X, then perform step #2, otherwise skip to step #3;
2) Install Python3 using apt as described [here](https://phoenixnap.com/kb/how-to-install-python-3-ubuntu);
3) Install the PAHO MQTT library with the command ```pip3 install paho-mqtt```;
4) Launch the command ```git clone --branch master https://github.com/s282133/sentinelFiles_vs_ransomware.git```.