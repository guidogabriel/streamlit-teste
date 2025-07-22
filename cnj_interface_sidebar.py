import streamlit as st
import pandas as pd
import altair as alt

# Configuração da página
st.set_page_config(
    page_title="Prêmio CNJ - Indicadores",
    page_icon="⚖️",
    layout="wide"
)

# CSS para cards
st.markdown("""
<style>
    .main-header {
        font-size: 36px;
        color: #1e3a5f;
        text-align: center;
        padding: 20px 0;
        border-bottom: 3px solid #0066cc;
        margin-bottom: 30px;
    }
    .card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        border: 1px solid #e0e0e0;
    }
    .card-header {
        font-size: 20px;
        font-weight: bold;
        color: #0066cc;
        margin-bottom: 15px;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .success-card {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        color: #1e3a5f;
    }
    .danger-card {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: #1e3a5f;
    }
    .reference-badge {
        background: #f0f2f5;
        padding: 5px 10px;
        border-radius: 5px;
        font-size: 12px;
        color: #666;
        display: inline-block;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">⚖️ Sistema de Indicadores CNJ</h1>', unsafe_allow_html=True)

# Sidebar para configurações
with st.sidebar:
    st.markdown("### ⚙️ Configurações")
    
    # Seleção do Eixo
    eixo = st.selectbox(
        "Eixo Temático",
        ["Dados e Tecnologia", "Governança", "Produtividade", "Transparência"]
    )
    
    if eixo == "Dados e Tecnologia":
        # Lista de indicadores disponíveis
        indicadores_disponiveis = {
            "Art. 12, II, b)": "Cadastro de magistrados(as) - até 5% inconsistências",
            "Art. 12, II, c)": "Cadastro de servidores(as) - até 5% inconsistências"
        }
        
        indicador_selecionado = st.selectbox(
            "Indicador",
            list(indicadores_disponiveis.keys()),
            format_func=lambda x: f"{x} - {indicadores_disponiveis[x]}"
        )
    
    st.markdown("---")
    
    # Filtros adicionais
    st.markdown("### 📊 Filtros")
    periodo = st.date_input("Data de Referência")
    tribunal = st.text_input("Tribunal", "Digite o nome do tribunal")
    
    # Botão de exportar
    st.markdown("---")
    if st.button("📥 Exportar Relatório", type="primary", use_container_width=True):
        st.success("Relatório exportado com sucesso!")

# Área principal
if eixo == "Dados e Tecnologia":
    # Container para o indicador selecionado
    st.markdown(f'<div class="card">', unsafe_allow_html=True)
    
    if indicador_selecionado == "Art. 12, II, b)":
        st.markdown('<div class="card-header">📋 Cadastro de Magistrados(as)</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("##### Entrada de Dados")
            total_magistrados = st.number_input(
                "Total de magistrados(as) ativos",
                min_value=1,
                value=150,
                help="Número total de magistrados ativos no sistema MPM"
            )
            
            magistrados_inconsistentes = st.number_input(
                "Magistrados(as) com 'não informado'",
                min_value=0,
                value=5,
                help="Campos preenchidos com 'não informado' são considerados inválidos"
            )
            
            st.markdown("""
            <div class="reference-badge">
            📖 Ref: Art. 12, II, b) | Meta: ≤5% | Pontos: 20
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Cálculos
            percentual = (magistrados_inconsistentes / total_magistrados * 100) if total_magistrados > 0 else 0
            aprovado = percentual <= 5.0
            pontos = 20 if aprovado else 0
            
            # Cards de resultado
            st.markdown("##### Resultados")
            
            card_class = "success-card" if aprovado else "danger-card"
            st.markdown(f"""
            <div class="metric-card {card_class}">
                <h2>{percentual:.2f}%</h2>
                <p>Percentual de Inconsistências</p>
            </div>
            """, unsafe_allow_html=True)
            
            col_res1, col_res2 = st.columns(2)
            with col_res1:
                st.metric("Status", "✅ Aprovado" if aprovado else "❌ Reprovado")
            with col_res2:
                st.metric("Pontuação", f"{pontos}/20 pts")
    
    elif indicador_selecionado == "Art. 12, II, c)":
        st.markdown('<div class="card-header">👥 Cadastro de Servidores(as)</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("##### Entrada de Dados")
            total_servidores = st.number_input(
                "Total de servidores(as) ativos",
                min_value=1,
                value=800,
                help="Total de servidores dos cargos especificados"
            )
            
            servidores_inconsistentes = st.number_input(
                "Servidores(as) com 'não informado'",
                min_value=0,
                value=30,
                help="Registros com campos 'não informado'"
            )
            
            # Checkboxes para tipos de cargo
            st.markdown("##### Cargos incluídos:")
            cargo1 = st.checkbox("Efetivo(a) ou removido(a)", value=True)
            cargo2 = st.checkbox("Cedido(a) de outro tribunal", value=True)
            cargo3 = st.checkbox("Cedido(a) de fora do judiciário", value=True)
            cargo4 = st.checkbox("Comissionado(a) sem vínculo", value=True)
            
            st.markdown("""
            <div class="reference-badge">
            📖 Ref: Art. 12, II, c) | Meta: ≤5% | Pontos: 20
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Cálculos
            percentual = (servidores_inconsistentes / total_servidores * 100) if total_servidores > 0 else 0
            aprovado = percentual <= 5.0
            pontos = 20 if aprovado else 0
            
            # Cards de resultado
            st.markdown("##### Resultados")
            
            card_class = "success-card" if aprovado else "danger-card"
            st.markdown(f"""
            <div class="metric-card {card_class}">
                <h2>{percentual:.2f}%</h2>
                <p>Percentual de Inconsistências</p>
            </div>
            """, unsafe_allow_html=True)
            
            col_res1, col_res2 = st.columns(2)
            with col_res1:
                st.metric("Status", "✅ Aprovado" if aprovado else "❌ Reprovado")
            with col_res2:
                st.metric("Pontuação", f"{pontos}/20 pts")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Gráfico de visualização
    st.markdown("---")
    st.markdown("### 📊 Visualização do Progresso")
    
    # Criar dados para o gráfico
    data = pd.DataFrame({
        'Categoria': ['Atual', 'Meta'],
        'Percentual': [percentual, 5.0],
        'Cor': ['Atual', 'Meta']
    })
    
    # Gráfico Altair
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('Categoria', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Percentual', scale=alt.Scale(domain=[0, 10])),
        color=alt.Color('Cor', scale=alt.Scale(
            domain=['Atual', 'Meta'],
            range=['#0066cc' if percentual <= 5 else '#ff4444', '#28a745']
        ), legend=None),
        tooltip=['Categoria', 'Percentual']
    ).properties(
        width=400,
        height=300
    )
    
    # Linha de meta
    rule = alt.Chart(pd.DataFrame({'y': [5]})).mark_rule(color='red', strokeDash=[5, 5]).encode(y='y')
    
    st.altair_chart(chart + rule, use_container_width=True)
    
    # Resumo geral
    st.markdown("### 📑 Resumo Geral dos Indicadores")
    
    # Tabela resumo
    resumo_data = {
        'Indicador': ['Art. 12, II, b)', 'Art. 12, II, c)', 'Art. 12, I', 'Art. 12, IV'],
        'Descrição': ['Cadastro magistrados', 'Cadastro servidores', 'DataJud', 'Processos eletrônicos'],
        'Meta': ['≤5%', '≤5%', '100%', '100%'],
        'Atual': ['3.33%', '3.75%', '98.5%', '99.8%'],
        'Pontos': ['20/20', '20/20', '170/174', '30/50'],
        'Status': ['✅', '✅', '⚠️', '✅']
    }
    
    df_resumo = pd.DataFrame(resumo_data)
    st.dataframe(df_resumo, use_container_width=True, hide_index=True)

else:
    st.info(f"O eixo '{eixo}' está em desenvolvimento. Por enquanto, apenas o eixo 'Dados e Tecnologia' está disponível.")
