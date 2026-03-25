import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import scipy.stats as stats
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
import seaborn as sns
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Dashboard", layout="wide")

@st.cache_data
def load_data():
    ip_data  = pd.read_excel("./data/IP_data.xlsx")
    ptd_data = pd.read_excel("./data/PTD_data.xlsx")

    ip_data["Is_Ineficiente"] = ip_data["Tipo de Lâmpada"].apply(
        lambda t: int(t in ["Sódio", "Mercúrio"])
    )
    ip_data["Pot_Kw"] = ip_data["Potência Instalada Total (W)"] / 1000

    p_ip_total = ip_data.groupby("CodDistritoConcelho")["Pot_Kw"].sum()
    p_ip_inef  = (
        ip_data[ip_data["Is_Ineficiente"] == 1]
        .groupby("CodDistritoConcelho")["Pot_Kw"]
        .sum()
    )
    concelhos = ip_data.groupby("CodDistritoConcelho")["Concelho"].first()

    result = pd.DataFrame({
        "Concelho":    concelhos,
        "P_IP_Total":  p_ip_total,
        "P_IP_Inef":   p_ip_inef,
    }).fillna(0)

    def parse_usage(u):
        if pd.isna(u):       return np.nan
        if u == "+100%":     return 1.0
        if "-" in str(u):    return int(str(u).split("-")[1].removesuffix("%")) / 100
        return np.nan

    ptd_data["Nível de Utilização [%]"] = ptd_data["Nível de Utilização [%]"].apply(parse_usage)

    ptd_stats = ptd_data.groupby("CodDistritoConcelho").agg(
        Cap_PTD    = ("Potência instalada [kVA]",  "sum"),
        Util_Media = ("Nível de Utilização [%]",   "mean"),
        N_PTDs     = ("CodDistritoConcelho",        "count"),
    )

    LED_SAVINGS = 0.65
    GRID_MARGIN = 0.92
    EV_KW       = 22
    EV_SIMULT   = 0.60

    df = pd.DataFrame(index=p_ip_inef.index)
    df["Concelho"]                  = concelhos
    df["P_IP_Total"]                = p_ip_total
    df["P_IP_Inef"]                 = p_ip_inef
    df["Ganho LED"]                 = p_ip_inef * LED_SAVINGS
    df["Cap_PTD"]                   = ptd_stats["Cap_PTD"]
    df["Util_Media"]                = ptd_stats["Util_Media"]
    df["N_PTDs"]                    = ptd_stats["N_PTDs"]
    df["Folga Rede"]                = (ptd_stats["Cap_PTD"] * GRID_MARGIN) * (1 - ptd_stats["Util_Media"])
    df["Carga VE"]                  = ptd_stats["N_PTDs"] * EV_KW * EV_SIMULT
    df["Saldo Final de Viabilidade"]= df["Folga Rede"] + df["Ganho LED"] - df["Carga VE"]
    df["Rate Ineficiencia"]         = p_ip_inef / p_ip_total
    df["CodDistrito"]               = df.index // 100

    return ip_data, ptd_data, ptd_stats, result, df

MAPA_DISTRITOS = {
    1:"Aveiro", 2:"Beja", 3:"Braga", 4:"Bragança", 5:"Castelo Branco",
    6:"Coimbra", 7:"Évora", 8:"Faro", 9:"Guarda", 10:"Leiria",
    11:"Lisboa", 12:"Portalegre", 13:"Porto", 14:"Santarém",
    15:"Setúbal", 16:"Viana do Castelo", 17:"Vila Real", 18:"Viseu",
}

ip_data, ptd_data, ptd_stats, result, df = load_data()
df["Distrito"] = df["CodDistrito"].map(MAPA_DISTRITOS)

st.sidebar.title("Dashboard Analítico")
page = st.sidebar.radio("Navegar", [
    "Visão Geral",
    "Perfis Horários",
    "Mix Tecnológico",
    "Capacidade PTD",
    "Potência Libertada",
    "Cenários VE",
    "Inferência Estatística",
    "Modelo Preditivo & Correl.",
    "Mapa Interativo"
])

if page == "Visão Geral":
    st.title("Visão Geral da Rede")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de Concelhos",    f"{len(df)}")
    col2.metric("Total PTDs",            f"{int(df['N_PTDs'].sum()):,}")
    col3.metric("Capacidade Total (kVA)",f"{int(df['Cap_PTD'].sum()):,}")
    col4.metric("Ocupação Média",        f"{df['Util_Media'].mean():.1%}")

    st.divider()
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Distribuição de Ocupação Média por Distrito")
        por_dist = df.groupby("Distrito")["Util_Media"].mean().sort_values().dropna()
        fig, ax = plt.subplots(figsize=(6, 6))
        cores = ["#e74c3c" if v > 0.6 else "#f39c12" if v > 0.5 else "#2ecc71" for v in por_dist]
        ax.barh(por_dist.index, por_dist.values, color=cores, alpha=0.85)
        ax.axvline(0.6, color="red", linestyle="--", linewidth=1.2, label="Patamar 60%")
        ax.axvline(por_dist.mean(), color="navy", linestyle="--", linewidth=1.2, label="Média")
        ax.set_xlabel("Ocupação Média")
        ax.legend(fontsize=8)
        ax.grid(axis="x", linestyle="--", alpha=0.4)
        st.pyplot(fig)
        plt.close()

    with col_b:
        st.subheader("Saldo de Viabilidade VE — Top 15 concelhos")
        top15 = df.nlargest(15, "Saldo Final de Viabilidade").dropna(subset=["Concelho"])
        fig, ax = plt.subplots(figsize=(6, 6))
        cores2 = ["#2ecc71" if v > 0 else "#e74c3c" for v in top15["Saldo Final de Viabilidade"]]
        ax.barh(top15["Concelho"].astype(str), top15["Saldo Final de Viabilidade"], color=cores2, alpha=0.85)
        ax.axvline(0, color="red", linestyle="--", linewidth=1)
        ax.set_xlabel("Saldo (kVA)")
        ax.grid(axis="x", linestyle="--", alpha=0.4)
        st.pyplot(fig)
        plt.close()

elif page == "Perfis Horários":
    st.title("Perfis Horários de Consumo de Iluminação Pública (simulado)")
    distrito_sel = st.selectbox("Distrito", sorted(MAPA_DISTRITOS.values()))
    led_factor   = st.slider("Fator poupança LED (%)", 50, 90, 65, step=5) / 100

    cod_dist = [k for k, v in MAPA_DISTRITOS.items() if v == distrito_sel][0]
    df_dist  = df[df["CodDistrito"] == cod_dist]
    p_total  = df_dist["P_IP_Total"].sum()
    p_led    = p_total * (1 - led_factor)

    horas  = list(range(24))
    perfil = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.8, 0.3, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.8, 1.0, 1.0, 1.0, 1.0]

    consumo_antes  = [p_total * f for f in perfil]
    consumo_depois = [p_led   * f for f in perfil]

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.fill_between(horas, consumo_antes,  alpha=0.3, color="#e74c3c", label="Antes (convencional)")
    ax.fill_between(horas, consumo_depois, alpha=0.3, color="#2ecc71", label="Depois (LED)")
    ax.plot(horas, consumo_antes,  color="#e74c3c", linewidth=2)
    ax.plot(horas, consumo_depois, color="#2ecc71", linewidth=2)
    ax.set_xticks(horas)
    ax.set_xticklabels([f"{h}h" for h in horas], fontsize=8)
    ax.set_xlabel("Hora do dia")
    ax.set_ylabel("Potência (kW)")
    ax.legend()
    ax.grid(linestyle="--", alpha=0.4)

    poupanca = sum(consumo_antes) - sum(consumo_depois)
    st.pyplot(fig)
    plt.close()

    col1, col2, col3 = st.columns(3)
    col1.metric("Consumo diário antes (kWh)",  f"{sum(consumo_antes):,.0f}")
    col2.metric("Consumo diário depois (kWh)", f"{sum(consumo_depois):,.0f}")
    col3.metric("Poupança diária (kWh)",       f"{poupanca:,.0f}")

elif page == "Mix Tecnológico":
    st.title("Mix Tecnológico. LED vs Convencional")
    col1, col2, col3 = st.columns(3)
    total_inef = df["P_IP_Inef"].sum()
    total_ip   = df["P_IP_Total"].sum()
    col1.metric("Potência Total IP (kW)",      f"{total_ip:,.0f}")
    col2.metric("Potência Ineficiente (kW)",   f"{total_inef:,.0f}")
    col3.metric("Rácio de Ineficiência",       f"{total_inef/total_ip:.1%}")

    st.divider()
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Mix nacional")
        fig, ax = plt.subplots(figsize=(5, 5))
        eficiente = total_ip - total_inef
        ax.pie([total_inef, eficiente], labels=[f"Ineficiente\n{total_inef/total_ip:.1%}", f"Eficiente (LED)\n{eficiente/total_ip:.1%}"],
               colors=["#e74c3c", "#2ecc71"], autopct="%1.1f%%", startangle=90)
        st.pyplot(fig)
        plt.close()

    with col_b:
        st.subheader("Rácio de ineficiência por distrito")
        por_dist2 = df.groupby("Distrito")[["P_IP_Inef","P_IP_Total"]].sum().assign(Pct_Inef=lambda x: x["P_IP_Inef"] / x["P_IP_Total"] * 100).sort_values("Pct_Inef").dropna()
        fig, ax = plt.subplots(figsize=(5, 6))
        cores3 = ["#e74c3c" if p > 20 else "#f39c12" if p > 10 else "#2ecc71" for p in por_dist2["Pct_Inef"]]
        bars = ax.barh(por_dist2.index, por_dist2["Pct_Inef"], color=cores3, alpha=0.85)
        ax.axvline(por_dist2["Pct_Inef"].mean(), color="navy", linestyle="--", label=f"Média: {por_dist2['Pct_Inef'].mean():.1f}%")
        ax.set_xlabel("% Potência Ineficiente")
        ax.legend(fontsize=8)
        st.pyplot(fig)
        plt.close()

elif page == "Capacidade PTD":
    st.title("Capacidade Instalada e Disponível nos PTDs")
    distrito_sel = st.selectbox("Filtrar por distrito", ["Todos"] + sorted(MAPA_DISTRITOS.values()))

    df_filt = df.copy()
    if distrito_sel != "Todos":
        df_filt = df_filt[df_filt["Distrito"] == distrito_sel]

    col1, col2, col3 = st.columns(3)
    col1.metric("Capacidade Total (kVA)",    f"{df_filt['Cap_PTD'].sum():,.0f}")
    col2.metric("Folga Disponível (kVA)",    f"{df_filt['Folga Rede'].sum():,.0f}")
    col3.metric("Ocupação Média",            f"{df_filt['Util_Media'].mean():.1%}")

    st.divider()
    st.subheader("Distribuição de ocupação por distrito")
    ptd_clean = ptd_data.dropna(subset=["Nível de Utilização [%]"]).copy()
    ptd_clean["CodDistrito"] = ptd_clean["CodDistritoConcelho"] // 100
    mapa4 = {1:"Aveiro", 11:"Lisboa", 13:"Porto", 15:"Setúbal"}
    ptd_alvo = ptd_clean[ptd_clean["CodDistrito"].isin(mapa4)].copy()
    ptd_alvo["Distrito"] = ptd_alvo["CodDistrito"].map(mapa4)

    fig, ax = plt.subplots(figsize=(10, 5))
    ptd_alvo.boxplot(column="Nível de Utilização [%]", by="Distrito", ax=ax, patch_artist=True, boxprops=dict(facecolor="lightblue"))
    plt.suptitle("")
    ax.set_title("")
    ax.set_ylabel("Nível de Utilização")
    st.pyplot(fig)
    plt.close()

elif page == "Potência Libertada":
    st.title("Estimativa de Potência Libertada pela Eficiência LED")
    led_factor = st.slider("Fator de poupança LED (%)", 50, 90, 65, step=5) / 100

    df_led = df.copy()
    df_led["Ganho LED Sim"] = df_led["P_IP_Inef"] * led_factor
    df_led["Folga Total"]   = df_led["Folga Rede"] + df_led["Ganho LED Sim"]

    col1, col2, col3 = st.columns(3)
    col1.metric("Ganho LED Total (kW)",       f"{df_led['Ganho LED Sim'].sum():,.0f}")
    col2.metric("Folga Total c/ LED (kVA)",   f"{df_led['Folga Total'].sum():,.0f}")
    col3.metric("Fator utilizado",            f"{led_factor:.0%}")

    st.divider()
    st.subheader("Antes vs Depois — Folga da rede (Top 10)")
    top10 = df_led.nlargest(10, "Ganho LED Sim").dropna(subset=["Concelho"])
    x = np.arange(len(top10))
    w = 0.35
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(x - w/2, top10["Folga Rede"], w, label="Folga sem LED", color="steelblue", alpha=0.85)
    ax.bar(x + w/2, top10["Folga Total"], w, label="Folga com LED", color="#2ecc71",  alpha=0.85)
    ax.set_xticks(x)
    ax.set_xticklabels(top10["Concelho"].astype(str), rotation=45, ha="right")
    ax.legend()
    st.pyplot(fig)
    plt.close()

elif page == "Cenários VE":
    st.title("Cenários de Integração de Carregadores VE")

    col_ctrl1, col_ctrl2, col_ctrl3 = st.columns(3)
    ev_kw      = col_ctrl1.slider("Potência por carregador (kW)", 7, 150, 22, step=1)
    ev_simult  = col_ctrl2.slider("Fator de simultaneidade (%)",  10, 100, 60, step=5) / 100
    led_factor = col_ctrl3.slider("Fator poupança LED (%)",       50,  90, 65, step=5) / 100

    df_ev = df.copy()
    df_ev["Ganho LED Sim"]  = df_ev["P_IP_Inef"] * led_factor
    df_ev["Carga VE Sim"]   = df_ev["N_PTDs"] * ev_kw * ev_simult
    df_ev["Saldo Sim"]      = df_ev["Folga Rede"] + df_ev["Ganho LED Sim"] - df_ev["Carga VE Sim"]
    df_ev["Viavel"]         = df_ev["Saldo Sim"] > 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Concelhos Viáveis",         f"{df_ev['Viavel'].sum()} / {len(df_ev)}")
    col2.metric("Saldo Total Positivo (kVA)",f"{df_ev[df_ev['Viavel']]['Saldo Sim'].sum():,.0f}")
    col3.metric("Carga VE Total (kVA)",      f"{df_ev['Carga VE Sim'].sum():,.0f}")

    st.divider()
    st.subheader("Top 10 concelhos mais viáveis")
    top10_ev = df_ev[df_ev["Viavel"]].nlargest(10, "Saldo Sim").dropna(subset=["Concelho"])[["Concelho","Util_Media","Folga Rede","Ganho LED Sim","Carga VE Sim","Saldo Sim"]]
    st.dataframe(top10_ev, use_container_width=True)

elif page == "Inferência Estatística":
    st.title("Robustez da Inferência Estatística")
    st.markdown("""
    Para garantir que os resultados dos testes de hipótese (realizados no Jupyter Notebook) não dependem de uma seleção aleatória de dados específica, corremos os mesmos testes repetidamente alterando a *seed* geradora.
    """)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.info("**Configurações dos Testes**")
        alpha = st.select_slider("Nível de Significância ($\alpha$)", options=[0.01, 0.05, 0.10], value=0.05)
        num_seeds = st.slider("Número de Seeds a testar", min_value=10, max_value=100, value=50, step=10)

    def fast_testes(seed, alpha):
        amostra1 = ptd_stats.sample(n=50, random_state=seed)['Util_Media']
        if stats.shapiro(amostra1).pvalue < alpha:
            res1 = None
        else:
            res1 = stats.ttest_1samp(amostra1, 0.60, alternative='less').pvalue >= alpha

        mediana = df['Rate Ineficiencia'].median()
        amostra_mod = df[df['Rate Ineficiencia'] <= mediana].sample(n=30, random_state=seed)['Util_Media']
        amostra_inef = df[df['Rate Ineficiencia'] > mediana].sample(n=30, random_state=seed)['Util_Media']
        
        if stats.shapiro(amostra_mod).pvalue < alpha or stats.shapiro(amostra_inef).pvalue < alpha:
            res2 = None
        else:
            eq_var = stats.levene(amostra_mod, amostra_inef).pvalue >= alpha
            res2 = stats.ttest_ind(amostra_mod, amostra_inef, equal_var=eq_var).pvalue >= alpha

        norte = df[df['CodDistrito'].isin([6, 3, 13])].sample(n=25, random_state=seed, replace=True)['Util_Media']
        sul = df[df['CodDistrito'].isin([11, 15, 1])].sample(n=25, random_state=seed, replace=True)['Util_Media']
        inter = df[df['CodDistrito'].isin([7, 2, 12])].sample(n=25, random_state=seed, replace=True)['Util_Media']
        
        if stats.shapiro(norte).pvalue < alpha or stats.shapiro(sul).pvalue < alpha or stats.shapiro(inter).pvalue < alpha:
            res3 = None
        else:
            res3 = stats.f_oneway(norte, sul, inter).pvalue >= alpha
            
        return res1, res2, res3

    # Executar Loop de seeds
    res_1, res_2, res_3 = [], [], []
    for s in range(1, num_seeds + 1):
        r1, r2, r3 = fast_testes(s, alpha)
        res_1.append(r1); res_2.append(r2); res_3.append(r3)

    def get_colors(res_list):
        return ["orange" if v is None else ("green" if v else "red") for v in res_list]

    st.divider()
    st.subheader("Resultados ao longo de múltiplas amostragens")
    
    fig, axes = plt.subplots(3, 1, figsize=(10, 6), sharex=True)
    titulos = ["T-Test (Ocupação < 60%)", "T-Test (Mod. vs Ineficientes)", "ANOVA (3 Macro-regiões)"]
    
    for ax, res_list, titulo in zip(axes, [res_1, res_2, res_3], titulos):
        ax.bar(range(1, num_seeds + 1), [1] * num_seeds, color=get_colors(res_list), width=1)
        ax.set_ylabel(titulo, fontsize=9)
        ax.set_yticks([])
        ax.set_xlim(0.5, num_seeds + 0.5)

    from matplotlib.patches import Patch
    legenda = [
        Patch(color="green",  label="Não rejeita H0 (Hipótese Nula)"),
        Patch(color="red",    label="Rejeita H0"),
        Patch(color="orange", label="Dados não normais (Teste Invalido)"),
    ]
    fig.legend(handles=legenda, loc="upper right", bbox_to_anchor=(0.9, 0.95))
    axes[-1].set_xlabel("Número da Seed (Amostragem)")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()


elif page == "Modelo Preditivo & Correl.":
    st.title("Correlação e Modelo Preditivo (Regressão Múltipla)")
    
    # Preparar Dados para a Regressão
    distritos_alvo = [1, 3, 11, 13] # Aveiro, Braga, Lisboa, Porto
    df_reg = df[df["CodDistrito"].isin(distritos_alvo)].copy()
    df_reg = df_reg.dropna(subset=['Util_Media', 'P_IP_Total', 'Cap_PTD', 'Rate Ineficiencia'])
    
    Y = df_reg['Util_Media']
    X = df_reg[['P_IP_Total', 'Cap_PTD', 'Rate Ineficiencia']]
    
    # Matriz de correlação
    st.subheader("Matriz de Correlação Linear (Pearson)")
    col1, col2 = st.columns([2, 1])
    with col1:
        corr_matrix = df_reg[['Util_Media', 'P_IP_Total', 'Cap_PTD', 'Rate Ineficiencia']].corr()
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", vmin=-1, vmax=1, ax=ax, fmt=".2f")
        st.pyplot(fig)
        plt.close()
    with col2:
        st.info("""
        **Observação:** Existe uma fortíssima colinearidade (0.91) entre a *Capacidade do PTD* e a *Potência Total IP*.
        Isto faz sentido, pois PTDs de maior capacidade são instalados em zonas que requerem mais iluminação.
        """)

    st.divider()

    # VIF e Modelo OLS
    col_vif, col_ols = st.columns(2)
    
    X_const = sm.add_constant(X)
    modelo = sm.OLS(Y, X_const).fit()

    with col_vif:
        st.subheader("Multicolinearidade (VIF)")
        vif_data = pd.DataFrame()
        vif_data["Variável"] = X.columns
        vif_data["VIF"] = [variance_inflation_factor(X_const.values, i+1) for i in range(X.shape[1])]
        st.dataframe(vif_data.style.format({"VIF": "{:.2f}"}), use_container_width=True)
        st.warning("Variáveis com VIF > 5 indicam problemas de multicolinearidade. A *Potência IP Total* e a *Cap_PTD* partilham demasiada informação.")

    with col_ols:
        st.subheader("Modelo OLS")
        st.metric("R-Squared (Ajustado)", f"{modelo.rsquared_adj:.3f}")
        st.metric("Probabilidade F-Statistic", f"{modelo.f_pvalue:.4f}")
        st.write("**P-Values dos Coeficientes:**")
        pvals = pd.DataFrame({"P-Value": modelo.pvalues[1:]}).style.format("{:.3f}")
        st.dataframe(pvals, use_container_width=True)
        
    st.divider()

    # SIMULADOR PREDITIVO
    st.subheader("Simulador Preditivo de Ocupação da Rede")
    st.markdown("Altere os valores abaixo para prever qual seria a **Ocupação Média** da rede para um Concelho hipotético nos distritos estudados.")
    
    sim_col1, sim_col2, sim_col3 = st.columns(3)
    val_ip = sim_col1.number_input("Potência Total IP (kW)", value=float(X["P_IP_Total"].mean()), step=100.0)
    val_ptd = sim_col2.number_input("Capacidade PTD (kVA)", value=float(X["Cap_PTD"].mean()), step=10000.0)
    val_inef = sim_col3.slider("Rácio Ineficiência (%)", 0, 100, int(X["Rate Ineficiencia"].mean()*100)) / 100

    novo_dado = pd.DataFrame({'const': 1, 'P_IP_Total': [val_ip], 'Cap_PTD': [val_ptd], 'Rate Ineficiencia': [val_inef]})
    previsao = modelo.predict(novo_dado).values[0]
    
    st.success(f"### Ocupação Prevista do Transformador: **{previsao:.1%}**")

elif page == "Mapa Interativo":
    st.title("Mapa das Zonas Analisadas")

    def parse_coords(coord_str):
        try:
            lat, lon = str(coord_str).split(",")
            return float(lat.strip()), float(lon.strip())
        except:
            return None, None

    ptd_map = ptd_data.copy()
    ptd_map[["lat","lon"]] = ptd_map["Coordenadas Geográficas"].apply(lambda x: pd.Series(parse_coords(x)))
    ptd_map = ptd_map.dropna(subset=["lat","lon"])

    df_ev_map = df.copy()
    df_ev_map["Ganho LED Sim"] = df_ev_map["P_IP_Inef"] * 0.65
    df_ev_map["Carga VE Sim"]  = df_ev_map["N_PTDs"] * 22 * 0.60
    df_ev_map["Saldo Sim"]     = df_ev_map["Folga Rede"] + df_ev_map["Ganho LED Sim"] - df_ev_map["Carga VE Sim"]
    df_ev_map["Viavel"]        = df_ev_map["Saldo Sim"] > 0

    ptd_map = ptd_map.merge(df_ev_map[["Viavel","Util_Media","Saldo Sim"]].reset_index(), on="CodDistritoConcelho", how="left")

    col1, col2 = st.columns(2)
    mostrar_ptd      = col1.checkbox("Mostrar PTDs", value=True)
    mostrar_viaveis  = col2.checkbox("Mostrar apenas concelhos viáveis", value=False)
    sample_size = st.slider("Número de PTDs a mostrar (por segurança da performance)", 100, 5000, 1000, step=100)
    
    ptd_sample = ptd_map.sample(min(sample_size, len(ptd_map)), random_state=42)
    if mostrar_viaveis:
        ptd_sample = ptd_sample[ptd_sample["Viavel"] == True]

    m = folium.Map(location=[39.5, -8.0], zoom_start=7, tiles="CartoDB positron")

    for _, row in ptd_sample.iterrows():
        if pd.isna(row.get("Viavel")): cor = "gray"
        elif row["Viavel"]: cor = "green"
        else: cor = "red"

        util = f"{row['Util_Media']:.1%}" if pd.notna(row.get("Util_Media")) else "N/D"
        saldo = f"{row['Saldo Sim']:,.0f} kVA" if pd.notna(row.get("Saldo Sim")) else "N/D"

        folium.CircleMarker(
            location=[row["lat"], row["lon"]], radius=4, color=cor, fill=True, fill_color=cor, fill_opacity=0.7,
            popup=folium.Popup(f"<b>{row.get('Concelho','N/D')}</b><br>Ocupação: {util}<br>Saldo VE: {saldo}<br>{'✅ Viável para VE' if row.get('Viavel') else '❌ Inviável'}", max_width=200)
        ).add_to(m)

    legenda = """
    <div style="position: fixed; bottom: 30px; left: 30px; z-index: 1000; background: white; padding: 10px; border-radius: 8px; border: 1px solid #ccc; font-size: 12px;">
        <b>Legenda</b><br>
        <span style="color:green">●</span> Viável para VE<br>
        <span style="color:red">●</span> Inviável<br>
        <span style="color:gray">●</span> Sem dados
    </div>
    """
    m.get_root().html.add_child(folium.Element(legenda))
    st_folium(m, width="100%", height=600, returned_objects=[])