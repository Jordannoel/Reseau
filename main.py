#!/usr/bin/python3

from grid import *
import random
import socket
import select

HOST = ''
PORT = 7777

def main():
	
	s = socket.socket(family = socket.AF_INET6, type = socket.SOCK_STREAM, proto = 0, fileno = None) #création de la socket serveur
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #pour relancer rapidement la connexion sur le même port
	s.bind((HOST, PORT)) #on associe au serveur le port 7777
	s.listen(1) #le serveur va accepter des connexions
	liste = [s] #liste contient tous les clients à qui envoyer
	
	while True:
		socketLecture,_,_ = select.select(liste, [], []) 	#socketLecture contient toutes les sockets disponibles en lecture
		for n in socketLecture: 							#on parcourt la liste des sockets 
			if n == s: 		#si n est la socket d'écoute (çàd un client vient de se connecter)
				connex, _ = s.accept() #connex contient l'adresse du client
				liste.append(connex) #que l'on ajoute à la liste des clients
			else:			
				data = n.recv(1500)
				if not data: 
					n.close()
					liste.remove(n)
					continue 	#siginifie arrête toi là et passe à l'itération suivante
				for i in liste:
					if i!=s: 	#si la socket est différente de celle qui nous a envoyé un message
						i.sendall(data) #on envoie à toutes les autres socket le message envoyé par s
main()
