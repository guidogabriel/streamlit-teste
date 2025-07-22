import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="CNJ - Sistema de Indicadores",
    page_icon="⚖️",
    layout="wide"
)

# CSS minimalista e profissional
st.markdown("""
<style>
    .stApp {
        background-color: #fafafa;
    }
    .main-title {
        font-size: 26px;
        font-weight: 400;
        color: #1a1a1a;
        margin-bottom: 5px;
    }
    .main-subtitle {
        font-size: 14px;
        color: #666;
        margin-bottom: 20px;
    }
    .data-source-bar {
        background: #f0f7ff;
        border: 1px solid #d0e4ff;
        padding: 12px 20px;
        border-radius: 6px;
        margin-bottom: 25px;
        font-size: 14px;
        color: #0066cc;
    }
    .indicator-card {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 20px;
        height: 100%;
        transition: box-shadow 0.2s;
    }
    .indicator-card:hover {
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .indicator-ref {
        font-size: 13px;
        color: #666;
        font-weight: 600;
        margin-bottom: 8px;
    }
    .indicator-name {
        font-size: 16px;
        font-weight: 500;
        color: #1a1a1a;
        margin-bottom: 15px;
    }
    .indicator-meta {
        font-size: 13px;
        color: #666;
        margin-bottom: 12px;
    }
    .result-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 15px;
        padding-top: 15px;
        border-top: 1px solid #f0f0f0;
    }
    .result-percentage {
        font-size: 20px;
        font-weight: 600;
    }
    .result-points {
        font-size: 14px;
        color: #666;
    }
    .status-approved {
        color: #00897b;
    }
    .status-rejected {
        color: #e53935;
    }
    .summary-table {
        margin-top: 30px;
    }
</style>
""", unsafe_allow_html=True)

# Cabeçalho
st.markdown('<h1 class="main-title">⚖️ Sistema de Indicadores - Prêmio CNJ de Qualidade</h1>', unsafe_allow_html=True)
st.markdown('<p class="main-subtitle">Eixo Dados e Tecnologia • Módulo de Pessoal e Estrutura Judiciária Mensal (MPM)</p>', unsafe_allow_html=True)

# Barra de seleção de fontes de dados (compacta)
with st.container():
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        fonte_mag = st.selectbox(
            "📁 Fonte Magistrados",
            ["MPM_Magistrados_2025_07.xlsx", "MPM_Magistrados_2025_06.xlsx", "MPM_Magistrados_2025_05.xlsx"],
            label_visibility="collapsed"
        )
    
    with col2:
        fonte_serv = st.selectbox(
            "📁 Fonte Servidores",
            ["MPM_Servidores_2025_07.xlsx", "MPM_Servidores_2025_06.xlsx", "MPM_Servidores_2025_05.xlsx"],
            label_visibility="collapsed"
        )
    
    with col3:
        if st.button("⚙️ Configurações"):
            st.info("Módulo de configurações em desenvolvimento")

st.markdown(f"""
<div class="data-source-bar">
    📊 <strong>Fontes ativas:</strong> Magistrados: {fonte_mag} | Servidores: {fonte_serv} | Referência: 31/07/2025
</div>
""", unsafe_allow_html=True)

# Grid de indicadores
st.markdown("### 📈 Indicadores Implementados")

# Primeira linha de indicadores
col1, col2 = st.columns(2)

with col1:
    with st.container():
        st.markdown('<div class="indicator-card">', unsafe_allow_html=True)
        st.markdown('<div class="indicator-ref">Art. 12, II, b)</div>', unsafe_allow_html=True)
        st.markdown('<div class="indicator-name">Cadastro de Magistrados(as)</div>', unsafe_allow_html=True)
        st.markdown('<div class="indicator-meta">Meta: ≤ 5% inconsistências • 20 pontos</div>', unsafe_allow_html=True)
        
        # Inputs inline
        col_a, col_b = st.columns(2)
        with col_a:
            total_mag = st.number_input("Total ativos", min_value=1, value=150, key="mag_total", label_visibility="visible")
        with col_b:
            incons_mag = st.number_input("Inconsistências", min_value=0, value=5, key="mag_incons", label_visibility="visible")
        
        # Cálculo
        perc_mag = (incons_mag / total_mag * 100) if total_mag > 0 else 0
        aprovado_mag = perc_mag <= 5.0
        pontos_mag = 20 if aprovado_mag else 0
        
        # Resultado
        st.markdown(f"""
        <div class="result-container">
            <div>
                <span class="result-percentage {'status-approved' if aprovado_mag else 'status-rejected'}">{perc_mag:.2f}%</span>
                <span style="margin-left: 10px;">{'✅' if aprovado_mag else '❌'}</span>
            </div>
            <div class="result-points">{pontos_mag}/20 pts</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    with st.container():
        st.markdown('<div class="indicator-card">', unsafe_allow_html=True)
        st.markdown('<div class="indicator-ref">Art. 12, II, c)</div>', unsafe_allow_html=True)
        st.markdown('<div class="indicator-name">Cadastro de Servidores(as)</div>', unsafe_allow_html=True)
        st.markdown('<div class="indicator-meta">Meta: ≤ 5% inconsistências • 20 pontos</div>', unsafe_allow_html=True)
        
        # Inputs inline
        col_a, col_b = st.columns(2)
        with col_a:
            total_serv = st.number_input("Total ativos", min_value=1, value=800, key="serv_total", label_visibility="visible")
        with col_b:
            incons_serv = st.number_input("Inconsistências", min_value=0, value=30, key="serv_incons", label_visibility="visible")
        
        # Cálculo
        perc_serv = (incons_serv / total_serv * 100) if total_serv > 0 else 0
        aprovado_serv = perc_serv <= 5.0
        pontos_serv = 20 if aprovado_serv else 0
        
        # Resultado
        st.markdown(f"""
        <div class="result-container">
            <div>
                <span class="result-percentage {'status-approved' if aprovado_serv else 'status-rejected'}">{perc_serv:.2f}%</span>
                <span style="margin-left: 10px;">{'✅' if aprovado_serv else '❌'}</span>
            </div>
            <div class="result-points">{pontos_serv}/20 pts</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Segunda linha - Indicadores futuros (placeholder)
st.markdown("### 🔄 Em Desenvolvimento")

col3, col4 = st.columns(2)

with col3:
    with st.container():
        st.markdown("""
        <div class="indicator-card" style="background: #f8f9fa; opacity: 0.7;">
            <div class="indicator-ref">Art. 12, I</div>
            <div class="indicator-name">Alimentar DataJud</div>
            <div class="indicator-meta">174 pontos • Em implementação</div>
        </div>
        """, unsafe_allow_html=True)

with col4:
    with st.container():
        st.markdown("""
        <div class="indicator-card" style="background: #f8f9fa; opacity: 0.7;">
            <div class="indicator-ref">Art. 12, III</div>
            <div class="indicator-name">Saneamento DataJud por Unidade</div>
            <div class="indicator-meta">30 pontos • Em implementação</div>
        </div>
        """, unsafe_allow_html=True)

# Resumo Geral
st.markdown("---")
st.markdown("### 📊 Resumo Geral dos Indicadores")

# Métricas resumidas
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Indicadores Ativos", "2 de 11")
with col2:
    st.metric("Pontos Possíveis", "40")
with col3:
    total_obtidos = pontos_mag + pontos_serv
    st.metric("Pontos Obtidos", f"{total_obtidos}")
with col4:
    aproveitamento = (total_obtidos / 40 * 100) if 40 > 0 else 0
    st.metric("Aproveitamento", f"{aproveitamento:.0f}%")

# Tabela resumo
resumo_df = pd.DataFrame({
    'Artigo': ['Art. 12, II, b)', 'Art. 12, II, c)', 'Art. 12, I', 'Art. 12, III', 'Art. 12, IV', 'Art. 12, V'],
    'Indicador': [
        'Cadastro de Magistrados(as)',
        'Cadastro de Servidores(as)',
        'Alimentar DataJud',
        'Saneamento DataJud',
        'Processos Eletrônicos',
        'iGovTIC-JUD'
    ],
    'Meta': ['≤ 5%', '≤ 5%', '100%', '100%', '100%', 'Satisfatório'],
    'Resultado': [
        f'{perc_mag:.2f}%',
        f'{perc_serv:.2f}%',
        '-',
        '-',
        '-',
        '-'
    ],
    'Pontos': [
        f'{pontos_mag}/20',
        f'{pontos_serv}/20',
        '0/174',
        '0/30',
        '0/50',
        '0/60'
    ],
    'Status': [
        '✅' if aprovado_mag else '❌',
        '✅' if aprovado_serv else '❌',
        '⏳',
        '⏳',
        '⏳',
        '⏳'
    ]
})

st.dataframe(
    resumo_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        'Artigo': st.column_config.TextColumn('Referência', width='small'),
        'Status': st.column_config.TextColumn('Status', width='small', help='✅ Aprovado | ❌ Reprovado | ⏳ Em desenvolvimento')
    }
)

# Rodapé com ações
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("📥 Exportar Relatório", use_container_width=True):
        st.success("Relatório exportado!")

with col2:
    if st.button("📊 Ver Histórico", use_container_width=True):
        st.info("Funcionalidade em desenvolvimento")

with col3:
    if st.button("ℹ️ Sobre o Prêmio CNJ", use_container_width=True):
        st.info("Base Legal: Ato CNJ nº 5880/2024 • Portaria nº 411/2024")
