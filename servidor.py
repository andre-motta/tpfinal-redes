#!/usr/bin/env python3
import select, socket, sys, queue, struct, time, re


def pegar_flag(msg: str, flag: str):
    flag_list = []
    while flag in msg:
        counter = msg.find(flag)
        print("counter: {0}".format(counter))
        msg = msg[counter+1:]
        prox_n_car = re.search('[^a-zA-Z0-9]', msg)
        if prox_n_car:
            if msg.find(prox_n_car.group(0)) != 0:
                flag_list.append(msg[:msg.find(prox_n_car.group(0))])
        else:
            flag_list.append(msg[:])
        print(flag_list)
    return flag_list


def processa_mensagem(msg_o: str):
    opt = ['#', '+', '-']
    if any(x in opt for x in msg_o):
        return [pegar_flag(msg_o, '#'), pegar_flag(msg_o, '+'), pegar_flag(msg_o, '-')]
    return []


servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
servidor.settimeout(15.0)
servidor.setblocking(0)
servidor.bind(('localhost', int(sys.argv[1])))
servidor.listen(5)

entradas = [servidor]
saidas = []
fila_de_mensagem = {}
dados_socket = {}
while entradas:
    leitura, escrita, excecao = select.select(entradas, saidas, entradas)

    for conteudo in leitura:
        if conteudo is servidor:
            (client_data, client_address) = s.recvfrom(512)
            print (client_address)
            print(client_data)
            
