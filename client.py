#!/usr/bin/python3

import socket 
import select
import errno
import sys
import time

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234

msg = f"Aujourd'hui on est {time.asctime(time.localtime(time.time()))}" 
print(msg)
time.sleep(1)
print("Veuillez insérer votre nom")
time.sleep(1)
name = input("Nom d'utilisateur: ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connexion à l'adresse et au port donnés
client_socket.connect((IP, PORT))
# La connexion est sur un état non bloquant, c'est à dire .recv() ne bloquera pas
client_socket.setblocking(False)

# Nous allons encoder le nom de client en octets, puis compter le nombre d'octets pour préparer l'entete de taille fixe qui est encodé en octets
username = name.encode("utf-8")
username_header = f"{len(username):<{HEADER_LENGTH}}".encode("utf-8")
client_socket.send(username_header + username)
time.sleep(1)
print("Connexion réussie")
time.sleep(2)
print(f'Bonjour cher {name}, vous êtes connecté maintenant')
time.sleep(2)
print('Vous pouvez envoyer et recevoir des messages')
time.sleep(1)
print("NB: Les messages d'autres clients peuvent être affichés mais après avoir cliquer sur la touche Entrée. ")
time.sleep(2)
print(f'\n{name}')
while True:
    # L'envoi du message
    message = input(f' --> ' )
    if message :
        message = message.encode("utf-8")
        message_header = f"{len(message) :< {HEADER_LENGTH}}".encode("utf-8")
        client_socket.send(message_header + message)


    try:
        while True:
            # recevoir des messages
            username_header = client_socket.recv(HEADER_LENGTH)
            if not len(username_header):
                print("connexion terminée par le server")
                sys.exit()

            username_length = int(username_header.decode("utf-8").strip())
            username = client_socket.recv(username_length).decode("utf-8")

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode("utf-8").strip())
            message = client_socket.recv(message_length).decode("utf-8")

            print(f"message entrant de la part de : {username} > {message}")
 
    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Erreur de lecture: {}'.format(str(e)))
            sys.exit()
        continue

    except Exception as e:
        print('Erreur général: {}'.format(str(e)))
        sys.exit()

