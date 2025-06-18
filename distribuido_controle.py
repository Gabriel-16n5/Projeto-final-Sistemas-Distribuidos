from xmlrpc.client import ServerProxy
import sys

def run_tests(server_url):
    server = ServerProxy(server_url)
    base = 10**6
    multipliers = [1, 5, 25, 125]
    
    for mult in multipliers:
        n = base * mult
        pi, elapsed = server.calculate_pi(n)
        print(f"Dist | N={n:>10,} → π≈{pi:.8f} | tempo={elapsed:.3f}s")

if __name__ == "__main__":
    server_url = "http://localhost:8000"
    run_tests(server_url)