import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Configuração da página
st.set_page_config(
    page_title="CNJ Indicadores",
    page_icon="⚖️",
    layout="centered"
)

# CSS minimalista
st.markdown("""
<style>
    .stApp {
        background-color: #fafafa;
    }
    .main-title {
        font-size: 28px;
        font-weight: 300;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 16px;
        color: #7f8c8d;
        text-align: center;
        margin-bottom: 40px;
    }
    .indicator-label {
        background: #e8f4f8;
        padding: 8px 12px;
        border-radius: 20px;
        font-size: 13px;
        color: #2980b9;
        display: inline-block;
        margin-bottom: 15px;
    }
    .result-box {
        background: white;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        text-align: center;
        margin: 20px 0;
    }
    .big-number {
        font-size: 64px;
        font-weight: 200;
        line-height: 1;
        margin: 10px 0;
    }
    .approved {
        color: #27ae60;
    }
    .rejected {
        color: #e74c3c;
    }
    .meta-info {
        font-size: 12px;
        color: #95a5a6;
        margin-top: 20px;
        padding-top: 20px;
        border-top: 1px solid #ecf0f1;
    }
</style>
""", unsafe_allow_html=True)

# Cabeçalho minimalista
st.markdown('<h1 class="main-title">Calculadora de Indicadores CNJ</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Sistema simplificado para cálculo de indicadores do Prêmio CNJ de Qualidade</p>', unsafe_allow_html=True)

# Dados dos indicadores
indicadores = {
    "magistrados": {
        "ref": "Art. 12, II, b)",
        "titulo": "Cadastro de Magistrados(as)",
        "descricao": "Até 5,00% de magistrados(as) ativos com registro de inconsistência ou com ausência de informação no sistema MPM",
        "meta": 5.0,
        "pontos": 20,
        "comprovacao": "Os campos preenchidos com 'não informado' serão considerados inválidos"
    },
    "servidores": {
        "ref": "Art. 12, II, c)",
        "titulo": "Cadastro de Servidores(as)",
        "descricao": "Até 5,00% de servidores(as) ativos com registros inconsistentes ou com ausência de informação no sistema MPM",
        "meta": 5.0,
        "pontos": 20,
        "cargos": [
            "Servidor(a) efetivo(a) ou removido(a) para o Tribunal",
            "Servidor(a) cedido(a) ou requisitado(a) de outro tribunal",
            "Servidor(a) cedido(a) ou requisitado(a) de órgãos de fora do judiciário",
            "Servidor(a) Comissionado(a) Sem vínculo"
        ],
        "comprovacao": "Os campos preenchidos com 'não informado' serão considerados inválidos"
    }
}

# Estado para controlar qual indicador está expandido
if 'current_indicator' not in st.session_state:
    st.session_state.current_indicator = None

# Indicador 1: Magistrados
with st.expander("📋 **Cadastro de Magistrados(as)**", expanded=(st.session_state.current_indicator == 'magistrados')):
    # Label do indicador
    st.markdown(f'<span class="indicator-label">{indicadores["magistrados"]["ref"]}</span>', unsafe_allow_html=True)
    
    # Descrição
    st.markdown(f'_{indicadores["magistrados"]["descricao"]}_')
    
    # Inputs em colunas
    col1, col2 = st.columns(2)
    with col1:
        total_mag = st.number_input(
            "Total de magistrados(as) ativos",
            min_value=1,
            value=100,
            key="total_mag"
        )
    with col2:
        incons_mag = st.number_input(
            "Com inconsistências",
            min_value=0,
            value=3,
            key="incons_mag"
        )
    
    # Cálculo
    perc_mag = (incons_mag / total_mag * 100) if total_mag > 0 else 0
    aprovado_mag = perc_mag <= indicadores["magistrados"]["meta"]
    pontos_mag = indicadores["magistrados"]["pontos"] if aprovado_mag else 0
    
    # Resultado
    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    st.markdown(f'<div class="big-number {"approved" if aprovado_mag else "rejected"}">{perc_mag:.2f}%</div>', unsafe_allow_html=True)
    st.markdown(f'**{"APROVADO" if aprovado_mag else "REPROVADO"}** • {pontos_mag}/{indicadores["magistrados"]["pontos"]} pontos')
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Gráfico simples
    fig, ax = plt.subplots(figsize=(8, 2))
    ax.barh([0], [perc_mag], height=0.5, color='#27ae60' if aprovado_mag else '#e74c3c', alpha=0.8)
    ax.axvline(x=5, color='#e74c3c', linestyle='--', linewidth=2, label='Meta (5%)')
    ax.set_xlim(0, 10)
    ax.set_ylim(-0.5, 0.5)
    ax.set_xlabel('Percentual de inconsistências (%)')
    ax.set_yticks([])
    ax.legend(loc='upper right')
    ax.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
    
    # Meta info
    st.markdown(f"""
    <div class="meta-info">
    <strong>Forma de comprovação:</strong> {indicadores["magistrados"]["comprovacao"]}<br>
    <strong>Referência:</strong> {indicadores["magistrados"]["ref"]} • Meta: ≤{indicadores["magistrados"]["meta"]}% • Pontuação máxima: {indicadores["magistrados"]["pontos"]} pontos
    </div>
    """, unsafe_allow_html=True)

# Indicador 2: Servidores
with st.expander("👥 **Cadastro de Servidores(as)**", expanded=(st.session_state.current_indicator == 'servidores')):
    # Label do indicador
    st.markdown(f'<span class="indicator-label">{indicadores["servidores"]["ref"]}</span>', unsafe_allow_html=True)
    
    # Descrição
    st.markdown(f'_{indicadores["servidores"]["descricao"]}_')
    
    # Cargos considerados
    st.markdown("**Cargos considerados:**")
    for cargo in indicadores["servidores"]["cargos"]:
        st.markdown(f"• {cargo}")
    
    # Inputs em colunas
    col1, col2 = st.columns(2)
    with col1:
        total_serv = st.number_input(
            "Total de servidores(as) ativos",
            min_value=1,
            value=500,
            key="total_serv"
        )
    with col2:
        incons_serv = st.number_input(
            "Com inconsistências",
            min_value=0,
            value=15,
            key="incons_serv"
        )
    
    # Cálculo
    perc_serv = (incons_serv / total_serv * 100) if total_serv > 0 else 0
    aprovado_serv = perc_serv <= indicadores["servidores"]["meta"]
    pontos_serv = indicadores["servidores"]["pontos"] if aprovado_serv else 0
    
    # Resultado
    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    st.markdown(f'<div class="big-number {"approved" if aprovado_serv else "rejected"}">{perc_serv:.2f}%</div>', unsafe_allow_html=True)
    st.markdown(f'**{"APROVADO" if aprovado_serv else "REPROVADO"}** • {pontos_serv}/{indicadores["servidores"]["pontos"]} pontos')
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Gráfico simples
    fig, ax = plt.subplots(figsize=(8, 2))
    ax.barh([0], [perc_serv], height=0.5, color='#27ae60' if aprovado_serv else '#e74c3c', alpha=0.8)
    ax.axvline(x=5, color='#e74c3c', linestyle='--', linewidth=2, label='Meta (5%)')
    ax.set_xlim(0, 10)
    ax.set_ylim(-0.5, 0.5)
    ax.set_xlabel('Percentual de inconsistências (%)')
    ax.set_yticks([])
    ax.legend(loc='upper right')
    ax.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
    
    # Meta info
    st.markdown(f"""
    <div class="meta-info">
    <strong>Forma de comprovação:</strong> {indicadores["servidores"]["comprovacao"]}<br>
    <strong>Referência:</strong> {indicadores["servidores"]["ref"]} • Meta: ≤{indicadores["servidores"]["meta"]}% • Pontuação máxima: {indicadores["servidores"]["pontos"]} pontos
    </div>
    """, unsafe_allow_html=True)

# Separador
st.markdown("---")

# Resumo compacto
st.markdown("### 📊 Resumo dos Indicadores Calculados")

# Criar dados do resumo apenas com indicadores calculados
resumo_data = []

if 'total_mag' in st.session_state and st.session_state.total_mag > 0:
    perc_mag = (st.session_state.incons_mag / st.session_state.total_mag * 100)
    resumo_data.append({
        'Indicador': indicadores["magistrados"]["ref"],
        'Descrição': 'Cadastro de Magistrados',
        'Percentual': f'{perc_mag:.2f}%',
        'Meta': '≤5%',
        'Status': '✅' if perc_mag <= 5 else '❌',
        'Pontos': f'{20 if perc_mag <= 5 else 0}/20'
    })

if 'total_serv' in st.session_state and st.session_state.total_serv > 0:
    perc_serv = (st.session_state.incons_serv / st.session_state.total_serv * 100)
    resumo_data.append({
        'Indicador': indicadores["servidores"]["ref"],
        'Descrição': 'Cadastro de Servidores',
        'Percentual': f'{perc_serv:.2f}%',
        'Meta': '≤5%',
        'Status': '✅' if perc_serv <= 5 else '❌',
        'Pontos': f'{20 if perc_serv <= 5 else 0}/20'
    })

if resumo_data:
    df_resumo = pd.DataFrame(resumo_data)
    st.dataframe(df_resumo, use_container_width=True, hide_index=True)
else:
    st.info("Calcule pelo menos um indicador para visualizar o resumo.")

# Footer
st.markdown("---")
st.markdown("""
<div class="meta-info" style="text-align: center;">
<strong>Referência:</strong> <a href="https://atos.cnj.jus.br/atos/detalhar/5880" target="_blank">Ato CNJ nº 5880</a> • 
Portaria Presidência Nº 411/2024 • Eixo Dados e Tecnologia
</div>
""", unsafe_allow_html=True)

# Adicionar mais indicadores (placeholder)
with st.expander("➕ **Adicionar Novo Indicador**", expanded=False):
    st.info("""
    Sistema preparado para expansão. Novos indicadores serão adicionados conforme necessidade:
    - Art. 12, I - Alimentar DataJud (174 pontos)
    - Art. 12, III - Saneamento DataJud por Unidade (30 pontos)
    - Art. 12, IV - Processos Eletrônicos (50 pontos)
    - Art. 12, V - Índice iGovTIC-JUD (60 pontos)
    - E outros...
    """)
