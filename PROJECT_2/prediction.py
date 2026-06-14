import streamlit as st
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

st.set_page_config(
    page_title="Painel PTD",
    layout="wide",
)

st.markdown("""
<style>
    /* Global font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }

    /* Tighter header spacing */
    h1 { color: #1a2744; font-weight: 700; margin-bottom: 0.2rem; }
    h2 { color: #1a2744; font-weight: 600; border-left: 4px solid #2e86ab; padding-left: 12px; }
    h3 { color: #334155; font-weight: 600; }

    /* Subtle separator */
    hr { border: none; border-top: 1px solid #e2e8f0; margin: 1.2rem 0; }

    /* Metric cards */
    [data-testid="stMetric"] {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 12px 16px;
    }
    [data-testid="stMetricLabel"] { font-size: 0.78rem; color: #64748b; font-weight: 500; }
    [data-testid="stMetricValue"] { font-size: 1.4rem; color: #1a2744; font-weight: 600; }

    /* Sidebar styling */
    section[data-testid="stSidebar"] { background: #f1f5f9; }
    section[data-testid="stSidebar"] h1 { font-size: 1.3rem; color: #1a2744; }
    section[data-testid="stSidebar"] h3 { font-size: 1rem; }

    /* Expander */
    [data-testid="stExpander"] { border: 1px solid #e2e8f0; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

import streamlit.components.v1 as components
components.html("""
<script>
// We need to access the parent document because components.html runs in an iframe
const parentDoc = window.parent.document;

const _iconMap = {
    'arrow_downward': '\u25BC',
    'arrow_upward': '\u25B2',
    'keyboard_double_arrow_right': '\u00BB',
    'keyboard_double_arrow_left': '\u00AB',
    'keyboard_arrow_right': '\u25B6',
    'keyboard_arrow_down': '\u25BC',
    'keyboard_arrow_up': '\u25B2',
    'keyboard_arrow_left': '\u25C0',
    'arrow_right': '\u25B6',
    'arrow_drop_down': '\u25BC',
    'arrow_forward_ios': '\u203A',
    'arrow_back_ios': '\u2039',
    'chevron_right': '\u203A',
    'chevron_left': '\u2039',
    'contrast': '\u25D0',
    'expand_more': '\u25BC',
    'expand_less': '\u25B2',
    'dark_mode': String.fromCodePoint(0x1F319),
    'light_mode': '\u2600',
    'close': '\u2715',
    'info': '\u24D8',
    'help': '?',
    'more_vert': '\u22EE',
    'more_horiz': '\u22EF',
    'check': '\u2713',
    'check_circle': '\u2713',
    'error': '\u26A0',
    'warning': '\u26A0',
    'search': String.fromCodePoint(0x1F50D),
    'menu': '\u2630',
    'settings': '\u2699',
    'content_copy': String.fromCodePoint(0x1F4CB),
    'download': '\u2B07',
    'upload': '\u2B06',
    'delete': String.fromCodePoint(0x1F5D1),
    'edit': '\u270F',
    'visibility': String.fromCodePoint(0x1F441),
    'visibility_off': String.fromCodePoint(0x1F441),
    'open_in_new': '\u2197',
    'refresh': '\u21BB',
    'add': '+',
    'remove': '\u2212',
    'star': '\u2B50',
    'favorite': '\u2764',
    'play_arrow': '\u25B6',
    'pause': '\u23F8',
    'stop': '\u23F9',
    'fullscreen': '\u26F6',
    'fullscreen_exit': '\u26F6',
    'zoom_in': '+',
    'zoom_out': '\u2212',
    'filter_list': '\u2630',
    'sort': '\u2195',
    'drag_indicator': '\u2630',
    'code': '</>',
};

function _replaceIcons() {
    parentDoc.querySelectorAll('span').forEach(function(el) {
        if (el.children.length === 0) { // Only leaf nodes
            var txt = el.textContent.trim();
            if (_iconMap[txt]) {
                // Replace if it's inside a button, menu, expander, or has icon-related classes
                var isIcon = (
                    el.closest('button') || 
                    el.closest('[role="menuitem"]') || 
                    el.closest('[data-testid="stThemeProviderToggle"]') ||
                    el.closest('summary') ||
                    el.className.toLowerCase().includes('icon') ||
                    el.className.toLowerCase().includes('symbol')
                );
                
                if (isIcon) {
                    el.innerHTML = _iconMap[txt];
                    el.style.fontFamily = "'Inter', system-ui, sans-serif";
                    el.style.fontSize = "1.2rem";
                }
            }
        }
    });
}
_replaceIcons();
var _iconObs = new MutationObserver(function() {
    window.requestAnimationFrame(_replaceIcons);
});
_iconObs.observe(parentDoc.body, { childList: true, subtree: true });
</script>
""", height=0, width=0)

PROFILES = {
    "Perfil Leve":  "Perfil_Leve",
    "Perfil Medio": "Perfil_Médio",
    "Perfil Pesado": "Perfil_Pesado",
}

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

CHARGER_TYPES = {
    "Normal (3.7 kW)":     3.7,
    "Semi-rápido (7.4 kW)": 7.4,
    "Rápido (22 kW)":      22.0,
    "Ultra-rápido (50 kW)": 50.0,
}

DATA_PATH = "./data/PTD_level_dataset.xlsx"


@st.cache_data
def load_raw_data():
    """Load the PTD dataset and precompute encoders and thresholds."""
    df = pd.read_excel(DATA_PATH)

    # Build label encoders identical to the notebook
    le_distrito = LabelEncoder()
    le_concelho = LabelEncoder()
    df['Distrito_enc'] = le_distrito.fit_transform(df['Distrito'])
    df['Concelho_enc'] = le_concelho.fit_transform(df['Concelho'])

    # Compute quantile thresholds for utilizRede classification
    valid_util = df['Util_Decimal'].dropna()
    q33 = float(valid_util.quantile(0.33))
    q66 = float(valid_util.quantile(0.66))

    return df, le_distrito, le_concelho, q33, q66


@st.cache_resource
def load_model(profile_tag):
    """Load regression model and scaler for the given profile."""
    result_dir = f'results/{profile_tag}'
    scaler = joblib.load(f'{result_dir}/{profile_tag}_scaler.pkl')
    model_lr = joblib.load(f'{result_dir}/{profile_tag}_model_lr.pkl')
    model_tree = joblib.load(f'{result_dir}/{profile_tag}_model_tree.pkl')

    # Load regression and classification metrics
    # Use joblib instead of pickle for better numpy version tolerance
    reg_results = joblib.load(f'{result_dir}/results.pkl')
    clf_results = joblib.load(f'{result_dir}/results_clf.pkl')

    return scaler, model_lr, model_tree, reg_results, clf_results


def classify_utilization(util_decimal, q33, q66):
    """Classify utilization level using the same thresholds as the notebook."""
    if util_decimal <= q33:
        return "baixo", "green"
    elif util_decimal <= q66:
        return "medio", "orange"
    else:
        return "alto", "red"


def derive_util_decimal(folga_kva, capacidade_kva):
    """Derive Util_Decimal from predicted PFolga and installed capacity."""
    if capacidade_kva <= 0:
        return 1.0
    return max(0.0, min(1.0, 1.0 - folga_kva / capacidade_kva))


df_raw, le_distrito, le_concelho, q33, q66 = load_raw_data()


with st.sidebar:
    st.title("Configuracao")

    st.markdown("---")

    # Profile selection
    profile_label = st.selectbox(
        "Perfil do Modelo",
        options=list(PROFILES.keys()),
        index=0,
        help="Perfil de treino usado no notebook. "
             "Pesado = mais dados de treino, mais iterações.",
    )
    profile_tag = PROFILES[profile_label]
    scaler, model_lr, model_tree, reg_results, clf_results = load_model(profile_tag)

    st.caption(f"MAE Linear: {reg_results['Linear']['mae_mean']:.2f} kVA")
    st.caption(f"MAE Tree: {reg_results['Tree']['mae_mean']:.2f} kVA")

    st.markdown("---")

    # Mode selection
    mode = st.radio(
        "Modo de Entrada",
        options=["Selecionar PTD Real", "Simulacao Manual"],
        index=0,
    )

    st.markdown("---")

    # Charger simulation config
    st.subheader("Simulacao de Carregadores")
    charger_type = st.selectbox(
        "Tipo de Carregador",
        options=list(CHARGER_TYPES.keys()),
    )
    charger_power = CHARGER_TYPES[charger_type]
    n_chargers = st.slider(
        "Número de Carregadores",
        min_value=1,
        max_value=20,
        value=2,
    )
    utilization_factor = st.slider(
        "Factor de Utilizacao Simultanea",
        min_value=0.1,
        max_value=1.0,
        value=0.7,
        step=0.05,
        help="Proporcao de carregadores ativos em simultaneo.",
    )


st.title("Painel de Gestao e Previsao de PTD")
st.caption(
    "Avaliacao da capacidade de absorcao de pontos de carregamento de VEs "
    "em Postos de Transformacao da rede e-REDES."
)

TUDO = "Tudo"

if mode == "Selecionar PTD Real":
    st.header("Selecao de PTD Real")
    st.caption(
        "Selecione um PTD existente na base de dados e-REDES. "
        "Todos os valores sao preenchidos automaticamente."
    )

    col_sel1, col_sel2, col_sel3 = st.columns(3)

    # Distrito filter
    distritos = sorted(df_raw['Distrito'].unique())
    with col_sel1:
        distrito = st.selectbox(
            "Distrito",
            options=[TUDO] + distritos,
            index=0,
            key="sel_distrito",
        )

    # Concelho filter (disabled if Distrito == Tudo)
    with col_sel2:
        if distrito == TUDO:
            concelho = st.selectbox(
                "Concelho", options=[TUDO], disabled=True,
                key="sel_concelho",
            )
        else:
            concelhos = sorted(
                df_raw[df_raw['Distrito'] == distrito]['Concelho'].unique()
            )
            concelho = st.selectbox(
                "Concelho", options=[TUDO] + concelhos, index=0,
                key="sel_concelho",
            )

    # Apply district + concelho filter
    ptds_filtered = df_raw.copy()
    if distrito != TUDO:
        ptds_filtered = ptds_filtered[ptds_filtered['Distrito'] == distrito]
    if concelho != TUDO:
        ptds_filtered = ptds_filtered[ptds_filtered['Concelho'] == concelho]

    # PTD filter (disabled if Concelho == Tudo)
    with col_sel3:
        if concelho == TUDO:
            ptd_id = st.selectbox(
                f"PTD ({len(ptds_filtered)} disponiveis)",
                options=[TUDO], disabled=True,
                key="sel_ptd",
            )
        else:
            ptd_options = ptds_filtered['Código de Instalação'].tolist()
            if ptd_options:
                ptd_id = st.selectbox(
                    f"PTD ({len(ptd_options)} disponiveis)",
                    options=[TUDO] + ptd_options,
                    index=0,
                    key="sel_ptd",
                )
            else:
                st.warning("Sem PTDs neste concelho.")
                st.stop()

    # Determine source data
    if ptd_id != TUDO:
        ptd_row = ptds_filtered[
            ptds_filtered['Código de Instalação'] == ptd_id
        ].iloc[0]
        single_ptd = True
    else:
        ptd_row = ptds_filtered.median(numeric_only=True)
        single_ptd = False

    # Base values from data
    base_potencia = float(ptd_row['Potência instalada [kVA]'])
    base_n_cli = int(round(float(ptd_row['N_Clientes'])))
    base_ip_total = float(ptd_row['P_IP_Total'])
    base_ip_inef = float(ptd_row['P_IP_Inef'])
    base_led = float(ptd_row['LED_Ratio'])
    base_lum = int(round(float(ptd_row['N_Luminarias'])))
    base_lamp = int(round(float(ptd_row['N_Lampadas'])))
    base_cap_cli = round(base_potencia / max(base_n_cli, 1), 2)
    real_folga = ptd_row.get('PFolga_PTD', None)
    real_util = ptd_row.get('Util_Decimal', None)

    # Use filter-dependent key prefix so widgets auto-reset on filter change
    _kp = f"{distrito}_{concelho}_{ptd_id}"

    # Check if user has any overrides in the expander
    potencia = st.session_state.get(f'ov_pot_{_kp}', base_potencia)
    n_clientes = st.session_state.get(f'ov_cli_{_kp}', base_n_cli)
    p_ip_total = st.session_state.get(f'ov_ipt_{_kp}', base_ip_total)
    p_ip_inef = st.session_state.get(f'ov_ipi_{_kp}', base_ip_inef)
    led_ratio = st.session_state.get(f'ov_led_{_kp}', base_led)
    n_luminarias = st.session_state.get(f'ov_lum_{_kp}', base_lum)
    n_lampadas = st.session_state.get(f'ov_lam_{_kp}', base_lamp)
    cap_per_cli_val = round(potencia / max(n_clientes, 1), 2)

    # Check if any value has been modified
    has_overrides = (
        potencia != base_potencia or n_clientes != base_n_cli or
        p_ip_total != base_ip_total or p_ip_inef != base_ip_inef or
        led_ratio != base_led or n_luminarias != base_lum or
        n_lampadas != base_lamp
    )

    # Display PTD info header
    st.markdown("---")
    hdr_col, btn_col = st.columns([5, 1])
    with hdr_col:
        if single_ptd:
            st.subheader("Dados do PTD Selecionado")
        else:
            scope = "Portugal"
            if distrito != TUDO:
                scope = distrito
            if concelho != TUDO:
                scope = concelho
            st.subheader(f"Valores medianos ({len(ptds_filtered)} PTDs em {scope})")
    with btn_col:
        if has_overrides:
            if st.button("Resetar valores", use_container_width=True):
                for k in list(st.session_state.keys()):
                    if k.startswith('ov_') and k.endswith(f'_{_kp}'):
                        del st.session_state[k]
                st.rerun()

    # Metric cards (read-only visual)
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Potencia Instalada", f"{potencia:.0f} kVA")
        st.metric("N. Clientes", f"{n_clientes}")
    with m2:
        st.metric("Cap/Cliente", f"{cap_per_cli_val:.2f} kVA/cli")
        st.metric("LED Ratio", f"{led_ratio:.1%}")
    with m3:
        st.metric("Potencia IP Total", f"{p_ip_total:.0f} W")
        st.metric("Potencia IP Inef.", f"{p_ip_inef:.0f} W")
    with m4:
        if real_folga is not None and not np.isnan(real_folga):
            lbl = "Folga Real" if single_ptd else "Folga Mediana"
            st.metric(lbl, f"{real_folga:.1f} kVA")
        else:
            st.metric("Folga Real", "N/D")
        if real_util is not None and not np.isnan(real_util):
            lbl = "Utilizacao Real" if single_ptd else "Utilizacao Mediana"
            st.metric(lbl, f"{real_util:.1%}")
        else:
            st.metric("Utilizacao Real", "N/D")

    # Editable expander for what-if simulation
    with st.expander("Editar valores para simulacao"):
        st.caption("Altere os valores para simular cenarios alternativos. Os resultados atualizam automaticamente.")
        e1, e2, e3, e4 = st.columns(4)
        with e1:
            potencia = st.number_input(
                "Potencia Instalada (kVA)",
                min_value=0.0, value=float(potencia), step=25.0,
                key=f"ov_pot_{_kp}", format="%.0f",
            )
            n_clientes = st.number_input(
                "N. Clientes",
                min_value=0, value=int(n_clientes), step=5,
                key=f"ov_cli_{_kp}",
            )
        with e2:
            p_ip_total = st.number_input(
                "Potencia IP Total (W)",
                min_value=0.0, value=float(p_ip_total), step=100.0,
                key=f"ov_ipt_{_kp}", format="%.0f",
            )
            p_ip_inef = st.number_input(
                "Potencia IP Inef. (W)",
                min_value=0.0, value=float(p_ip_inef), step=50.0,
                key=f"ov_ipi_{_kp}", format="%.0f",
            )
        with e3:
            led_ratio = st.number_input(
                "LED Ratio",
                min_value=0.0, max_value=1.0, value=float(led_ratio), step=0.01,
                key=f"ov_led_{_kp}", format="%.2f",
            )
            n_luminarias = st.number_input(
                "N. Luminarias",
                min_value=0, value=int(n_luminarias), step=100,
                key=f"ov_lum_{_kp}",
            )
        with e4:
            n_lampadas = st.number_input(
                "N. Lampadas",
                min_value=0, value=int(n_lampadas), step=100,
                key=f"ov_lam_{_kp}",
            )
        cap_per_cli_val = round(potencia / max(n_clientes, 1), 2)

    # Encode location
    if single_ptd:
        distrito_enc = ptd_row['Distrito_enc']
        concelho_enc = ptd_row['Concelho_enc']
    else:
        if distrito != TUDO and distrito in le_distrito.classes_:
            distrito_enc = int(le_distrito.transform([distrito])[0])
        else:
            distrito_enc = int(ptds_filtered['Distrito_enc'].median())
        if concelho != TUDO and concelho in le_concelho.classes_:
            concelho_enc = int(le_concelho.transform([concelho])[0])
        else:
            concelho_enc = int(ptds_filtered['Concelho_enc'].median())

else:
    # Manual simulation mode
    st.header("Simulacao Manual")
    st.caption(
        "Introduza os parametros tecnicos do PTD hipotetico. "
        "As variaveis de IP sao agregadas ao nivel do concelho."
    )

    col_ptd, col_ip = st.columns(2)

    with col_ptd:
        st.subheader("Configuracao do PTD")
        potencia = st.number_input(
            "Potencia Instalada (kVA)",
            min_value=25, max_value=2000, value=250, step=25,
        )
        n_clientes = st.number_input(
            "Número de Clientes",
            min_value=1, max_value=1000, value=50, step=5,
        )
        cap_per_cli_val = round(potencia / max(n_clientes, 1), 2)
        st.caption(f"Cap/Cliente calculado: **{cap_per_cli_val:.2f}** kVA/cli")

        distrito = st.selectbox(
            "Distrito",
            options=sorted(df_raw['Distrito'].unique()),
            key="sim_distrito",
        )
        concelhos_sim = sorted(
            df_raw[df_raw['Distrito'] == distrito]['Concelho'].unique()
        )
        concelho = st.selectbox(
            "Concelho",
            options=concelhos_sim,
            key="sim_concelho",
        )

    with col_ip:
        st.subheader("Iluminacao Publica (Concelho)")
        st.caption("Valores tipicos do concelho selecionado:")

        # Show default values from the dataset for this concelho
        conc_data = df_raw[df_raw['Concelho'] == concelho]
        default_ip_total = float(conc_data['P_IP_Total'].median()) if len(conc_data) > 0 else 1307.0
        default_ip_inef = float(conc_data['P_IP_Inef'].median()) if len(conc_data) > 0 else 991.0
        default_led = float(conc_data['LED_Ratio'].median()) if len(conc_data) > 0 else 0.24
        default_lum = int(conc_data['N_Luminarias'].median()) if len(conc_data) > 0 else 21315
        default_lamp = int(conc_data['N_Lampadas'].median()) if len(conc_data) > 0 else 21286

        p_ip_total = st.number_input(
            "Potencia IP Total (W)", value=default_ip_total, step=100.0,
        )
        p_ip_inef = st.number_input(
            "Potencia IP Ineficiente (W)", value=default_ip_inef, step=50.0,
        )
        led_ratio = st.slider(
            "Ratio LED",
            min_value=0.0, max_value=1.0, value=default_led, step=0.01,
        )
        n_luminarias = st.number_input(
            "N. Luminarias", value=default_lum, step=100,
        )
        n_lampadas = st.number_input(
            "N. Lampadas", value=default_lamp, step=100,
        )

    # Encode location
    if distrito in le_distrito.classes_:
        distrito_enc = int(le_distrito.transform([distrito])[0])
    else:
        distrito_enc = 0
    if concelho in le_concelho.classes_:
        concelho_enc = int(le_concelho.transform([concelho])[0])
    else:
        concelho_enc = 0


X_input = pd.DataFrame([{
    'Potência instalada [kVA]': potencia,
    'N_Clientes':               n_clientes,
    'P_IP_Total':               p_ip_total,
    'P_IP_Inef':                p_ip_inef,
    'LED_Ratio':                led_ratio,
    'N_Luminarias':             n_luminarias,
    'N_Lampadas':               n_lampadas,
    'Cap_per_Cliente':          cap_per_cli_val,
    'Distrito_enc':             distrito_enc,
    'Concelho_enc':             concelho_enc,
}])

X_scaled = pd.DataFrame(
    scaler.transform(X_input),
    columns=FEATURE_COLS,
)

# Regression predictions
folga_lr = float(model_lr.predict(X_scaled)[0])
folga_tree = float(model_tree.predict(X_scaled)[0])
folga_avg = (folga_lr + folga_tree) / 2

# Classification from regression output
util_decimal_pred = derive_util_decimal(folga_avg, potencia)
classe_util, classe_icon = classify_utilization(util_decimal_pred, q33, q66)

# Charger simulation
total_charger_load = n_chargers * charger_power * utilization_factor
folga_after_chargers = folga_avg - total_charger_load
viable = folga_after_chargers > 0


st.markdown("---")
st.header("Resultados da Previsao")

# Row 1: Core predictions
r1c1, r1c2, r1c3, r1c4 = st.columns(4)

with r1c1:
    st.metric(
        "Folga Prevista (Linear)",
        f"{folga_lr:.1f} kVA",
    )
with r1c2:
    st.metric(
        "Folga Prevista (Árvore)",
        f"{folga_tree:.1f} kVA",
    )
with r1c3:
    st.metric(
        "Folga Media",
        f"{folga_avg:.1f} kVA",
        help="Media das previsoes dos dois modelos disponiveis.",
    )
with r1c4:
    st.metric(
        "Utilizacao da Rede",
        f"{util_decimal_pred:.1%}",
        delta=f"Classe: {classe_util}",
        delta_color="inverse" if classe_util == "alto" else ("off" if classe_util == "medio" else "normal"),
    )

# Row 2: Classification context
st.caption(
    f"Limiares de classificacao (quantis do dataset): "
    f"baixo <= {q33:.3f}  |  medio <= {q66:.3f}  |  alto > {q66:.3f}"
)

# Row 3: Charger simulation
st.markdown("---")
st.header("Simulacao de Carregadores VE")

sim1, sim2, sim3 = st.columns(3)

with sim1:
    st.metric(
        "Carga Total dos Carregadores",
        f"{total_charger_load:.1f} kW",
        help=f"{n_chargers}x {charger_type} x {utilization_factor:.0%} utilizacao",
    )
with sim2:
    st.metric(
        "Folga Residual Após Carregadores",
        f"{folga_after_chargers:.1f} kVA",
        delta=f"-{total_charger_load:.1f} kVA",
        delta_color="normal" if viable else "inverse",
    )
with sim3:
    max_chargers = max(0, int(folga_avg / (charger_power * utilization_factor)))
    st.metric(
        "Máx. Carregadores Suportados",
        f"{max_chargers}",
        help=f"Com {charger_type} a {utilization_factor:.0%} utilizacao simultanea.",
    )

# Viability assessment
if viable:
    remaining_pct = (folga_after_chargers / potencia) * 100 if potencia > 0 else 0
    if folga_after_chargers > 100:
        st.success(
            f"Viavel: {n_chargers} carregadores com folga confortavel "
            f"de {folga_after_chargers:.1f} kVA ({remaining_pct:.0f}% da capacidade)."
        )
    elif folga_after_chargers > 30:
        st.warning(
            f"Viavel com cuidado: {n_chargers} carregadores possiveis mas "
            f"com margem reduzida de {folga_after_chargers:.1f} kVA ({remaining_pct:.0f}%). "
            f"Recomenda-se monitorizacao."
        )
    else:
        st.warning(
            f"Margem critica: Apenas {folga_after_chargers:.1f} kVA "
            f"({remaining_pct:.0f}%) de margem restante. "
            f"Considerar reduzir o numero de carregadores."
        )
else:
    deficit = abs(folga_after_chargers)
    st.error(
        f"Inviavel: {n_chargers} carregadores excedem a folga disponivel "
        f"em {deficit:.1f} kVA. "
        f"Maximo suportado: {max_chargers} carregadores deste tipo."
    )

# Progress bar for capacity usage
st.markdown("---")
st.subheader("Utilizacao da Capacidade do PTD")

if potencia > 0:
    carga_base_pct = util_decimal_pred
    carga_ve_pct = total_charger_load / potencia
    total_pct = min(carga_base_pct + carga_ve_pct, 1.0)

    bar1, bar2 = st.columns([3, 1])
    with bar1:
        st.progress(
            min(total_pct, 1.0),
            text=f"Utilizacao total: {total_pct:.1%} "
                 f"(Base: {carga_base_pct:.1%} + VE: {carga_ve_pct:.1%})",
        )
    with bar2:
        capacity_remaining = max(0, potencia - (potencia * carga_base_pct) - total_charger_load)
        st.metric("Capacidade Livre", f"{capacity_remaining:.0f} kVA")

# Model info expander
with st.expander("Informacao do Modelo"):
    st.markdown(f"**Perfil ativo:** {profile_label}")
    st.markdown("**Modelos de regressao disponiveis:** Regressao Linear, Arvore de Decisao")
    st.markdown(
        "Os modelos foram treinados com validacao cruzada k-fold. "
        "Apenas os modelos Linear e Arvore de Decisao foram persistidos como "
        "objetos sklearn; os restantes (SVM, NN, KNN) foram guardados apenas "
        "como metricas de avaliacao."
    )
    st.markdown("#### Metricas de Regressao (k-fold CV)")
    metrics_data = []
    for name, res in reg_results.items():
        metrics_data.append({
            'Modelo': name,
            'MAE': f"{res['mae_mean']:.2f} ± {res['mae_std']:.2f}",
            'RMSE': f"{res['rmse_mean']:.2f} ± {res['rmse_std']:.2f}",
        })
    st.dataframe(pd.DataFrame(metrics_data), use_container_width=True, hide_index=True)

    st.markdown("#### Metricas de Classificacao (k-fold CV)")
    clf_data = []
    for name, res in clf_results.items():
        clf_data.append({
            'Modelo': name,
            'Accuracy': f"{res['Accuracy_mean']:.4f} ± {res['Accuracy_std']:.4f}",
            'F1': f"{res['F1_mean']:.4f} ± {res['F1_std']:.4f}",
        })
    st.dataframe(pd.DataFrame(clf_data), use_container_width=True, hide_index=True)