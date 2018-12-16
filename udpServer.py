import socket, json
import time 

#####COMENTÁRIOS: ESTE PROGRAMA EXECUTA A FUNÇÃO DO SERVIDOR TCP E DEVE SER INICIALIZADO APÓS O DNS SERVER
#### A variável "serverHost" deve conter o ip da máquina que está rodando o código
#### A variável "nomeDNS" deve conter o ip da máquina que está rodando o código dnsServer.py
####

#serverPort = 12000
#serverHost = '172.22.67.194' #LUANA

nomes = b''
response = b''

datas = [ 
                {
                        "nome": "InfraCom",
                        "descricao": "Cadeira do quinto periodo, Professor Jose Suruagy"
                },

                {
                        "nome": "Estatistica",
                        "descricao": "Cadeira do quarto periodo"
                },

                {
                        "nome": "Hardware",
                        "descricao": "Cadeira do terceiro periodo, Professora Edna"
                },

                {
                        "nome": "Software",
                        "descricao": "Cadeira do terceiro periodo, Professor Eduardo"
                },

                {
                        "nome": "IP",
                        "descricao": "Cadeira do primeiro periodo, Professor Alexandre"
                }
]

######### COMUNICAÇÃO COM DNS SERVER ############ 


def dnsCom():

    while True:
        nomeDNS = '192.168.0.13'
        portaDNS = 12000

        print('Comunicando com DNS')
        sok = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dominio = 'fb.com'
        sok.sendto(bytes(dominio, 'utf-8'), (nomeDNS, portaDNS))
        sok.close()
        print('Fechei comunicação com DNSserver')
        #sok.close()
        break

######### COMUNICAÇÃO COM O UDP CLIENT ##############
def clientCom():
    serverHost = '192.168.0.13' #cin lua
    serverPort = 12001

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((serverHost, serverPort))

    print ('--Nova conexão com Cliente UDP--')

    numSeq = 5
    numExp = numSeq + 1
    i = 0

    while True:
        sentence, addr = sock.recvfrom(1024)
        print('O que o cliente quer?')
        print(f'Cliente  {addr[0]} solicitando: {sentence.decode()[3:]}')
        
        if not sentence: break  
         ##acho q pode tirar essa parte aqui 
        print(f'numero de sequencia cliente: {sentence.decode()[0]}')
        print(f'numero esperado cliente: {sentence.decode()[1]}')
        if i == 0:
                print(f'ACK : x')
                AKC = sentence.decode()[1]
                newResponse = str(numSeq) + str(numExp) + AKC
        else: 
                print(f'ACK : {sentence.decode()[2]}')        
                AKC = sentence.decode()[1]
                numSeq = int(sentence.decode()[2])
                numExp = numSeq + 1
                newResponse = str(numSeq) + str(numExp) + AKC 
        
        
        
        #DECODIFICAÇÃO DA SOLICITAÇÃO
        ####TA DANDO MERDA AQUI
        if sentence.decode()[3:] == "LISTAR" :
            nomes = b''
            for x in datas:
                nomes += bytes(x["nome"], "utf-8")
                nomes += b' '
            newResponse = bytes(newResponse, "utf-8")
            newResponse += nomes
            sock.sendto(newResponse, addr)
                

        elif sentence.decode()[3:10] == "ARQUIVO" :
            response = 'Arquivo nao encontrado'
            for x in datas:
                if sentence.decode()[11:] == x["nome"] :
                    response = bytes(x["descricao"], "utf-8")
            newResponse = bytes(newResponse, "utf-8")
            newResponse += response
            sock.sendto(newResponse, addr)                    
                                

        elif sentence.decode()[3:] == "ENCERRAR":
                
                response = 'Encerrada conexao com servidor'
                print(f'encerrando conexão com cliente {addr}')
                newResponse += response
                newResponse = bytes(newResponse, "utf-8")
                sock.sendto(newResponse, addr) 
                sock.close()
                break


        else:
            response = ''
            response = 'Operacao nao identificada pelo Servidor'
            newResponse += response
            newResponse = bytes(newResponse, "utf-8")
            sock.sendto(newResponse, addr)
        
        i += 1

        

##MAIN:
###executando cliente
def main():
    dnsCom()
    clientCom()

###fim da execução servidor

if __name__ == "__main__":
    main()
#FUNÇÕES DO SERVIDOR
# 1. Listar arquivos do servidor CÓDIGO 1
# 2. Sinalizar que arquivo não existe 
# 3. Enviar arquivo para cliente solicitante CÓDIGO 2
# 4. Encerrar conexão

