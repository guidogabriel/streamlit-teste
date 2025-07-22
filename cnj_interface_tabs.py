import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuração da página
st.set_page_config(
    page_title="Prêmio CNJ de Qualidade - Calculadora",
    page_icon="⚖️",
    layout="wide"
)


# CSS customizado para design clean
st.markdown("""
<style>
    .indicator-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #0066cc;
    }
    .metric-value {
        font-size: 48px;
        font-weight: bold;
        color: #0066cc;
    }
    .reference-text {
        color: #666;
        font-size: 14px;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.title("⚖️ Calculadora de Indicadores - Prêmio CNJ de Qualidade")
st.markdown("### Sistema de Cálculo de Indicadores para o Eixo Dados e Tecnologia")

# Tabs para organização
tab1, tab2, tab3 = st.tabs(["📊 Cálculo de Indicadores", "📈 Visualizações", "ℹ️ Sobre"])

with tab1:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### Dados de Entrada")
        
        # Seletor de indicador
        indicador = st.selectbox(
            "Selecione o Indicador",
            [
                "Art. 12, II, b) - Cadastro de magistrados(as)",
                "Art. 12, II, c) - Cadastro de servidores(as)"
            ]
        )
        
        # Inputs baseados no indicador selecionado
        if "magistrados" in indicador:
            total = st.number_input("Total de magistrados(as) ativos", min_value=1, value=100)
            inconsistentes = st.number_input("Magistrados(as) com inconsistências", min_value=0, value=4)
            
            # Referência do indicador
            st.markdown("""
            <div class="reference-text">
            <strong>Referência:</strong> Art. 12, II, b)<br>
            <strong>Meta:</strong> Até 5,00% com inconsistências<br>
            <strong>Pontuação:</strong> 20 pontos
            </div>
            """, unsafe_allow_html=True)
            
        else:
            total = st.number_input("Total de servidores(as) ativos", min_value=1, value=500)
            inconsistentes = st.number_input("Servidores(as) com inconsistências", min_value=0, value=20)
            
            # Tipos de cargo considerados
            st.markdown("##### Cargos considerados:")
            st.markdown("""
            - Servidor(a) efetivo(a) ou removido(a)
            - Servidor(a) cedido(a) ou requisitado(a) de outro tribunal
            - Servidor(a) cedido(a) ou requisitado(a) de fora do judiciário
            - Servidor(a) Comissionado(a) Sem vínculo
            """)
            
            st.markdown("""
            <div class="reference-text">
            <strong>Referência:</strong> Art. 12, II, c)<br>
            <strong>Meta:</strong> Até 5,00% com inconsistências<br>
            <strong>Pontuação:</strong> 20 pontos
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### Resultados")
        
        # Cálculo do percentual
        percentual = (inconsistentes / total) * 100 if total > 0 else 0
        pontos = 20 if percentual <= 5.0 else 0
        
        # Cards de métricas
        col_m1, col_m2, col_m3 = st.columns(3)
        
        with col_m1:
            st.metric("Percentual de Inconsistências", f"{percentual:.2f}%")
        
        with col_m2:
            st.metric("Status", "✅ Aprovado" if percentual <= 5.0 else "❌ Reprovado")
        
        with col_m3:
            st.metric("Pontos Obtidos", f"{pontos}/20")
        
        # Gráfico de progresso
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = percentual,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Percentual de Inconsistências"},
            delta = {'reference': 5.0, 'decreasing': {'color': "green"}},
            gauge = {
                'axis': {'range': [None, 10], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "green" if percentual <= 5.0 else "red"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 5], 'color': 'lightgreen'},
                    {'range': [5, 10], 'color': 'lightcoral'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 5.0
                }
            }
        ))
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Detalhamento
        with st.expander("Ver detalhamento do cálculo"):
            st.markdown(f"""
            **Cálculo realizado:**
            - Total de registros: {total}
            - Registros com inconsistências: {inconsistentes}
            - Percentual: ({inconsistentes} ÷ {total}) × 100 = {percentual:.2f}%
            - Meta: ≤ 5,00%
            - Resultado: {'Dentro da meta' if percentual <= 5.0 else 'Fora da meta'}
            """)

with tab2:
    st.markdown("#### Visualização Comparativa")
    
    # Dados exemplo para múltiplos indicadores
    indicadores_data = {
        'Indicador': [
            'Cadastro de magistrados(as)',
            'Cadastro de servidores(as)',
            'Alimentar DataJud',
            'Processos eletrônicos'
        ],
        'Percentual': [3.5, 4.2, 98.5, 99.8],
        'Meta': [5.0, 5.0, 95.0, 98.0],
        'Pontos Possíveis': [20, 20, 174, 50],
        'Pontos Obtidos': [20, 20, 174, 50]
    }
    
    df = pd.DataFrame(indicadores_data)
    
    # Gráfico de barras comparativo
    fig = px.bar(df, x='Indicador', y=['Percentual', 'Meta'], 
                 title="Comparativo de Indicadores vs Metas",
                 barmode='group',
                 color_discrete_map={'Percentual': '#0066cc', 'Meta': '#ff6b6b'})
    st.plotly_chart(fig, use_container_width=True)
    
    # Resumo de pontuação
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Pontos Possíveis", sum(df['Pontos Possíveis']))
    with col2:
        st.metric("Total de Pontos Obtidos", sum(df['Pontos Obtidos']))
    with col3:
        percentual_total = (sum(df['Pontos Obtidos']) / sum(df['Pontos Possíveis'])) * 100
        st.metric("Percentual de Aproveitamento", f"{percentual_total:.1f}%")

with tab3:
    st.markdown("#### Sobre o Sistema")
    
    st.markdown("""
    Este sistema foi desenvolvido para auxiliar no cálculo dos indicadores do **Prêmio CNJ de Qualidade**,
    especificamente para o **Eixo Dados e Tecnologia**.
    
    ##### Indicadores Implementados:
    
    1. **Art. 12, II, b) - Cadastro de magistrados(as)**
       - Meta: até 5,00% de magistrados(as) ativos com registro de inconsistência
       - Pontuação: 20 pontos
       - Forma de comprovação: Campos preenchidos com "não informado" são considerados inválidos
    
    2. **Art. 12, II, c) - Cadastro de servidores(as)**
       - Meta: até 5,00% de servidores(as) ativos com registros inconsistentes
       - Pontuação: 20 pontos
       - Cargos considerados: efetivos, cedidos, requisitados e comissionados sem vínculo
    
    ##### Referência Legal:
    - [Ato CNJ nº 5880](https://atos.cnj.jus.br/atos/detalhar/5880)
    - Portaria Presidência Nº 411 de 02 de dezembro de 2024
    
    ##### Como usar:
    1. Selecione o indicador desejado
    2. Insira os dados solicitados
    3. O sistema calculará automaticamente o percentual e a pontuação
    4. Visualize os resultados e gráficos comparativos
    """)
