import socket
import pickle

class Machine:
    def __init__(self, id, host, port):
        self.id = id
        self.host = host
        self.port = port

class Controller:
    def __init__(self, machines):
        self.machines = machines
        self.port = 6000
        self.host = '127.0.0.1'
        

    def inicializaMatrixes(self):
        pass

    def matrixBreaker(self, matrixA, matrixB):
        if(len(matrixA) != len(matrixB)):
            raise ValueError("Erro: As matrizes não podem ser multiplicadas, pois tem tamanhos divergentes de linhas de A e colunas de B")
        number = 0
        machinesQuantity = len(self.machines)
        linesMatrixA = {}

        if(machinesQuantity == 0):
            raise ValueError('Error: Deve ter pelo menos uma máquina para fazer o cálculo')

        for i in range(machinesQuantity):
            linesMatrixA[i] = matrixA[number:number+machinesQuantity-1]
            number += machinesQuantity-1

        
        return linesMatrixA
    
    def sendData(self):
        matrixA = [[1, 2], [3, 4]]
        matrixB = [[6, 5], [4, 3]]

        linesA = self.matrixBreaker(matrixA, matrixB)
       
        for i in range(len(self.machines)):
            data = pickle.dumps((linesA[i], matrixB))  
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.machines[i].host, self.machines[i].port))
                s.sendall(data)

    def recibeData(self):
        matrizC = []
        while(True):
            linhasMatrizC = []
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
                    linhasMatrizC = pickle.loads(data)  
                    print("Matriz C recebida:", linhasMatrizC)
                matrizC.append(linhasMatrizC)
                
               
class Main():
    machine1 = Machine(1, '127.0.0.1', 5000)
    machine2 = Machine(2, '127.0.0.1', 5001)

    c1 = Controller([machine1, machine2])
    c1.sendData()

        
Main()