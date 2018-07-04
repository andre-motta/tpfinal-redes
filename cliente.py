#!/usr/bin/env python3
import socket, sys, time, struct


cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#cliente.settimeout(15.0)
cliente.connect((sys.argv[1], int(sys.argv[2])))

mensagemFinal = '' ##ler da stdin

mensagemCodificada = []


mensagemFinal = ''.join(mensagemCodificada)

cliente.send(mensagemFinal.encode('ASCII', 'ignore'))
#time.sleep(0.2)


#time.sleep(0.2)
#Acho que devemos enviar primeiro um numero q é o numero de mensagens e dps cada mensagem pra gt fazer um loop disso aqui \/
mensagem = cliente.recv(2048)

print(mensagem.decode())
