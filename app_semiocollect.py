import streamlit as st
import pandas as pd

sistemas = {
    'rev_pele': "1. Pele e Anexos (cor, umidade, prurido, pelos, unhas)",
    'rev_cabeca': "2. Cabeça (cefaleia, tontura, síncope, lipotimia)",
    'rev_olhos': "3. Olhos (acuidade, diplopia, dor, vermelhidão)",
    'rev_ouvido': "4. Ouvido (acuidade, otalgia, zumbidos)",
    'rev_nariz': "5. Nariz (olfato, epistaxe, coriza, obstrução)",
    'rev_boca': "6. Boca e Garganta (dentes, gengivorragia, rouquidão, halitose)",
    'rev_mama': "7. Mamas (nódulos, mastalgia, secreção)",
    'rev_resp': "8. Aparelho Respiratório (tosse, escarro, dispneia, chieira)",
    'rev_circ': "9. Aparelho Circulatório (dor precordial, palpitações, ortopneia, edema)",
    'rev_digest': "10. Aparelho Digestório (disfagia, pirose, dor abdominal, hábito intestinal)",
    'rev_urinario': "11. Aparelho Urinário (disúria, alteração de cor, nictúria, dor lombar)",
    'rev_gen_masc': "12. Aparelho Genital Masculino (lesões, libido, testículos)",
    'rev_gen_fem': "13. Aparelho Genital Feminino (menarca, ciclo, DUM, corrimento)",
    'rev_musc': "14. Aparelho Locomotor (dor articular, rigidez matinal, fraqueza)",
    'rev_linfatico': "15. Sistema Hemolinfopoético (palidez, sangramentos, ínguas)",
    'rev_endocrino': "16. Sistema Endócrino/Metabólico (polidipsia, polifagia, intolerância térmica)",
    'rev_neuro': "17. Sistema Neuropsíquico (linguagem, parestesias, humor, memória)"
}

# Configuração da página do Streamlit
st.set_page_config(
    page_title="SemioCollect - Aplicativo de Apoio à Anamnese",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo customizado para interface limpa e profissional
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
    }
    .step-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .lacuna-warning {
        background-color: #ffeef0;
        border-left: 5px solid #ff4d4f;
        padding: 15px;
        border-radius: 4px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Inicialização de variáveis de sessão caso não existam
if 'etapa' not in st.session_state:
    st.session_state.etapa = 1

# Dicionário de armazenamento global de dados da Anamnese
if 'anamnese' not in st.session_state:
    st.session_state.anamnese = {
        # Identificação
        'ident_nome': '',
        'ident_idade': None,
        'ident_sexo': 'Não informado',
        'ident_genero': '',
        'ident_cor': 'Não informado',
        'ident_est_civil': 'Não informado',
        'ident_profissao': '',
        'ident_naturalidade': '',
        'ident_procedencia': '',
        'ident_religiao': '',
        'ident_leito': '',
        'ident_informante': '',
        'ident_acompanhante': '',
        
        # Queixa Principal
        'qp_atendimento': 'Consulta Direta',
        'qp_queixa': '',
        'qp_duracao_num': 1,
        'qp_duracao_unidade': 'Dias',
        
        # HMA
        'hma_localizacao': '',
        'hma_caracteristica': '',
        'hma_intensidade': 5,
        'hma_cronologia': '',
        'hma_desencadeantes': '',
        'hma_melhora_piora': '',
        'hma_manifestacoes_assoc': '',
        'hma_anorexia': False,
        'hma_astenia': False,
        'hma_febre': False,
        'hma_emagrecimento': False,
        'hma_emagrecimento_kg': 0.0,
        'hma_emagrecimento_tempo': 1,
        'hma_repercussao_funcional': '',
        'hma_investigacao_previa': '',
        'hma_condicao_atual': '',
        
        # Revisão dos Sistemas (17 subsistemas)
        'rev_pele': 'Sem Alterações (S.A.)',
        'rev_pele_detalhes': '',
        'rev_cabeca': 'Sem Alterações (S.A.)',
        'rev_cabeca_detalhes': '',
        'rev_olhos': 'Sem Alterações (S.A.)',
        'rev_olhos_detalhes': '',
        'rev_ouvido': 'Sem Alterações (S.A.)',
        'rev_ouvido_detalhes': '',
        'rev_nariz': 'Sem Alterações (S.A.)',
        'rev_nariz_detalhes': '',
        'rev_boca': 'Sem Alterações (S.A.)',
        'rev_boca_detalhes': '',
        'rev_mama': 'Sem Alterações (S.A.)',
        'rev_mama_detalhes': '',
        'rev_resp': 'Sem Alterações (S.A.)',
        'rev_resp_detalhes': '',
        'rev_circ': 'Sem Alterações (S.A.)',
        'rev_circ_detalhes': '',
        'rev_digest': 'Sem Alterações (S.A.)',
        'rev_digest_detalhes': '',
        'rev_urinario': 'Sem Alterações (S.A.)',
        'rev_urinario_detalhes': '',
        'rev_gen_masc': 'Sem Alterações (S.A.)',
        'rev_gen_masc_detalhes': '',
        'rev_gen_fem': 'Sem Alterações (S.A.)',
        'rev_gen_fem_detalhes': '',
        'rev_musc': 'Sem Alterações (S.A.)',
        'rev_musc_detalhes': '',
        'rev_linfatico': 'Sem Alterações (S.A.)',
        'rev_linfatico_detalhes': '',
        'rev_endocrino': 'Sem Alterações (S.A.)',
        'rev_endocrino_detalhes': '',
        'rev_neuro': 'Sem Alterações (S.A.)',
        'rev_neuro_detalhes': '',

        # Antecedentes Pessoais Patológicos
        'ant_infancia': [],
        'ant_infancia_outras': '',
        'ant_adulto': [],
        'ant_adulto_outras': '',
        'ant_alergias': '',
        'ant_tabagismo': 'Não fumante',
        'ant_tabaco_cigs_dia': 0,
        'ant_tabaco_anos': 0,
        'ant_etilismo': 'Não consome',
        'ant_etilismo_bebida': '',
        'ant_etilismo_vol': '',
        'ant_cage_1': False,
        'ant_cage_2': False,
        'ant_cage_3': False,
        'ant_cage_4': False,
        'ant_drogas': 'Não consome',
        'ant_drogas_detalhes': '',
        'ant_cirurgias': '',
        'ant_hospitalizacoes': '',
        'ant_transfusoes': '',
        'ant_obstetrico_gestas': 0,
        'ant_obstetrico_partos': 0,
        'ant_obstetrico_abortos': 0,
        'ant_obstetrico_cesareas': 0,
        'ant_obstetrico_comp': '',
        
        # Medicamentos
        'meds_lista': [],
        
        # Não Patológica
        'np_proc_remota': '',
        'np_hab_tipo': 'Alvenaria',
        'np_hab_saneamento': [],
        'np_hab_vetores': '',
        'np_escolaridade': 'Não informado',
        'np_renda': '',
        'np_alimentacao': 'Alimentação quantitativa e qualitativamente adequada',
        'np_alimentacao_detalhes': '',
        'np_lazer_exercicio': '',
        'np_viagens': '',
        'np_imunizacao': 'Não informada',
        'np_desenv_psicomotor': '',
        'np_desenv_sexual_menarca': '',
        'np_desenv_sexual_sexarca': '',
        'np_desenv_sexual_menopausa': '',
        'np_orientacao_sexual': '',
        
        # Familiar
        'fam_pai': 'Vivo, sem alterações',
        'fam_mae': 'Viva, sem alterações',
        'fam_irmaos': '',
        'fam_filhos': '',
        'fam_heredo': [],
        'fam_heredo_outros': '',
        
        # Fidedignidade
        'fide_grau': 'Fidedigna',
        'fide_justificativa': []
    }

# Menu lateral de Navegação por etapas
st.sidebar.title("🩺 SemioCollect")
st.sidebar.caption("Suporte à Entrevista Clínica")

etapas_nomes = [
    "1. Identificação",
    "2. Queixa Principal (Q.P.)",
    "3. História da Moléstia Atual",
    "4. Revisão dos Sistemas",
    "5. História Pessoal Patológica",
    "6. Medicamentos em Uso",
    "7. História Não Patológica",
    "8. Histórico Familiar",
    "9. Fidedignidade",
    "📋 Revisão e Exportação"
]

# Rádio no menu lateral para pular etapas caso necessário
etapa_selecionada = st.sidebar.radio("Navegação:", etapas_nomes, index=st.session_state.etapa - 1)
st.session_state.etapa = etapas_nomes.index(etapa_selecionada) + 1

# Título do Aplicativo principal
st.title("Coleta de Anamnese Estruturada")
st.caption("Baseado rigorosamente nas normas de Semiologia Médica padrão.")

# ETAPA 1: IDENTIFICAÇÃO
if st.session_state.etapa == 1:
    st.header("1. Identificação do Paciente")
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.anamnese['ident_nome'] = st.text_input(
                "Nome Completo (ou Nome Social para pessoas transexuais):",
                value=st.session_state.anamnese['ident_nome']
            )
            st.session_state.anamnese['ident_idade'] = st.number_input(
                "Idade (Anos):",
                min_value=0, max_value=120, step=1,
                value=st.session_state.anamnese['ident_idade'] if st.session_state.anamnese['ident_idade'] is not None else 0
            )
            st.session_state.anamnese['ident_sexo'] = st.selectbox(
                "Sexo Biológico:",
                ["Não informado", "Masculino", "Feminino"],
                index=["Não informado", "Masculino", "Feminino"].index(st.session_state.anamnese['ident_sexo'])
            )
            st.session_state.anamnese['ident_genero'] = st.text_input(
                "Identidade de Gênero (como se identifica):",
                value=st.session_state.anamnese['ident_genero']
            )
            st.session_state.anamnese['ident_cor'] = st.selectbox(
                "Cor/Etnia (Categorias IBGE):",
                ["Não informado", "Branca", "Parda", "Preta", "Amarela", "Indígena"],
                index=["Não informado", "Branca", "Parda", "Preta", "Amarela", "Indígena"].index(st.session_state.anamnese['ident_cor'])
            )
            st.session_state.anamnese['ident_est_civil'] = st.selectbox(
                "Estado Civil:",
                ["Não informado", "Solteiro(a)", "Casado(a)", "Divorciado(a)", "Viúvo(a)", "União Estável"],
                index=["Não informado", "Solteiro(a)", "Casado(a)", "Divorciado(a)", "Viúvo(a)", "União Estável"].index(st.session_state.anamnese['ident_est_civil'])
            )
        with col2:
            st.session_state.anamnese['ident_profissao'] = st.text_input(
                "Profissão / Ocupação Atual:",
                value=st.session_state.anamnese['ident_profissao']
            )
            st.session_state.anamnese['ident_naturalidade'] = st.text_input(
                "Naturalidade:",
                value=st.session_state.anamnese['ident_naturalidade']
            )
            st.session_state.anamnese['ident_procedencia'] = st.text_input(
                "Procedência / Residência Atual:",
                value=st.session_state.anamnese['ident_procedencia']
            )
            st.session_state.anamnese['ident_religiao'] = st.text_input(
                "Religião:",
                value=st.session_state.anamnese['ident_religiao']
            )
            st.session_state.anamnese['ident_leito'] = st.text_input(
                "Número do Leito (se hospitalizado):",
                value=st.session_state.anamnese['ident_leito']
            )
            st.session_state.anamnese['ident_informante'] = st.text_input(
                "Fonte / Informante (Próprio paciente, parente, etc.):",
                value=st.session_state.anamnese['ident_informante']
            )
            st.session_state.anamnese['ident_acompanhante'] = st.text_input(
                "Acompanhante (se houver):",
                value=st.session_state.anamnese['ident_acompanhante']
            )

# ETAPA 2: QUEIXA PRINCIPAL
elif st.session_state.etapa == 2:
    st.header("2. Queixa Principal (Q.P.)")
    with st.container(border=True):
        st.session_state.anamnese['qp_atendimento'] = st.selectbox(
            "Tipo de Atendimento:",
            ["Consulta Direta", "Encaminhamento"],
            index=["Consulta Direta", "Encaminhamento"].index(st.session_state.anamnese['qp_atendimento'])
        )
        
        if st.session_state.anamnese['qp_atendimento'] == "Consulta Direta":
            st.info("Registre nas palavras exatas do paciente. O aplicativo adicionará automaticamente as aspas.")
            st.session_state.anamnese['qp_queixa'] = st.text_area(
                "O que o paciente relatou que está sentindo / incomodando?",
                value=st.session_state.anamnese['qp_queixa'],
                help="Exemplo: dor de cabeça e vômitos"
            )
        else:
            st.info("Em caso de encaminhamento formal, registre em linguagem semiotécnica (sem aspas obrigatórias).")
            st.session_state.anamnese['qp_queixa'] = st.text_area(
                "Descrição do motivo de encaminhamento / avaliação solicitada:",
                value=st.session_state.anamnese['qp_queixa'],
                help="Exemplo: Encaminhado para avaliação pré-operatória por cardiomiopatia de base."
            )
            
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.anamnese['qp_duracao_num'] = st.number_input(
                "Duração aproximada da queixa:",
                min_value=1, step=1,
                value=st.session_state.anamnese['qp_duracao_num']
            )
        with col2:
            st.session_state.anamnese['qp_duracao_unidade'] = st.selectbox(
                "Unidade de tempo:",
                ["Minutos", "Horas", "Dias", "Semanas", "Meses", "Anos"],
                index=["Minutos", "Horas", "Dias", "Semanas", "Meses", "Anos"].index(st.session_state.anamnese['qp_duracao_unidade'])
            )

# ETAPA 3: HISTÓRIA DA MOLÉSTIA ATUAL
elif st.session_state.etapa == 3:
    st.header("3. História da Moléstia Atual (H.M.A.)")
    st.caption("Reconstrução detalhada e cronológica do sintoma-guia investigado.")
    
    with st.container(border=True):
        st.subheader("Os Sete Atributos Clínicos do Sintoma")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.anamnese['hma_localizacao'] = st.text_input(
                "1. Localização e Irradiação da dor / desconforto:",
                value=st.session_state.anamnese['hma_localizacao'],
                help="Onde começa? Ela se espalha para outro lugar?"
            )
            st.session_state.anamnese['hma_caracteristica'] = st.text_input(
                "2. Característica / Tipo da Dor:",
                value=st.session_state.anamnese['hma_caracteristica'],
                help="Como é a sensação? (Queimação, pontada, aperto, cólica, etc.)"
            )
            st.session_state.anamnese['hma_intensidade'] = st.slider(
                "3. Intensidade do sintoma (0 a 10):",
                min_value=0, max_value=10,
                value=st.session_state.anamnese['hma_intensidade'],
                help="Escala de Dor Visual Analógica"
            )
            st.session_state.anamnese['hma_cronologia'] = st.text_input(
                "4. Cronologia e padrão temporal:",
                value=st.session_state.anamnese['hma_cronologia'],
                help="Como se comporta no decorrer do dia? É contínua ou intermitente?"
            )
        with col2:
            st.session_state.anamnese['hma_desencadeantes'] = st.text_input(
                "5. Condições de Início / Fatores Desencadeantes:",
                value=st.session_state.anamnese['hma_desencadeantes'],
                help="O que o paciente estava fazendo quando o sintoma iniciou?"
            )
            st.session_state.anamnese['hma_melhora_piora'] = st.text_input(
                "6. Fatores de Melhora e Piora:",
                value=st.session_state.anamnese['hma_melhora_piora'],
                help="O que alivia ou agrava o quadro? (Posição, repouso, alimentação)"
            )
            st.session_state.anamnese['hma_manifestacoes_assoc'] = st.text_input(
                "7. Manifestações Associadas:",
                value=st.session_state.anamnese['hma_manifestacoes_assoc'],
                help="Surgiram outros sintomas ao mesmo tempo?"
            )

    with st.container(border=True):
        st.subheader("Repercussões Clínicas Sistêmicas")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.anamnese['hma_anorexia'] = st.checkbox("Anorexia (Perda de apetite)", value=st.session_state.anamnese['hma_anorexia'])
            st.session_state.anamnese['hma_astenia'] = st.checkbox("Astenia (Fraqueza generalizada)", value=st.session_state.anamnese['hma_astenia'])
            st.session_state.anamnese['hma_febre'] = st.checkbox("Febre / Calafrios", value=st.session_state.anamnese['hma_febre'])
            st.session_state.anamnese['hma_emagrecimento'] = st.checkbox("Perda de peso involuntária", value=st.session_state.anamnese['hma_emagrecimento'])
            
            if st.session_state.anamnese['hma_emagrecimento']:
                col_emag1, col_emag2 = st.columns(2)
                with col_emag1:
                    st.session_state.anamnese['hma_emagrecimento_kg'] = st.number_input(
                        "Quilos perdidos (kg):",
                        min_value=0.1, max_value=100.0, step=0.5,
                        value=st.session_state.anamnese['hma_emagrecimento_kg'] if st.session_state.anamnese['hma_emagrecimento_kg'] > 0 else 5.0
                    )
                with col_emag2:
                    st.session_state.anamnese['hma_emagrecimento_tempo'] = st.number_input(
                        "Tempo decorrido (Meses):",
                        min_value=1, max_value=120, step=1,
                        value=st.session_state.anamnese['hma_emagrecimento_tempo']
                    )
        with col2:
            st.session_state.anamnese['hma_repercussao_funcional'] = st.text_area(
                "Repercussão Funcional (Impacto no trabalho ou atividades diárias):",
                value=st.session_state.anamnese['hma_repercussao_funcional']
            )
            st.session_state.anamnese['hma_investigacao_previa'] = st.text_area(
                "Exames já realizados e tratamentos anteriores tentados:",
                value=st.session_state.anamnese['hma_investigacao_previa']
            )
            st.session_state.anamnese['hma_condicao_atual'] = st.text_area(
                "Condição Atual do paciente na entrevista / motivo de busca:",
                value=st.session_state.anamnese['hma_condicao_atual']
            )

# ETAPA 4: REVISÃO DOS SISTEMAS
elif st.session_state.etapa == 4:
    st.header("4. Revisão dos Sistemas / Interrogatório Sintomatológico")
    st.caption("Pergunte ativamente por sintomas ocultados ou não relacionados à Q.P. em cada um dos 17 subsistemas.")
    
    # 'sistemas' is defined globally at the top of the file
    
    for chave, label in sistemas.items():
        with st.container(border=True):
            col1, col2 = st.columns([1, 2])
            with col1:
                st.session_state.anamnese[chave] = st.selectbox(
                    f"{label}:",
                    ["Sem Alterações (S.A.)", "Com Alterações"],
                    index=["Sem Alterações (S.A.)", "Com Alterações"].index(st.session_state.anamnese[chave]),
                    key=f"sel_{chave}"
                )
            with col2:
                if st.session_state.anamnese[chave] == "Com Alterações":
                    st.session_state.anamnese[f"{chave}_detalhes"] = st.text_input(
                        "Descreva as alterações encontradas:",
                        value=st.session_state.anamnese[f"{chave}_detalhes"],
                        key=f"txt_{chave}"
                    )
                else:
                    st.session_state.anamnese[f"{chave}_detalhes"] = ""

# ETAPA 5: HISTÓRIA PESSOAL PATOLÓGICA
elif st.session_state.etapa == 5:
    st.header("5. História Pessoal Patológica")
    
    with st.container(border=True):
        st.subheader("Doenças Prévias e Comorbidades")
        col1, col2 = st.columns(2)
        with col1:
            infancia_lista = ["Varicela (Catapora)", "Sarampo", "Caxumba", "Rubéola", "Coqueluche", "Febre Reumática"]
            st.session_state.anamnese['ant_infancia'] = st.multiselect(
                "Doenças Comuns na Infância:",
                infancia_lista,
                default=st.session_state.anamnese['ant_infancia']
            )
            st.session_state.anamnese['ant_infancia_outras'] = st.text_input(
                "Outras doenças da infância (se houver):",
                value=st.session_state.anamnese['ant_infancia_outras']
            )
        with col2:
            adulto_lista = ["Hipertensão Arterial Sanguínea (HAS)", "Diabetes Mellitus (DM)", "Dislipidemia", "Doenças do Coração (Isquêmica/Valvar)", "Doenças Infecciosas Crônicas", "Infecção Sexualmente Transmissível (IST)"]
            st.session_state.anamnese['ant_adulto'] = st.multiselect(
                "Doenças do Adulto / Comorbidades:",
                adulto_lista,
                default=st.session_state.anamnese['ant_adulto']
            )
            st.session_state.anamnese['ant_adulto_outras'] = st.text_input(
                "Outras patologias / comorbidades do adulto:",
                value=st.session_state.anamnese['ant_adulto_outras']
            )
            
    with st.container(border=True):
        st.subheader("Alergias, Reações e Tolerâncias")
        st.session_state.anamnese['ant_alergias'] = st.text_area(
            "Descreva alergias a medicamentos, alimentos ou outras substâncias:",
            value=st.session_state.anamnese['ant_alergias'],
            placeholder="Nega alergias medicamentosas e alimentares ou descreva..."
        )

    with st.container(border=True):
        st.subheader("Hábitos e Adições")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.anamnese['ant_tabagismo'] = st.selectbox(
                "Hábito de Fumar (Tabagismo):",
                ["Não fumante", "Fumante atual", "Ex-fumante"],
                index=["Não fumante", "Fumante atual", "Ex-fumante"].index(st.session_state.anamnese['ant_tabagismo'])
            )
            if st.session_state.anamnese['ant_tabagismo'] != "Não fumante":
                col_tab1, col_tab2 = st.columns(2)
                with col_tab1:
                    st.session_state.anamnese['ant_tabaco_cigs_dia'] = st.number_input(
                        "Média de cigarros por dia:",
                        min_value=1, max_value=100, step=1,
                        value=st.session_state.anamnese['ant_tabaco_cigs_dia'] if st.session_state.anamnese['ant_tabaco_cigs_dia'] > 0 else 10
                    )
                with col_tab2:
                    st.session_state.anamnese['ant_tabaco_anos'] = st.number_input(
                        "Tempo de tabagismo (Anos):",
                        min_value=1, max_value=80, step=1,
                        value=st.session_state.anamnese['ant_tabaco_anos'] if st.session_state.anamnese['ant_tabaco_anos'] > 0 else 10
                    )
                carga = (st.session_state.anamnese['ant_tabaco_cigs_dia'] / 20.0) * st.session_state.anamnese['ant_tabaco_anos']
                st.metric("Carga Tabágica Calculada:", f"{carga:.2f} maços-ano")
                
            st.session_state.anamnese['ant_drogas'] = st.selectbox(
                "Uso de Drogas Ilícitas:",
                ["Não consome", "Uso ocasional", "Uso frequente", "Histórico de uso prévio"],
                index=["Não consome", "Uso ocasional", "Uso frequente", "Histórico de uso prévio"].index(st.session_state.anamnese['ant_drogas'])
            )
            if st.session_state.anamnese['ant_drogas'] != "Não consome":
                st.session_state.anamnese['ant_drogas_detalhes'] = st.text_input(
                    "Descreva o tipo, frequência e via de administração:",
                    value=st.session_state.anamnese['ant_drogas_detalhes']
                )

        with col2:
            st.session_state.anamnese['ant_etilismo'] = st.selectbox(
                "Consumo de Álcool (Etilismo):",
                ["Não consome", "Consumo social", "Consumo frequente", "Consumo diário abusivo"],
                index=["Não consome", "Consumo social", "Consumo frequente", "Consumo diário abusivo"].index(st.session_state.anamnese['ant_etilismo'])
            )
            if st.session_state.anamnese['ant_etilismo'] != "Não consome":
                st.session_state.anamnese['ant_etilismo_bebida'] = st.text_input(
                    "Tipo de bebida consumida (Cerveja, destilados, vinho, etc.):",
                    value=st.session_state.anamnese['ant_etilismo_bebida']
                )
                st.session_state.anamnese['ant_etilismo_vol'] = st.text_input(
                    "Quantidade aproximada / Frequência semanal:",
                    value=st.session_state.anamnese['ant_etilismo_vol'],
                    placeholder="Ex: 6 latas de cerveja aos finais de semana"
                )
                
                st.caption("Investigação CAGE (Triagem para abuso de álcool):")
                st.session_state.anamnese['ant_cage_1'] = st.checkbox(
                    "1. C (Cut down) - Já sentiu a necessidade de diminuir ou parar de beber?",
                    value=st.session_state.anamnese['ant_cage_1']
                )
                st.session_state.anamnese['ant_cage_2'] = st.checkbox(
                    "2. A (Annoyed) - Já se sentiu incomodado com críticas das pessoas à sua bebida?",
                    value=st.session_state.anamnese['ant_cage_2']
                )
                st.session_state.anamnese['ant_cage_3'] = st.checkbox(
                    "3. G (Guilty) - Já sentiu culpa ou remorso por beber?",
                    value=st.session_state.anamnese['ant_cage_3']
                )
                st.session_state.anamnese['ant_cage_4'] = st.checkbox(
                    "4. E (Eye-opener) - Já sentiu necessidade de beber ao acordar para acalmar os nervos ou ressaca?",
                    value=st.session_state.anamnese['ant_cage_4']
                )
                
                pontos_cage = sum([
                    st.session_state.anamnese['ant_cage_1'],
                    st.session_state.anamnese['ant_cage_2'],
                    st.session_state.anamnese['ant_cage_3'],
                    st.session_state.anamnese['ant_cage_4']
                ])
                if pontos_cage >= 2:
                    st.warning(f"Triagem CAGE Positiva ({pontos_cage}/4): Indica 75% de probabilidade de alcoolismo com alta especificidade.")

    with st.container(border=True):
        st.subheader("Eventos Cirúrgicos e Médicos Prévios")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.anamnese['ant_cirurgias'] = st.text_area(
                "Cirurgias Prévias (Ano, Motivo e Complicações):",
                value=st.session_state.anamnese['ant_cirurgias'],
                placeholder="Nega cirurgias prévias ou descreva (Ex: Colecistectomia em 2021 por colelitíase)..."
            )
            st.session_state.anamnese['ant_hospitalizacoes'] = st.text_area(
                "Hospitalizações prévias e Traumatismos graves:",
                value=st.session_state.anamnese['ant_hospitalizacoes']
            )
        with col2:
            st.session_state.anamnese['ant_transfusoes'] = st.text_area(
                "Histórico de Transfusões Sanguíneas (Ano, Motivo):",
                value=st.session_state.anamnese['ant_transfusoes'],
                placeholder="Nega hemotransfusões ou descreva..."
            )
            
            # Histórico obstétrico se sexo biológico for feminino
            if st.session_state.anamnese['ident_sexo'] == "Feminino":
                st.markdown("**Antecedentes Obstétricos (AGO)**")
                col_obs1, col_obs2, col_obs3, col_obs4 = st.columns(4)
                with col_obs1:
                    st.session_state.anamnese['ant_obstetrico_gestas'] = st.number_input("Gestações:", min_value=0, step=1, value=st.session_state.anamnese['ant_obstetrico_gestas'])
                with col_obs2:
                    st.session_state.anamnese['ant_obstetrico_partos'] = st.number_input("Partos:", min_value=0, step=1, value=st.session_state.anamnese['ant_obstetrico_partos'])
                with col_obs3:
                    st.session_state.anamnese['ant_obstetrico_abortos'] = st.number_input("Abortos:", min_value=0, step=1, value=st.session_state.anamnese['ant_obstetrico_abortos'])
                with col_obs4:
                    st.session_state.anamnese['ant_obstetrico_cesareas'] = st.number_input("Cesáreas:", min_value=0, step=1, value=st.session_state.anamnese['ant_obstetrico_cesareas'])
                
                st.session_state.anamnese['ant_obstetrico_comp'] = st.text_input(
                    "Complicações gestacionais / parto / período de amamentação:",
                    value=st.session_state.anamnese['ant_obstetrico_comp']
                )

# ETAPA 6: MEDICAMENTOS EM USO ATUAL
elif st.session_state.etapa == 6:
    st.header("6. Medicamentos em Uso Atual")
    st.caption("Identifique todos os medicamentos alopáticos, suplementos ou terapias alternativas que o paciente utiliza atualmente.")
    
    with st.container(border=True):
        st.subheader("Adicionar Novo Medicamento:")
        col_med1, col_med2, col_med3 = st.columns(3)
        with col_med1:
            med_nome = st.text_input("Nome do Fármaco:", key="add_med_nome")
        with col_med2:
            med_dose = st.text_input("Dose / Concentração:", key="add_med_dose", placeholder="Ex: 50 mg")
        with col_med3:
            med_poso = st.text_input("Esquema Diário / Posologia:", key="add_med_poso", placeholder="Ex: 1-0-1 (Manhã e Noite)")
            
        if st.button("➕ Adicionar Medicamento à Lista"):
            if med_nome:
                st.session_state.anamnese['meds_lista'].append({
                    'nome': med_nome,
                    'dose': med_dose,
                    'posologia': med_poso
                })
                st.success(f"{med_nome} adicionado com sucesso.")
            else:
                st.error("Insira ao menos o nome do medicamento.")
                
    with st.container(border=True):
        st.subheader("Lista de Medicamentos em Uso:")
        if len(st.session_state.anamnese['meds_lista']) == 0:
            st.warning("Nenhum medicamento adicionado até o momento.")
        else:
            df_meds = pd.DataFrame(st.session_state.anamnese['meds_lista'])
            st.table(df_meds)
            
            med_excluir = st.selectbox(
                "Selecione um medicamento para remover:",
                [med['nome'] for med in st.session_state.anamnese['meds_lista']]
            )
            if st.button("🗑️ Remover Selecionado"):
                st.session_state.anamnese['meds_lista'] = [med for med in st.session_state.anamnese['meds_lista'] if med['nome'] != med_excluir]
                st.toast(f"{med_excluir} removido.")
                st.rerun()

# ETAPA 7: HISTÓRIA NÃO PATOLÓGICA (AMBIENTAL E SOCIAL)
elif st.session_state.etapa == 7:
    st.header("7. História Pessoal Não Patológica (Ambiental e Social)")
    
    with st.container(border=True):
        st.subheader("Desenvolvimento e Orientação")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.anamnese['np_desenv_psicomotor'] = st.text_area(
                "Desenvolvimento psicomotor e neural:",
                value=st.session_state.anamnese['np_desenv_psicomotor']
            )
            st.session_state.anamnese['np_desenv_sexual_menarca'] = st.text_input(
                "Idade da Menarca (se aplicável):",
                value=st.session_state.anamnese['np_desenv_sexual_menarca']
            )
            st.session_state.anamnese['np_desenv_sexual_sexarca'] = st.text_input(
                "Idade da Sexarca / Início da Atividade Sexual:",
                value=st.session_state.anamnese['np_desenv_sexual_sexarca']
            )
        with col2:
            st.session_state.anamnese['np_desenv_sexual_menopausa'] = st.text_input(
                "Idade da Menopausa (se aplicável):",
                value=st.session_state.anamnese['np_desenv_sexual_menopausa']
            )
            st.session_state.anamnese['np_orientacao_sexual'] = st.text_input(
                "Orientação sexual (opcional - usar notação neutra e respeitosa):",
                value=st.session_state.anamnese['np_orientacao_sexual'],
                placeholder="Ex: MSH, HSH, etc."
            )

    with st.container(border=True):
        st.subheader("Condições Habitacionais e Saneamento")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.anamnese['np_proc_remota'] = st.text_input(
                "Procedência Remota (Locais onde morou anteriormente):",
                value=st.session_state.anamnese['np_proc_remota']
            )
            st.session_state.anamnese['np_hab_tipo'] = st.selectbox(
                "Tipo de Construção de Habitação:",
                ["Alvenaria", "Madeira", "Taipa", "Outro"],
                index=["Alvenaria", "Madeira", "Taipa", "Outro"].index(st.session_state.anamnese['np_hab_tipo'])
            )
        with col2:
            saneamento_opcoes = ["Água tratada", "Rede de esgoto", "Fossa séptica", "Coleta de lixo"]
            st.session_state.anamnese['np_hab_saneamento'] = st.multiselect(
                "Infraestrutura de Saneamento Básico:",
                saneamento_opcoes,
                default=st.session_state.anamnese['np_hab_saneamento']
            )
            st.session_state.anamnese['np_hab_vetores'] = st.text_input(
                "Presença de vetores ou animais peçonhentos no domicílio:",
                value=st.session_state.anamnese['np_hab_vetores']
            )

    with st.container(border=True):
        st.subheader("Estilo de Vida e Aspectos Socioeconômicos")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.anamnese['np_escolaridade'] = st.selectbox(
                "Nível Educacional / Escolaridade:",
                ["Não informado", "Analfabeto(a)", "Alfabetizado(a)", "Ensino Fundamental", "Ensino Médio", "Ensino Superior (Graduação)", "Pós-graduação"],
                index=["Não informado", "Analfabeto(a)", "Alfabetizado(a)", "Ensino Fundamental", "Ensino Médio", "Ensino Superior (Graduação)", "Pós-graduação"].index(st.session_state.anamnese['np_escolaridade'])
            )
            st.session_state.anamnese['np_renda'] = st.text_input(
                "Renda Familiar Mensal (Opcional):",
                value=st.session_state.anamnese['np_renda']
            )
            st.session_state.anamnese['np_alimentacao'] = st.selectbox(
                "Avaliação Básica de Hábitos Alimentares:",
                [
                    "Alimentação quantitativa e qualitativamente adequada",
                    "Reduzida ingesta de fibras",
                    "Insuficiente consumo de proteínas (à base de carboidratos)",
                    "Consumo de calorias acima das necessidades",
                    "Alimentação com alto teor de gorduras",
                    "Baixa ingestão de líquidos"
                ],
                index=[
                    "Alimentação quantitativa e qualitativamente adequada",
                    "Reduzida ingesta de fibras",
                    "Insuficiente consumo de proteínas (à base de carboidratos)",
                    "Consumo de calorias acima das necessidades",
                    "Alimentação com alto teor de gorduras",
                    "Baixa ingestão de líquidos"
                ].index(st.session_state.anamnese['np_alimentacao'])
            )
            st.session_state.anamnese['np_alimentacao_detalhes'] = st.text_input(
                "Detalhamento dos Hábitos Alimentares:",
                value=st.session_state.anamnese['np_alimentacao_detalhes']
            )
        with col2:
            st.session_state.anamnese['np_lazer_exercicio'] = st.text_area(
                "Atividades de Lazer e Exercícios Físicos (Tipo, Frequência, Duração):",
                value=st.session_state.anamnese['np_lazer_exercicio'],
                placeholder="Ex: Musculação, 3 vezes/semana, por 1 hora diária."
            )
            st.session_state.anamnese['np_viagens'] = st.text_area(
                "Viagens recentes para áreas de endemias / risco epidemiológico:",
                value=st.session_state.anamnese['np_viagens']
            )
            st.session_state.anamnese['np_imunizacao'] = st.selectbox(
                "Status de Imunizações / Carteira de Vacina:",
                ["Não informada", "Completa / Em dia", "Atrasada / Incompleta"],
                index=["Não informada", "Completa / Em dia", "Atrasada / Incompleta"].index(st.session_state.anamnese['np_imunizacao'])
            )

# ETAPA 8: HISTÓRICO FAMILIAR
elif st.session_state.etapa == 8:
    st.header("8. Histórico Familiar")
    
    with st.container(border=True):
        st.subheader("Estado de Saúde dos Familiares Próximos")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.anamnese['fam_pai'] = st.text_area(
                "Genitor (Idade, estado de saúde se vivo, ou causa da morte e idade se falecido):",
                value=st.session_state.anamnese['fam_pai']
            )
            st.session_state.anamnese['fam_mae'] = st.text_area(
                "Genitora (Idade, estado de saúde se vivo, ou causa da morte e idade se falecido):",
                value=st.session_state.anamnese['fam_mae']
            )
        with col2:
            st.session_state.anamnese['fam_irmaos'] = st.text_area(
                "Irmãos (Número de irmãos vivos, idades e condições de saúde):",
                value=st.session_state.anamnese['fam_irmaos']
            )
            st.session_state.anamnese['fam_filhos'] = st.text_area(
                "Filhos / Cônjuge (Se houver, condições de saúde):",
                value=st.session_state.anamnese['fam_filhos']
            )
            
    with st.container(border=True):
        st.subheader("Investigação de Doenças Heredofamiliares prevalentes")
        doencas_fam = ["Hipertensão Arterial Sanguínea (HAS)", "Diabetes Mellitus", "Tuberculose", "Neoplasias (Câncer)", "Doença Arterial Coronariana (Infarto/Angina)", "Acidente Vascular Cerebral (AVC)", "Dislipidemias", "Transtornos Psiquiátricos / Bipolaridade", "Alcoolismo"]
        st.session_state.anamnese['fam_heredo'] = st.multiselect(
            "Selecione patologias recorrentes ou detectadas na família:",
            doencas_fam,
            default=st.session_state.anamnese['fam_heredo']
        )
        st.session_state.anamnese['fam_heredo_outros'] = st.text_input(
            "Outras doenças herdofamiliares detectadas:",
            value=st.session_state.anamnese['fam_heredo_outros']
        )

# ETAPA 9: FIDEDIGNIDADE
elif st.session_state.etapa == 9:
    st.header("9. Fidedignidade das Informações")
    st.caption("A fidedignidade é um item de avaliação médica subjetiva sobre a confiabilidade do histórico clínico coletado.")
    
    with st.container(border=True):
        st.session_state.anamnese['fide_grau'] = st.selectbox(
            "Classificação da Fidedignidade:",
            ["Fidedigna", "Parcialmente Fidedigna", "Não Fidedigna"],
            index=["Fidedigna", "Parcialmente Fidedigna", "Não Fidedigna"].index(st.session_state.anamnese['fide_grau'])
        )
        
        justificativa_opcoes = [
            "Coerência lógica e cronológica do relato",
            "Paciente calmo, orientado no tempo e espaço",
            "Déficits de memória ou de cognição relatados ou observados",
            "Barreiras de linguagem ou de comunicação",
            "Relato conflitante ou confuso",
            "Informações validadas por terceiros (acompanhante)"
        ]
        st.session_state.anamnese['fide_justificativa'] = st.multiselect(
            "Fatores que justificam a classificação:",
            justificativa_opcoes,
            default=st.session_state.anamnese['fide_justificativa']
        )

# ETAPA 10: REVISÃO, EXPORTAÇÃO E LACUNAS
elif st.session_state.etapa == 10:
    st.header("📋 Revisão Geral e Exportação da Anamnese")
    
    # 1. ALGORITMO DE VALIDAÇÃO / MAPA DE LACUNAS
    lacunas = []
    
    # Identificação
    if not st.session_state.anamnese['ident_nome']: lacunas.append("Identificação: Nome do Paciente não preenchido")
    if not st.session_state.anamnese['ident_idade']: lacunas.append("Identificação: Idade do Paciente não informada")
    if st.session_state.anamnese['ident_sexo'] == "Não informado": lacunas.append("Identificação: Sexo Biológico não informado")
    if st.session_state.anamnese['ident_cor'] == "Não informado": lacunas.append("Identificação: Cor/Etnia não especificada")
    if st.session_state.anamnese['ident_est_civil'] == "Não informado": lacunas.append("Identificação: Estado Civil não informado")
    if not st.session_state.anamnese['ident_profissao']: lacunas.append("Identificação: Profissão não preenchida")
    if not st.session_state.anamnese['ident_naturalidade']: lacunas.append("Identificação: Naturalidade não preenchida")
    if not st.session_state.anamnese['ident_procedencia']: lacunas.append("Identificação: Procedência não preenchida")
    
    # QP
    if not st.session_state.anamnese['qp_queixa']: lacunas.append("Queixa Principal: Campo de relato está em branco")
    
    # HMA
    if not st.session_state.anamnese['hma_localizacao']: lacunas.append("HMA: Localização/Irradiação do sintoma")
    if not st.session_state.anamnese['hma_caracteristica']: lacunas.append("HMA: Característica/Tipo da dor")
    if not st.session_state.anamnese['hma_desencadeantes']: lacunas.append("HMA: Fatores Desencadeantes")
    if not st.session_state.anamnese['hma_melhora_piora']: lacunas.append("HMA: Fatores de Melhora/Piora")
    
    # Meds
    if len(st.session_state.anamnese['meds_lista']) == 0:
        lacunas.append("Medicamentos: Lista de medicamentos vazia (se paciente não usa nada, registrar negação no prontuário)")
        
    # Família
    if not st.session_state.anamnese['fam_pai']: lacunas.append("Histórico Familiar: Dados do pai")
    if not st.session_state.anamnese['fam_mae']: lacunas.append("Histórico Familiar: Dados da mãe")
    
    # Exibir Avisos de Lacunas
    if len(lacunas) > 0:
        st.error(f"⚠️ Atenção: Detectamos {len(lacunas)} lacunas/informações incompletas que exigem investigação complementar:")
        for lac in lacunas:
            st.markdown(f"- {lac}")
    else:
        st.success("✅ Excelente! Todas as seções e campos estruturados de forma robusta e completa.")

    # 2. CONSTRUÇÃO DO MARKDOWN FINAL
    # Formatação da Queixa Principal
    qp_formatada = st.session_state.anamnese['qp_queixa']
    if st.session_state.anamnese['qp_atendimento'] == "Consulta Direta" and qp_formatada:
        qp_formatada = f'"{qp_formatada}"'
    duracao = f" há {st.session_state.anamnese['qp_duracao_num']} {st.session_state.anamnese['qp_duracao_unidade'].lower()}"
    qp_final = f"{qp_formatada}{duracao}" if qp_formatada else "Não preenchida"

    # Formatação de Revisão de Sistemas
    is_text = ""
    for k, v in sistemas.items():
        sub_nome = v.split("(")[0].strip()
        status = st.session_state.anamnese[k]
        detalhes = st.session_state.anamnese[f"{k}_detalhes"]
        if status == "Com Alterações" and detalhes:
            is_text += f"* **{sub_nome}:** {detalhes}\n"
        else:
            is_text += f"* **{sub_nome}:** S.A. (Sem Alterações)\n"

    # Formatação do Etilismo e CAGE
    etilismo_relato = st.session_state.anamnese['ant_etilismo']
    if etilismo_relato != "Não consome":
        etilismo_relato += f" ({st.session_state.anamnese['ant_etilismo_bebida']}, {st.session_state.anamnese['ant_etilismo_vol']})"
        if any([st.session_state.anamnese['ant_cage_1'], st.session_state.anamnese['ant_cage_2'], st.session_state.anamnese['ant_cage_3'], st.session_state.anamnese['ant_cage_4']]):
            cage_itens = []
            if st.session_state.anamnese['ant_cage_1']: cage_itens.append("Cut down")
            if st.session_state.anamnese['ant_cage_2']: cage_itens.append("Annoyed")
            if st.session_state.anamnese['ant_cage_3']: cage_itens.append("Guilty")
            if st.session_state.anamnese['ant_cage_4']: cage_itens.append("Eye-opener")
            etilismo_relato += f" | CAGE Positivo para: {', '.join(cage_itens)}"

    # Carga Tabágica
    tabagismo_relato = st.session_state.anamnese['ant_tabagismo']
    if tabagismo_relato != "Não fumante":
        carga_calc = (st.session_state.anamnese['ant_tabaco_cigs_dia'] / 20.0) * st.session_state.anamnese['ant_tabaco_anos']
        tabagismo_relato += f" ({st.session_state.anamnese['ant_tabaco_cigs_dia']} cigs/dia por {st.session_state.anamnese['ant_tabaco_anos']} anos | Carga Tabágica: {carga_calc:.2f} maços-ano)"

    # Formatação dos Medicamentos
    meds_text = ""
    if len(st.session_state.anamnese['meds_lista']) == 0:
        meds_text = "Nega uso de medicamentos contínuos de forma ativa."
    else:
        for m in st.session_state.anamnese['meds_lista']:
            meds_text += f"1. {m['nome']} {m['dose']} - Esquema: {m['posologia']}\n"

    # Gestações / AGO
    obst_text = ""
    if st.session_state.anamnese['ident_sexo'] == "Feminino":
        obst_text = f"**Antecedentes Gineco-Obstétricos (AGO):** G{st.session_state.anamnese['ant_obstetrico_gestas']} P{st.session_state.anamnese['ant_obstetrico_partos']} A{st.session_state.anamnese['ant_obstetrico_abortos']} C{st.session_state.anamnese['ant_obstetrico_cesareas']}"
        if st.session_state.anamnese['ant_obstetrico_comp']:
            obst_text += f" | Complicações: {st.session_state.anamnese['ant_obstetrico_comp']}"
    else:
        obst_text = "Não se aplica (Sexo Biológico Masculino)"

    markdown_final = f"""# PRONTUÁRIO CLÍNICO ESTRUTURADO - ANAMNESE

## 1. IDENTIFICAÇÃO
* **Nome do Paciente / Social:** {st.session_state.anamnese['ident_nome'] if st.session_state.anamnese['ident_nome'] else 'Não informado'}
* **Idade:** {st.session_state.anamnese['ident_idade'] if st.session_state.anamnese['ident_idade'] > 0 else 'Não informada'} anos
* **Sexo Biológico:** {st.session_state.anamnese['ident_sexo']} | **Gênero:** {st.session_state.anamnese['ident_genero'] if st.session_state.anamnese['ident_genero'] else 'Não informado'}
* **Cor/Etnia:** {st.session_state.anamnese['ident_cor']}
* **Estado Civil:** {st.session_state.anamnese['ident_est_civil']}
* **Profissão Atual:** {st.session_state.anamnese['ident_profissao'] if st.session_state.anamnese['ident_profissao'] else 'Não informada'}
* **Naturalidade:** {st.session_state.anamnese['ident_naturalidade'] if st.session_state.anamnese['ident_naturalidade'] else 'Não informada'}
* **Procedência / Residência Atual:** {st.session_state.anamnese['ident_procedencia'] if st.session_state.anamnese['ident_procedencia'] else 'Não informada'}
* **Religião:** {st.session_state.anamnese['ident_religiao'] if st.session_state.anamnese['ident_religiao'] else 'Não informada'}
* **Número do Leito:** {st.session_state.anamnese['ident_leito'] if st.session_state.anamnese['ident_leito'] else 'Não hospitalizado'}
* **Informante / Fonte:** {st.session_state.anamnese['ident_informante'] if st.session_state.anamnese['ident_informante'] else 'Não informado'}
* **Acompanhante:** {st.session_state.anamnese['ident_acompanhante'] if st.session_state.anamnese['ident_acompanhante'] else 'Sem acompanhante'}

## 2. QUEIXA PRINCIPAL (Q.P.)
{qp_final}

## 3. HISTÓRIA DA MOLÉSTIA ATUAL (H.M.A.)
Paciente refere sintomatologia descrita de forma cronológica com as seguintes características:
* **Localização / Irradiação:** {st.session_state.anamnese['hma_localizacao'] if st.session_state.anamnese['hma_localizacao'] else 'Não informada'}
* **Característica / Tipo:** {st.session_state.anamnese['hma_caracteristica'] if st.session_state.anamnese['hma_caracteristica'] else 'Não informada'}
* **Intensidade:** {st.session_state.anamnese['hma_intensidade']}/10 (Escala Analógica de Dor)
* **Cronologia / Padrão:** {st.session_state.anamnese['hma_cronologia'] if st.session_state.anamnese['hma_cronologia'] else 'Não informada'}
* **Condições de Início / Desencadeantes:** {st.session_state.anamnese['hma_desencadeantes'] if st.session_state.anamnese['hma_desencadeantes'] else 'Não informadas'}
* **Fatores de Melhora ou Piora:** {st.session_state.anamnese['hma_melhora_piora'] if st.session_state.anamnese['hma_melhora_piora'] else 'Não informados'}
* **Manifestações Associadas:** {st.session_state.anamnese['hma_manifestacoes_assoc'] if st.session_state.anamnese['hma_manifestacoes_assoc'] else 'Não informadas'}

### Repercussões Clínicas e Gerais:
* **Estado Geral (Geral):** Astenia: {"Sim" if st.session_state.anamnese['hma_astenia'] else "Não"} | Anorexia: {"Sim" if st.session_state.anamnese['hma_anorexia'] else "Não"} | Febre: {"Sim" if st.session_state.anamnese['hma_febre'] else "Não"}
* **Perda Ponderal:** {"Sim, de " + str(st.session_state.anamnese['hma_emagrecimento_kg']) + " kg em " + str(st.session_state.anamnese['hma_emagrecimento_tempo']) + " meses" if st.session_state.anamnese['hma_emagrecimento'] else "Nega emagrecimento involuntário"}
* **Repercussão Funcional:** {st.session_state.anamnese['hma_repercussao_funcional'] if st.session_state.anamnese['hma_repercussao_funcional'] else 'Sem prejuízo relatado'}
* **Investigações e Condutas Anteriores:** {st.session_state.anamnese['hma_investigacao_previa'] if st.session_state.anamnese['hma_investigacao_previa'] else 'Sem exames ou tratamentos prévios anotados'}
* **Condição Atual:** {st.session_state.anamnese['hma_condicao_atual'] if st.session_state.anamnese['hma_condicao_atual'] else 'Não descrita'}

## 4. REVISÃO DOS SISTEMAS (INTERROGATÓRIO SINTOMATOLÓGICO)
{is_text}

## 5. HISTÓRIA PESSOAL PATOLÓGICA (ANTECEDENTES)
* **Doenças da Infância:** {', '.join(st.session_state.anamnese['ant_infancia']) if len(st.session_state.anamnese['ant_infancia']) > 0 else 'Nega doenças típicas da infância'} {st.session_state.anamnese['ant_infancia_outras']}
* **Doenças do Adulto (Comorbidades):** {', '.join(st.session_state.anamnese['ant_adulto']) if len(st.session_state.anamnese['ant_adulto']) > 0 else 'Nega comorbidades crônicas de base'} {st.session_state.anamnese['ant_adulto_outras']}
* **Alergias e Intolerâncias:** {st.session_state.anamnese['ant_alergias'] if st.session_state.anamnese['ant_alergias'] else 'Nega alergias alimentares ou medicamentosas'}
* **Hábitos de Vida / Adições:**
  * **Tabagismo:** {tabagismo_relato}
  * **Etilismo:** {etilismo_relato}
  * **Drogas Ilícitas:** {st.session_state.anamnese['ant_drogas']} {st.session_state.anamnese['ant_drogas_detalhes'] if st.session_state.anamnese['ant_drogas'] != 'Não consome' else ''}
* **Eventos Cirúrgicos e Internações Prévias:**
  * **Cirurgias Prévias:** {st.session_state.anamnese['ant_cirurgias'] if st.session_state.anamnese['ant_cirurgias'] else 'Nega'}
  * **Hospitalizações/Traumatismos:** {st.session_state.anamnese['ant_hospitalizacoes'] if st.session_state.anamnese['ant_hospitalizacoes'] else 'Nega'}
  * **Transfusões Sanguíneas:** {st.session_state.anamnese['ant_transfusoes'] if st.session_state.anamnese['ant_transfusoes'] else 'Nega'}
* **História Obstétrica (AGO):** {obst_text}

## 6. MEDICAMENTOS EM USO ATUAL
{meds_text}

## 7. HISTÓRIA PESSOAL NÃO PATOLÓGICA (AMBIENTAL E SOCIAL)
* **Procedência Remota:** {st.session_state.anamnese['np_proc_remota'] if st.session_state.anamnese['np_proc_remota'] else 'Não informada'}
* **Habitação e Saneamento:** Casa de {st.session_state.anamnese['np_hab_tipo'].lower()} | Saneamento: {', '.join(st.session_state.anamnese['np_hab_saneamento']) if len(st.session_state.anamnese['np_hab_saneamento']) > 0 else 'Sem saneamento básico relatado'} | Vetores: {st.session_state.anamnese['np_hab_vetores'] if st.session_state.anamnese['np_hab_vetores'] else 'Sem registro de vetores'}
* **Escolaridade / Renda:** Escolaridade: {st.session_state.anamnese['np_escolaridade']} | Renda familiar mensal: {st.session_state.anamnese['np_renda'] if st.session_state.anamnese['np_renda'] else 'Não informada'}
* **Hábitos Alimentares:** {st.session_state.anamnese['np_alimentacao']} | Detalhes: {st.session_state.anamnese['np_alimentacao_detalhes']}
* **Atividades de Lazer e Exercícios Físicos:** {st.session_state.anamnese['np_lazer_exercicio'] if st.session_state.anamnese['np_lazer_exercicio'] else 'Não realiza atividade física estruturada'}
* **Viagens Recentes:** {st.session_state.anamnese['np_viagens'] if st.session_state.anamnese['np_viagens'] else 'Não relata viagens recentes de risco'}
* **Status Imunológico:** {st.session_state.anamnese['np_imunizacao']}
* **Desenvolvimento Psicossexual:**
  * **Desenvolvimento Psicomotor/Neural:** {st.session_state.anamnese['np_desenv_psicomotor'] if st.session_state.anamnese['np_desenv_psicomotor'] else 'Não informado'}
  * **Desenvolvimento Sexual:** Menarca: {st.session_state.anamnese['np_desenv_sexual_menarca'] if st.session_state.anamnese['np_desenv_sexual_menarca'] else 'N/A'} | Sexarca: {st.session_state.anamnese['np_desenv_sexual_sexarca'] if st.session_state.anamnese['np_desenv_sexual_sexarca'] else 'N/A'} | Menopausa: {st.session_state.anamnese['np_desenv_sexual_menopausa'] if st.session_state.anamnese['np_desenv_sexual_menopausa'] else 'N/A'}
  * **Orientação Sexual:** {st.session_state.anamnese['np_orientacao_sexual'] if st.session_state.anamnese['np_orientacao_sexual'] else 'Não declarada'}

## 8. HISTÓRICO FAMILIAR
* **Saúde dos Pais:** Pai: {st.session_state.anamnese['fam_pai'] if st.session_state.anamnese['fam_pai'] else 'Não informado'} | Mãe: {st.session_state.anamnese['fam_mae'] if st.session_state.anamnese['fam_mae'] else 'Não informada'}
* **Irmãos:** {st.session_state.anamnese['fam_irmaos'] if st.session_state.anamnese['fam_irmaos'] else 'Sem informações'}
* **Filhos:** {st.session_state.anamnese['fam_filhos'] if st.session_state.anamnese['fam_filhos'] else 'Sem informações'}
* **Doenças Hereditárias na Família:** {', '.join(st.session_state.anamnese['fam_heredo']) if len(st.session_state.anamnese['fam_heredo']) > 0 else 'Nega doenças familiares conhecidas'} {st.session_state.anamnese['fam_heredo_outros']}

## 9. FIDEDIGNIDADE
Anamnese classificada como: **{st.session_state.anamnese['fide_grau']}**
* **Fatores de validação / justificativas:** {', '.join(st.session_state.anamnese['fide_justificativa']) if len(st.session_state.anamnese['fide_justificativa']) > 0 else 'Critérios de justificativa não especificados'}
"""

    st.markdown(markdown_final)
    
    st.download_button(
        "💾 Baixar Prontuário em Markdown (.md)",
        data=markdown_final,
        file_name="anamnese_estruturada.md",
        mime="text/markdown"
    )

# Navegação de Rodapé (Botões Voltar / Avançar)
st.markdown("---")
col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
with col_b1:
    if st.session_state.etapa > 1:
        if st.button("⬅️ Etapa Anterior"):
            st.session_state.etapa -= 1
            st.rerun()
with col_b3:
    if st.session_state.etapa < 10:
        if st.button("Avançar Etapa ➡️"):
            st.session_state.etapa += 1
            st.rerun()
