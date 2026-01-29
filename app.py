import streamlit as st

st.set_page_config(page_title="Calculadora de Cotas PVE/PV de Projeto", layout="centered")

st.title("📏 Calculadora de Cotas e Declividade")
st.markdown("Cálculo de Cota de Fundo ($CF$) e Profundidade ($P$) para PVEs e PVs de Projeto.")

st.divider()

st.subheader("📝 Dados de Entrada")

col1, col2 = st.columns(2)

with col1:
    st.info("📍 PVE 1")
    pve1_ct = st.number_input("PVE 1: Cota de Tampa (CT)", value=0.0, format="%.3f", key="ct1")
    pve1_ch = st.number_input("PVE 1: Chaminé (CH)", value=0.0, format="%.3f", key="ch1")
    pve1_p = st.number_input("PVE 1: Profundidade (P)", value=0.0, format="%.3f", key="p1")

with col2:
    st.info("📍 PVE 2")
    pve2_ct = st.number_input("PVE 2: Cota de Tampa (CT)", value=0.0, format="%.3f", key="ct2")
    pve2_ch = st.number_input("PVE 2: Chaminé (CH)", value=0.0, format="%.3f", key="ch2")
    pve2_p = st.number_input("PVE 2: Profundidade (P)", value=0.0, format="%.3f", key="p2")

st.divider()

col3, col4 = st.columns(2)

with col3:
    st.info("📐 PV de Projeto")
    pvp_ct = st.number_input("PV de Projeto: Cota de Tampa (CT)", value=0.0, format="%.3f", key="ct_pvp")

with col4:
    st.info("🛣️ Distâncias")
    dist_pve1_pve2 = st.number_input("Distância PVE1 ↔ PVE2", value=0.0, format="%.2f", key="d12")
    dist_pve1_pvp = st.number_input("Distância PVE1 ↔ PV de Projeto", value=0.0, format="%.2f", key="d1p")

st.divider()

if st.button("Executar Cálculos", type="primary", use_container_width=True):
    try:
        cf_pve1 = (pve1_ct - pve1_ch) - (pve1_p - pve1_ch)
        cf_pve2 = (pve2_ct - pve2_ch) - (pve2_p - pve2_ch)
        diff_cota = cf_pve1 - cf_pve2
        
        if dist_pve1_pve2 == 0:
            st.error("A distância entre PVE1 e PVE2 não pode ser zero.")
            st.stop()
        
        declividade = diff_cota / dist_pve1_pve2
        desnivel_parcial = declividade * dist_pve1_pvp
        cf_pvp = cf_pve1 - desnivel_parcial
        p_pvp = pvp_ct - cf_pvp

        st.subheader("📊 Resultados Finais")
        
        st.markdown("**Dados dos PVEs**")
        res1, res2, res3 = st.columns(3)
        res1.metric("CF PVE 1", f"{cf_pve1:.3f} m")
        res2.metric("CF PVE 2", f"{cf_pve2:.3f} m")
        res3.metric("Diferença de Cota", f"{diff_cota:.3f} m")

        st.divider()
        st.markdown("**Declividade e Desníveis**")
        res4, res5, res6 = st.columns(3)
        res4.metric("Declividade", f"{declividade:.5f} m/m")
        res5.metric("Desnível Parcial", f"{desnivel_parcial:.3f} m")
        
        st.divider()
        st.markdown("**Resultado no PV de Projeto**")
        res7, res8 = st.columns(2)
        res7.metric("CF PV de Projeto", f"{cf_pvp:.3f} m")
        res8.metric("P PV de Projeto (Profundidade)", f"{p_pvp:.3f} m")

        if p_pvp < 0:
            st.warning("Atenção: A profundidade do PV de Projeto calculada é negativa. Verifique as cotas de tampa.")

    except Exception as e:
        st.error(f"Ocorreu um erro matemático: {e}")
else:
    st.info("Clique no botão acima para processar os dados inseridos.")