# 🏢 Projeto IoT: Bem-Estar no Trabalho

## Monitoramento Inteligente e Reativo de Conforto e Segurança Ambiental

# 💡 1. Visão Geral e Proposta de Valor

Este projeto apresenta uma solução completa de **IoT (Internet das Coisas)** com foco em **Saúde e Segurança Ocupacional (SSO)** em ambientes corporativos. A solução foi projetada para monitorar, classificar e reagir em tempo real a quatro parâmetros ambientais críticos, garantindo conforto ergonômico e a prevenção de riscos.

## 🌟 A Conexão Entre Tecnologia e Bem-Estar no Trabalho

Como um sistema IoT pode transformar ambientes corporativos e proteger a saúde das pessoas.

---

O ambiente de trabalho moderno evoluiu — não basta mais ter um local para trabalhar, é preciso ter um espaço que cumpra seu papel social, promotivo de **saúde, segurança, produtividade e qualidade de vida**. Hoje, empresas que se preocupam com o bem-estar físico e mental de seus colaboradores são exatamente as que mais prosperam.

E é nesse ponto que tecnologias como **IoT, FIWARE e sensoriamento inteligente** deixam de ser apenas ferramentas e passam a ser **agentes de transformação humana**.

## 🧠 Por que monitorar o ambiente é essencial para o bem-estar?

O ar que respiramos, a luz que incide sobre nós, a temperatura ao nosso redor — todos esses fatores criam a base invisível que molda:

* **Nosso humor**
* **Nossa capacidade cognitiva**
* **Nosso desempenho profissional**
* **Nossa saúde a longo prazo**

Controlar esses elementos manualmente é impossível. Mas monitorá-los em tempo real, automaticamente, com precisão milimétrica… é exatamente a função deste projeto.

---

## 🏢 A tecnologia como guardiã da segurança e do conforto

Ao combinar **ESP32 + sensores ambientais + FIWARE + Dashboard analítico**, o sistema atua como um **"vigia digital inteligente"**, capaz de identificar desde uma iluminação inadequada — que causa fadiga ocular — até variações de temperatura que geram desconforto, ou ainda níveis perigosos de gases que representam risco real à vida.

O projeto cria um ciclo contínuo e autônomo:

$$\text{Detecta} \rightarrow \text{Analisa} \rightarrow \text{Classifica} \rightarrow \text{Alerta} \rightarrow \text{Atua} \rightarrow \text{Envia para a Nuvem}$$

Isso significa que antes mesmo de o funcionário notar o problema, o sistema já:

* sinalizou via **LEDs** qual sensor detectou alteração;
* ajustou o nível de alerta com **buzzer** progressivo que pode ser controlado com um botão se a pessoa quiser deixar ativado ou não;
* registrou o evento no **FIWARE** via Orion;
* disponibilizou no **dashboard** gráficos completos e históricos.

É tecnologia trabalhando silenciosamente pelo bem-estar de quem está no ambiente.

---

## 🌫️ Respirar melhor é trabalhar melhor

Um dos sensores mais importantes é o **MQ-2**, responsável por detectar gases, fumaças e compostos inflamáveis.

A qualidade do ar é um fator frequentemente ignorado, mas essencial:

* Ar contaminado **reduz a concentração**.
* Partículas irritantes **prejudicam a saúde respiratória**.
* Vazamentos de gases podem gerar **acidentes graves**.

Com o MQ-2 integrado ao ESP32 e ao FIWARE, o ambiente se torna autoconsciente, capaz de alertar imediatamente quando algo foge do normal. É **prevenção ativa**, não apenas reação tardia.

---

## 💡 Luz adequada evita fadiga. Temperatura inadequada destrói produtividade.

Seu projeto não apenas monitora números — ele protege:

* O **foco**
* O **conforto térmico**
* A **saúde ocular**
* O **bem-estar emocional**

Colaboradores que trabalham em ambientes equilibrados apresentam:

* ✔ Menos estresse
* ✔ Maior motivação
* ✔ Rendimento superior
* ✔ Menos erros
* ✔ Menos afastamentos

Ou seja: **bem-estar não é custo — é investimento.**

### Parâmetros Monitorados e Sensores

| Parâmetro | Sensor | Finalidade | 
 | ----- | ----- | ----- | 
| 🌡 **Temperatura** | DHT22 | Conforto térmico e fadiga. | 
| 💧 **Umidade** | DHT22 | Risco de proliferação de mofo e saúde respiratória. | 
| 💡 **Luminosidade** | LDR | Conforto visual e produtividade. | 
| 🌫 **Qualidade do Ar (Gás)** | MQ-2 | Detecção de gases combustíveis/fumos e prevenção de acidentes. | 

### Reações Automáticas e Atuação Local

O sistema opera em um **Loop de Controle (Lê, Avalia, Atua, Envia)**, garantindo uma resposta imediata a desvios dos parâmetros ideais:

* **Alertas Visuais:** LEDs de três cores (**Ideal, Moderado, Crítico**) para feedback visual instantâneo por sensor.

* **Alertas Sonoros:** Buzzer com diferentes intensidades conforme a gravidade do risco.

* **Context Management:** Atualização contínua do estado no Orion Context Broker, permitindo atuação remota através da nuvem.

## 🏛️ 2. Arquitetura e Fluxo de Dados (FIWARE Context Management)

A arquitetura segue o padrão **Smart Solution** da plataforma FIWARE, utilizando o Context Broker como o principal ponto de gestão e persistência do estado do ambiente.

 <img width="686" height="649" alt="Captura de tela 2025-11-17 004848" src="https://github.com/user-attachments/assets/bfad40b3-701c-4ae9-be65-a082a7dcb8f8" />


### Stack Tecnológico Principal

| Componente | Função Primária | Tecnologia Principal | 
 | ----- | ----- | ----- | 
| **Edge (ESP32)** | Aquisição de dados, classificação de risco e atuação local. | C/C++ (Arduino), MQTT | 
| **IoT Agent MQTT** | Tradução do payload MQTT (UltraLight) para a linguagem **NGSI-v2**. | FIWARE Component | 
| **Orion Context Broker** | Persistência do **Estado Atual** de todas as entidades (Digital Twin). | FIWARE Context Broker (NGSI-v2) | 
| **STH-Comet** | Armazenamento de dados históricos (**Time-Series**) para análise e gráficos. | FIWARE Time-Series | 
| **Dashboard Python** | Visualização interativa e gestão de comandos remotos. | Python, Dash, Plotly, NGSI-v2 API | 


### Fluxo de Comunicação dos Componentes:

O dado flui em um ciclo contínuo, começando no microcontrolador e culminando na interface do usuário e no sistema de atuação:

`ESP32` → `IoT Agent MQTT` → `Orion Context Broker` → `STH-Comet` → `Dashboard Python`

| Componente | Função no Fluxo de Dados |
| :--- | :--- |
| **Sensores (DHT22/LDR)** | Realizam as medições periódicas. |
| **ESP32** | Envia os dados via MQTT. |
| **IoT Agent MQTT** | Recebe os dados e os converte em Entidades de Contexto NGSI-v2. |
| **Orion Context Broker (Coração FIWARE)** | Gerencia o estado atual das entidades e aciona o STH-Comet para persistência histórica. |
| **Dashboard Python** | Consome os dados do Orion e do STH-Comet para visualização. |
| **Atuação** | O Orion envia comandos de volta ao ESP32 para acionamento remoto do LED Azul e do Buzzer em caso de anomalia. |

## 🚨 3. Parâmetros de Alerta e Atuação

Os limites de alerta são rigorosamente definidos com base em normas de conforto e segurança para garantir a ação preventiva do sistema.

| Sensor | Faixa Ideal | Faixa Moderada | Faixa Crítica | 
 | ----- | ----- | ----- | ----- | 
| **Temperatura** | 21–24°C | 24–27°C | <18 ou >27 | 
| **Umidade** | 45–60% | 35–45% / 60–70% | <35% ou >70% | 
| **Luminosidade** | 40–60% | 25–40% / 60–75% | <25% ou >75% | 
| **Gás MQ-2 (ppm)** | ≤300 | 300–1000 | >1000 | 

### Lógica de Atuação Local

* **Moderado:** LED do respectivo sensor piscando + buzzer fraco.

* **Crítico:** LED do respectivo sensor aceso fixo + buzzer forte.

## ⚙️ 4. Configuração e Provisionamento

### 4.1 Interface de Contexto (NGSI-v2 e Comandos Remotos)

O sistema permite consulta do estado atual e envio de comandos remotos via API NGSI-v2 (Postman).

* **Comando Remoto (Exemplo):** O atributo `led` é exposto para atuação remota:

  ```json
  { "led": { "type": "command", "value": "on/off" } }

  
---

## 🚀 Passo a Passo de Execução

1.  **Configurar ambiente FIWARE:** Em uma máquina virtual (VM), configure o ambiente FIWARE usando Docker ou Azure.

2.  **Registrar o dispositivo:** Registre o dispositivo no IoT Agent com o modelo abaixo:

### Configuração do Dispositivo no IoT Agent

Abaixo está o payload JSON usado para provisionar o dispositivo `esp32_001` no IOT Agent for UltraLight (South Bound):


## 🚀 Provisionamento do Dispositivo (IoT Agent)

```json
{
  "devices": [
    {
      "device_id": "esp32_001",
      "entity_name": "urn:ngsi-ld:esp32_001",
      "entity_type": "ESP32",
      "protocol": "PDI-IoTA-UltraLight",
      "transport": "MQTT",
      "apikey": "TEF",
      "commands": [
        { "name": "led", "type": "command" }
      ],
      "attributes": [
        { "object_id": "t", "name": "temperature", "type": "Float" },
        { "object_id": "h", "name": "humidity", "type": "Float" },
        { "object_id": "l", "name": "luminosity", "type": "Float" },
        { "object_id": "gppm", "name": "gas_ppm", "type": "Float" },
        { "object_id": "b", "name": "led_purples_state", "type": "Text" }
      ]
    }
  ]
}
```

3.  **Programar o ESP32 (no Wokwi):**

      - Conectar ao Wi-Fi.
      - Conectar ao broker MQTT.
      - Ler valores de temperatura e umidade via DHT22 e luminosidade no ldr
      - Publicar os dados nos tópicos configurados.
      - 
4.  **Testar no Postman:**

      - Fazer um **GET** nos endpoints:
      - `http://20.116.216.196:1026/v2/entities/urn:ngsi-ld:esp32_001/attrs/temperature` `http://20.116.216.196:1026/v2/entities/urn:ngsi-ld:esp32_001/attrs/luminosity` `http://20.116.216.196:1026/v2/entities/urn:ngsi-ld:esp32_001/attrs/humidity` `http://20.116.216.196:1026/v2/entities/urn:ngsi-ld:esp32_001/attrs/gas_ppm` `http://20.116.216.196:1026/v2/entities/urn:ngsi-ld:esp32_001/attrs/led_purples_state` 
      - Visualizar os dados de temperatura, umidade, luminosidade, gas e led(que indica o buzzer) atualizados.


## 🧩 Hardware 

| Componente | Função |
|:---|:---|
| **ESP32 DevKit V1** | Microcontrolador principal |
| **DHT22** | Temperatura e umidade |
| **LDR** | Luminosidade |
| **MQ-2** | Qualidade do ar |
| **Buzzer** | Alertas sonoros |
| **LEDs** | Indicadores individuais dos sensores |
| **Botão** | Liga/desliga o sistema de alerta |

---

## 💻 Software e Plataforma

| Serviço | Função |
|:---|:---|
| **Orion Context Broker** | Estado atual do ambiente |
| **IoT Agent MQTT** | Interface MQTT/NGSI |
| **STH-Comet** | Histórico |
| **MongoDB** | Armazenamento |
| **Dashboard Python** | Visualização |
| **Docker Compose** | Orquestração |

---

## 🚨 Parâmetros Ambientais do Projeto

| Sensor | Ideal | Moderado | Crítico |
|:---|:---|:---|:---|
| **Temperatura** | 21–24°C | 24–27°C | <18 ou >27 |
| **Umidade** | 45–60% | 35–45% / 60–70% | <35% ou >70% |
| **Luminosidade** | 40–60% | 25–40% / 60–75% | <25% ou >75% |
| **Gás MQ-2 (ppm)** | $\le 300$ | $300–1000$ | $> 1000$ |

### Reações do Sistema

| Nível | LED | Buzzer | Dashboard |
|:---|:---|:---|:---|
| **Ideal** | Apagado | Desligado | Verde |
| **Moderado** | Piscando | Som baixo | Amarelo |
| **Crítico** | Aceso | Som forte | Vermelho |

---

## 📊 Dashboard Python

O dashboard mostra:

* 4 gráficos: temperatura, umidade, luminosidade, gás
* Interruptor digital do buzzer
* Alerta geral colorido
* Histórico FIWARE em tempo real

---

## 🚀 Instalação e Execução

Para instalar e executar o sistema, siga os passos abaixo na sua Máquina Virtual (Azure/Ubuntu Server):

### 1. Clonagem e Configuração do FIWARE

```bash
# 1. Clonar o repositório
git clone [https://github.com/seuusuario/fiware-vinharia-agnello.git](https://github.com/seuusuario/fiware-vinharia-agnello.git)
cd fiware-vinharia-agnello

# 2. Subir todos os contêineres FIWARE (Orion, IoT Agent, STH-Comet, MongoDB)
sudo docker-compose up -d

# 3. Verificar o status dos contêineres
sudo docker ps
```

### 2. Configuração e Inicialização do Dashboard
```bash

# 1. Acessar a pasta do dashboard
cd dashboard

# 2. Instalar as dependências Python
pip install -r requirements.txt
# Dependências: Dash, Plotly, Requests, Pytz

# 3. Executar o dashboard
# Opção A: Execução manual para debug
python3 app.py

# Opção B: Execução como serviço (recomendado para produção)
sudo systemctl start fiware-dashboard.service

#O dashboard estará disponível em seu navegador no endereço: [http://<IP_DA_SUA_VM>:5000]
#depois de iniciar a VM no azure
```
### 3. tornar o Dashboard automatico
Para garantir que o Dashboard inicie automaticamente e permaneça ativo (mesmo após reinicializações da VM), criaremos um serviço **Systemd**.

###### 1. Criar o Arquivo de Serviço

Crie o arquivo de serviço `fiware-dashboard.service` utilizando o `nano`:

```bash
sudo nano /etc/systemd/system/fiware-dashboard.service
[Unit]
Description=Dashboard FIWARE
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/seu user/dashboard/app.py
WorkingDirectory=/home/seu user/dashboard
Restart=always
User=seu user

[Install]
WantedBy=multi-user.target
#3. Ativar e Iniciar o Serviço
#Após salvar o arquivo, execute os seguintes comandos para recarregar o Systemd, habilitar o serviço e iniciá-lo imediatamente:

sudo systemctl daemon-reload
sudo systemctl enable fiware-dashboard.service
sudo systemctl start fiware-dashboard.service
```

---

## 🖼️ Mídias do Projeto

* 📌 Dashboard  <img width="1907" height="909" alt="image" src="https://github.com/user-attachments/assets/ded69311-ce1b-45d0-9814-43fd14ebd0bb" />

* 📌 Hardware ESP32  <img width="413" height="365" alt="image" src="https://github.com/user-attachments/assets/b8e36892-a6fb-4d47-99bd-9af76913eec8" />

* 📌 Postman  <img width="1916" height="862" alt="image" src="https://github.com/user-attachments/assets/c6ba3cf0-06e6-4321-a036-feb0fcd87646" />


---

## 🌟 Conclusão

O projeto **Bem-Estar no Trabalho** demonstra como a tecnologia IoT combinada com o ecossistema FIWARE pode criar ambientes profissionais seguros, inteligentes e eficientes.
A solução:

* Monitora variáveis ambientais essenciais
* Atua automaticamente em situações de risco
* Registra histórico para auditoria e análise
* Exibe tudo em um dashboard moderno
* É modular, escalável e altamente aplicável

Ideal para empresas, escritórios, laboratórios, salas técnicas e ambientes que exigem controle ambiental.

---

## 👨‍💻 Desenvolvido por:

* Rafael Augusto Carmona – RM 563758
* Eduardo Tolentino – RM 562169
* Enzo Hort Ramos – RM 561872

## 👨‍🏫 Professor

* Fábio Enrique Cabrini

## 🏫 Curso

* Engenharia de Software – FIAP

---

## 🔗 Links Importantes
**vídeo no youtube:**

**Simulação Wokwi:**
`https://wokwi.com/projects/44727608930033152`

**Collection Postman:**
`https://rafinhaacarmona-8827768.postman.co/workspace/Rafael-carmona's-Workspace~1d0e5f81-4f93-4496-8336-903a367dee49/collection/47624777-4f5b3c33-01f5-4b55-b80c-8330052301b0?action=share&source=copy-link&creator=47624777`

