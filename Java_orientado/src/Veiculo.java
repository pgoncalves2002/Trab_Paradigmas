public class Veiculo {
    private String placa;
    private String tipo; // "P" ou "G"
    private int horaEntrada;
    private int minutoEntrada;

    public Veiculo(String placa, String tipo, int horaEntrada, int minutoEntrada) {
        this.placa = placa;
        this.tipo = tipo;
        this.horaEntrada = horaEntrada;
        this.minutoEntrada = minutoEntrada;
    }

    public String getPlaca() {
        return placa;
    }

    public String getTipo() {
        return tipo;
    }

    public int getHoraEntrada() {
        return horaEntrada;
    }

    public int getMinutoEntrada() {
        return minutoEntrada;
    }

    public int getMinutosEntradaTotal() {
        return horaEntrada * 60 + minutoEntrada;
    }
}
