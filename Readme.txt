Steps for Installation:
1 Install Python IDLE 3.8
2 Open cmd(command prompt)
3 pip install opencv
4 pip install tensorflow
5 pip install numpy
6 pip install pyserial
7 pip install audioplayer

Steps for Execution:
1 Naviagte Project>Python
2 Connect cable from laptop to Arduinio. Wear the gsr connected bands.
3 Right click on Main.py ->Show more options ->Edit with IDLE ->Edit with IDLE 3.8(64 bit)
4 Check for PORT number from device manager after connecting the hardware components. Ex: COM3, COM5
5 Based on the port number make changes in Code in the following line:
	arduinoData = serial.Serial('COM5', 115200)
6 Press F5
7 If Save prompt appears, Click OK 
8 Result appears after sometime. 
