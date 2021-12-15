import os
import socket
import threading


HOST = '0.0.0.0'
PORT = 8080

sem = threading.Lock()

def connectionThread(client_socket):
    headers = client_socket.recv(2048).decode().split('\n')
    route = headers[0].split()[1]

    if route == '/':
        response = 'HTTP/1.0 200 OK\n\n' + 'SUCCESS'
    else:
        response = 'HTTP/1.0 404 NOT FOUND\n\n' + 'ERROR'

    client_socket.send(response.encode())
    client_socket.close()
    sem.release()

def executeConnections():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)

    while True:
        client_socket, address = s.accept()
        print("Connected: ", address, "\n")

        sem.acquire()
        threading.Thread(target=connectionThread, args=(client_socket, )).start()
    s.close()

if __name__ == '__main__':
    executeConnections()
