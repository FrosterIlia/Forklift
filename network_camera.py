import socket
import cv2
import numpy as np

class NetworkCamera:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

        print("trying to connect")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip, self.port))
        print(f"Connected to port {self.port}")
        
        self.buffer = b''
        
    def receive_frame(self, frame_position):
        if frame_position == "Center":
            self.sock.sendall(b'G 2')
        elif frame_position == "Top":
            self.sock.sendall(b'G 1')
        else:
            print(frame_position)
        
        while True:
            start = self.buffer.find(b'\xff\xd8')
            
            if start != -1:
                self.buffer = self.buffer[start:]
                
                end = self.buffer.find(b'\xff\xd9')
                
                if end != -1:
                    jpg = self.buffer[:end+2]
                    
                    self.buffer = self.buffer[end+2:]

                    frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    return frame

            data = self.sock.recv(65535)
            if not data:
                print("Connection closed by server")
                return None

            self.buffer += data