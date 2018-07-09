#!/usr/bin/env python3
import sys, socket, select
import unidecode


if __name__ == '__main__':

    print("CLIENTE")

    if (len(sys.argv) < 4):
        print("Erro: Faltam argumentos.")
        print("Formato: client.py portaLocal IpServidor PortaServidor")
        sys.exit()

    # Input arguments
    LocalHost = '127.0.1.2'
    LocalPort  = int(sys.argv[1])
    ServerIP   = sys.argv[2]
    ServerPort = int(sys.argv[3])

    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

    sys.stdout.flush()

    while True:
        socketList = [udp]

        readSockets, writeSockets, errorSockets = select.select(socketList, [sys.stdin], [])

        for sock in readSockets:
            if sock == udp:
                message, conn = sock.recvfrom(512)
                if not message:
                    print("Desconectado do servidor!")
                    sys.exit()
                else:
                    print("Mensagens recebidas:")
                    sys.stdout.write(message.decode("utf-8"))
                    sys.stdout.write("\n")
                    sys.stdout.flush()

        for w in writeSockets:
            msg = sys.stdin.readline().strip()

            msg = unidecode.unidecode(msg)
            
            msg = bytes(msg, "UTF-8")
            udp.sendto(msg, (ServerIP, ServerPort))
            sys.stdout.flush()
