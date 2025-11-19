//// Projeto: Bem-Estar no Trabalho - IoT com ESP32 e FIWARE
// Mantém base da Vinharia Agnello com adições de MQ-2, LEDs e botão de controle

#include <WiFi.h>          // Biblioteca para conexão Wi-Fi
#include <PubSubClient.h>  // Biblioteca MQTT
#include "DHT.h"           // Biblioteca do sensor DHT22

// ===================== DEFINIÇÃO DE PINOS =====================
#define DHT_PIN 15       // Pino do sensor DHT22
#define LDR_PIN 35       // Pino do LDR
#define GAS_PIN 34       // Pino do MQ-2
#define BUZZER_PIN 23    // Pino do buzzer
#define BUTTON_PIN 25    // Botão para ativar/desativar sistema

// LEDs individuais por sensor
#define LED_TEMP 12      // Laranja - temperatura
#define LED_HUM 14       // Azul - umidade
#define LED_LUM 19       // Amarelo - luminosidade
#define LED_GAS 21       // Branco - gás
#define LED_PURPLE 18    // Roxo - indica sistema ativo
#define LED_AZUL 2       // LED onboard - controle via FIWARE

#define DHTTYPE DHT22    // Tipo do DHT
DHT dhtSensor(DHT_PIN, DHTTYPE);  // Instância do sensor

// ===================== CONFIGURAÇÃO DE REDE =====================
const char* WIFI_NAME = "Wokwi-GUEST";    // Rede Wi-Fi
const char* WIFI_PASSWORD = "";           // Senha
const char* mqtt_server = "20.116.216.196";  // Servidor MQTT (IoT Agent)
const int mqtt_port = 1883;                  // Porta MQTT
const char* mqtt_client_id = "esp32_001";    // ID do dispositivo
const char* mqtt_username = "TEF";           // Usuário
const char* mqtt_password = "";              // Senha MQTT
const char* mqtt_topic = "/TEF/esp32_001/attrs"; // Tópico de envio

WiFiClient espClient;
PubSubClient client(espClient);

// ===================== FAIXAS IDEAIS =====================
// Limites definidos pelo projeto (ambiente de bem-estar)
float tempMin = 21.0, tempMax = 24.0;
float humMin = 45.0, humMax = 60.0;
float lumMin = 40.0, lumMax = 60.0;

float gasIdeal = 300.0;
float gasModerado = 1000.0;

// ===================== VARIÁVEIS DE CONTROLE =====================
bool sistemaAtivo = false;     // Se o sistema de alertas está ligado
bool botaoPressionado = false; // Antirruído do botão
unsigned long tempoUltimoClique = 0;

unsigned long ultimoEnvio = 0; // Controle do envio ao FIWARE
unsigned long intervaloEnvio = 6000;

uint16_t gasBaseline = 0;      // Base para MQ-2
float gasPPM_ema = 0.0f;       // Filtro EMA (suavização)
const float GAS_EMA_ALPHA = 0.2;

// ===================== CALLBACK MQTT =====================
// Recebe comandos do IoT Agent (liga/desliga LED)
void callback(char* topic, byte* payload, unsigned int length) {
  String msg;
  for (unsigned int i = 0; i < length; i++) msg += (char)payload[i];

  msg.toLowerCase();

  // Comando → liga LED AZUL
  if (msg.indexOf("led") >= 0 && msg.indexOf("on") >= 0) {
    digitalWrite(LED_AZUL, HIGH);
    Serial.println("💡 LED Azul LIGADO via FIWARE!");
  }
  // Comando → desliga LED AZUL
  else if (msg.indexOf("led") >= 0 && msg.indexOf("off") >= 0) {
    digitalWrite(LED_AZUL, LOW);
    Serial.println("💡 LED Azul DESLIGADO via FIWARE!");
  }

  // Envia ao IoT Agent uma confirmação de execução
  client.publish("/TEF/esp32_001/cmdexe", msg.c_str());
}

// ===================== CONEXÃO Wi-Fi =====================
void conectarWiFi() {
  Serial.print("🔌 Conectando ao Wi-Fi...");
  WiFi.begin(WIFI_NAME, WIFI_PASSWORD);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500); Serial.print(".");
  }

  Serial.println("\n✅ Wi-Fi conectado!");
  Serial.print("IP local: ");
  Serial.println(WiFi.localIP());
}

// ===================== CONEXÃO MQTT =====================
void conectarMQTT() {
  while (!client.connected()) {
    Serial.print("🔗 Conectando ao IoT Agent MQTT...");

    if (client.connect(mqtt_client_id, mqtt_username, mqtt_password)) {
      Serial.println("✅ Conectado!");
      client.subscribe("/TEF/esp32_001/cmd"); // Recebe comandos
    } else {
      delay(2000);
    }
  }
}

// ===================== BOTÃO =====================
// Liga / Desliga o sistema de alertas
void checarBotao() {
  bool estadoBotao = digitalRead(BUTTON_PIN);

  // Quando pressionado
  if (estadoBotao == LOW && !botaoPressionado && (millis() - tempoUltimoClique > 250)) {
    botaoPressionado = true;
    tempoUltimoClique = millis();

    sistemaAtivo = !sistemaAtivo; // Alterna estado
    digitalWrite(LED_PURPLE, sistemaAtivo ? HIGH : LOW);

    if (!sistemaAtivo) noTone(BUZZER_PIN);

    Serial.println(sistemaAtivo ? "🔊 Sistema ATIVADO" : "🔇 Sistema DESATIVADO");
  }

  if (estadoBotao == HIGH) botaoPressionado = false;
}

// ===================== CONTROLE DE LEDS =====================
// Função de piscar individual controlando cada LED
void piscarLed(int ledPin, int intervalo) {
  static unsigned long ultimoTempoTemp = 0;
  static unsigned long ultimoTempoHum = 0;
  static unsigned long ultimoTempoLum = 0;
  static unsigned long ultimoTempoGas = 0;

  static bool estadoTemp = false;
  static bool estadoHum = false;
  static bool estadoLum = false;
  static bool estadoGas = false;

  unsigned long agora = millis();

  // Controle independente para cada LED
  if (ledPin == LED_TEMP) {
    if (agora - ultimoTempoTemp >= intervalo) {
      ultimoTempoTemp = agora;
      estadoTemp = !estadoTemp;
      digitalWrite(LED_TEMP, estadoTemp);
    }
  }

  if (ledPin == LED_HUM) {
    if (agora - ultimoTempoHum >= intervalo) {
      ultimoTempoHum = agora;
      estadoHum = !estadoHum;
      digitalWrite(LED_HUM, estadoHum);
    }
  }

  if (ledPin == LED_LUM) {
    if (agora - ultimoTempoLum >= intervalo) {
      ultimoTempoLum = agora;
      estadoLum = !estadoLum;
      digitalWrite(LED_LUM, estadoLum);
    }
  }

  if (ledPin == LED_GAS) {
    if (agora - ultimoTempoGas >= intervalo) {
      ultimoTempoGas = agora;
      estadoGas = !estadoGas;
      digitalWrite(LED_GAS, estadoGas);
    }
  }
}

// Decide qual comportamento o LED deve ter
void atualizarLedSensor(int ledPin, bool ideal, bool moderado, bool critico) {
  if (ideal) {
    digitalWrite(ledPin, LOW);   // Desligado = ideal
  }
  else if (moderado) {
    piscarLed(ledPin, 200);      // Piscar rápido = moderado
  }
  else if (critico) {
    digitalWrite(ledPin, HIGH);  // Acende forte = crítico
  }
}

// ===================== MQ-2 (CORREÇÃO DO ZERO) =====================
// Média de várias leituras brutas do ADC
uint16_t readADCavg(uint8_t pin, uint16_t samples = 10) {
  uint32_t acc = 0;
  for (uint16_t i = 0; i < samples; i++) {
    acc += analogRead(pin);
    delay(2);
  }
  return acc / samples;
}

// Conversão de ADC → PPM usando baseline e suavização
float gasADCtoPPM(uint16_t adc) {
  int32_t delta = adc - gasBaseline;

  if (delta < 5) delta = 5;

  uint16_t span = max<uint16_t>(1, 4095 - gasBaseline);

  float ppm = delta * (5000.0f / (float)span);

  // Suavização exponencial
  if (gasPPM_ema <= 0.01f) gasPPM_ema = ppm;
  else gasPPM_ema = GAS_EMA_ALPHA * ppm + (1 - GAS_EMA_ALPHA) * gasPPM_ema;

  return gasPPM_ema;
}

// ===================== SETUP =====================
void setup() {
  Serial.begin(115200);
  dhtSensor.begin();

  // Define pinos como entrada/saída
  pinMode(LDR_PIN, INPUT);
  pinMode(GAS_PIN, INPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(LED_TEMP, OUTPUT);
  pinMode(LED_HUM, OUTPUT);
  pinMode(LED_LUM, OUTPUT);
  pinMode(LED_GAS, OUTPUT);
  pinMode(LED_PURPLE, OUTPUT);
  pinMode(LED_AZUL, OUTPUT);

  conectarWiFi();
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
  conectarMQTT();

  // Calibração do MQ-2
  Serial.println("🧪 Calibrando MQ-2 (2s) — mantenha o ar limpo...");
  delay(250);

  uint32_t acc = 0;
  for (int i = 0; i < 200; i++) {
    acc += analogRead(GAS_PIN);
    delay(10);
  }

  gasBaseline = acc / 200;
  if (gasBaseline > 4000) gasBaseline = 4000;

  Serial.print("✅ Baseline MQ-2: ");
  Serial.println(gasBaseline);
}

// ===================== LOOP =====================
void loop() {
  if (!client.connected()) conectarMQTT();
  client.loop();
  checarBotao();

  // ======= Leitura dos sensores =======
  float temperature = dhtSensor.readTemperature();
  float humidity = dhtSensor.readHumidity();
  int ldrRaw = analogRead(LDR_PIN);

  // Converte LDR → luminosidade (%)
  float luminosity = map(ldrRaw, 0, 4095, 100, 0);

  int gasADC = readADCavg(GAS_PIN);
  float gasPPM = gasADCtoPPM(gasADC);

  // ======= CLASSIFICAÇÕES =======

  // TEMPERATURA
  bool tempIdeal = (temperature >= 21 && temperature <= 24);
  bool tempModerado = (temperature > 24 && temperature <= 27);
  bool tempCri­tico = (temperature < 18 || temperature > 27);

  // UMIDADE
  bool humIdeal = (humidity >= 45 && humidity <= 60);
  bool humModerado = (humidity >= 35 && humidity < 45) || (humidity > 60 && humidity <= 70);
  bool humCritico = (humidity < 35 || humidity > 70);

  // LUMINOSIDADE
  bool lumIdeal = (luminosity >= 40 && luminosity <= 60);
  bool lumModerado = (luminosity >= 25 && luminosity < 40) || (luminosity > 60 && luminosity <= 75);
  bool lumCritico = (luminosity < 25 || luminosity > 75);

  // GÁS
  bool gasIdealNivel = (gasPPM <= 300);
  bool gasModeradoNivel = (gasPPM > 300 && gasPPM <= 1000);
  bool gasCritico = (gasPPM > 1000);

  // ======= LEDS =======
  atualizarLedSensor(LED_TEMP, tempIdeal, tempModerado, tempCri­tico);
  atualizarLedSensor(LED_HUM, humIdeal, humModerado, humCritico);
  atualizarLedSensor(LED_LUM, lumIdeal, lumModerado, lumCritico);
  atualizarLedSensor(LED_GAS, gasIdealNivel, gasModeradoNivel, gasCritico);

  // ======= BUZZER =======
  if (sistemaAtivo) {
    if (tempCri­tico || humCritico || lumCritico || gasCritico)
      tone(BUZZER_PIN, 1500);  // Som forte
    else if (tempModerado || humModerado || lumModerado || gasModeradoNivel)
      tone(BUZZER_PIN, 800);   // Som moderado
    else
      noTone(BUZZER_PIN);
  } else {
    noTone(BUZZER_PIN);
  }

  // ======= ENVIO AO FIWARE =======
  if (millis() - ultimoEnvio < intervaloEnvio) return;
  ultimoEnvio = millis();

  String payload = "t|" + String(temperature, 2) +
                   "|h|" + String(humidity, 1) +
                   "|l|" + String(luminosity, 1) +
                   "|gppm|" + String(gasPPM, 0) +
                   "|b|" + String(digitalRead(LED_PURPLE) == HIGH ? "on" : "off");

  client.publish(mqtt_topic, payload.c_str());

  // ======= LOG NO SERIAL =======
  Serial.println("============================");
  Serial.println("🌡 Temp: " + String(temperature, 2));
  Serial.println("💧 Umidade: " + String(humidity, 1));
  Serial.println("💡 Luminosidade: " + String(luminosity, 1));
  Serial.println("🌫 Gás MQ-2: " + String(gasPPM, 0));
  Serial.println("🔘 Sistema ativo: " + String(sistemaAtivo ? "Sim" : "Não"));
}
