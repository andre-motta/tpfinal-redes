#!/usr/bin/env python3
import select, socket, sys, queue, struct, time, re
from collections import defaultdict


def pegar_flag(msg: str, flag: str):
    flag_list = []
    while flag in msg:
        counter = msg.find(flag)        
        msg = msg[counter+1:]
        prox_n_car = re.search('[^a-zA-Z0-9]', msg)
        if prox_n_car:
            if msg.find(prox_n_car.group(0)) != 0:
                flg = msg[:msg.find(prox_n_car.group(0))]
                if flg != '':
                    flag_list.append(flg)
        else:
            flg = msg[:]
            if flg != '':
                flag_list.append(flg)       
    return flag_list


def processa_mensagem(msg_o: str):
    opt = ['#', '+', '-']
    if any(x in opt for x in msg_o):
        return [pegar_flag(msg_o, '#'), pegar_flag(msg_o, '+'), pegar_flag(msg_o, '-')]
    return []


servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
servidor.settimeout(15.0)
servidor.bind(('localhost', int(sys.argv[1])))
tag_user = defaultdict(list)
print("SERVIDOR")

entradas = [servidor]
saidas = []
fila_de_mensagem = {}
dados_socket = {}
while entradas:
    leitura, escrita, excecao = select.select(entradas, saidas, entradas)
    #print(leitura)
    #print(saidas)
    messages = defaultdict(dict)
    for conteudo in leitura:
        if conteudo is servidor:
            (client_data, client_address) = servidor.recvfrom(512)
            #print (client_address)
            client = client_address
            msg = client_data.decode("utf-8")
            flags = processa_mensagem(msg)
            #print("flags")
            #print(flags)
            if len(flags) > 1:
                for hashtag in flags[1]:                    
                    if client_address not in tag_user[hashtag]:
                        tag_user[hashtag].append(client_address)
                        #print(tag_user)
            if len(flags) > 2:
                for hashtag in flags[2]:
                    try:
                        #print("remove " + str(hashtag))
                        tag_user[hashtag].remove(client_address)
                        #print(tag_user)
                    except ValueError:
                        "Do Nothing"
                        #print("Not Found")
            if len(flags) > 0:                        
                for hashtag in flags[0]:
                    for data in tag_user[hashtag]:
                        messages[data] = msg
            #print(tag_user)
            #print(messages)
            messagelist = []
            for key, value in dict(messages).items():
                temp = [key,value]
                messagelist.append(temp)
            saidas.append(servidor)

            
    for saida in escrita:
        for message in messagelist:
            #print(message)
            servidor.sendto(message[1].encode("utf-8"), (message[0][0], message[0][1]))
        messagelist = []
        saidas = []
        #sendMessages()
            
