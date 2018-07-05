#!/usr/bin/env python3
import select, socket, sys, queue, struct, time


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
            
