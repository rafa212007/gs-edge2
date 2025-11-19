# ===========================================
# DASHBOARD – Bem-Estar no Trabalho (FIWARE + ESP32)
# Autor: Rafael Carmona
# ===========================================

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import requests
from datetime import datetime
import pytz

# ==============================
# CONFIGURAÇÕES DO SISTEMA
# ==============================
IP_ADDRESS = "20.116.216.196"
PORT_STH = 8666
DASH_PORT = 5000
ENTITY_ID = "urn:ngsi-ld:esp32_001"
ENTITY_TYPE = "ESP32"
HEADERS = {"Fiware-Service": "smart", "Fiware-ServicePath": "/"}

# ==============================
# FUNÇÕES DE ACESSO AO STH-COMET
# ==============================
def get_attribute_data(attribute: str, lastN: int = 20):
    """
    Busca os últimos N valores de um atributo no STH-Comet.
    Retorna a lista de 'values' do STH.
    """
    url = (
        f"http://{IP_ADDRESS}:{PORT_STH}/STH/v1/contextEntities/"
        f"type/{ENTITY_TYPE}/id/{ENTITY_ID}/attributes/{attribute}?lastN={lastN}"
    )
    try:
        response = requests.get(url, headers=HEADERS, timeout=5)
        if response.status_code != 200:
            print(f"Erro HTTP {response.status_code} ao acessar {url}")
            return []
        data = response.json()
        return data["contextResponses"][0]["contextElement"]["attributes"][0]["values"]
    except Exception as e:
        print(f"Erro ao buscar atributo {attribute}: {e}")
        return []


def convert_to_brazil_time(timestamps):
    """
    Converte uma lista de timestamps (string) UTC para horário de Brasília.
    """
    utc = pytz.utc
    br_tz = pytz.timezone("America/Sao_Paulo")
    converted = []
    for t in timestamps:
        try:
            t = t.replace("T", " ").replace("Z", "")
            try:
                dt = datetime.strptime(t, "%Y-%m-%d %H:%M:%S.%f")
            except:
                dt = datetime.strptime(t, "%Y-%m-%d %H:%M:%S")
            converted.append(utc.localize(dt).astimezone(br_tz))
        except:
            pass
    return converted


# ==============================
# FUNÇÕES DE CLASSIFICAÇÃO (MESMAS FAIXAS DO ESP32)
# ==============================
def classificar_temperatura(valor: float) -> str:
    if valor < 18 or valor > 27:
        return "critico"
    if (18 <= valor < 21) or (24 < valor <= 27):
        return "moderado"
    if 21 <= valor <= 24:
        return "ideal"
    return "moderado"


def classificar_umidade(valor: float) -> str:
    if valor < 35 or valor > 70:
        return "critico"
    if (35 <= valor < 45) or (60 < valor <= 70):
        return "moderado"
    if 45 <= valor <= 60:
        return "ideal"
    return "moderado"


def classificar_luminosidade(valor: float) -> str:
    if valor < 25 or valor > 75:
        return "critico"
    if (25 <= valor < 40) or (60 < valor <= 75):
        return "moderado"
    if 40 <= valor <= 60:
        return "ideal"
    return "moderado"


def classificar_gas(valor: float) -> str:
    if valor > 1000:
        return "critico"
    if valor > 300:
        return "moderado"
    return "ideal"


def status_cor(status: str) -> str:
    if status == "ideal":
        return "#008f39"
    if status == "moderado":
        return "#b38f00"
    return "#8B0000"


# ==============================
# DASHBOARD
# ==============================
app = dash.Dash(__name__)
app.title = "Dashboard – Bem-Estar no Trabalho"

BACKGROUND = "#050814"
CARD_BG = "#0b1020"
BORDER_COLOR = "#1f2840"

app.layout = html.Div(
    style={
        "backgroundColor": BACKGROUND,
        "minHeight": "100vh",
        "padding": "20px 40px",
        "fontFamily": "Segoe UI, system-ui, -apple-system, sans-serif",
        "color": "#f5f5f5",
    },
    children=[
        html.Div(
            style={"textAlign": "center", "marginBottom": "20px"},
            children=[
                html.H1(
                    "🏢 Bem-Estar no Trabalho – Monitoramento IoT",
                    style={"color": "#00d4ff", "fontSize": "32px", "marginBottom": "8px"},
                ),
                html.P(
                    "Acompanhamento em tempo real de temperatura, umidade, luminosidade e qualidade do ar no ambiente de trabalho.",
                    style={"color": "#a0aec0", "fontSize": "15px"},
                ),
            ],
        ),

        html.Hr(style={"borderColor": "#1f2933"}),

        dcc.Store(
            id="data-store",
            data={"temp": [], "hum": [], "lum": [], "gas": [], "buzzer": [], "timestamps": []},
        ),

        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "2fr 1fr",
                "gap": "20px",
                "marginTop": "20px",
                "marginBottom": "10px",
            },
            children=[
                html.Div(
                    id="alerta-status",
                    style={
                        "backgroundColor": "#111827",
                        "borderRadius": "14px",
                        "padding": "16px 20px",
                        "boxShadow": "0 12px 30px rgba(0,0,0,0.35)",
                        "border": f"1px solid {BORDER_COLOR}",
                        "fontSize": "20px",
                        "fontWeight": "bold",
                        "display": "flex",
                        "flexDirection": "column",
                        "alignItems": "flex-start",
                    },
                ),
                html.Div(
                    id="buzzer-switch",
                    style={
                        "backgroundColor": CARD_BG,
                        "borderRadius": "14px",
                        "padding": "16px 20px",
                        "boxShadow": "0 12px 30px rgba(0,0,0,0.35)",
                        "border": f"1px solid {BORDER_COLOR}",
                        "textAlign": "center",
                    },
                ),
            ],
        ),

        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(2, minmax(0, 1fr))",
                "gap": "20px",
                "marginTop": "10px",
            },
            children=[
                html.Div(
                    style={"backgroundColor": CARD_BG, "borderRadius": "14px", "padding": "12px", "boxShadow": "0 10px 24px rgba(0,0,0,0.35)", "border": f"1px solid {BORDER_COLOR}"},
                    children=[dcc.Graph(id="graph-temp", config={"displayModeBar": False})],
                ),
                html.Div(
                    style={"backgroundColor": CARD_BG, "borderRadius": "14px", "padding": "12px", "boxShadow": "0 10px 24px rgba(0,0,0,0.35)", "border": f"1px solid {BORDER_COLOR}"},
                    children=[dcc.Graph(id="graph-hum", config={"displayModeBar": False})],
                ),
                html.Div(
                    style={"backgroundColor": CARD_BG, "borderRadius": "14px", "padding": "12px", "boxShadow": "0 10px 24px rgba(0,0,0,0.35)", "border": f"1px solid {BORDER_COLOR}"},
                    children=[dcc.Graph(id="graph-lum", config={"displayModeBar": False})],
                ),
                html.Div(
                    style={"backgroundColor": CARD_BG, "borderRadius": "14px", "padding": "12px", "boxShadow": "0 10px 24px rgba(0,0,0,0.35)", "border": f"1px solid {BORDER_COLOR}"},
                    children=[dcc.Graph(id="graph-gas", config={"displayModeBar": False})],
                ),
            ],
        ),

        dcc.Interval(id="interval-update", interval=8000, n_intervals=0),
    ],
)

# ==============================
# CALLBACK PARA COLETAR DADOS
# ==============================
@app.callback(
    Output("data-store", "data"),
    Input("interval-update", "n_intervals"),
    State("data-store", "data"),
)
def update_data(n, stored):

    dados = {
        "temp": get_attribute_data("temperature"),
        "hum": get_attribute_data("humidity"),
        "lum": get_attribute_data("luminosity"),
        "gas": get_attribute_data("gas_ppm"),
        "buzzer": get_attribute_data("led_purples_state"),
    }

    any_data = any(len(v) > 0 for v in dados.values())
    if not any_data:
        return stored

    timestamps = [x["recvTime"] for x in dados["temp"] if "recvTime" in x]
    timestamps = convert_to_brazil_time(timestamps)

    stored["temp"] = [float(x["attrValue"]) for x in dados["temp"] if x.get("attrValue")]
    stored["hum"] = [float(x["attrValue"]) for x in dados["hum"] if x.get("attrValue")]
    stored["lum"] = [float(x["attrValue"]) for x in dados["lum"] if x.get("attrValue")]
    stored["gas"] = [float(x["attrValue"]) for x in dados["gas"] if x.get("attrValue")]
    stored["buzzer"] = [x["attrValue"] for x in dados["buzzer"] if x.get("attrValue")]
    stored["timestamps"] = timestamps

    return stored


# ==============================
# CALLBACK PARA GRÁFICOS / BUZZER / ALERTAS
# ==============================
@app.callback(
    [
        Output("graph-temp", "figure"),
        Output("graph-hum", "figure"),
        Output("graph-lum", "figure"),
        Output("graph-gas", "figure"),
        Output("buzzer-switch", "children"),
        Output("buzzer-switch", "style"),
        Output("alerta-status", "children"),
        Output("alerta-status", "style"),
    ],
    Input("data-store", "data"),
)
def update_graphs(data):

    def create_graph(values, timestamps, title, emoji, cor_linha, status: str):
        fig = go.Figure(
            [
                go.Scatter(
                    x=timestamps,
                    y=values,
                    mode="lines+markers",
                    line=dict(color=cor_linha, width=2.3),
                    marker=dict(size=6),
                )
            ]
        )
        fig.update_layout(
            title=f"{emoji} {title} — {status.upper()}",
            template="plotly_dark",
            paper_bgcolor="#050814",
            plot_bgcolor="#050814",
            font=dict(color="#f5f5f5"),
            margin=dict(l=35, r=15, t=40, b=40),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="#1f2933"),
        )
        return fig

    ultima_temp = data["temp"][-1] if data["temp"] else 0
    ultima_hum = data["hum"][-1] if data["hum"] else 0
    ultima_lum = data["lum"][-1] if data["lum"] else 0
    ultima_gas = data["gas"][-1] if data["gas"] else 0

    status_temp = classificar_temperatura(ultima_temp)
    status_hum = classificar_umidade(ultima_hum)
    status_lum = classificar_luminosidade(ultima_lum)
    status_gas = classificar_gas(ultima_gas)

    fig_temp = create_graph(data["temp"], data["timestamps"], f"Temperatura (°C) – {ultima_temp:.1f}°C", "🌡", "#ff6b6b", status_temp)
    fig_hum = create_graph(data["hum"], data["timestamps"], f"Umidade (%) – {ultima_hum:.1f}%", "💧", "#4fd1c5", status_hum)
    fig_lum = create_graph(data["lum"], data["timestamps"], f"Luminosidade (%) – {ultima_lum:.1f}", "💡", "#f6ad55", status_lum)
    fig_gas = create_graph(data["gas"], data["timestamps"], f"Gás (ppm) – {ultima_gas:.0f} ppm", "🌫", "#b794f4", status_gas)

    # ======================
    # BUZZER – DEIXEI IGUALZINHO
    # ======================
    if data["buzzer"]:
        estado = data["buzzer"][-1]
        if estado == "on":
            buz_text = [
                html.Div("🔔 BUZZER ATIVO", style={"fontSize": "22px", "fontWeight": "bold", "marginBottom": "4px"}),
                html.Div("Sistema sonoro ligado para alertar condições de risco.", style={"fontSize": "13px", "color": "#cbd5f5"}),
            ]
            buz_style = {
                "backgroundColor": "#064e3b",
                "color": "white",
                "padding": "14px 18px",
                "fontWeight": "bold",
                "borderRadius": "14px",
                "width": "100%",
                "border": "1px solid #10b981",
                "textAlign": "center",
                "boxShadow": "0 12px 30px rgba(0,0,0,0.4)",
            }
        else:
            buz_text = [
                html.Div("🔕 BUZZER DESATIVADO", style={"fontSize": "22px", "fontWeight": "bold", "marginBottom": "4px"}),
                html.Div("Sistema silencioso — ambiente aparentemente seguro.", style={"fontSize": "13px", "color": "#e5e7eb"}),
            ]
            buz_style = {
                "backgroundColor": "#3f1f1f",
                "color": "white",
                "padding": "14px 18px",
                "fontWeight": "bold",
                "borderRadius": "14px",
                "width": "100%",
                "border": "1px solid #f97373",
                "textAlign": "center",
                "boxShadow": "0 12px 30px rgba(0,0,0,0.4)",
            }
    else:
        buz_text = [
            html.Div("🔕 BUZZER — sem dados", style={"fontSize": "20px", "fontWeight": "bold", "marginBottom": "4px"}),
            html.Div("Ainda não há informações sobre o estado do buzzer.", style={"fontSize": "13px", "color": "#e5e7eb"}),
        ]
        buz_style = {
            "backgroundColor": "#374151",
            "color": "white",
            "padding": "14px 18px",
            "fontWeight": "bold",
            "borderRadius": "14px",
            "width": "100%",
            "border": "1px solid #4b5563",
            "textAlign": "center",
        }

    # ======================
    # ALERTAS INDIVIDUAIS (NOVO SISTEMA)
    # ======================
    def gerar_alerta_individual(nome, status, msg_ideal, msg_moderado, msg_critico):
        if status == "critico":
            return html.Div(
                [
                    html.Div(f"🚨 {nome} – CRÍTICO!", style={"fontSize": "20px", "marginBottom": "4px"}),
                    html.Div(msg_critico, style={"fontSize": "13px", "color": "#fee2e2"}),
                ],
                style={
                    "backgroundColor": "#7f1d1d",
                    "color": "white",
                    "border": "1px solid #f87171",
                    "borderRadius": "12px",
                    "padding": "10px 12px",
                    "marginBottom": "10px",
                },
            )
        elif status == "moderado":
            return html.Div(
                [
                    html.Div(f"⚠️ {nome} – Moderado", style={"fontSize": "20px", "marginBottom": "4px"}),
                    html.Div(msg_moderado, style={"fontSize": "13px", "color": "#fef3c7"}),
                ],
                style={
                    "backgroundColor": "#78350f",
                    "color": "white",
                    "border": "1px solid #facc15",
                    "borderRadius": "12px",
                    "padding": "10px 12px",
                    "marginBottom": "10px",
                },
            )
        else:
            return html.Div(
                [
                    html.Div(f"✅ {nome} – Ideal", style={"fontSize": "20px", "marginBottom": "4px"}),
                    html.Div(msg_ideal, style={"fontSize": "13px", "color": "#d1fae5"}),
                ],
                style={
                    "backgroundColor": "#065f46",
                    "color": "white",
                    "border": "1px solid #34d399",
                    "borderRadius": "12px",
                    "padding": "10px 12px",
                    "marginBottom": "10px",
                },
            )

    alerta_text = html.Div(
        [
            gerar_alerta_individual(
                "Temperatura", status_temp,
                "Temperatura adequada ao conforto térmico.",
                "Temperatura levemente fora — ajuste recomendado.",
                "Temperatura crítica! Pode causar fadiga e mal-estar."
            ),
            gerar_alerta_individual(
                "Umidade", status_hum,
                "Umidade estável e confortável.",
                "Umidade um pouco fora — atenção.",
                "Umidade crítica! Pode causar mofo ou desconforto."
            ),
            gerar_alerta_individual(
                "Luminosidade", status_lum,
                "Iluminação ideal para produtividade.",
                "Iluminação moderada — pode causar cansaço visual.",
                "Iluminação crítica! Alto risco de fadiga ocular."
            ),
            gerar_alerta_individual(
                "Qualidade do Ar (Gás)", status_gas,
                "Ar limpo e seguro para respiração.",
                "Concentração moderada de gases — atenção.",
                "Ar perigoso! Concentração crítica de gás."
            ),
        ]
    )

    alerta_style = {
        "backgroundColor": "transparent",
        "border": "none",
        "padding": "0",
        "margin": "0",
    }

    return (
        fig_temp,
        fig_hum,
        fig_lum,
        fig_gas,
        buz_text,
        buz_style,
        alerta_text,
        alerta_style,
    )


# ==============================
# EXECUÇÃO
# ==============================
if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=DASH_PORT)
