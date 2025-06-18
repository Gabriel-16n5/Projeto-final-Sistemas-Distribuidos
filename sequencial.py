# monte_carlo_seq.py
import random
import time

def estimate_pi(n_samples: int) -> float:
    inside = 0
    for _ in range(n_samples):
        x, y = random.random(), random.random()
        if x*x + y*y <= 1.0:
            inside += 1
    return 4 * inside / n_samples

if __name__ == "__main__":
    # 4 rodadas com N crescente
    base = 10**6
    for i in range(4):
        n = base * (5 ** i)  # 1e6, 5e6, 25e6, 125e6
        start = time.perf_counter()
        pi = estimate_pi(n)
        elapsed = time.perf_counter() - start
        print(f"Seq | N={n:>10,} → π≈{pi:.6f} | tempo={elapsed:.3f}s")