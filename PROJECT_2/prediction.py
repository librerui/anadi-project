# prediction.py
# Correr com: streamlit run prediction.py

import streamlit as st
import joblib
import numpy as np
import pandas as pd
import folium
from streamlit_folium import st_folium

# -----------------------------------------------------------------------------
# CONFIGURAÇÕES DA PÁGINA
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Painel de Gestão e Previsão PTD", layout="wide")

# -----------------------------------------------------------------------------
# CONSTANTES
# -----------------------------------------------------------------------------
PROFILE    = 'Perfil_Leve'
RESULT_DIR = f'results/{PROFILE}'

FEATURE_COLS = [
    'Potência instalada [kVA]',
    'N_Clientes',
    'P_IP_Total',
    'P_IP_Inef',
    'LED_Ratio',
    'N_Luminarias',
    'N_Lampadas',
    'Cap_per_Cliente',
    'Distrito_enc',
    'Concelho_enc',
]

CLASS_LABELS = {0: 'Alto', 1: 'Baixo', 2: 'Medio'}

# -----------------------------------------------------------------------------
# MODELOS DE CARREGADORES (exemplos reais) - potência em kW, fator simultaneidade, custo instalação (€)
# -----------------------------------------------------------------------------
CHARGER_MODELS = {
    'Wallbox Pulsar Plus':      {'power_kW': 7.4,  'simult_factor': 0.7, 'install_cost_eur': 800},
    'Wallbox Commander 2':     {'power_kW': 22.0, 'simult_factor': 0.6, 'install_cost_eur': 1300},
    'ABB Terra AC':            {'power_kW': 22.0, 'simult_factor': 0.6, 'install_cost_eur': 1500},
    'Schneider EVlink':        {'power_kW': 11.0, 'simult_factor': 0.65,'install_cost_eur': 1100},
    'EO Mini Pro':             {'power_kW': 7.0,  'simult_factor': 0.7, 'install_cost_eur': 750},
    'EVBox BusinessLine':      {'power_kW': 22.0, 'simult_factor': 0.55,'install_cost_eur': 1400},
}

# -----------------------------------------------------------------------------
# PRESETS DE CENÁRIO (valores representativos para preencher inputs rapidamente)
# -----------------------------------------------------------------------------
PRESETS = {
    'Posto Residencial Urbano': {
        'potencia': 125.0, 'n_clientes': 20, 'p_ip_total': 800.0, 'p_ip_inef': 500.0,
        'led_ratio': 0.35, 'cap_per_cli': 3.0, 'n_luminarias': 8000, 'n_lampadas': 7900,
    },
    'Posto Industrial / Logístico': {
        'potencia': 1000.0, 'n_clientes': 250, 'p_ip_total': 6000.0, 'p_ip_inef': 3200.0,
        'led_ratio': 0.15, 'cap_per_cli': 4.0, 'n_luminarias': 500, 'n_lampadas': 480,
    },
    'Posto Rural / Aéreo': {
        'potencia': 75.0, 'n_clientes': 8, 'p_ip_total': 400.0, 'p_ip_inef': 250.0,
        'led_ratio': 0.20, 'cap_per_cli': 3.5, 'n_luminarias': 1200, 'n_lampadas': 1180,
    },
    'Posto com Geração Distribuída (Solar)': {
        'potencia': 300.0, 'n_clientes': 60, 'p_ip_total': 1500.0, 'p_ip_inef': 900.0,
        'led_ratio': 0.40, 'cap_per_cli': 3.0, 'n_luminarias': 9000, 'n_lampadas': 8900,
    },
    'Posto de Alta Capacidade (630 kVA+)': {
        'potencia': 800.0, 'n_clientes': 400, 'p_ip_total': 12000.0, 'p_ip_inef': 6000.0,
        'led_ratio': 0.10, 'cap_per_cli': 5.0, 'n_luminarias': 200, 'n_lampadas': 190,
    }
}
# -----------------------------------------------------------------------------
# CARREGAR MODELOS E DATASET REAL
# -----------------------------------------------------------------------------
@st.cache_resource
def load_assets():
    scaler    = joblib.load(f'{RESULT_DIR}/{PROFILE}_scaler.pkl')
    model_reg = joblib.load(f'{RESULT_DIR}/{PROFILE}_model_lr.pkl')

    knn_cached = joblib.load(f'{RESULT_DIR}/{PROFILE}_model_knn.pkl')
    model_clf  = joblib.load(f'{RESULT_DIR}/{PROFILE}_model_tree.pkl') \
                 if isinstance(knn_cached, dict) else knn_cached

    return scaler, model_reg, model_clf


@st.cache_data
def load_ptd_data():
    """
    Carrega o dataset real e constrói as colunas de encoding geográfico a partir
    de CodDistritoConcelho (ex: 1307 → Distrito 13, Concelho 07).
    Também parseia as coordenadas geográficas para lat/lon separados.
    """
    try:
        df = pd.read_excel("./data/PTD_level_dataset.xlsx")
    except Exception:
        exit(1)

    # --- Parsing de coordenadas ---
    def parse_coords(s):
        try:
            lat, lon = str(s).split(',')
            return float(lat.strip()), float(lon.strip())
        except Exception:
            return None, None

    df[['lat', 'lon']] = df['Coordenadas Geográficas'].apply(
        lambda x: pd.Series(parse_coords(x))
    )
    df = df.dropna(subset=['lat', 'lon'])

    # --- Encoding geográfico derivado de CodDistritoConcelho ---
    # CodDistritoConcelho é um inteiro de 4 dígitos: ex 1307 → Distrito=13, Concelho=07
    # Usamos LabelEncoder implícito: índice ordinal dos valores únicos ordenados
    df['CodDistritoConcelho'] = df['CodDistritoConcelho'].astype(int)

    dist_codes = sorted(df['Distrito'].unique())
    conc_codes  = sorted(df['Concelho'].unique())

    df['Distrito_enc'] = df['Distrito'].apply(lambda x: dist_codes.index(x))
    df['Concelho_enc'] = df['Concelho'].apply(lambda x: conc_codes.index(x))

    return df, dist_codes, conc_codes


scaler, model_reg, model_clf = load_assets()
ptd_data, dist_codes, conc_codes = load_ptd_data()

# -----------------------------------------------------------------------------
# ESTADO INICIAL DOS INPUTS
# -----------------------------------------------------------------------------
DEFAULTS = {
    "potencia": 250.0,
    "n_clientes": 50,
    "p_ip_total": 1307.0,
    "p_ip_inef": 991.0,
    "led_ratio": 0.24,
    "cap_per_cli": 3.0,
    "n_luminarias": 21315,
    "n_lampadas": 21286,
}

for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# -----------------------------------------------------------------------------
# INTERFACE
# -----------------------------------------------------------------------------
def aplicar_preset():
    preset = st.session_state.get("preset")

    if preset is None or preset == "-- Nenhum --":
        return

    p = PRESETS[preset]

    st.session_state.potencia = p['potencia']
    st.session_state.n_clientes = p['n_clientes']
    st.session_state.p_ip_total = p['p_ip_total']
    st.session_state.p_ip_inef = p['p_ip_inef']
    st.session_state.led_ratio = p['led_ratio']
    st.session_state.cap_per_cli = p['cap_per_cli']
    st.session_state.n_luminarias = p['n_luminarias']
    st.session_state.n_lampadas = p['n_lampadas']

st.title("Painel Unificado de Gestão e Previsão de PTD — E-REDES")
st.markdown("Altere os parâmetros para obter previsões instantâneas e visualizar a distribuição geoespacial dos postos.")
st.markdown("---")

col_inputs, col_kpis = st.columns([6, 4], gap="large")

# ─── INPUTS ───────────────────────────────────────────────────────────────────
with col_inputs:
    st.subheader("🛠️ Parâmetros Técnicos do Posto Simulador")

    r1c1, r1c2, r1c3 = st.columns(3)
    with r1c1:
        potencia = st.number_input(
            "Potência Instalada (kVA)",
            step=50.0,
            key='potencia'
        )
        n_clientes = st.number_input(
            "Nº Clientes Ativos",
            step=5,
            key='n_clientes'
        )

    with r1c2:
        p_ip_total = st.number_input(
            "Potência IP Total (W)",
            step=100.0,
            key='p_ip_total'
        )

        p_ip_inef = st.number_input(
            "Potência IP Ineficiente (W)",
            step=50.0,
            key='p_ip_inef'
        )

    with r1c3:
        led_ratio = st.slider(
            "Rácio LED",
            min_value=0.0,
            max_value=1.0,
            step=0.01,
            key='led_ratio'
        )

        cap_per_cli = st.number_input(
            "Cap. por Cliente (kVA/cli)",
            step=0.5,
            key='cap_per_cli'
        )


    n_luminarias = st.number_input(
        "Nº Luminárias",
        step=100,
        key='n_luminarias'
    )

    n_lampadas = st.number_input(
        "Nº Lâmpadas",
        step=100,
        key='n_lampadas'
    )

    st.subheader("📍 Localização")
    lc1, lc2 = st.columns(2)
    with lc1:
        distrito_nome = st.selectbox("Distrito", options=sorted(ptd_data['Distrito'].unique()))
    with lc2:
        concs_do_dist = sorted(ptd_data[ptd_data['Distrito'] == distrito_nome]['Concelho'].unique())
        concelho_nome = st.selectbox("Concelho", options=concs_do_dist)

    # Presets e seleção de modelos
    st.subheader("⚡ Modelos de Carregador e Presets")
    preset = st.selectbox(
        "Escolher Preset de Cenário",
        options=["-- Nenhum --"] + list(PRESETS.keys()),
        key="preset"
    )

    st.button(
        "Aplicar preset",
        on_click=aplicar_preset
    )

    default_model = st.selectbox("Modelo de Carregador (padrão)", options=list(CHARGER_MODELS.keys()), index=1)
    mix_models = st.multiselect("Modelos para Análise de Mix", options=list(CHARGER_MODELS.keys()), default=[default_model])

# ─── KPIs ────────────────────────────────────────────────────────────────────
with col_kpis:
    st.subheader("📊 Previsão para o Posto Atual")

    distrito_enc = dist_codes.index(distrito_nome)
    concelho_enc = conc_codes.index(concelho_nome) if concelho_nome in conc_codes else 0

    X_input = pd.DataFrame([{
        'Potência instalada [kVA]': potencia,
        'N_Clientes':               n_clientes,
        'P_IP_Total':               p_ip_total,
        'P_IP_Inef':                p_ip_inef,
        'LED_Ratio':                led_ratio,
        'N_Luminarias':             n_luminarias,
        'N_Lampadas':               n_lampadas,
        'Cap_per_Cliente':          cap_per_cli,
        'Distrito_enc':             distrito_enc,
        'Concelho_enc':             concelho_enc,
    }])

    X_scaled = pd.DataFrame(scaler.transform(X_input), columns=FEATURE_COLS)
    folga_pred = model_reg.predict(X_scaled)[0]

    if hasattr(model_clf, 'predict'):
        ocp_id     = model_clf.predict(X_scaled)[0]
        label_ocp  = CLASS_LABELS.get(int(ocp_id), f"Código {ocp_id}")
    else:
        label_ocp = "Indisponível"

    st.metric("Folga de Rede Predita (PFolga_PTD)", f"{folga_pred:.2f} kVA")
    st.metric("Nível de Ocupação (utilizRede)",      label_ocp)

    max_chargers = int(max(0, folga_pred) / (22 * 0.60))
    # cálculo de viabilidade por modelo selecionado
    sel_model = CHARGER_MODELS.get(default_model, {'power_kW': 22.0, 'simult_factor': 0.6, 'install_cost_eur': 1200})
    eff_kva_per_unit = sel_model['power_kW'] * sel_model['simult_factor']
    max_chargers = int(max(0, folga_pred) / eff_kva_per_unit) if eff_kva_per_unit > 0 else 0
    st.metric(f"Máx. Carregadores {sel_model['power_kW']} kW estimados", max_chargers)

    if folga_pred > 200:
        st.success("Folga Elevada — excelente viabilidade para VE.")
    elif folga_pred > 50:
        st.warning("Folga Moderada — requer monitorização.")
    else:
        st.error("Saturação Crítica — risco de sobrecarga.")

    # Análise de mix de carregadores
    st.subheader("🔢 Análise de Mix de Carregadores")
    mix_results = []
    total_cost = 0
    for mname in mix_models:
        spec = CHARGER_MODELS[mname]
        eff = spec['power_kW'] * spec['simult_factor']
        units = int(max(0, folga_pred) // eff) if eff > 0 else 0
        cost = units * spec['install_cost_eur']
        mix_results.append({'Modelo': mname, 'Potência kW': spec['power_kW'], 'Fator Simult.': spec['simult_factor'], 'Máx Unidades': units, 'Custo Est. (€)': cost})
        total_cost += cost

    if len(mix_results) > 0:
        st.table(pd.DataFrame(mix_results))
        st.markdown(f"**Custo total estimado de instalação (mix): €{total_cost:,.0f}**")

# ─── MAPA ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("🗺️ Análise Geoespacial Dinâmica")

mc1, mc2, mc3 = st.columns([1, 1, 2])
with mc1:
    mostrar_viaveis = st.checkbox("Só PTDs com margem para VE", value=False)
with mc2:
    todos_distritos = st.checkbox("Mostrar todos os distritos", value=False)
with mc3:
    sample_size = st.slider("Amostragem de postos no mapa:", 50, min(2000, len(ptd_data)), 400, step=50)

# Filtro geográfico
if todos_distritos:
    ptd_mapa = ptd_data.copy()
else:
    ptd_mapa = ptd_data[ptd_data['Distrito'] == distrito_nome].copy()
    if len(ptd_mapa) == 0:
        ptd_mapa = ptd_data.copy()

# Batch predictions sobre os postos do mapa
X_batch = ptd_mapa[FEATURE_COLS].copy()
X_batch_scaled = pd.DataFrame(scaler.transform(X_batch), columns=FEATURE_COLS)

ptd_mapa['Folga_Modelada'] = model_reg.predict(X_batch_scaled).clip(min=0)
ptd_mapa['Max_Carregadores'] = (ptd_mapa['Folga_Modelada'] / (22 * 0.60)).astype(int)

if hasattr(model_clf, 'predict'):
    ocp_ids = model_clf.predict(X_batch_scaled)
    ptd_mapa['Ocupacao_Modelada'] = pd.Series(ocp_ids, index=ptd_mapa.index).map(CLASS_LABELS).fillna('N/D')
else:
    ptd_mapa['Ocupacao_Modelada'] = 'N/D'

if mostrar_viaveis:
    ptd_mapa = ptd_mapa[ptd_mapa['Max_Carregadores'] > 0]

if len(ptd_mapa) == 0:
    st.warning("Nenhum posto cumpre os critérios de filtragem para esta região.")
else:
    ptd_sample = ptd_mapa.sample(min(sample_size, len(ptd_mapa)), random_state=42)

    def cor_gradiente(n):
        if n == 0:   return "#e74c3c"
        elif n < 2:  return "#e8673c"
        elif n < 5:  return "#e8973c"
        elif n < 10: return "#e8b73c"
        elif n < 20: return "#a8cc3c"
        else:        return "#2ecc71"

    centro_lat = ptd_sample['lat'].mean()
    centro_lon = ptd_sample['lon'].mean()

    m = folium.Map(location=[centro_lat, centro_lon], zoom_start=10, tiles="CartoDB positron")

    for _, row in ptd_sample.iterrows():
        n   = int(row['Max_Carregadores'])
        cor = cor_gradiente(n)
        # construir sumário de viabilidade por modelo selecionado
        viability_lines = []
        for mname in mix_models:
            spec = CHARGER_MODELS.get(mname)
            if spec is None:
                continue
            eff = spec['power_kW'] * spec['simult_factor']
            units = int(max(0, row['Folga_Modelada']) // eff) if eff > 0 else 0
            viability_lines.append(f"{mname}: {units} un. (≈{spec['power_kW']}kW, fator {spec['simult_factor']})")

        popup_html = (
            f"<b>{row.get('Código de Instalação', 'N/D')}</b><br>"
            f"Concelho: {row.get('Concelho', 'N/D')}<br>"
            f"Potência: {row['Potência instalada [kVA]']} kVA<br>"
            f"Ocupação (ML): {row['Ocupacao_Modelada']}<br>"
            f"Folga (ML): {row['Folga_Modelada']:.1f} kVA<br>"
            f"<b>Máx. Carregadores 22kW: {n} un.</b><br>"
            f"<i>Viabilidade por modelo:</i><br>"
            + "<br>".join(viability_lines)
        )
        popup = folium.Popup(popup_html, max_width=320)

        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=6,
            color=cor,
            fill=True,
            fill_color=cor,
            fill_opacity=0.85,
            popup=popup
        ).add_to(m)

    legenda_html = """
    <div style="position:fixed;bottom:40px;left:40px;z-index:1000;background:white;
                padding:12px;border-radius:6px;border:2px solid #ddd;
                font-size:11px;line-height:1.8;box-shadow:2px 2px 6px rgba(0,0,0,0.15);">
        <b>Carregadores 22 kW estimados (ML)</b><br>
        <span style="color:#e74c3c;font-size:14px;">●</span> 0 = Saturação Crítica<br>
        <span style="color:#e8673c;font-size:14px;">●</span> 1 = Capacidade Muito Limitada<br>
        <span style="color:#e8973c;font-size:14px;">●</span> 2 a 4 = Margem Condicionada<br>
        <span style="color:#e8b73c;font-size:14px;">●</span> 5 a 9 = Margem Moderada<br>
        <span style="color:#a8cc3c;font-size:14px;">●</span> 10 a 19 = Infraestrutura Fluida<br>
        <span style="color:#2ecc71;font-size:14px;">●</span> >= 20 = Excelente Integração VE
    </div>
    """
    m.get_root().html.add_child(folium.Element(legenda_html))

    map_key = f"map_{distrito_nome}_{concelho_nome}_{sample_size}_{mostrar_viaveis}_{todos_distritos}"
    st_folium(m, width="100%", height=620, key=map_key, returned_objects=[])