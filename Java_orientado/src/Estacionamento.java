import java.time.LocalTime;
import java.util.Scanner;

public class Estacionamento {

    private static final int MAX_VAGAS = 1;
    private static final double TARIFA_HORA = 5.0;

    // 1 = usar hora/minuto atual automaticamente
    // 0 = perguntar HH:MM ao usuário
    private static final int MODO_HORA_ENTRADA = 1;
    private static final int MODO_HORA_SAIDA   = 1;

    // Tempo de tolerância em minutos
    private static final int TOLERANCIA_MINUTOS = 15;

    private Veiculo[] vagas;
    private Scanner sc;

    public Estacionamento() {
        this.vagas = new Veiculo[MAX_VAGAS];
        this.sc = new Scanner(System.in);
    }

    private void obterHoraAtual(int[] horaMinuto) {
        LocalTime agora = LocalTime.now();
        horaMinuto[0] = agora.getHour();
        horaMinuto[1] = agora.getMinute();
    }

    private int encontrarVagaLivre() {
        for (int i = 0; i < MAX_VAGAS; i++) {
            if (vagas[i] == null) {
                return i;
            }
        }
        return -1;
    }

    public void registrarEntrada() {
        int vaga = encontrarVagaLivre();
        if (vaga == -1) {
            System.out.println("Estacionamento lotado!");
            return;
        }

        System.out.print("Placa: ");
        String placa = sc.nextLine().trim();
        if (placa.isEmpty()) {
            placa = sc.nextLine().trim(); // caso tenha sobrado \n
        }

        System.out.print("Tipo (P/G): ");
        String tipo = sc.nextLine().trim().toUpperCase();
        if (tipo.isEmpty()) {
            tipo = "P";
        } else {
            tipo = tipo.substring(0, 1);
        }

        int hora, minuto;

        if (MODO_HORA_ENTRADA == 1) {
            int[] hm = new int[2];
            obterHoraAtual(hm);
            hora = hm[0];
            minuto = hm[1];
            System.out.printf("Entrada automática: %02dh%02d%n", hora, minuto);
        } else {
            System.out.print("Hora de entrada (HH:MM): ");
            String horario = sc.nextLine().trim();
            try {
                String[] partes = horario.split(":");
                hora = Integer.parseInt(partes[0]);
                minuto = Integer.parseInt(partes[1]);
            } catch (Exception e) {
                System.out.println("Formato inválido. Use HH:MM.");
                return;
            }
        }

        vagas[vaga] = new Veiculo(placa, tipo, hora, minuto);
        System.out.println("Veículo estacionado na vaga " + (vaga + 1));
    }

    public void registrarSaida() {
        System.out.print("Número da vaga para saída: ");
        int numVaga;
        try {
            numVaga = Integer.parseInt(sc.nextLine());
        } catch (NumberFormatException e) {
            System.out.println("Entrada inválida.");
            return;
        }

        int idx = numVaga - 1;

        if (idx < 0 || idx >= MAX_VAGAS || vagas[idx] == null) {
            System.out.println("Vaga inválida ou vazia.");
            return;
        }

        Veiculo v = vagas[idx];

        int horaSaida, minutoSaida;

        if (MODO_HORA_SAIDA == 1) {
            int[] hm = new int[2];
            obterHoraAtual(hm);
            horaSaida = hm[0];
            minutoSaida = hm[1];
            System.out.printf("Saída automática: %02dh%02d%n", horaSaida, minutoSaida);
        } else {
            System.out.print("Hora de saída (HH:MM): ");
            String horario = sc.nextLine().trim();
            try {
                String[] partes = horario.split(":");
                horaSaida = Integer.parseInt(partes[0]);
                minutoSaida = Integer.parseInt(partes[1]);
            } catch (Exception e) {
                System.out.println("Formato inválido. Use HH:MM.");
                return;
            }
        }

        int entradaMin = v.getMinutosEntradaTotal();
        int saidaMin   = horaSaida * 60 + minutoSaida;
        int tempoMin   = saidaMin - entradaMin;

        if (tempoMin < 0) {
            tempoMin = 0;
        }

        // Regra da tolerância:
        // até TOLERANCIA_MINUTOS -> grátis
        // passou -> cobra tudo, sem desconto
        if (tempoMin <= TOLERANCIA_MINUTOS) {
            System.out.printf("%nTempo total: %d min — dentro da tolerância de %d min.%n",
                    tempoMin, TOLERANCIA_MINUTOS);
            System.out.println("Cliente não paga.");
            vagas[idx] = null;
            return;
        }

        int horasCobradas = tempoMin / 60;
        if (tempoMin % 60 != 0) {
            horasCobradas++;
        }
        if (horasCobradas < 1) {
            horasCobradas = 1;
        }

        double valor = horasCobradas * TARIFA_HORA;

        System.out.printf("%nPlaca %s saiu da vaga %d.%n", v.getPlaca(), idx + 1);
        System.out.printf("Tempo total: %d h %d min%n", tempoMin / 60, tempoMin % 60);
        System.out.println("Horas cobradas: " + horasCobradas);
        System.out.printf("Valor a pagar: R$ %.2f%n", valor);

        vagas[idx] = null;
    }

    public void listarOcupadas() {
        System.out.println("Vagas ocupadas:");
        boolean alguma = false;

        for (int i = 0; i < MAX_VAGAS; i++) {
            Veiculo v = vagas[i];
            if (v != null) {
                alguma = true;
                System.out.printf("Vaga %d - Placa: %s - Tipo: %s - Entrada: %02dh%02d",
                        i + 1,
                        v.getPlaca(),
                        v.getTipo(),
                        v.getHoraEntrada(),
                        v.getMinutoEntrada()
                );

                // Se horários são automáticos, mostra permanência atual
                if (MODO_HORA_ENTRADA == 1 && MODO_HORA_SAIDA == 1) {
                    int[] hm = new int[2];
                    obterHoraAtual(hm);
                    int agoraMin = hm[0] * 60 + hm[1];
                    int entradaMin = v.getMinutosEntradaTotal();
                    int tempoMin = agoraMin - entradaMin;
                    if (tempoMin < 0) tempoMin = 0;
                    System.out.printf(" | Permanência: %d h %d min",
                            tempoMin / 60, tempoMin % 60);
                }

                System.out.println();
            }
        }

        if (!alguma) {
            System.out.println("Nenhuma vaga ocupada.");
        }
    }

    public void mostrarStatus() {
        int livres = 0;
        for (Veiculo v : vagas) {
            if (v == null) livres++;
        }
        System.out.println("Total de vagas: " + MAX_VAGAS);
        System.out.println("Vagas livres: " + livres);
        System.out.println("Vagas ocupadas: " + (MAX_VAGAS - livres));
    }
}
