Cálculo Base (Monte Carlo): A ideia fundamental é simular a geração de vários pontos aleatórios dentro de um quadrado (no intervalo [0, 1] para cada coordenada). Para cada ponto, se a soma dos quadrados de suas coordenadas for menor ou igual a 1, ele está dentro de um quarto de um círculo unitário. Como a razão entre a área desse quarto de círculo e a área do quadrado é π/4, podemos estimar π multiplicando a razão de pontos internos por 4.

Versão Sequencial/Paralela Local: Nos primeiros códigos que você enviou (sequencial e paralelo), o método base é aplicado, porém distribuindo o trabalho:

Versão Sequencial: O código roda uma simulação inteira em um único processo, gerando todos os pontos e contando quantos estão dentro do círculo.

Versão Paralela: O trabalho é dividido entre múltiplos processos, que cada um calcula uma parte do total de pontos, e depois os resultados são combinados para formar a estimativa de π.

Versão Distribuída com Sockets e RMI (XML-RPC): Nesta implementação mais avançada, a tarefa é distribuída em uma rede:

Servidor Coordenador: Gerencia os workers que se registram e distribui a carga de pontos entre eles para o cálculo parcial de π.

Workers (Clientes): Cada worker executa a função que calcula quantos de seus pontos gerados estão dentro do círculo. Eles se registram no servidor coordenador usando comunicação via XML-RPC.

Controlador: Inicia os testes chamando o servidor para calcular π com diferentes números de amostras e exibe os resultados.