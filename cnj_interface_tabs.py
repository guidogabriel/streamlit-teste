import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="CNJ - Sistema de Indicadores",
    page_icon="⚖️",
    layout="wide"
)

# Inicializar session state para armazenar resultados
if 'resultados' not in st.session_state:
    st.session_state.resultados = {}

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
st.markdown("## 📈 Cálculo de Indicador")

# Dicionário com todos os indicadores disponíveis
indicadores = {
    "Art. 12, II, b) - Cadastro de Magistrados(as)": {
        "ref": "Art. 12, II, b)",
        "pontos_max": 20,
        "meta": 5.0,
        "tipo": "magistrados",
        "descricao": "Verifica se há até 5% de magistrados(as) ativos com registro de inconsistência ou ausência de informação no sistema MPM.",
        "obs": "Campos com 'não informado' são considerados inválidos."
    },
    "Art. 12, II, c) - Cadastro de Servidores(as)": {
        "ref": "Art. 12, II, c)",
        "pontos_max": 20,
        "meta": 5.0,
        "tipo": "servidores",
        "descricao": "Verifica se há até 5% de servidores(as) ativos com registros inconsistentes no MPM.",
        "obs": "Considera: efetivos, removidos, cedidos, requisitados e comissionados sem vínculo."
    },
    "Art. 12, I - Alimentar DataJud": {
        "ref": "Art. 12, I",
        "pontos_max": 174,
        "meta": 100.0,
        "tipo": "datajud",
        "descricao": "Alimentação da Base Nacional de Dados do Poder Judiciário (DataJud).",
        "obs": "Em desenvolvimento"
    },
    "Art. 12, III - Saneamento DataJud por Unidade": {
        "ref": "Art. 12, III",
        "pontos_max": 30,
        "meta": 100.0,
        "tipo": "saneamento",
        "descricao": "Saneamento do DataJud por Unidade Judiciária.",
        "obs": "Em desenvolvimento"
    },
    "Art. 12, IV - Processos Eletrônicos": {
        "ref": "Art. 12, IV",
        "pontos_max": 50,
        "meta": 100.0,
        "tipo": "eletronicos",
        "descricao": "Tramitar as ações judiciais de forma eletrônica.",
        "obs": "Em desenvolvimento"
    }
}

# Seleção do indicador
col1, col2 = st.columns([3, 1])

with col1:
    indicador_selecionado = st.selectbox(
        "Selecione o indicador para calcular:",
        list(indicadores.keys()),
        help="Escolha um indicador para realizar o cálculo"
    )

with col2:
    # Botão para visualizar múltiplos
    modo_multiplo = st.checkbox("Comparar múltiplos", help="Permite selecionar vários indicadores")

# Se modo múltiplo ativado
if modo_multiplo:
    indicadores_multiplos = st.multiselect(
        "Selecione os indicadores para comparar:",
        list(indicadores.keys()),
        default=[indicador_selecionado],
        max_selections=4
    )
    indicadores_para_calcular = indicadores_multiplos
else:
    indicadores_para_calcular = [indicador_selecionado]

# Container para os indicadores
for indicador_nome in indicadores_para_calcular:
    indicador_info = indicadores[indicador_nome]
    
    st.markdown("---")
    
    # Container do indicador
    with st.container():
        # Verificar se o indicador está implementado
        if indicador_info["tipo"] in ["magistrados", "servidores"]:
            col1, col2 = st.columns([3, 2])
            
            with col1:
                # Cabeçalho
                st.markdown(f"### {indicador_nome.split(' - ')[1]}")
                st.markdown(f"**{indicador_info['ref']}** • {indicador_info['pontos_max']} pontos")
                
                # Descrição
                st.markdown(indicador_info["descricao"])
                if indicador_info["obs"]:
                    st.caption(indicador_info["obs"])
                
                # Container para inputs
                st.markdown("##### 📝 Dados para cálculo:")
                
                input_col1, input_col2 = st.columns(2)
                
                with input_col1:
                    if indicador_info["tipo"] == "magistrados":
                        label_total = "Total de magistrados(as) ativos"
                        key_total = "total_mag"
                        default_total = 150
                    else:
                        label_total = "Total de servidores(as) ativos"
                        key_total = "total_serv"
                        default_total = 800
                    
                    st.markdown(f"**{label_total}**")
                    total = st.number_input(
                        label_total,
                        min_value=1,
                        value=default_total,
                        key=f"{key_total}_{indicador_info['ref']}",
                        label_visibility="collapsed"
                    )
                    st.caption("Total no sistema MPM")
                
                with input_col2:
                    st.markdown("**Registros com 'não informado'**")
                    inconsistentes = st.number_input(
                        "Inconsistências",
                        min_value=0,
                        value=5 if indicador_info["tipo"] == "magistrados" else 30,
                        key=f"incons_{indicador_info['ref']}",
                        label_visibility="collapsed"
                    )
                    st.caption("Campos inconsistentes")
            
            with col2:
                # Cálculo
                percentual = (inconsistentes / total * 100) if total > 0 else 0
                aprovado = percentual <= indicador_info["meta"]
                pontos = indicador_info["pontos_max"] if aprovado else 0
                
                # Armazenar resultado
                st.session_state.resultados[indicador_info["ref"]] = {
                    "nome": indicador_nome.split(' - ')[1],
                    "percentual": percentual,
                    "pontos": pontos,
                    "pontos_max": indicador_info["pontos_max"],
                    "aprovado": aprovado,
                    "total": total,
                    "inconsistentes": inconsistentes
                }
                
                # Box de resultado
                st.markdown("### Resultado")
                
                if aprovado:
                    st.success(f"### {percentual:.2f}%")
                    st.markdown("✅ **APROVADO**")
                else:
                    st.error(f"### {percentual:.2f}%")
                    st.markdown("❌ **REPROVADO**")
                
                st.markdown(f"**{pontos} de {indicador_info['pontos_max']} pontos**")
                
                # Botão para salvar
                if st.button(f"💾 Salvar resultado", key=f"save_{indicador_info['ref']}"):
                    st.success("Resultado salvo!")
                
                # Detalhes
                with st.expander("Ver detalhes"):
                    st.markdown(f"""
                    **Cálculo:** ({inconsistentes} ÷ {total}) × 100 = {percentual:.2f}%
                    
                    **Meta:** ≤ {indicador_info['meta']:.0f}%
                    
                    **Status:** {"Dentro da meta ✅" if aprovado else "Fora da meta ❌"}
                    """)
        
        else:
            # Indicador não implementado
            st.markdown(f"### {indicador_nome.split(' - ')[1]}")
            st.markdown(f"**{indicador_info['ref']}** • {indicador_info['pontos_max']} pontos")
            st.warning("🚧 Este indicador está em desenvolvimento e será implementado em breve.")

# Separador antes do resumo
st.markdown("---")

# Resumo dos Indicadores Calculados
st.markdown("## 📊 Resumo dos Indicadores")

# Verificar se há resultados salvos
if st.session_state.resultados:
    # Métricas gerais
    col1, col2, col3, col4 = st.columns(4)
    
    total_indicadores_calculados = len(st.session_state.resultados)
    total_pontos_possiveis = sum(r["pontos_max"] for r in st.session_state.resultados.values())
    total_pontos_obtidos = sum(r["pontos"] for r in st.session_state.resultados.values())
    aproveitamento = (total_pontos_obtidos / total_pontos_possiveis * 100) if total_pontos_possiveis > 0 else 0
    
    with col1:
        st.metric("Indicadores Calculados", f"{total_indicadores_calculados}")
    with col2:
        st.metric("Pontos Possíveis", f"{total_pontos_possiveis}")
    with col3:
        st.metric("Pontos Obtidos", f"{total_pontos_obtidos}")
    with col4:
        st.metric("Aproveitamento", f"{aproveitamento:.0f}%")
    
    # Tabela com resultados calculados
    st.markdown("### Indicadores Calculados")
    
    dados_tabela = []
    for ref, resultado in st.session_state.resultados.items():
        dados_tabela.append({
            'Referência': ref,
            'Indicador': resultado['nome'],
            'Total': resultado['total'],
            'Inconsistências': resultado['inconsistentes'],
            'Percentual': f"{resultado['percentual']:.2f}%",
            'Pontos': f"{resultado['pontos']}/{resultado['pontos_max']}",
            'Status': '✅' if resultado['aprovado'] else '❌'
        })
    
    df = pd.DataFrame(dados_tabela)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Botões de ação
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Exportar Todos", use_container_width=True, type="primary"):
            st.success("Relatório exportado!")
    
    with col2:
        if st.button("📊 Gerar Gráfico", use_container_width=True):
            # Criar um gráfico simples de barras
            import matplotlib.pyplot as plt
            
            fig, ax = plt.subplots(figsize=(10, 4))
            nomes = [r['nome'] for r in st.session_state.resultados.values()]
            pontos = [r['pontos'] for r in st.session_state.resultados.values()]
            pontos_max = [r['pontos_max'] for r in st.session_state.resultados.values()]
            
            x = range(len(nomes))
            ax.bar(x, pontos_max, label='Pontos Máximos', alpha=0.3, color='gray')
            ax.bar(x, pontos, label='Pontos Obtidos', color='green')
            ax.set_xticks(x)
            ax.set_xticklabels(nomes, rotation=45, ha='right')
            ax.set_ylabel('Pontos')
            ax.legend()
            ax.set_title('Pontuação por Indicador')
            plt.tight_layout()
            st.pyplot(fig)
    
    with col3:
        if st.button("🗑️ Limpar Resultados", use_container_width=True):
            st.session_state.resultados = {}
            st.rerun()

else:
    st.info("Nenhum indicador foi calculado ainda. Selecione um indicador acima e insira os dados para começar.")

# Tabela com todos os indicadores disponíveis
with st.expander("📋 Ver todos os indicadores do sistema"):
    todos_dados = []
    for nome, info in indicadores.items():
        todos_dados.append({
            'Referência': info['ref'],
            'Indicador': nome.split(' - ')[1],
            'Pontos Máximos': info['pontos_max'],
            'Meta': f"≤ {info['meta']:.0f}%" if info['meta'] <= 100 else f"{info['meta']:.0f}%",
            'Status': '✅ Implementado' if info['tipo'] in ['magistrados', 'servidores'] else '🚧 Em desenvolvimento'
        })
    
    df_todos = pd.DataFrame(todos_dados)
    st.dataframe(df_todos, use_container_width=True, hide_index=True)

# Informações legais
st.caption("**Base Legal:** Ato CNJ nº 5880/2024 • Portaria Presidência Nº 411/2024 • Resolução CNJ nº 587/2024")
