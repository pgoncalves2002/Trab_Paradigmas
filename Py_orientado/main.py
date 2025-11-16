from estacionamento_class import Estacionamento

def main():
    est = Estacionamento()

    while True:
        print("\n=== MENU ESTACIONAMENTO ===")
        print("1 - Registrar entrada")
        print("2 - Registrar saída")
        print("3 - Listar vagas ocupadas")
        print("0 - Sair")
        op = input("Opção: ")

        if op == "1":
            placa = input("Placa: ")
            tipo = input("Tipo (P/G): ")
            vaga = est.registrar_entrada(placa, tipo)
            if vaga == "manual_time_needed":
                print("Este modo exige horário manual (não implementado aqui)")
            elif vaga is None:
                print("Estacionamento cheio")
            else:
                print(f"Veículo estacionado na vaga {vaga + 1}")

        elif op == "2":
            vaga = int(input("Número da vaga: ")) - 1
            info = est.registrar_saida(vaga)
            if info is None:
                print("Vaga vazia")
            elif info == "manual_time_needed":
                print("Modo exige horário manual")
            elif info["gratis"]:
                print("Dentro da tolerância — cliente não paga")
            else:
                print(f"Tempo total: {info['tempo_h']}h {info['tempo_m']}min")
                print(f"Horas cobradas: {info['horas']}")
                print(f"Valor: R$ {info['valor']:.2f}")

        elif op == "3":
            lista = est.listar_ocupadas()
            if not lista:
                print("Nenhuma vaga ocupada.")
            else:
                for v in lista:
                    linha = f"Vaga {v['vaga']} - Placa {v['placa']} - Tipo {v['tipo']} - Entrada {v['hora']:02d}h{v['minuto']:02d}"
                    if 'tempo_h' in v:
                        linha += f" | Permanência: {v['tempo_h']}h {v['tempo_m']}min"
                    print(linha)

        elif op == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()