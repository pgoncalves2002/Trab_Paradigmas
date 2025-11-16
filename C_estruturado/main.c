#include <stdio.h>
#include <string.h>
#include <time.h>

#define MAX_VAGAS 10
#define TAM_PLACA 10
#define TARIFA_HORA 5.0

// 1 = usar hora/minuto atual automaticamente
// 0 = perguntar HH:MM ao usuário
#define MODO_HORA_ENTRADA 1
#define MODO_HORA_SAIDA   1

// Tempo de tolerância em minutos
#define TOLERANCIA_MINUTOS 15

char placas[MAX_VAGAS][TAM_PLACA];
char tipos[MAX_VAGAS];
int horaEntrada[MAX_VAGAS];
int minutoEntrada[MAX_VAGAS];
int ocupada[MAX_VAGAS];

void inicializar() {
    for (int i = 0; i < MAX_VAGAS; i++) {
        ocupada[i] = 0;
    }
}

// Obtém hora e minuto atuais do sistema
void obterHoraAtual(int *hora, int *minuto) {
    time_t agora;
    struct tm *infoTempo;

    time(&agora);
    infoTempo = localtime(&agora);

    *hora = infoTempo->tm_hour;
    *minuto = infoTempo->tm_min;
}

int encontrarVagaLivre() {
    for (int i = 0; i < MAX_VAGAS; i++) {
        if (!ocupada[i]) {
            return i;
        }
    }
    return -1;
}

void registrarEntrada() {
    int vaga = encontrarVagaLivre();
    if (vaga == -1) {
        printf("Estacionamento lotado!\n");
        return;
    }

    printf("Placa: ");
    scanf("%9s", placas[vaga]);

    printf("Tipo (P/G): ");
    scanf(" %c", &tipos[vaga]);

    int hora, minuto;

    if (MODO_HORA_ENTRADA == 1) {
        obterHoraAtual(&hora, &minuto);
        printf("Entrada automática: %02dh%02d\n", hora, minuto);
    } else {
        printf("Hora de entrada (HH:MM): ");
        scanf("%d:%d", &hora, &minuto);
    }

    horaEntrada[vaga] = hora;
    minutoEntrada[vaga] = minuto;
    ocupada[vaga] = 1;

    printf("Veículo estacionado na vaga %d\n", vaga + 1);
}

void registrarSaida() {
    int numVaga;
    printf("Número da vaga para saída: ");
    if (scanf("%d", &numVaga) != 1) {
        printf("Entrada inválida.\n");
        return;
    }

    int vaga = numVaga - 1;

    if (vaga < 0 || vaga >= MAX_VAGAS || !ocupada[vaga]) {
        printf("Vaga inválida ou vazia.\n");
        return;
    }

    int horaSaida, minutoSaida;

    if (MODO_HORA_SAIDA == 1) {
        obterHoraAtual(&horaSaida, &minutoSaida);
        printf("Saída automática: %02dh%02d\n", horaSaida, minutoSaida);
    } else {
        printf("Hora de saída (HH:MM): ");
        scanf("%d:%d", &horaSaida, &minutoSaida);
    }

    int entradaMin = horaEntrada[vaga] * 60 + minutoEntrada[vaga];
    int saidaMin   = horaSaida * 60 + minutoSaida;
    int tempoMin   = saidaMin - entradaMin;

    if (tempoMin < 0) {
        // caso raro (mudança de dia etc.), garante algo não negativo
        tempoMin = 0;
    }

    // REGRA DE TOLERÂNCIA:
    // até TOLERANCIA_MINUTOS -> grátis
    // ultrapassou -> ignora tolerância e cobra tudo
    if (tempoMin <= TOLERANCIA_MINUTOS) {
        printf("\nTempo total: %d min — dentro da tolerância de %d min.\n",
               tempoMin, TOLERANCIA_MINUTOS);
        printf("Cliente não paga.\n");
        ocupada[vaga] = 0;
        return;
    }

    // Se passou da tolerância, usa tempoMin completo (sem desconto)
    int horasCobradas = tempoMin / 60;
    if (tempoMin % 60 != 0) {
        horasCobradas++;  // arredonda pra cima
    }

    if (horasCobradas < 1) {
        horasCobradas = 1; // garantia: mínimo 1 hora cobrada
    }

    float valor = horasCobradas * TARIFA_HORA;

    printf("\nPlaca %s saiu da vaga %d.\n", placas[vaga], vaga + 1);
    printf("Tempo total: %d h %d min\n", tempoMin / 60, tempoMin % 60);
    printf("Horas cobradas: %d\n", horasCobradas);
    printf("Valor a pagar: R$ %.2f\n", valor);

    ocupada[vaga] = 0;
}

void listarOcupadas() {
    printf("Vagas ocupadas:\n");

    for (int i = 0; i < MAX_VAGAS; i++) {
        if (ocupada[i]) {
            printf("Vaga %d - Placa: %s - Tipo: %c - Entrada: %02dh%02d",
                   i + 1,
                   placas[i],
                   tipos[i],
                   horaEntrada[i],
                   minutoEntrada[i]);

            // Se horários são automáticos, mostra tempo de permanência atual
            if (MODO_HORA_ENTRADA == 1 && MODO_HORA_SAIDA == 1) {
                int horaAtual, minutoAtual;
                obterHoraAtual(&horaAtual, &minutoAtual);

                int entradaMin = horaEntrada[i] * 60 + minutoEntrada[i];
                int agoraMin   = horaAtual * 60 + minutoAtual;

                int tempoMin = agoraMin - entradaMin;
                if (tempoMin < 0) tempoMin = 0;

                printf(" | Permanência: %d h %d min",
                       tempoMin / 60, tempoMin % 60);
            }

            printf("\n");
        }
    }
}

void mostrarStatus() {
    int livres = 0;
    for (int i = 0; i < MAX_VAGAS; i++) {
        if (!ocupada[i]) {
            livres++;
        }
    }

    printf("Total de vagas: %d\n", MAX_VAGAS);
    printf("Vagas livres: %d\n", livres);
    printf("Vagas ocupadas: %d\n", MAX_VAGAS - livres);
}

int main() {
    int op;
    inicializar();

    do {
        printf("\n=== MENU ESTACIONAMENTO ===\n");
        printf("1 - Registrar entrada\n");
        printf("2 - Registrar saída\n");
        printf("3 - Listar vagas ocupadas\n");
        printf("4 - Mostrar status geral\n");
        printf("0 - Sair\n");
        printf("Opção: ");
        if (scanf("%d", &op) != 1) {
            printf("Entrada inválida.\n");
            break;
        }

        switch (op) {
            case 1:
                registrarEntrada();
                break;
            case 2:
                registrarSaida();
                break;
            case 3:
                listarOcupadas();
                break;
            case 4:
                mostrarStatus();
                break;
            case 0:
                printf("Encerrando...\n");
                break;
            default:
                printf("Opção inválida.\n");
        }

    } while (op != 0);

    return 0;
}
