class Veiculo:
    def __init__(self, placa, tipo, hora, minuto):
        self.placa = placa
        self.tipo = tipo
        self.hora_entrada = hora
        self.minuto_entrada = minuto

    def get_minutos_entrada(self):
        return self.hora_entrada * 60 + self.minuto_entrada
