#!/usr/bin/python3

from grid import *
import random
import socket
import select
import sys
import time

HOST = ''
PORT = 7777

def main():
	
	if len(sys.argv) == 1:

		s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((HOST, PORT))
		s.listen(1)
		liste=[]		#liste contient tous les clients, même le serveur (je crois)
		while True: 
			socketList,_,_ = select.select(liste+[s], [], []) 	#contient la liste des sockets en lecture
			for n in socketList: 							#on parcourt la liste des sockets 
				if (n == s): 		#si n est la socket d'écoute (çàd un client vient de se connecter)
					connex, _ = s.accept() #on créé une nouvelle connexion entre le client et le serveur
					liste.append(connex) #que l'on ajoute à la liste des clients
					if len(liste) == 1:
						connex.send("1er joueur".encode())
					if len(liste) == 2:
						connex.send("2ème joueur".encode())
					if len(liste) > 2:
						connex.send("Spectateur".encode())
				else:			
					data = n.recv(1500)
					if(data==0): 
						n.close()
						liste.remove(n)
						break #siginifie arrête toi là et passe à l'itération suivante
					for i in liste:
						if (i!=n): 	#si la socket est différente de celle qui nous a envoyé un message
							i.send(data) #on envoie à toutes les autres socket le message envoyé par s




	elif len(sys.argv) == 2:
	
		s = socket.socket(family = socket.AF_INET6, type = socket.SOCK_STREAM, proto = 0, fileno = None) #création de la socket
		s.connect((HOST, 7777))
		string_player = s.recv(1500).decode()
		if string_player == "1er joueur":
			current_player = J1
		elif string_player == "2ème joueur":
			current_player = J2
		elif string_player == "Spectateur":
			current_player = 0
		print(current_player)
		
		while True:
		
			grids = [grid(), grid(), grid()]
			grids[current_player].display()
			while grids[0].gameOver() == -1:
				shot = -1
				if current_player == J1:
					while shot <0 or shot >=NB_CELLS:
						shot = int(input ("Quelle case allez-vous jouer ?"))
					if (grids[0].cells[shot] != EMPTY):
						grids[current_player].cells[shot] = grids[0].cells[shot]
						grids[current_player].display()
					else:
						grids[current_player].cells[shot] = current_player
						grids[0].play(current_player, shot)
						shot +=1
						s.send(bytes(shot))
						grids[current_player].display()
						print(current_player)
				else:
					shot = s.recv(1500)
					shotint = len(shot)-1
					grids[0].play(current_player, shotint)
					if current_player == 0: #pour le mode spectateur
						grids[0].display()
					else:
						grids[J1].display()
					print(current_player)

			print("Game over")
			grids[0].display()
			if grids[0].gameOver() == J1:
				print("You win !")
			else:
				print("You lose !")
				
			"""------- permet au joueur de rejouer tant qu'il veut-------"""
			answer = ''
			while True: 
				answer = input("Do you want to continue? y/n ")
				print(answer)
				if answer != 'y' or answer != 'n':
					break
			if answer == 'n':
				break
			"""----------------------------------------------------------"""
		#fin du while(True)
	#fin du client
							
main()


#else:
				#	shot = random.randint(0,8)
				#	while grids[current_player].cells[shot] != EMPTY:
				#		shot = random.randint(0,8)
