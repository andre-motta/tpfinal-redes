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
            conexao, endereco_cliente = conteudo.accept()
            conexao.setblocking(0)
            entradas.append(conexao)
            fila_de_mensagem[conexao] = queue.Queue()
            dados_socket[conexao] = [endereco_cliente, 0] ### INSERE A TUPLA AQUI <---------
        else:
            dados = conteudo.recv(2048)
            if dados:
                fila_de_mensagem[conteudo].put(dados)
                if conteudo not in saidas:
                    saidas.append(conteudo)
            else:
                if conteudo in saidas:
                    saidas.remove(conteudo)
                entradas.remove(conteudo)

    for conteudo in escrita:
        filled = True
        try:
            next_msg = fila_de_mensagem[conteudo].get_nowait()
        except queue.Empty:
            saidas.remove(conteudo)
        else:
            for i in range(0, len(dados_socket[conteudo])):
                if (dados_socket[conteudo][i] == -1):
                    filled = False
            if filled:


    for conteudo in excecao:
        entradas.remove(conteudo)
        if conteudo in saidas:
            saidas.remove(conteudo)
        conteudo.close()
        del fila_de_mensagem[conteudo]
