#include <avr/io.h>
#include <util/delay.h>

int main() {
    // Configurar los pines del PORTB del 1 al 5 como salidas
    DDRB |= 0b00111110;

    while (1) {
        for (uint8_t i = PB1; i <= PB5; i++) {
            // Encender el LED correspondiente
            PORTB |= (1 << i);
            // Esperar un momento
            _delay_ms(500);
            // Apagar el LED correspondiente
            PORTB &= ~(1 << i);
        }
    }

    return 0;
}