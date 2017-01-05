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
	
	score = [0]
	if len(sys.argv) == 1:

		s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((HOST, PORT))
		s.listen(1)
		liste=[]		#liste contient tous les clients
		while True: 
			socketList,_,_ = select.select(liste+[s], [], []) 	#contient la liste des sockets en lecture
			for n in socketList: 							#on parcourt la liste des sockets 
				if (n == s): 		#si n est la socket d'écoute (çàd un client vient de se connecter)
					connex, _ = s.accept() #on créé une nouvelle connexion entre le client et le serveur
					liste.append(connex) #que l'on ajoute à la liste des clients
					if len(liste) == 1:
						connex.send("1".encode())
					if len(liste) == 2:
						connex.send("2".encode())
					if len(liste) > 2:
						connex.send("Spectator".encode())
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
	
		s = socket.socket(family = socket.AF_INET6, type = socket.SOCK_STREAM, proto = 0, fileno = None)
		s.connect((HOST, 7777))
		string_player = s.recv(1500).decode()
		if string_player == "1":
			current_player = J1
		elif string_player == "2":
			current_player = J2
		elif string_player == "Spectator":
			current_player = 3
		if current_player == 1 or current_player == 2:
			print("You are the player " + str(current_player))
		else:
			print("You are a spectator")
		
		while True:
			grids = [grid(), grid(), grid()]
			grids[J1].display()
			while grids[0].gameOver() == -1:
				shot = -1
				if current_player == J1:
					while True:
						tmp = input ("In which position do you want to play? ")
						if ord(tmp) >= 48 and ord(tmp) <= 56: #conversion en ascii
							shot = ord(tmp)-48
						if shot >= 0 and shot < NB_CELLS:
							break
						else:
							print("You should choose between 0 and 8.")
					if (grids[0].cells[shot] != EMPTY):
						grids[current_player].cells[shot] = grids[0].cells[shot]
						grids[current_player].display()
					else:
						grids[current_player].cells[shot] = current_player
						grids[0].play(current_player, shot)
						grids[current_player].display()
						shot_to_send = bytes(str(shot),"ascii")
						s.send(shot_to_send)
						current_player = current_player%2+1
						
				else:
					shot = int(s.recv(1500))
					grids[0].play(current_player, shot)
					if current_player == 0: #pour le mode spectateur
						grids[0].display()
					else:
						current_player = current_player%2+1		

			print("Game over")
			grids[0].display()
			if grids[0].gameOver() == J1:
				print("You win !")
				score[0] += 1
			else:
				print("You lose !")
			print("Score : " + str(score[0]))
				
			"""-------Allows the player to play again-------"""
			answer = ''
			while answer != 'y' or answer != 'n': 
				answer = input("Do you want to continue? y/n ")
				print(answer)
				if answer == 'y' or answer == 'n':
					break
			if answer == 'n':
				break
			"""----------------------------------------------------------"""
		#end of while(True)
	#end of client
							
main()


#else:
				#	shot = random.randint(0,8)
				#	while grids[current_player].cells[shot] != EMPTY:
				#		shot = random.randint(0,8)
