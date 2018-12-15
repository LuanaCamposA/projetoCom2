
import socket, json

########ESTE PROGRAMA RODA A EXECUÇÃO DO DNS SERVER; DEVE SER O PRIMEIRO A SER EXECUTADO
######OBSERVAÇÕES:
###### a variável "serverHost" deve conter o ip da máquina que está rodando o código 


serverHost = '192.168.0.15' #cin lua
serverPort1 = 12000

dados = []                                              ###dados salva o domínio e o respectivo endereço do servidor

def addDadosJSON(nome, addr):
        doc = {
                "nome": nome,
                "addr": addr
        }

        dados.append(doc)

##serverCom faz a comunicação DNS/SERVIDOR      
def serverCom():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        sock.bind((serverHost, serverPort1))

        while True: 
                data, addr = sock.recvfrom(1024) 
                print(f'Recebendo dados do SERVIDOR: {addr}')
                addDadosJSON(data.decode(), addr[0])
                #print(dados)
                print('Encerrando conexão com SERVIDOR...')
                sock.close()
                break
        #return addr


##  clientCom faz a comunicação dns/cliente
def clienteCom():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((serverHost, serverPort1))

        while True:
                data, addr = sock.recvfrom(1024)
                print(f'Cliente  {addr[0]} solicitando: {data.decode()}')
                dominio = searchDomain(data.decode())
                #print(dominio)
                sock.sendto(bytes(dominio, "utf-8"), addr)
                if dominio != "Dominio não encontrado":
                        sock.close()
                        print('Encerrando conexão com cliente...')
                        break
        

## searchDomain procura pelo dominio solicitado pelo cliente
def searchDomain(domain): 
        #print(f'aqui eh dominio: {domain}')
        for x in dados:
                if x["nome"] == domain:
                        return x["addr"]
        return "Dominio não encontrado"

##MAIN
def main():
        print('Iniciando execução do DNS...')

        serverCom()
        print('---Nova conexão ---')       
        clienteCom()
        print('Encerrando DNS...')

if __name__ == "__main__":
    main()