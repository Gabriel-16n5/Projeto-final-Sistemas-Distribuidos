from xmlrpc.client import ServerProxy
import sys

def run_tests(server_url):
    """
    Conecta-se ao servidor coordenador e, para diferentes números 
    de amostras, solicita o cálculo distribuído de π. Mostra os resultados.
    """
    server = ServerProxy(server_url)
    base = 10**6  # Define 1 milhão como base
    multipliers = [1, 5, 25, 125]
    
    for mult in multipliers:
        n = base * mult
        # Chama a função de cálculo do servidor e recebe π estimado e o tempo gasto.
        pi, elapsed = server.calculate_pi(n)
        print(f"Dist | N={n:>10,} → π≈{pi:.8f} | tempo={elapsed:.3f}s")

if __name__ == "__main__":
    server_url = "http://localhost:8000"
    run_tests(server_url)
