import xmlrpc.server
from xmlrpc.client import ServerProxy
import threading
import time

# Lista que armazenará os endereços (URLs) dos workers registrados.
workers = []
# Um lock (trava) para garantir que a lista seja modificada por apenas uma thread por vez.
lock = threading.Lock()

def register_worker(worker_url):
    """
    Registra um novo worker se ele ainda não estiver na lista.
    Usa uma trava para evitar problemas de concorrência.
    """
    with lock:
        if worker_url not in workers:
            workers.append(worker_url)
            print(f"Worker registrado: {worker_url}")
            return True
    return False

def calculate_pi(n_samples):
    """
    Distribui a tarefa de cálculo parcial de pontos do método de Monte Carlo
    entre os workers registrados e junta os resultados para estimar π.
    
    n_samples: número total de amostras/pontos a serem gerados.
    
    Retorna: uma tupla (pi_estimado, tempo_de_execução).
    """
    start_time = time.perf_counter()
    
    # Obtém o número de workers disponíveis de forma segura.
    with lock:
        n_workers = len(workers)
        
    # Se não houver nenhum worker registrado, retorna 0.0 para π e tempo 0.0.
    if n_workers == 0:
        return 0.0, 0.0 
    
    # Divide os pontos igualmente entre os workers
    samples_per_worker = n_samples // n_workers
    remainder = n_samples % n_workers
    # Se houver sobras, distribui um a mais para os primeiros workers.
    tasks = [
        samples_per_worker + 1 if i < remainder else samples_per_worker
        for i in range(n_workers)
    ]
    
    results = []
    # Para cada worker, envia a tarefa e coleta o resultado.
    for i, worker_url in enumerate(workers):
        try:
            worker = ServerProxy(worker_url)
            # Cada worker calcula quantos pontos caem dentro do círculo.
            results.append(worker.calculate_partial_pi(tasks[i]))
        except ConnectionError:
            print(f"Worker {worker_url} inacessível")
            results.append(0)
    
    total_inside = sum(results)
    # A estimativa de π é dada pela razão dos pontos no círculo vezes 4.
    pi = 4.0 * total_inside / n_samples
    elapsed = time.perf_counter() - start_time
    return pi, elapsed

if __name__ == "__main__":
    # Cria um servidor XML-RPC que escuta em todas as interfaces na porta 8000.
    server = xmlrpc.server.SimpleXMLRPCServer(
        ('0.0.0.0', 8000),
        allow_none=True,
        logRequests=False
    )
    # Registra as funções que poderão ser chamadas pelos clientes.
    server.register_function(register_worker, 'register_worker')
    server.register_function(calculate_pi, 'calculate_pi')
    print("Servidor ouvindo na porta 8000...")
    # Inicia o loop do servidor para aguardar requisições.
    server.serve_forever()
