# Importa os módulos que vamos usar:
# random: para gerar números aleatórios.
# time: para medir o tempo de execução.
import random
import time

# Função para estimar o valor de π usando o método de Monte Carlo.
def estima_pi(numero_de_vezes: int) -> float:
    pontos_dentro = 0  # Contador para os pontos que caem dentro do círculo.
    
    # Vamos simular 'numero_de_vezes' lançamentos.
    for _ in range(numero_de_vezes):
        # Gera um ponto (x, y) com coordenadas aleatórias entre 0 e 1.
        x = random.random()
        y = random.random()
        # Verifica se o ponto está dentro do quadrante do círculo unitário.
        # Se a soma dos quadrados for menor ou igual a 1, o ponto está dentro.
        if x * x + y * y <= 1.0:
            pontos_dentro += 1
    
    # O valor de π é aproximado por 4 vezes a razão dos pontos dentro do círculo
    # sobre o total de pontos simulados.
    return 4 * pontos_dentro / numero_de_vezes

# Se este script estiver sendo executado diretamente, e não importado:
if __name__ == "__main__":
    base = 10 ** 6  # Começamos com 1 milhão de pontos.
    # Testamos a função usando diferentes números de pontos.
    for i in range(4):
        # N é multiplicado por 5 na cada iteração, aumentando o número de pontos.
        n = base * (5 ** i)
        # Começa a contar o tempo de execução
        inicio = time.perf_counter()
        # Estima π usando a função estima_pi com n pontos.
        pi_estimado = estima_pi(n)
        # Calcula o tempo que levou para a execução.
        tempo_gasto = time.perf_counter() - inicio
        # Mostra os resultados, formatando a exibição.
        print(f"Seq | N={n:>10,} → π≈{pi_estimado:.6f} | tempo={tempo_gasto:.3f}s")
