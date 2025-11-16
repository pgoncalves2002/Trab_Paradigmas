public class Main {
    public static void main(String[] args) {
        Estacionamento est = new Estacionamento();
        java.util.Scanner sc = new java.util.Scanner(System.in);
        int op;

        do {
            System.out.println("\n=== MENU ESTACIONAMENTO ===");
            System.out.println("1 - Registrar entrada");
            System.out.println("2 - Registrar saída");
            System.out.println("3 - Listar vagas ocupadas");
            System.out.println("4 - Mostrar status geral");
            System.out.println("0 - Sair");
            System.out.print("Opção: ");

            try {
                op = Integer.parseInt(sc.nextLine());
            } catch (NumberFormatException e) {
                System.out.println("Opção inválida.");
                op = -1;
            }

            switch (op) {
                case 1:
                    est.registrarEntrada();
                    break;
                case 2:
                    est.registrarSaida();
                    break;
                case 3:
                    est.listarOcupadas();
                    break;
                case 4:
                    est.mostrarStatus();
                    break;
                case 0:
                    System.out.println("Encerrando...");
                    break;
                default:
                    System.out.println("Opção inválida.");
            }

        } while (op != 0);

        sc.close();
    }
}
