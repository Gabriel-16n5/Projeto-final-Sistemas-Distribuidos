import random
import time
from multiprocessing import Pool, cpu_count

def conta_interno(n_amostras: int) -> int:
    """
    Conta quantos pontos, dentre 'n_amostras', caem dentro do 
    quarto de círculo unitário (raio = 1) no primeiro quadrante.
    """
    dentro = 0
    for _ in range(n_amostras):
        x, y = random.random(), random.random()
        if x*x + y*y <= 1.0:
            dentro += 1
    return dentro

def estima_pi_paralelo(n_amostras: int, n_processos: int) -> float:
    """
    Divide as simulações entre vários processos. Cada processo calcula 
    quantos pontos caem dentro do círculo. Depois, com os resultados 
    individuais, estima o valor de π.
    """
    # Divide igualmente as amostras entre os processos
    amostras_por_processo = n_amostras // n_processos
    # Cria uma lista com a quantidade de amostras para cada processo
    lista_amostras = [amostras_por_processo] * n_processos
    
    # Caso n_amostras não seja divisível igualmente, adiciona o restante ao primeiro grupo
    resto = n_amostras % n_processos
    if resto:
        lista_amostras[0] += resto
    
    # Cria o pool de processos e distribui a função 'conta_interno' para cada grupo de amostras
    with Pool(processes=n_processos) as pool:
        resultados = pool.map(conta_interno, lista_amostras)
    
    total_dentro = sum(resultados)
    # A razão entre os pontos dentro do círculo e o total de pontos, multiplicada por 4, dá a estimativa de π.
    return 4 * total_dentro / n_amostras

if __name__ == "__main__":
    base = 10 ** 6  # Inicia com 1 milhão de pontos
    # Usa a quantidade de núcleos disponíveis no computador para paralelismo
    n_processos = cpu_count()
    
    # Para cada multiplicador, aumenta o número total de pontos, realiza a estimativa e mede o tempo
    for multiplicador in [1, 5, 25, 125]:
        n = base * multiplicador
        inicio = time.perf_counter()
        pi_estimado = estima_pi_paralelo(n, n_processos)
        tempo_gasto = time.perf_counter() - inicio
        # Exibe o resultado formatado, indicando que esta é a versão paralela ("Par")
        print(f"Par | N={n:>10,} → π≈{pi_estimado:.6f} | tempo={tempo_gasto:.3f}s")
