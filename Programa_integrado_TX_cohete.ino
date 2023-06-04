// Programa para el transmisor de un sistema de comunicación inalambrica que utiliza 2 sensores (MPU6050, BMP280)y un modulo inalambrico NRF24L01
#include <SPI.h> //Incluye libreria SPI para comunicarse con dispositivos externos utilizando el protocolo SPI.
#include <Wire.h> //Incluye libreria Wire para comunicarse con varios dispositivos el protocolo I2C
#include <Adafruit_Sensor.h> // Incluye la biblioteca Adafruit_Sensor, esta proporciona una interfaz común para leer datos de sensores.
#include <Adafruit_BMP280.h> //  Incluye la biblioteca Adafruit_BMP280, esta permite la comunicación con el sensor de presión y temperatura BMP280 
#include <RF24.h> // Incluye la biblioteca RF24, se utiliza para la comunicación inalámbrica utilizando módulos de radio NRF24L01. 

RF24 radio(10,8); // Define los puertos CE pin 10, CSN pin 8
const byte address[6] = "00001"; // Define una constante tipo byte ("address") que tiene la secuencia "00001".

Adafruit_BMP280 bmp;

float TEMPERATURA, ALTITUD;
float PRESION, P0;

const int MPU_addr=0x68;  // Direccion del sensor MPU6050 en el bus I2C
int16_t AcX,AcY,AcZ,Tmp,GyX,GyY,GyZ; // Almacena valores enteros en el rango de 16 bits 2^15= 32768, en el rango de +-32768

void setup()
{
  Serial.begin(9600);  // Inicializar la comunicación serial a 9600 baudios
  Serial.println("Iniciando...");
  Wire.begin();        // Inicializar el bus I2C
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x6B);     // PWR_MGMT_1 register
  Wire.write(0);        // Setear en 0 para activar el sensor
  Wire.endTransmission(true);

  radio.begin(); //  Inicializa el módulo de radio.
  radio.openWritingPipe(address); // Establece la dirección de escritura del módulo de radi
  radio.setChannel(101); // Configura el canal 101 (2501 MHz) como canal de comunicación (Mismo canal en ambos casos)
  radio.setDataRate(RF24_250KBPS); // Establece la tasa de datos de la comunicación (250K, 1M, 2M)
  radio.setPALevel(RF24_PA_MAX); // Establece nivel de potencia del modulo (MAX, MIN, HIGH, LOW)
  /*pinMode(7, OUTPUT); // establecer el pin del LED como salida
  digitalWrite(7, HIGH); // encender el 
  pinMode(6, OUTPUT); // establecer el pin del LED como salida
  digitalWrite(6, HIGH); // encender el LED*/

  if (!bmp.begin()){
    Serial.println("BMP280 no encontrado !");
    while (1);
  }
  P0 = bmp.readPressure()/100; // Lee la presión del BMP, la divide en 100 y almacena el resultado en P0
}

void loop()
{
  Wire.beginTransmission(MPU_addr); // Iniciar la comunicación con el MPU6050
  Wire.write(0x3B);                 // Direccion del registro donde comienza la lectura
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_addr,14,true); // Leer 14 bytes de datos

  AcX=Wire.read()<<8|Wire.read();   // Leer los valores del acelerometro
  AcY=Wire.read()<<8|Wire.read();
  AcZ=Wire.read()<<8|Wire.read();
  Tmp=Wire.read()<<8|Wire.read();   // Leer el valor de la temperatura
  GyX=Wire.read()<<8|Wire.read();   // Leer los valores del giroscopio
  GyY=Wire.read()<<8|Wire.read();
  GyZ=Wire.read()<<8|Wire.read();

  ALTITUD = bmp.readAltitude(P0);// Lee el valor de la altitud
  TEMPERATURA = bmp.readTemperature(); // Leer el valor de la temperatura

  float datos[8] = {ALTITUD, AcX, AcY, AcZ, GyX, GyY, GyZ,TEMPERATURA}; // Declara una variable "datos" como un arreglo de 8 elementos de tipo float (números decimales).
  radio.write(datos, sizeof(datos)); // Envia los datos almancenados en la variable datos a traves del objeto radio. El tamaño de los datos se determina utilizando la función "sizeof(datos)"

    Serial.print(ALTITUD); // Imprime los valores a traves del puerto serial
    Serial.print(",");
    Serial.print(AcX);
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
    Serial.println (TEMPERATURA);

delay(50); 
}
