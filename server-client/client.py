#!/usr/bin/python3.8
import socket

def client_program():
    host = socket.gethostname()
    port = 5000
    client_socket = socket.socket()
    client_socket.connect((host,port))
    message = input("enter data ->")

    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())
        data = client_socket.recv(1024).decode()
        print("received data is: "+ data)
        message = input('->')
        client_socket.send(message.encode())

    client_socket.close()

if __name__ == '__main__':
    client_program()
