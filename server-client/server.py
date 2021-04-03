
#!/usr/bin/python3.8
import socket
import threading
import time

threads = []
clients = []
send_poll = "poll"

def polling(conn):
    conn.send(send_poll.encode())
    received_data = conn.recv(1024).decode()
    print(" Received data from client is: "+str(received_data) + "  "+ str(conn))




def timer_on_clients():
    global clients
    while True:
        if len(clients) > 0:
            print("\n entries are present")
            for c in clients:
                tt = threading.Timer(5.0, polling, args=(c,))
                tt.start()
                tt.join()
        else:
            time.sleep(5)


def server_program():
    monitor = threading.Thread(target=timer_on_clients,args=())
    monitor.start()
    # monitor.join()
    print(" Reached place")
    host = socket.gethostname()
    port = 5000
    server_socket = socket.socket()
    server_socket.bind((host,port))
    server_socket.listen(3)
    while True:
        conn, address = server_socket.accept()
        print("connection from: " + str(address))
        thr = threading.Thread(target=deal_client )
        thr.start()
        thr.join()
        global threads
        threads.append(thr)
        global clients
        clients.append(conn)




def deal_client():
    print(" Nothing in client thread")



if __name__ == '__main__':
    server_program()
