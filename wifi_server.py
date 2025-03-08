import socket
from Motor import *            
PWM=Motor()          

from Ultrasonic import *
ultrasonic=Ultrasonic()  

def MoveForward(client): 		
 print ("The car is moving forward")
 uData=ultrasonic.get_distance()   #Get the value
 strData = "Obstacle distance is "+str(uData)+"CM"                            
 client.sendall(strData.encode('utf-8')) 
 if(uData < 60):        
  PWM.setMotorModel(0,0,0,0)
 else:
  PWM.setMotorModel(1000,1000,1000,1000)
 return uData#Forward
    
    

def MoveBackward():
    PWM.setMotorModel(-1000,-1000,-1000,-1000)     #Back
    print ("The car is going backwards")
    time.sleep(1)
    PWM.setMotorModel(0,0,0,0)

	
def MoveLeft():
    PWM.setMotorModel(-800,-800,1200,1200)       #Turn left
    print ("The car is turning left")
    time.sleep(1)
    PWM.setMotorModel(0,0,0,0)


def MoveRight():
    PWM.setMotorModel(1200,1200,-800,-800)       #Turn right 
    print ("The car is turning right")
    time.sleep(1)
    PWM.setMotorModel(0,0,0,0)


def GetDecoded(client):
    data = client.recv(1024)  # Receive up to 1024 bytes
    if not data:  # If no data is received, the connection is closed
        print("Client disconnected:", clientInfo)
        decoded = ""
    decoded = data.decode('utf-8').strip()
    print("Received:", decoded)  # Decode and print the message
    return decoded

HOST = "192.168.86.38"  # IP address of your Raspberry Pi
PORT = 65432            # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    try:
        print(f"Server listening on {HOST}:{PORT}")
        PWM.setMotorModel(0,0,0,0)
        while True:
            client, clientInfo = s.accept()
            print("Server connected to:", clientInfo)
            with client:  # Use a context manager for the client socket
                while True:                    
                    decoded = GetDecoded(client)                   
                    if(decoded == "Stop"):
                        PWM.setMotorModel(0,0,0,0)                        
                    while decoded == "MoveForward":
                       if MoveForward(client) < 60:
                           break                           
                    if decoded == "MoveBackward":                        
                        MoveBackward()                        
                    if decoded == "MoveLeft":
                        print("MoveLeft")
                        MoveLeft()                                                           
                    if decoded == "MoveRight":
                        print("MoveRight")
                        MoveRight()                                                                                                 
                    else:                                           
                        break
                    
                                              
    except KeyboardInterrupt:
        print("Server shutting down...")        
        
        s.close()
        PWM.setMotorModel(0,0,0,0)
    except Exception as e:
        print(f"An error occurred: {e}")   
        
        s.close()
        PWM.setMotorModel(0,0,0,0)
    finally:        
        
        s.close()
