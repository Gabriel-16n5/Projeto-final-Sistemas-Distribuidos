import xmlrpc.server
from xmlrpc.client import ServerProxy
import threading
import time

workers = []
lock = threading.Lock()

def register_worker(worker_url):
    with lock:
        if worker_url not in workers:
            workers.append(worker_url)
            print(f"Worker registrado: {worker_url}")
            return True
    return False

def calculate_pi(n_samples):
    start_time = time.perf_counter()
    
    with lock:
        n_workers = len(workers)
    if n_workers == 0:
        return 0.0, 0.0  # pi=0, tempo=0
    
    # Distribui tarefas
    samples_per_worker = n_samples // n_workers
    remainder = n_samples % n_workers
    tasks = [samples_per_worker + 1 if i < remainder else samples_per_worker 
             for i in range(n_workers)]
    
    # Executa chamadas RPC
    results = []
    for i, worker_url in enumerate(workers):
        try:
            worker = ServerProxy(worker_url)
            results.append(worker.calculate_partial_pi(tasks[i]))
        except ConnectionError:
            print(f"Worker {worker_url} inacessível")
            results.append(0)
    
    # Calcula resultado final
    total_inside = sum(results)
    pi = 4.0 * total_inside / n_samples
    elapsed = time.perf_counter() - start_time
    return pi, elapsed

if __name__ == "__main__":
    server = xmlrpc.server.SimpleXMLRPCServer(
        ('0.0.0.0', 8000), 
        allow_none=True,
        logRequests=False
    )
    server.register_function(register_worker, 'register_worker')
    server.register_function(calculate_pi, 'calculate_pi')
    print("Servidor ouvindo na porta 8000...")
    server.serve_forever()