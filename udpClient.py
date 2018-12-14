
import socket
import time
import threading

####ESSE PROGRAMA RODA O CLIENTE; DEVE SER INICIALIZADO APÓS O DNS SERVER E O SERVIDOR.
###Na função, dnsServerComunication(), a variavel nomeDns deve ser setada com o IP da máquina que está rodando o código do dnsServer
### quando for solicitado o site, digite: "fb.com"
###Na função, tcpServerComunication() não é necessária nenhuma modificação;


    

### faz a comunicação cliente/servidor -- vai ter que ser UDP
def tcpServerComunication(add):
    
    print('\n')                                                       
    print('---DIGITE A OPÇÃO DESEJADA : -----')
    print('----->ENCERRAR ')
    print('----->LISTAR ')
    print('----->ARQUIVO <nome do arquivo> ')
    print('\n')                                                                
    request = input()

    serverName = add
    serverPort = 12001

    sockt =  socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 0 --- 7 8 --- 15 16 --- 23 23 --- 31  
    # numSeq    ACK        0          0  
    # ------------------------------------
    # ---------------DADOS----------------
    # ------------------------------------



    while True:
        i=0
        numSeq = '1'
        numExp =  str(int(numExp) + 1)
        AKC = '0'
        newResquest = numSeq + request

        while i<3 : 
            try:
                sockt.sendto(bytes(newResquest, 'utf-8'), (serverName, serverPort))
                sockt.settimeout(5.00)
                dados, addr = sockt.recvfrom(1024)
                if dados.decode()[0] == int(numExp):
                    i = 3
                else: 
                    print('NumSeq errado...')

            except socket.timeout:
                print('Pacote perdido')
                i += 1

        if request == "ENCERRAR" :
            print('\n')    
            print(dados.decode())
            #print(f'Encerrando conexão com Servidor: {addr[0]}')
            sockt.close()
            break
        
        elif request == "LISTAR":
            print('\n')    
            print("Listando arquivos existentes...")
            print(dados.decode())
            print('\n')    

        
        elif request[:7] == "ARQUIVO":
            print('\n')    
            print("Arquivo solicitado: ")
            print(dados.decode())
            print('\n')    

        else:
            print(dados.decode())

                
        print('Digite novo comando: \n')
        request = input()





#### dnsServerComunication() faz a comunicação cliente/dns ###
def dnsServerComunication():

    nomeDNS = '172.22.67.194' #LUANA
    portaDNS = 12000

    print('Digite site:')
    message = input(" ")

    sok =  socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sok.sendto(bytes(message, 'utf-8'), (nomeDNS, portaDNS))

    #dad vai ser o adress do servidorTCP com quem o cliente vai estabelecer conexão
    dad, addr = sok.recvfrom(1024)

    while True:    
        
        print (f'Endereço do site solicitado: \n', dad.decode())
        print('Encerrando conexão com DNS...')
        break
    sok.close()
    return dad.decode()


##MAIN:
###executando cliente
def main():
    print('Iniciando execução...')
    
    end = dnsServerComunication() ##end vai receber o dominio/ip do servidor

    tcpServerComunication(end)    ##comunicação com o servidor

###fim da execução cliente

if __name__ == "__main__":
    main()

