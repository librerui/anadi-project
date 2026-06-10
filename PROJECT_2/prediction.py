import streamlit as st
import joblib
import pandas as pd

# Page setup
st.set_page_config(page_title="Painel de Gestao e Previsao PTD", layout="wide")

# Constants
PROFILE = 'Perfil_Leve'
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

# Profile presets for quick data entry
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

# Assets and data loading
@st.cache_resource
def load_assets():
    scaler = joblib.load(f'{RESULT_DIR}/{PROFILE}_scaler.pkl')
    model_reg = joblib.load(f'{RESULT_DIR}/{PROFILE}_model_lr.pkl')
    
    knn_cached = joblib.load(f'{RESULT_DIR}/{PROFILE}_model_knn.pkl')
    model_clf = joblib.load(f'{RESULT_DIR}/{PROFILE}_model_tree.pkl') \
                if isinstance(knn_cached, dict) else knn_cached

    return scaler, model_reg, model_clf

@st.cache_data
def load_ptd_data():
    try:
        df = pd.read_excel("./data/PTD_level_dataset.xlsx")
    except Exception:
        st.error("Erro ao carregar o ficheiro de dados.")
        st.stop()

    df['CodDistritoConcelho'] = df['CodDistritoConcelho'].astype(int)
    dist_codes = sorted(df['Distrito'].unique())
    conc_codes = sorted(df['Concelho'].unique())

    return df, dist_codes, conc_codes

scaler, model_reg, model_clf = load_assets()
ptd_data, dist_codes, conc_codes = load_ptd_data()

# Initialize session state defaults
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

def aplicar_preset():
    preset = st.session_state.get("preset")
    if preset is None or preset == "Nenhum":
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

# User Interface Header
st.title("Painel de Gestão e Previsão de PTD")
st.text("Modifique os parâmetros técnicos ou selecione um perfil predefinido para analisar as previsões de rede.")

col_inputs, col_kpis = st.columns([6, 4], gap="large")

# Technical Inputs Side
with col_inputs:
    st.header("Parâmetros Técnicos")
    
    preset = st.selectbox(
        "Perfil de Cenário Predefinido",
        options=["Nenhum"] + list(PRESETS.keys()),
        key="preset",
        on_change=aplicar_preset
    )
    
    st.subheader("Configuração Estrutural")
    r1c1, r1c2 = st.columns(2)
    with r1c1:
        potencia = st.number_input("Potência Instalada (kVA)", step=50.0, key='potencia')
        n_clientes = st.number_input("Número de Clientes Ativos", step=5, key='n_clientes')
        cap_per_cli = st.number_input("Capacidade por Cliente (kVA/cli)", step=0.5, key='cap_per_cli')
    with r1c2:
        distrito_nome = st.selectbox("Distrito", options=sorted(ptd_data['Distrito'].unique()), key='distrito_nome')
        concs_do_dist = sorted(ptd_data[ptd_data['Distrito'] == distrito_nome]['Concelho'].unique())
        concelho_nome = st.selectbox("Concelho", options=concs_do_dist, key='concelho_nome')

    st.subheader("Iluminação Pública")
    r2c1, r2c2 = st.columns(2)
    with r2c1:
        p_ip_total = st.number_input("Potência IP Total (W)", step=100.0, key='p_ip_total')
        p_ip_inef = st.number_input("Potência IP Ineficiente (W)", step=50.0, key='p_ip_inef')
        led_ratio = st.slider("Rácio LED", min_value=0.0, max_value=1.0, step=0.01, key='led_ratio')
    with r2c2:
        n_luminarias = st.number_input("Número de Luminárias", step=100, key='n_luminarias')
        n_lampadas = st.number_input("Número de Lâmpadas", step=100, key='n_lampadas')

# Machine Learning Outputs Side
with col_kpis:
    st.header("Análise de Previsão")

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
        ocp_id = model_clf.predict(X_scaled)[0]
        label_ocp = CLASS_LABELS.get(int(ocp_id), f"Código {ocp_id}")
    else:
        label_ocp = "Indisponível"

    st.metric("Folga de Rede Estimada (PFolga_PTD)", f"{folga_pred:.2f} kVA")
    st.metric("Nível de Ocupação da Rede", label_ocp)

    st.subheader("Estado Operacional")
    if folga_pred > 200:
        st.success("Folga Elevada: Excelente viabilidade para novos pontos de consumo.")
    elif folga_pred > 50:
        st.warning("Folga Moderada: Requer monitorização regular da infraestrutura.")
    else:
        st.error("Saturação Crítica: Risco elevado de sobrecarga na rede.")