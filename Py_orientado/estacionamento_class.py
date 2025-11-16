from datetime import datetime
from veiculo import Veiculo

MODO_HORA_ENTRADA = 1
MODO_HORA_SAIDA = 1
TOLERANCIA_MINUTOS = 15
TARIFA_HORA = 5.0
MAX_VAGAS = 10

class Estacionamento:
    def __init__(self):
        self.vagas = [None] * MAX_VAGAS

    def obter_hora_atual(self):
        agora = datetime.now()
        return agora.hour, agora.minute

    def encontrar_vaga_livre(self):
        for i in range(MAX_VAGAS):
            if self.vagas[i] is None:
                return i
        return -1

    def registrar_entrada(self, placa, tipo):
        vaga = self.encontrar_vaga_livre()
        if vaga == -1:
            return None

        if MODO_HORA_ENTRADA == 1:
            h, m = self.obter_hora_atual()
        else:
            return "manual_time_needed"

        self.vagas[vaga] = Veiculo(placa, tipo, h, m)
        return vaga

    def registrar_saida(self, vaga_idx):
        veiculo = self.vagas[vaga_idx]
        if veiculo is None:
            return None

        if MODO_HORA_SAIDA == 1:
            h_saida, m_saida = self.obter_hora_atual()
        else:
            return "manual_time_needed"

        entrada_min = veiculo.get_minutos_entrada()
        saida_min = h_saida * 60 + m_saida
        tempo_min = saida_min - entrada_min

        if tempo_min <= TOLERANCIA_MINUTOS:
            self.vagas[vaga_idx] = None
            return {"gratis": True}

        horas = tempo_min // 60
        if tempo_min % 60 != 0:
            horas += 1
        if horas < 1:
            horas = 1

        valor = horas * TARIFA_HORA

        self.vagas[vaga_idx] = None

        return {
            "gratis": False,
            "horas": horas,
            "valor": valor,
            "tempo_h": tempo_min // 60,
            "tempo_m": tempo_min % 60
        }

    def listar_ocupadas(self):
        lista = []
        for i, v in enumerate(self.vagas):
            if v is not None:
                info = {
                    "vaga": i + 1,
                    "placa": v.placa,
                    "tipo": v.tipo,
                    "hora": v.hora_entrada,
                    "minuto": v.minuto_entrada
                }
                if MODO_HORA_ENTRADA == 1 and MODO_HORA_SAIDA == 1:
                    h_atual, m_atual = self.obter_hora_atual()
                    entrada_min = v.get_minutos_entrada()
                    atual_min = h_atual * 60 + m_atual
                    tempo = max(0, atual_min - entrada_min)
                    info["tempo_h"] = tempo // 60
                    info["tempo_m"] = tempo % 60
                lista.append(info)
        return lista
