import socket, json

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
        nomeDNS = '172.22.67.194'
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
    serverHost = '172.22.67.194' #cin lua
    serverPort = 12001

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((serverHost, serverPort))

    print ('--Nova conexão com Cliente UDP--')

    while True:
        sentence, addr = sock.recvfrom(1024)
        print('O que o cliente quer?')
        print(f'Cliente  {addr[0]} solicitando: {sentence.decode()}')
        
        if not sentence: break        
        print(sentence.decode()[:7])
        print(sentence.decode()[8:])
                    
        #DECODIFICAÇÃO DA SOLICITAÇÃO
        ####TA DANDO MERDA AQUI
        if sentence.decode() == "LISTAR" :
            nomes = b''
            for x in datas:
                nomes += bytes(x["nome"], "utf-8")
                nomes += b' '
            sock.sendto(nomes, addr)
                

        elif sentence.decode()[:7] == "ARQUIVO" :
            response = 'Arquivo nao encontrado'
            for x in datas:
                if sentence.decode()[8:] == x["nome"] :
                    response = bytes(x["descricao"], "utf-8")
            sock.sendto(response, addr)                    
                                

        elif sentence.decode() == "ENCERRAR":
                
                response = 'Encerrada conexao com servidor'
                print(f'encerrando conexão com cliente {addr}')
                sock.sendto(bytes(response, "utf-8"), addr) 
                sock.close()
                break


        else:
            response = ''
            response = 'Operacao nao identificada pelo Servidor'
            sock.sendto(bytes(response, "utf-8"), addr)

        

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

