#!/usr/bin/python3

import socket
import select
import time
from datetime import datetime


HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# SO - Socket Option
# SOL - Socket Option Level
# Modifier socket pour reutiliser l'adresse
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Le serveur informe l'OS qu'il va utiliser cette adresse suivi du port
server_socket.bind((IP, PORT))
# Ecoute de nouvelles connexions
server_socket.listen()
# Liste des sockets pour select.select()
sockets_list = [server_socket]
# Liste des clients connectés
clients = {}
msg = f"Ceci correspond au temps exacte d'ouverture du salon {time.asctime(time.localtime(time.time()))}"
print("\nBienvenue sur notre salon de messagerie")
time.sleep(2)
print("Un salon simple pour échanger des messages")
time.sleep(2)
print("Autrement dit : un groupe de communication entre différents clients \n")
time.sleep(2)
print(msg)
time.sleep(2)
print(f'Ecoute de la connexion depuis ip: {IP}, port :{PORT}....')
time.sleep(2)
print(f"Serveur en attente pour une connexion des clients\n")

# Fonction pour gérer la reception des messages
def receive_message(client_socket):
    try:
        # Reception de l'entete contenant la longueur du message 
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return false
        # Convertir l'entete en un entier 
        message_length = int(message_header.decode("utf-8").strip())
        return {"header": message_header, "data": client_socket.recv(message_length)}
        
    except:
        return False


while True:
    # Leture des sockets sur lesquels nous avons reçu les données
    # Les sockets avec des exceptions
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    
    # Itération sur les sockets notifiées
    for notified_socket in read_sockets:
        # Si socket notifiée est une socket serveur, on l'accepte
        if notified_socket == server_socket:
            # On donne la nouvelle socket au client, qui est unique
            client_socket, client_address = server_socket.accept()
            # Le client doit envoyer son nom
            user = receive_message(client_socket)
            # Si ce n'est pas le cas, il déconnecte avant d'envoyer son nom
            if user is False:
                continue
            # Ajouter la socket accepter au select liste
            sockets_list.append(client_socket)
            
            # Sauvegarder le nom et l'entete de client
            clients[client_socket] = user
            heure_de_connexion = datetime.now()            
            print(f"\nEtablissement d'une nouvelle connexion sur {client_address[0]}:{client_address[1]}, Utilisateur: {user['data'].decode('utf-8')} , heure de connexion :{heure_de_connexion.hour}:{heure_de_connexion.minute}:{heure_de_connexion.second}")
            print(f"Serveur prêt à recevoir des messages de : {user['data'].decode('utf-8')}")        
        else:
            message = receive_message(notified_socket)
            if message is False :
                print(f"Connexion terminée avec l'utilisateur {clients[notified_socket]['data'].decode('utf-8')}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue
            user = clients[notified_socket]
            print(f"Message reçu de la part de {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")

            for client_socket in clients : 
                if client_socket != notified_socket :
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
    # Cela n'est pas necessaire
    for notified_socket in exception_sockets:
        # Supprimer de la liste pour socket.socket()
        sockets_list.remove(notified_socket)
        # Supprimer de la liste des clients
        del clients[notified_socket]
