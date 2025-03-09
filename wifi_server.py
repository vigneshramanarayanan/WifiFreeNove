import socket
from Motor import *            
PWM=Motor()          

from Ultrasonic import *
ultrasonic=Ultrasonic()  

def MoveForward(client): 		
 try:
     print ("The car is moving forward")     
     PWM.setMotorModel(1000,1000,1000,1000)
     
 except Exception as e:
        print(f"MoveForward An error occurred: {e}")  
    
    

def MoveBackward(client):
    try:
        PWM.setMotorModel(-1000,-1000,-1000,-1000)     #Back
        print ("The car is going backwards")
        strData = "The car is going backwards"        
        SendBackToClient(client,strData)                            
        time.sleep(1)    
        PWM.setMotorModel(0,0,0,0)
    except Exception as e:
        print(f"An error occurred: {e}")  

	
def MoveLeft(client):
    try:
        PWM.setMotorModel(-800,-800,1000,1000)       #Turn left
        strData = "The car is turning left"                            
        SendBackToClient(client,strData)    
        time.sleep(1)
        PWM.setMotorModel(0,0,0,0)
    except Exception as e:
        print(f"An error occurred: {e}")  


def MoveRight(client):
    try:
        PWM.setMotorModel(1000,1000,-800,-800)       #Turn right     
        strData = "The car is turning right"                            
        SendBackToClient(client,strData)
        time.sleep(1)
        PWM.setMotorModel(0,0,0,0)
    except Exception as e:
        print(f"An error occurred: {e}")  


def SendBackToClient(client,strData):
    try:
        client.sendall(strData.encode('utf-8')) 
    except Exception as e:
        print(f"SendBackToClient An error occurred: {e}")  


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
                    while decoded == "MoveForwardTillObstacle":                       
                        uData=ultrasonic.get_distance()   #Get the value                        
                        strData = "Obstacle distance is "+str(uData)+"CM"                            
                        client.sendall(strData.encode('utf-8'))                         
                        if(uData < 60):        
                            PWM.setMotorModel(0,0,0,0)
                            break
                        else:
                            MoveForward(client)                        
                    if(decoded == "Stop"):
                        PWM.setMotorModel(0,0,0,0)
                        strData = "The car has stopped"                            
                        SendBackToClient(client,strData)
                    if decoded == "MoveForward":                        
                        MoveForward(client)                        
                    if decoded == "MoveBackward":                        
                        MoveBackward(client)                        
                    if decoded == "MoveLeft":
                        print("MoveLeft")
                        MoveLeft(client)                                                           
                    if decoded == "MoveRight":
                        print("MoveRight")
                        MoveRight(client)                                                                                                 
                    else:                                           
                        break                 
    except KeyboardInterrupt:
        print("Server shutting down...")        
        PWM.setMotorModel(0,0,0,0)
    except Exception as e:
        print(f"An error occurred: {e}")   
        PWM.setMotorModel(0,0,0,0)
    finally:                
        s.close()
