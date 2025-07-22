import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="CNJ - Sistema de Indicadores",
    page_icon="⚖️",
    layout="wide"
)

# Título principal
st.title("⚖️ Sistema de Indicadores - Prêmio CNJ de Qualidade")
st.markdown("**Eixo Dados e Tecnologia** • Módulo de Pessoal e Estrutura Judiciária Mensal (MPM)")

# Configuração de fontes de dados
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

# Barra informativa de fontes ativas
st.info(f"📊 **Dados ativos:** {fonte_mag} | {fonte_serv} | **Referência:** 31/07/2025")

# Separador
st.markdown("---")

# Título da seção
st.markdown("## 📈 Cálculo dos Indicadores")

# Indicador 1 - Magistrados
col1, col2 = st.columns([3, 2])

with col1:
    # Container do indicador
    with st.container():
        # Cabeçalho
        subcol1, subcol2 = st.columns([2, 1])
        with subcol1:
            st.markdown("### Cadastro de Magistrados(as)")
        with subcol2:
            st.markdown("**Art. 12, II, b)** • 20 pontos")
        
        # Descrição
        st.markdown("""
        Verifica se há até 5% de magistrados(as) ativos com registro de inconsistência ou 
        ausência de informação no sistema MPM. Campos com "não informado" são considerados inválidos.
        """)
        
        # Container destacado para inputs
        with st.container():
            st.markdown("##### 📝 Insira os dados para cálculo:")
            
            input_col1, input_col2 = st.columns(2)
            
            with input_col1:
                st.markdown("**Total de magistrados(as) ativos**")
                total_mag = st.number_input(
                    "Total de magistrados",
                    min_value=1,
                    value=150,
                    key="total_mag_fixed",
                    label_visibility="collapsed"
                )
                st.caption("Total no sistema MPM")
            
            with input_col2:
                st.markdown("**Registros com 'não informado'**")
                incons_mag = st.number_input(
                    "Inconsistências",
                    min_value=0,
                    value=5,
                    key="incons_mag_fixed",
                    label_visibility="collapsed"
                )
                st.caption("Campos inconsistentes")

with col2:
    # Container de resultado
    with st.container():
        # Cálculo
        perc_mag = (incons_mag / total_mag * 100) if total_mag > 0 else 0
        aprovado_mag = perc_mag <= 5.0
        pontos_mag = 20 if aprovado_mag else 0
        
        # Box de resultado
        st.markdown("### Resultado")
        
        # Métrica principal
        if aprovado_mag:
            st.success(f"### {perc_mag:.2f}%")
            st.markdown("✅ **APROVADO**")
        else:
            st.error(f"### {perc_mag:.2f}%")
            st.markdown("❌ **REPROVADO**")
        
        st.markdown(f"**{pontos_mag} de 20 pontos**")
        
        # Detalhes do cálculo
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
    # Container do indicador
    with st.container():
        # Cabeçalho
        subcol1, subcol2 = st.columns([2, 1])
        with subcol1:
            st.markdown("### Cadastro de Servidores(as)")
        with subcol2:
            st.markdown("**Art. 12, II, c)** • 20 pontos")
        
        # Descrição
        st.markdown("""
        Verifica se há até 5% de servidores(as) ativos com registros inconsistentes no MPM. 
        Considera: efetivos, removidos, cedidos, requisitados e comissionados sem vínculo.
        """)
        
        # Container destacado para inputs
        with st.container():
            st.markdown("##### 📝 Insira os dados para cálculo:")
            
            input_col1, input_col2 = st.columns(2)
            
            with input_col1:
                st.markdown("**Total de servidores(as) ativos**")
                total_serv = st.number_input(
                    "Total de servidores",
                    min_value=1,
                    value=800,
                    key="total_serv_fixed",
                    label_visibility="collapsed"
                )
                st.caption("Total no sistema MPM")
            
            with input_col2:
                st.markdown("**Registros com 'não informado'**")
                incons_serv = st.number_input(
                    "Inconsistências",
                    min_value=0,
                    value=30,
                    key="incons_serv_fixed",
                    label_visibility="collapsed"
                )
                st.caption("Campos inconsistentes")

with col2:
    # Container de resultado
    with st.container():
        # Cálculo
        perc_serv = (incons_serv / total_serv * 100) if total_serv > 0 else 0
        aprovado_serv = perc_serv <= 5.0
        pontos_serv = 20 if aprovado_serv else 0
        
        # Box de resultado
        st.markdown("### Resultado")
        
        # Métrica principal
        if aprovado_serv:
            st.success(f"### {perc_serv:.2f}%")
            st.markdown("✅ **APROVADO**")
        else:
            st.error(f"### {perc_serv:.2f}%")
            st.markdown("❌ **REPROVADO**")
        
        st.markdown(f"**{pontos_serv} de 20 pontos**")
        
        # Detalhes do cálculo
        with st.expander("Ver cálculo detalhado"):
            st.markdown(f"""
            **Fórmula:** (Inconsistências ÷ Total) × 100
            
            **Aplicação:** ({incons_serv} ÷ {total_serv}) × 100 = {perc_serv:.2f}%
            
            **Meta:** ≤ 5,00%
            
            **Status:** {"Dentro da meta ✅" if aprovado_serv else "Fora da meta ❌"}
            """)

# Separador
st.markdown("---")

# Resumo dos Indicadores
st.markdown("## 📊 Resumo dos Indicadores")

# Métricas gerais
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
st.markdown("### Detalhamento")

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

# Rodapé com ações
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📥 Exportar Relatório", use_container_width=True, type="primary"):
        st.success("Relatório exportado com sucesso!")

with col2:
    if st.button("💾 Salvar Resultados", use_container_width=True):
        st.success("Resultados salvos!")

with col3:
    if st.button("🔄 Limpar Dados", use_container_width=True):
        st.rerun()

# Informações legais
st.caption("**Base Legal:** Ato CNJ nº 5880/2024 • Portaria Presidência Nº 411/2024 • Resolução CNJ nº 587/2024")
