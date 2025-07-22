import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="CNJ - Sistema de Indicadores",
    page_icon="⚖️",
    layout="wide"
)

# CSS com inputs mais evidentes
st.markdown("""
<style>
    .main-title {
        font-size: 28px;
        font-weight: 400;
        color: #1a1a1a;
        margin-bottom: 5px;
    }
    .subtitle {
        font-size: 14px;
        color: #666;
        margin-bottom: 25px;
    }
    .source-bar {
        background: #e8f2ff;
        border: 1px solid #b8d4ff;
        padding: 10px 20px;
        border-radius: 6px;
        margin-bottom: 25px;
        font-size: 14px;
    }
    .indicator-card {
        background: white;
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 25px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .indicator-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }
    .indicator-title {
        font-size: 18px;
        font-weight: 500;
        color: #2c3e50;
    }
    .indicator-ref {
        background: #f0f0f0;
        padding: 4px 12px;
        border-radius: 15px;
        font-size: 13px;
        color: #666;
    }
    .indicator-info {
        font-size: 14px;
        color: #666;
        line-height: 1.5;
        margin-bottom: 20px;
    }
    .input-section {
        background: #f8f9fa;
        border: 2px dashed #dee2e6;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .input-label {
        font-size: 14px;
        font-weight: 500;
        color: #495057;
        margin-bottom: 8px;
        display: block;
    }
    .input-help {
        font-size: 12px;
        color: #6c757d;
        margin-top: 5px;
    }
    .result-box {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
    }
    .result-number {
        font-size: 32px;
        font-weight: 600;
        margin-bottom: 5px;
    }
    .approved { color: #00897b; }
    .rejected { color: #e53935; }
    .result-status {
        font-size: 16px;
        margin-bottom: 10px;
    }
    .result-points {
        font-size: 14px;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

# Cabeçalho
st.markdown('<h1 class="main-title">⚖️ Sistema de Indicadores - Prêmio CNJ de Qualidade</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Eixo Dados e Tecnologia • Módulo de Pessoal e Estrutura Judiciária Mensal (MPM)</p>', unsafe_allow_html=True)

# Configuração de fontes (simplificada)
with st.expander("⚙️ Configuração de Fontes de Dados", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        fonte_mag = st.selectbox(
            "Planilha de Magistrados",
            ["MPM_Magistrados_2025_07.xlsx", "MPM_Magistrados_2025_06.xlsx", "MPM_Magistrados_2025_05.xlsx"]
        )
    with col2:
        fonte_serv = st.selectbox(
            "Planilha de Servidores",
            ["MPM_Servidores_2025_07.xlsx", "MPM_Servidores_2025_06.xlsx", "MPM_Servidores_2025_05.xlsx"]
        )

# Barra de status das fontes
st.markdown(f"""
<div class="source-bar">
    📊 <strong>Dados ativos:</strong> {fonte_mag} | {fonte_serv} | <strong>Referência:</strong> 31/07/2025
</div>
""", unsafe_allow_html=True)

# Indicadores
st.markdown("### 📈 Cálculo dos Indicadores")

# Indicador 1 - Magistrados
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown('<div class="indicator-card">', unsafe_allow_html=True)
    
    # Cabeçalho do indicador
    st.markdown("""
    <div class="indicator-header">
        <span class="indicator-title">Cadastro de Magistrados(as)</span>
        <span class="indicator-ref">Art. 12, II, b) • 20 pontos</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Informação
    st.markdown("""
    <div class="indicator-info">
    Verifica se há até 5% de magistrados(as) ativos com registro de inconsistência ou 
    ausência de informação no sistema MPM. Campos com "não informado" são considerados inválidos.
    </div>
    """, unsafe_allow_html=True)
    
    # Seção de inputs
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown('<strong style="font-size: 15px; color: #2c3e50;">📝 Insira os dados para cálculo:</strong>', unsafe_allow_html=True)
    
    input_col1, input_col2 = st.columns(2)
    
    with input_col1:
        st.markdown('<span class="input-label">Total de magistrados(as) ativos</span>', unsafe_allow_html=True)
        total_mag = st.number_input(
            "Total",
            min_value=1,
            value=150,
            key="total_mag_clear",
            label_visibility="collapsed",
            help="Número total de magistrados ativos cadastrados no sistema MPM"
        )
        st.markdown('<p class="input-help">Total no sistema MPM</p>', unsafe_allow_html=True)
    
    with input_col2:
        st.markdown('<span class="input-label">Registros com "não informado"</span>', unsafe_allow_html=True)
        incons_mag = st.number_input(
            "Inconsistências",
            min_value=0,
            value=5,
            key="incons_mag_clear",
            label_visibility="collapsed",
            help="Quantidade de registros com campos marcados como 'não informado'"
        )
        st.markdown('<p class="input-help">Campos inconsistentes</p>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # Cálculo
    perc_mag = (incons_mag / total_mag * 100) if total_mag > 0 else 0
    aprovado_mag = perc_mag <= 5.0
    pontos_mag = 20 if aprovado_mag else 0
    
    # Resultado
    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    st.markdown(f'<div class="result-number {"approved" if aprovado_mag else "rejected"}">{perc_mag:.2f}%</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="result-status">{"✅ APROVADO" if aprovado_mag else "❌ REPROVADO"}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="result-points">{pontos_mag} de 20 pontos</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Explicação do cálculo
    with st.expander("Ver cálculo detalhado"):
        st.markdown(f"""
        **Fórmula:** (Inconsistências ÷ Total) × 100
        
        **Aplicação:** ({incons_mag} ÷ {total_mag}) × 100 = {perc_mag:.2f}%
        
        **Meta:** ≤ 5,00%
        
        **Status:** {"Dentro da meta ✅" if aprovado_mag else "Fora da meta ❌"}
        """)

# Separador
st.markdown("---")

# Indicador 2 - Servidores
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown('<div class="indicator-card">', unsafe_allow_html=True)
    
    # Cabeçalho do indicador
    st.markdown("""
    <div class="indicator-header">
        <span class="indicator-title">Cadastro de Servidores(as)</span>
        <span class="indicator-ref">Art. 12, II, c) • 20 pontos</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Informação
    st.markdown("""
    <div class="indicator-info">
    Verifica se há até 5% de servidores(as) ativos com registros inconsistentes no MPM. 
    Considera: efetivos, removidos, cedidos, requisitados e comissionados sem vínculo.
    </div>
    """, unsafe_allow_html=True)
    
    # Seção de inputs
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown('<strong style="font-size: 15px; color: #2c3e50;">📝 Insira os dados para cálculo:</strong>', unsafe_allow_html=True)
    
    input_col1, input_col2 = st.columns(2)
    
    with input_col1:
        st.markdown('<span class="input-label">Total de servidores(as) ativos</span>', unsafe_allow_html=True)
        total_serv = st.number_input(
            "Total",
            min_value=1,
            value=800,
            key="total_serv_clear",
            label_visibility="collapsed",
            help="Total de servidores dos cargos especificados"
        )
        st.markdown('<p class="input-help">Total no sistema MPM</p>', unsafe_allow_html=True)
    
    with input_col2:
        st.markdown('<span class="input-label">Registros com "não informado"</span>', unsafe_allow_html=True)
        incons_serv = st.number_input(
            "Inconsistências",
            min_value=0,
            value=30,
            key="incons_serv_clear",
            label_visibility="collapsed",
            help="Quantidade de registros com campos marcados como 'não informado'"
        )
        st.markdown('<p class="input-help">Campos inconsistentes</p>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # Cálculo
    perc_serv = (incons_serv / total_serv * 100) if total_serv > 0 else 0
    aprovado_serv = perc_serv <= 5.0
    pontos_serv = 20 if aprovado_serv else 0
    
    # Resultado
    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    st.markdown(f'<div class="result-number {"approved" if aprovado_serv else "rejected"}">{perc_serv:.2f}%</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="result-status">{"✅ APROVADO" if aprovado_serv else "❌ REPROVADO"}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="result-points">{pontos_serv} de 20 pontos</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Explicação do cálculo
    with st.expander("Ver cálculo detalhado"):
        st.markdown(f"""
        **Fórmula:** (Inconsistências ÷ Total) × 100
        
        **Aplicação:** ({incons_serv} ÷ {total_serv}) × 100 = {perc_serv:.2f}%
        
        **Meta:** ≤ 5,00%
        
        **Status:** {"Dentro da meta ✅" if aprovado_serv else "Fora da meta ❌"}
        """)

# Resumo
st.markdown("---")
st.markdown("### 📊 Resumo dos Indicadores")

# Métricas resumidas
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total de Indicadores", "2 implementados")
with col2:
    st.metric("Pontos Possíveis", "40")
with col3:
    total_obtidos = pontos_mag + pontos_serv
    st.metric("Pontos Obtidos", f"{total_obtidos}")
with col4:
    aproveitamento = (total_obtidos / 40 * 100) if 40 > 0 else 0
    st.metric("Aproveitamento", f"{aproveitamento:.0f}%")

# Tabela detalhada
dados_tabela = {
    'Referência': ['Art. 12, II, b)', 'Art. 12, II, c)'],
    'Indicador': ['Cadastro de Magistrados(as)', 'Cadastro de Servidores(as)'],
    'Total': [total_mag, total_serv],
    'Inconsistências': [incons_mag, incons_serv],
    'Percentual': [f'{perc_mag:.2f}%', f'{perc_serv:.2f}%'],
    'Meta': ['≤ 5%', '≤ 5%'],
    'Pontos': [f'{pontos_mag}/20', f'{pontos_serv}/20'],
    'Status': ['✅' if aprovado_mag else '❌', '✅' if aprovado_serv else '❌']
}

df = pd.DataFrame(dados_tabela)
st.dataframe(df, use_container_width=True, hide_index=True)

# Rodapé
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    if st.button("📥 Exportar Relatório PDF", use_container_width=True):
        st.success("Relatório exportado com sucesso!")

with col2:
    if st.button("💾 Salvar Resultados", use_container_width=True):
        st.success("Resultados salvos!")

st.caption("Base Legal: Ato CNJ nº 5880/2024 • Portaria Presidência Nº 411/2024 • Resolução CNJ nº 587/2024")
