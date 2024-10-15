import socket
import pickle

##just test
class Cliente:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def recibeData(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            print('Esperando por conexión...')
            conn, addr = s.accept()
            print('adrss: ', addr)  
            with conn:
                print('Conectado por', addr)
                # Recebe dados
                data = conn.recv(4096)
                matrizes = pickle.loads(data)  # Desserializa os dados
                linesA, matrixB = matrizes  # Desempacota as matrizes
                print("Matriz 1 recebida:", linesA)
                print("Matriz 2 recebida:", matrixB)
                return linesA, matrixB

    def fazMultiplicacao(self, linesA, matrixB):
        resultados = []
        for i in range(len(linesA)):   
            resultadoLinha = []
            for j in range(len(matrixB)):
                soma = 0
                for k in range(len(linesA[0])):
                    print('multiplicando esses valores:', linesA[i][k] , matrixB[j][k])
                    soma += linesA[i][k] * matrixB[j][k]
                resultadoLinha.append(soma)   
            resultados.append(resultadoLinha)
        return resultados          

    def sendData(self, resultados, host, port):
        data = pickle.dumps((resultados))  
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(data)



porta = input('Digite a porta:')
c1 = Cliente('127.0.0.1', int(porta))
linesA, columnsB = c1.recibeData()
resultados = c1.fazMultiplicacao(linesA, columnsB)
print('resultados:', resultados)    