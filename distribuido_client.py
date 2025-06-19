import random
from xmlrpc.server import SimpleXMLRPCServer
import socket
import time
from xmlrpc.client import ServerProxy

def calculate_partial_pi(n_samples):
    """
    Calcula quantos pontos, dentre n_samples gerados aleatoriamente,
    caem dentro de um quarto de círculo unitário.
    """
    inside = 0
    for _ in range(n_samples):
        x, y = random.random(), random.random()
        if x*x + y*y <= 1.0:
            inside += 1
    return inside

if __name__ == "__main__":
    # Configura um servidor XML-RPC para o worker, usando uma porta dinâmica.
    worker_server = SimpleXMLRPCServer(('0.0.0.0', 0), logRequests=False)
    # Registra a função que será chamada pelo coordenador.
    worker_server.register_function(calculate_partial_pi, 'calculate_partial_pi')
    # Obtém a porta que o sistema escolheu para o servidor.
    worker_port = worker_server.server_address[1]
    
    # Cria a URL do worker e a URL do servidor (coordenador)
    server_url = "http://localhost:8000"
    worker_url = f"http://localhost:{worker_port}"
    
    # Tentativa de registro do worker no servidor coordenador.
    try:
        server = ServerProxy(server_url)
        if server.register_worker(worker_url):
            print(f"Worker registrado: {worker_url}")
        else:
            print("Falha no registro")
    except ConnectionError:
        print("Servidor coordenador inacessível")
        exit(1)
    
    # Inicia o loop do servidor do worker para atender requisições.
    worker_server.serve_forever()
