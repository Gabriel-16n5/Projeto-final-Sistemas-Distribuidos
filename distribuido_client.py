import random
from xmlrpc.server import SimpleXMLRPCServer
import socket
import time
from xmlrpc.client import ServerProxy

def calculate_partial_pi(n_samples):
    inside = 0
    for _ in range(n_samples):
        x, y = random.random(), random.random()
        if x*x + y*y <= 1.0:
            inside += 1
    return inside

if __name__ == "__main__":
    # Configura servidor RPC do worker
    worker_server = SimpleXMLRPCServer(('0.0.0.0', 0), logRequests=False)
    worker_server.register_function(calculate_partial_pi, 'calculate_partial_pi')
    worker_port = worker_server.server_address[1]
    
    # Registra no coordenador
    server_url = "http://localhost:8000"
    worker_url = f"http://localhost:{worker_port}"
    
    try:
        server = ServerProxy(server_url)
        if server.register_worker(worker_url):
            print(f"Worker registrado: {worker_url}")
        else:
            print("Falha no registro")
    except ConnectionError:
        print("Servidor coordenador inacessível")
        exit(1)
    
    # Inicia atendimento de requisições
    worker_server.serve_forever()