// Programa para el receptor de un sistema de comunicación inalambrica 
#include <SPI.h>  //Incluye libreria SPI para comunicarse con dispositivos externos utilizando el protocolo SPI.
#include <RF24.h> // Incluye la biblioteca RF24, se utiliza para la comunicación inalámbrica utilizando módulos de radio NRF24L01. 

RF24 radio(10, 8); // Define los puertos CE pin 10, CSN pin 8
const byte address[6] = "00001"; // Define una constante tipo byte ("address") que tiene la secuencia "00001".

float ALTITUD, AcX, AcY, AcZ, GyX, GyY, GyZ, TEMPERATURA; // Declara datos de tipo decimal 

void setup() 
{
  Serial.begin(9600); // Inicializa la comunicación con una velocidad de transmisión de datos de 9600 baudios.
  radio.begin(); // Inicializa el módulo de radiofrecuencia.
  radio.openReadingPipe(0, address); // Toma dos parametros, 0 y la dirección de destino 
  radio.setChannel(101); // Configura el canal 101 (2501 MHz) como canal de comunicación (Mismo canal en ambos casos TX y RX)
  radio.setDataRate(RF24_250KBPS); // Establece la tasa de datos de la comunicación (250K, 1M, 2M)
  radio.setPALevel(RF24_PA_MAX); // Establece nivel de potencia del modulo (MAX, MIN, HIGH, LOW)
  radio.startListening();// Pone el modulo en modo escucha, en este momento puede recibir los datos del TX 
}

void loop()
{
  if (radio.available())     
  {  
    float datos[8]; // Arreglo con 8 elementos de tipo float (número decimal)
    radio.read(datos, sizeof(datos)); // Lee los datos del objeto radio creado anteriormente, y los almacena en el arreglo datos
    ALTITUD = datos[0];
    AcX = datos[1];
    AcY = datos[2];
    AcZ = datos[3];
    GyX = datos[4];
    GyY = datos[5];
    GyZ = datos[6];
    TEMPERATURA = datos[7];

    Serial.print(ALTITUD); // Imprime los valores a traves del puerto serial
    Serial.print(",");
    Serial.print(AcX); // Imprime el valor de la aceleración a traves del puerto serial
    Serial.print(",");
    Serial.print(AcY);
    Serial.print(",");
    Serial.print(AcZ);
    Serial.print(",");
    Serial.print(GyX);
    Serial.print(",");
    Serial.print(GyY);
    Serial.print(",");
    Serial.print(GyZ);
    Serial.print(",");
    Serial.println(TEMPERATURA); 
  }
  delay(10);
}
