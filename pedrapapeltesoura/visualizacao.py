import time

from modelos import Escolha, Resultado


class Render:
    def __init__(self, sleep_contador: int = 1, sleep_movimentos: int = 3, sleep_resultado: int = 3) -> None:
        self.sleep_contador = sleep_contador
        self.sleep_movimentos = sleep_movimentos
        self.sleep_resultado = sleep_resultado
        
    def atualizar_contador(self, contagem: int) -> None: 
        ...

    def mostrar_movimentos(self, j1: Escolha | None, j2: Escolha | None) -> None: 
        ...

    def mostrar_resultado(self, resultado: Resultado, escolha: Escolha | None) -> None: 
        ...

    def mostrar_resultado_final(self, resultado: Resultado, pontos_j1: int, pontos_j2: int) -> None: 
        ...

    def ler_movimento(self) -> tuple[Escolha, Escolha]: 
        ...


class RenderTemporario(Render):
    def atualizar_contador(self, contagem: int):
        if contagem != 0:
            print(f"{contagem}...")
        else:
            print(f"{contagem}!")
        time.sleep(self.sleep_contador)

    def mostrar_movimentos(self, j1: Escolha | None, j2: Escolha | None):
        movimento_j1 = j1 or "Não reconhecido"
        movimento_j2 = j2 or "Não reconhecido"
        print(f"{movimento_j1} x {movimento_j2}")
        time.sleep(self.sleep_movimentos)

    def mostrar_resultado(self, resultado: Resultado, escolha: Escolha | None):
        if resultado == Resultado.EMPATE:
            print(f"Empate!")
        else:
            print(f"Jogador {resultado} venceu utilizando {escolha}")
        time.sleep(self.sleep_resultado)

    def mostrar_resultado_final(self, resultado: Resultado, pontos_j1: int, pontos_j2: int) -> None: 
        print(f"Pontuação final: {pontos_j1} x {pontos_j2}")
        if resultado == Resultado.EMPATE:
            print("Empate!")
        elif pontos_j1 > pontos_j2:
            print("Jogador 1 Venceu!")
        else:
            print("Jogador 2 Venceu!")
        time.sleep(self.sleep_resultado)

    def ler_movimento(self) -> tuple[Escolha, Escolha]:
        jogador1 = self.entrada_usuario(1)
        jogador2 = self.entrada_usuario(2)
    
        return jogador1, jogador2

    def entrada_usuario(self, jogador: int):
        while True:
            entrada = input(f"Jogador {jogador}, escolha: pedra, papel ou tesoura: ")
            try:
                return Escolha(entrada.strip().lower())
            except ValueError:
                print("Escolha inválida! Escolha entre: pedra, papel ou tesoura.")
