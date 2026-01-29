import streamlit as st

st.set_page_config(page_title="Calculadora de Cotas PVE/PV de Projeto", layout="wide")

if 'res' not in st.session_state:
    st.session_state.res = {
        'cf_pve1': 0.0, 'cf_pve2': 0.0, 'diff_cota': 0.0,
        'declividade': 0.0, 'desnivel_parcial': 0.0,
        'cf_pvp': 0.0, 'p_pvp': 0.0, 'calculado': False
    }

st.title("📏 Calculadora de Cotas Integrada")
st.markdown("Insira os dados técnicos para atualizar os campos de resultado.")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.info("📍 PVE 1")
    pve1_ct = st.number_input("Cota de Tampa (CT)", value=0.0, format="%.5f", key="ct1")
    pve1_ch = st.number_input("Chaminé (CH)", value=0.0, format="%.5f", key="ch1")
    pve1_p = st.number_input("Profundidade (P)", value=0.0, format="%.5f", key="p1")
    st.number_input("Resultado: Cota de Fundo (CF)", value=st.session_state.res['cf_pve1'], format="%.5f", disabled=True, key="disp_cf1")

with col2:
    st.info("📍 PVE 2")
    pve2_ct = st.number_input("Cota de Tampa (CT)", value=0.0, format="%.5f", key="ct2")
    pve2_ch = st.number_input("Chaminé (CH)", value=0.0, format="%.5f", key="ch2")
    pve2_p = st.number_input("Profundidade (P)", value=0.0, format="%.5f", key="p2")
    st.number_input("Resultado: Cota de Fundo (CF)", value=st.session_state.res['cf_pve2'], format="%.5f", disabled=True, key="disp_cf2")

with col3:
    st.info("📐 PV de Projeto")
    pvp_ct = st.number_input("Cota de Tampa (CT)", value=0.0, format="%.5f", key="ct_pvp")
    st.number_input("Resultado: Cota de Fundo (CF)", value=st.session_state.res['cf_pvp'], format="%.5f", disabled=True, key="disp_cf_pvp")
    st.number_input("Resultado: Profundidade (P)", value=st.session_state.res['p_pvp'], format="%.5f", disabled=True, key="disp_p_pvp")

st.divider()

c1, c2 = st.columns(2)
with c1:
    st.info("🛣️ Distâncias")
    dist_pve1_pve2 = st.number_input("Distância PVE1 ↔ PVE2", value=0.0, format="%.5f", key="d12")
    dist_pve1_pvp = st.number_input("Distância PVE1 ↔ PV de Projeto", value=0.0, format="%.5f", key="d1p")

with c2:
    st.info("📊 Parâmetros de Cálculo")
    st.text_input("Diferença de Cota (m)", value=f"{st.session_state.res['diff_cota']:.5f}", disabled=True, key="view_diff")
    st.text_input("Declividade (m/m)", value=f"{st.session_state.res['declividade']:.5f}", disabled=True, key="view_decliv")
    st.text_input("Desnível Parcial (m)", value=f"{st.session_state.res['desnivel_parcial']:.5f}", disabled=True, key="view_desnivel")

st.divider()

if st.button("Calcular e Atualizar Campos", type="primary", use_container_width=True):
    try:
        if dist_pve1_pve2 == 0:
            st.error("A distância entre PVE1 e PVE2 não pode ser zero.")
        else:
            cf1 = (pve1_ct - pve1_ch) - (pve1_p - pve1_ch)
            cf2 = (pve2_ct - pve2_ch) - (pve2_p - pve2_ch)
            diff = cf1 - cf2
            decliv = diff / dist_pve1_pve2
            desnivel = decliv * dist_pve1_pvp
            cf_proj = cf1 - desnivel
            p_proj = pvp_ct - cf_proj

            st.session_state.res = {
                'cf_pve1': cf1,
                'cf_pve2': cf2,
                'diff_cota': diff,
                'declividade': decliv,
                'desnivel_parcial': desnivel,
                'cf_pvp': cf_proj,
                'p_pvp': p_proj,
                'calculado': True
            }
            
            st.rerun()

    except Exception as e:
        st.error(f"Erro: {e}")

if st.session_state.res['calculado'] and st.session_state.res['p_pvp'] < 0:
    st.warning("Atenção: A profundidade do PV de Projeto calculada é negativa.")