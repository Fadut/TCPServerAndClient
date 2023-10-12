from socket import *
import threading
import random

# To use this TCP server and client: Start the server and then the client
# Then from the client, type either random, add, or subtract followed by 2 numbers, like so: add 5 2, or random 1 10

def handle_client(connectionSocket, address):
    print(f"Connected from IP: {address[0]}")
    keep_communicating = True

    while keep_communicating:
        sentence = connectionSocket.recv(1024).decode()
        print(sentence)

        parts = sentence.strip().split()

        if len(parts) < 2:
            response = "Invalid request. Type either random, add or subtract followed by 2 numbers with space inbetween"
        else:
            operation = parts[0].lower()
            operands = [int(part) for part in parts [1:]]

            if operation == "random" and len(operands) == 2:
                response = str(random.randint(operands[0], operands[1]))
            elif operation == "add" and len(operands) == 2:
                response = str(operands[0] + operands[1])
            elif operation == "subtract" and len(operands) == 2:
                response = str(operands[0] - operands[1])
            else:
                response = "Invalid request"
        
        connectionSocket.send(response.encode())

        if sentence.strip() == "close":
            keep_communicating = False

    connectionSocket.close()

    
serverPort = 12000

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(5)
print ("Server is ready to listen")

while True:
    connectionSocket, address = serverSocket.accept()
    threading.Thread(target = handle_client, args = (connectionSocket, address)).start()