from datetime import datetime
import math

# Configurações
MAX_VAGAS = 10
TARIFA_HORA = 5.0

# 1 = usar hora/minuto atual automaticamente
# 0 = perguntar HH:MM ao usuário
MODO_HORA_ENTRADA = 1
MODO_HORA_SAIDA = 1

# Tempo de tolerância em minutos
TOLERANCIA_MINUTOS = 15

# Estruturas de dados
placas = [None] * MAX_VAGAS
tipos = [None] * MAX_VAGAS
hora_entrada = [0] * MAX_VAGAS
minuto_entrada = [0] * MAX_VAGAS
ocupada = [False] * MAX_VAGAS


def inicializar():
    """Marca todas as vagas como livres."""
    for i in range(MAX_VAGAS):
        ocupada[i] = False


def obter_hora_atual():
    """Retorna hora e minuto atuais do sistema."""
    agora = datetime.now()
    return agora.hour, agora.minute


def encontrar_vaga_livre():
    """Retorna o índice da primeira vaga livre ou -1 se estiver lotado."""
    for i in range(MAX_VAGAS):
        if not ocupada[i]:
            return i
    return -1


def registrar_entrada():
    vaga = encontrar_vaga_livre()
    if vaga == -1:
        print("Estacionamento lotado!")
        return

    placa = input("Placa: ").strip()
    tipo = input("Tipo (P/G): ").strip().upper()[:1]

    if MODO_HORA_ENTRADA == 1:
        h, m = obter_hora_atual()
        print(f"Entrada automática: {h:02d}h{m:02d}")
    else:
        horario = input("Hora de entrada (HH:MM): ").strip()
        try:
            h_str, m_str = horario.split(":")
            h = int(h_str)
            m = int(m_str)
        except ValueError:
            print("Formato inválido. Use HH:MM.")
            return

    placas[vaga] = placa
    tipos[vaga] = tipo
    hora_entrada[vaga] = h
    minuto_entrada[vaga] = m
    ocupada[vaga] = True

    print(f"Veículo estacionado na vaga {vaga + 1}")


def registrar_saida():
    try:
        num_vaga = int(input("Número da vaga para saída: "))
    except ValueError:
        print("Entrada inválida.")
        return

    vaga = num_vaga - 1

    if vaga < 0 or vaga >= MAX_VAGAS or not ocupada[vaga]:
        print("Vaga inválida ou vazia.")
        return

    if MODO_HORA_SAIDA == 1:
        h_saida, m_saida = obter_hora_atual()
        print(f"Saída automática: {h_saida:02d}h{m_saida:02d}")
    else:
        horario = input("Hora de saída (HH:MM): ").strip()
        try:
            h_str, m_str = horario.split(":")
            h_saida = int(h_str)
            m_saida = int(m_str)
        except ValueError:
            print("Formato inválido. Use HH:MM.")
            return

    entrada_min = hora_entrada[vaga] * 60 + minuto_entrada[vaga]
    saida_min = h_saida * 60 + m_saida
    tempo_min = saida_min - entrada_min

    if tempo_min < 0:
        tempo_min = 0  # caso estranho (mudança de dia etc.)

    # Regra de tolerância:
    # até TOLERANCIA_MINUTOS -> grátis
    # ultrapassou -> cobra tudo, sem desconto
    if tempo_min <= TOLERANCIA_MINUTOS:
        print(f"\nTempo total: {tempo_min} min — dentro da tolerância de {TOLERANCIA_MINUTOS} min.")
        print("Cliente não paga.")
        ocupada[vaga] = False
        return

    horas_cobradas = math.ceil(tempo_min / 60)
    if horas_cobradas < 1:
        horas_cobradas = 1

    valor = horas_cobradas * TARIFA_HORA

    print(f"\nPlaca {placas[vaga]} saiu da vaga {vaga + 1}.")
    print(f"Tempo total: {tempo_min // 60} h {tempo_min % 60} min")
    print(f"Horas cobradas: {horas_cobradas}")
    print(f"Valor a pagar: R$ {valor:.2f}")

    ocupada[vaga] = False


def listar_ocupadas():
    print("Vagas ocupadas:")
    alguma = False

    for i in range(MAX_VAGAS):
        if ocupada[i]:
            alguma = True
            print(
                f"Vaga {i + 1} - Placa: {placas[i]} - Tipo: {tipos[i]} "
                f"- Entrada: {hora_entrada[i]:02d}h{minuto_entrada[i]:02d}",
                end=""
            )

            # Se ambos os modos são automáticos, mostra permanência atual
            if MODO_HORA_ENTRADA == 1 and MODO_HORA_SAIDA == 1:
                h_atual, m_atual = obter_hora_atual()
                entrada_min = hora_entrada[i] * 60 + minuto_entrada[i]
                agora_min = h_atual * 60 + m_atual
                tempo_min = agora_min - entrada_min
                if tempo_min < 0:
                    tempo_min = 0
                print(f" | Permanência: {tempo_min // 60} h {tempo_min % 60} min", end="")

            print()

    if not alguma:
        print("Nenhuma vaga está ocupada.")


def mostrar_status():
    livres = sum(1 for o in ocupada if not o)
    print(f"Total de vagas: {MAX_VAGAS}")
    print(f"Vagas livres: {livres}")
    print(f"Vagas ocupadas: {MAX_VAGAS - livres}")


def main():
    inicializar()

    while True:
        print("\n=== MENU ESTACIONAMENTO ===")
        print("1 - Registrar entrada")
        print("2 - Registrar saída")
        print("3 - Listar vagas ocupadas")
        print("4 - Mostrar status geral")
        print("0 - Sair")

        op = input("Opção: ").strip()

        if op == "1":
            registrar_entrada()
        elif op == "2":
            registrar_saida()
        elif op == "3":
            listar_ocupadas()
        elif op == "4":
            mostrar_status()
        elif op == "0":
            print("Encerrando...")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
