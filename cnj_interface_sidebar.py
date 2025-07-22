import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Prêmio CNJ - Indicadores",
    page_icon="⚖️",
    layout="wide"
)

# CSS clean e minimalista
st.markdown("""
<style>
    .main-header {
        font-size: 32px;
        color: #1e3a5f;
        font-weight: 500;
        margin-bottom: 5px;
    }
    .subtitle {
        color: #666;
        font-size: 16px;
        margin-bottom: 30px;
    }
    .indicator-box {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
        border: 1px solid #e9ecef;
    }
    .indicator-title {
        font-size: 18px;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 10px;
    }
    .reference-badge {
        background: #e3f2fd;
        color: #1976d2;
        padding: 4px 12px;
        border-radius: 4px;
        font-size: 13px;
        display: inline-block;
        margin-bottom: 15px;
    }
    .result-metric {
        background: white;
        padding: 15px;
        border-radius: 6px;
        text-align: center;
        border: 1px solid #dee2e6;
    }
    .metric-value {
        font-size: 24px;
        font-weight: 600;
        color: #2c3e50;
    }
    .metric-label {
        font-size: 14px;
        color: #6c757d;
        margin-top: 5px;
    }
    .info-text {
        font-size: 14px;
        color: #6c757d;
        line-height: 1.6;
    }
    .data-source-info {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        padding: 10px;
        border-radius: 5px;
        font-size: 13px;
        color: #856404;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar session state para fontes de dados
if 'fonte_magistrados' not in st.session_state:
    st.session_state.fonte_magistrados = None
if 'fonte_servidores' not in st.session_state:
    st.session_state.fonte_servidores = None

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Configurações")
    
    # Seleção de Fontes de Dados
    with st.expander("📁 Fontes de Dados", expanded=True):
        st.markdown("##### Planilhas de Magistrados")
        fonte_mag = st.selectbox(
            "Selecione a planilha",
            ["MPM_Magistrados_2025_07.xlsx", "MPM_Magistrados_2025_06.xlsx", 
             "MPM_Magistrados_2025_05.xlsx", "Carregar nova..."],
            key="sel_mag"
        )
        
        st.markdown("##### Planilhas de Servidores")
        fonte_serv = st.selectbox(
            "Selecione a planilha",
            ["MPM_Servidores_2025_07.xlsx", "MPM_Servidores_2025_06.xlsx", 
             "MPM_Servidores_2025_05.xlsx", "Carregar nova..."],
            key="sel_serv"
        )
        
        if fonte_mag == "Carregar nova..." or fonte_serv == "Carregar nova...":
            uploaded_file = st.file_uploader("Carregar arquivo", type=['xlsx', 'csv'])
    
    st.markdown("---")
    
    # Filtros
    st.markdown("### 📊 Filtros")
    periodo_ref = st.date_input("Período de Referência", value=datetime(2025, 7, 31))
    
    # Ações
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Atualizar", use_container_width=True):
            st.rerun()
    with col2:
        if st.button("💾 Exportar", use_container_width=True):
            st.success("Exportado!")

# Área principal
st.markdown('<h1 class="main-header">Sistema de Indicadores - Prêmio CNJ de Qualidade</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Eixo Dados e Tecnologia - Módulo de Pessoal e Estrutura Judiciária Mensal (MPM)</p>', unsafe_allow_html=True)

# Alerta sobre fontes de dados selecionadas
if fonte_mag and fonte_serv:
    st.markdown(f"""
    <div class="data-source-info">
    📁 <strong>Fontes ativas:</strong> Magistrados: {fonte_mag} | Servidores: {fonte_serv}
    </div>
    """, unsafe_allow_html=True)

# Tabs para organizar indicadores
tab1, tab2, tab3 = st.tabs(["📊 Cálculo de Indicadores", "📋 Resumo Geral", "ℹ️ Informações"])

with tab1:
    # Indicador 1 - Magistrados
    st.markdown('<div class="indicator-box">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="indicator-title">Cadastro de Magistrados(as)</div>', unsafe_allow_html=True)
        st.markdown('<span class="reference-badge">Art. 12, II, b) • 20 pontos</span>', unsafe_allow_html=True)
        
        st.markdown("""
        <p class="info-text">
        Até 5,00% de magistrados(as) ativos com registro de inconsistência ou com ausência 
        de informação no sistema MPM. Campos preenchidos com "não informado" serão considerados inválidos.
        </p>
        """, unsafe_allow_html=True)
        
        # Inputs
        col_input1, col_input2 = st.columns(2)
        with col_input1:
            total_mag = st.number_input("Total de magistrados(as) ativos", min_value=1, value=150, key="total_mag_v2")
        with col_input2:
            incons_mag = st.number_input("Com inconsistências", min_value=0, value=5, key="incons_mag_v2")
    
    with col2:
        # Cálculo
        perc_mag = (incons_mag / total_mag * 100) if total_mag > 0 else 0
        aprovado_mag = perc_mag <= 5.0
        pontos_mag = 20 if aprovado_mag else 0
        
        # Resultado
        st.markdown('<div class="result-metric">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value" style="color: {"#28a745" if aprovado_mag else "#dc3545"};">{perc_mag:.2f}%</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-label">{"✅ Aprovado" if aprovado_mag else "❌ Reprovado"} • {pontos_mag}/20 pts</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Indicador 2 - Servidores
    st.markdown('<div class="indicator-box">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="indicator-title">Cadastro de Servidores(as)</div>', unsafe_allow_html=True)
        st.markdown('<span class="reference-badge">Art. 12, II, c) • 20 pontos</span>', unsafe_allow_html=True)
        
        st.markdown("""
        <p class="info-text">
        Até 5,00% de servidores(as) ativos com registros inconsistentes ou com ausência de informação no sistema MPM.
        Considera os cargos: efetivos/removidos, cedidos/requisitados de outro tribunal, 
        cedidos/requisitados de fora do judiciário, e comissionados sem vínculo.
        </p>
        """, unsafe_allow_html=True)
        
        # Inputs
        col_input1, col_input2 = st.columns(2)
        with col_input1:
            total_serv = st.number_input("Total de servidores(as) ativos", min_value=1, value=800, key="total_serv_v2")
        with col_input2:
            incons_serv = st.number_input("Com inconsistências", min_value=0, value=30, key="incons_serv_v2")
    
    with col2:
        # Cálculo
        perc_serv = (incons_serv / total_serv * 100) if total_serv > 0 else 0
        aprovado_serv = perc_serv <= 5.0
        pontos_serv = 20 if aprovado_serv else 0
        
        # Resultado
        st.markdown('<div class="result-metric">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value" style="color: {"#28a745" if aprovado_serv else "#dc3545"};">{perc_serv:.2f}%</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-label">{"✅ Aprovado" if aprovado_serv else "❌ Reprovado"} • {pontos_serv}/20 pts</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Espaço para mais indicadores
    st.info("🔄 Novos indicadores serão adicionados conforme implementação")

with tab2:
    st.markdown("### 📊 Resumo Geral dos Indicadores")
    
    # Métricas gerais
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total de Indicadores", "4 ativos")
    with col2:
        total_pontos_possiveis = 40  # Soma dos dois indicadores implementados
        st.metric("Pontos Possíveis", f"{total_pontos_possiveis}")
    with col3:
        total_pontos_obtidos = pontos_mag + pontos_serv
        st.metric("Pontos Obtidos", f"{total_pontos_obtidos}")
    with col4:
        percentual_aproveitamento = (total_pontos_obtidos / total_pontos_possiveis * 100) if total_pontos_possiveis > 0 else 0
        st.metric("Aproveitamento", f"{percentual_aproveitamento:.0f}%")
    
    # Tabela resumo
    st.markdown("### Detalhamento por Indicador")
    
    resumo_data = {
        'Referência': ['Art. 12, II, b)', 'Art. 12, II, c)', 'Art. 12, I', 'Art. 12, III'],
        'Indicador': [
            'Cadastro de Magistrados(as)',
            'Cadastro de Servidores(as)',
            'Alimentar DataJud',
            'Saneamento DataJud por Unidade'
        ],
        'Meta': ['≤ 5%', '≤ 5%', '174 pts', '30 pts'],
        'Resultado': [f'{perc_mag:.2f}%', f'{perc_serv:.2f}%', '-', '-'],
        'Pontos': [f'{pontos_mag}/20', f'{pontos_serv}/20', '0/174', '0/30'],
        'Status': [
            '✅' if aprovado_mag else '❌',
            '✅' if aprovado_serv else '❌',
            '⏳',
            '⏳'
        ]
    }
    
    df_resumo = pd.DataFrame(resumo_data)
    st.dataframe(
        df_resumo,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Status': st.column_config.TextColumn('Status', width='small'),
            'Referência': st.column_config.TextColumn('Referência', width='medium'),
        }
    )
    
    # Observações
    st.markdown("##### Legenda")
    st.markdown("✅ Aprovado | ❌ Reprovado | ⏳ Em implementação")

with tab3:
    st.markdown("### 📚 Informações sobre os Indicadores")
    
    st.markdown("""
    #### Base Legal
    - **Ato CNJ nº 5880/2024** - Institui o Regulamento do Prêmio CNJ de Qualidade
    - **Portaria Presidência Nº 411/2024** - Define os critérios de avaliação
    - **Resolução CNJ nº 587/2024** - Regulamenta o Sistema MPM
    
    #### Forma de Comprovação
    - Dados extraídos do sistema MPM (Módulo de Pessoal e Estrutura Judiciária Mensal)
    - Período de referência: situação em 31/07/2025
    - Campos com "não informado" são considerados inconsistências
    
    #### Pontuação do Eixo Dados e Tecnologia
    - Total de pontos possíveis no eixo: 589 pontos
    - Indicadores implementados neste sistema: 2 (40 pontos)
    - Em desenvolvimento: DataJud, Processos Eletrônicos, iGovTIC-JUD, entre outros
    """)
