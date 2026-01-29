import streamlit as st

st.set_page_config(page_title="Calculadora de Cotas PVE/PV de Projeto", layout="wide")

# Inicialização robusta do session_state
if 'calculos' not in st.session_state or not isinstance(st.session_state.calculos.get('inputs'), dict):
    st.session_state.calculos = {
        'inputs': {},
        'results': {},
        'executado': False
    }

st.title("📏 Calculadora de Cotas PVE/PV de Projeto")

st.subheader("📝 Dados de Entrada")

col_inp1, col_inp2 = st.columns(2)

with col_inp1:
    st.info("📍 PVE 1")
    pve1_ct = st.number_input("PVE 1: Cota de Tampa (CT)", value=0.0, format="%.5f", key="ct1")
    pve1_ch = st.number_input("PVE 1: Chaminé (CH)", value=0.0, format="%.5f", key="ch1")
    pve1_p = st.number_input("PVE 1: Profundidade (P)", value=0.0, format="%.5f", key="p1")

with col_inp2:
    st.info("📍 PVE 2")
    pve2_ct = st.number_input("PVE 2: Cota de Tampa (CT)", value=0.0, format="%.5f", key="ct2")
    pve2_ch = st.number_input("PVE 2: Chaminé (CH)", value=0.0, format="%.5f", key="ch2")
    pve2_p = st.number_input("PVE 2: Profundidade (P)", value=0.0, format="%.5f", key="p2")

st.divider()

col_inp3, col_inp4 = st.columns(2)

with col_inp3:
    st.info("📐 PV de Projeto")
    pvp_ct = st.number_input("PV de Projeto: Cota de Tampa (CT)", value=0.0, format="%.5f", key="ct_pvp")

with col_inp4:
    st.info("🛣️ Distâncias")
    dist_pve1_pve2 = st.number_input("Distância PVE1 ↔ PVE2", value=0.0, format="%.5f", key="d12")
    dist_pve1_pvp = st.number_input("Distância PVE1 ↔ PV de Projeto", value=0.0, format="%.5f", key="d1p")

st.divider()

if st.button("Executar Cálculos", type="primary", use_container_width=True):
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

            # Atualiza o estado com a estrutura completa de uma vez
            st.session_state.calculos = {
                'inputs': {
                    'pve1': {'ct': pve1_ct, 'ch': pve1_ch, 'p': pve1_p},
                    'pve2': {'ct': pve2_ct, 'ch': pve2_ch, 'p': pve2_p},
                    'pvp': {'ct': pvp_ct},
                    'dist': {'d12': dist_pve1_pve2, 'd1p': dist_pve1_pvp}
                },
                'results': {
                    'cf_pve1': cf1,
                    'cf_pve2': cf2,
                    'cf_pvp': cf_proj,
                    'p_pvp': p_proj,
                    'diff_cota': diff,
                    'declividade': decliv,
                    'desnivel_parcial': desnivel
                },
                'executado': True
            }
            st.rerun()

    except Exception as e:
        st.error(f"Erro no processamento: {e}")

# Só tenta renderizar se 'executado' for True E as chaves necessárias existirem
if st.session_state.calculos.get('executado') and 'pve1' in st.session_state.calculos.get('inputs', {}):
    st.subheader("📤 Dados de Saída (Resumo Completo)")
    
    calc = st.session_state.calculos
    
    res_col1, res_col2, res_col3 = st.columns(3)
    
    with res_col1:
        st.success("📍 PVE 1")
        st.write(f"**CT:** {calc['inputs']['pve1']['ct']:.5f}")
        st.write(f"**CH:** {calc['inputs']['pve1']['ch']:.5f}")
        st.write(f"**P:** {calc['inputs']['pve1']['p']:.5f}")
        st.metric("Cota de Fundo (CF)", f"{calc['results']['cf_pve1']:.5f} m")

    with res_col2:
        st.success("📍 PVE 2")
        st.write(f"**CT:** {calc['inputs']['pve2']['ct']:.5f}")
        st.write(f"**CH:** {calc['inputs']['pve2']['ch']:.5f}")
        st.write(f"**P:** {calc['inputs']['pve2']['p']:.5f}")
        st.metric("Cota de Fundo (CF)", f"{calc['results']['cf_pve2']:.5f} m")

    with res_col3:
        st.success("📐 PV de Projeto")
        st.write(f"**CT:** {calc['inputs']['pvp']['ct']:.5f}")
        st.metric("Cota de Fundo (CF)", f"{calc['results']['cf_pvp']:.5f} m")
        st.metric("Profundidade (P)", f"{calc['results']['p_pvp']:.5f} m")

    st.divider()
    
    param_col1, param_col2 = st.columns(2)
    with param_col1:
        st.info("🛣️ Distâncias Aplicadas")
        st.write(f"**Distância 1 ↔ 2:** {calc['inputs']['dist']['d12']:.5f} m")
        st.write(f"**Distância 1 ↔ Projeto:** {calc['inputs']['dist']['d1p']:.5f} m")
        
    with param_col2:
        st.info("📊 Parâmetros Calculados")
        st.write(f"**Diferença de Cota:** {calc['results']['diff_cota']:.5f} m")
        st.write(f"**Declividade:** {calc['results']['declividade']:.5f} m/m")
        st.write(f"**Desnível Parcial:** {calc['results']['desnivel_parcial']:.5f} m")

    if calc['results']['p_pvp'] < 0:
        st.warning("⚠️ Atenção: A profundidade do PV de Projeto calculada é negativa. Verifique as cotas de tampa.")
else:
    st.info("Aguardando inserção de dados e clique em 'Executar Cálculos' para exibir os resultados.")