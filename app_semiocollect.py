import streamlit as st
import pandas as pd

# Dicionário de Sistemas e suas opções típicas para a Revisão de Sistemas
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

sistemas_sintomas = {
    'rev_pele': [
        "Prurido (coceira)", 
        "Palidez cutâneo-mucosa", 
        "Icterícia", 
        "Cianose (coloração azulada)", 
        "Vermelhidão / Eritema", 
        "Erupções cutâneas / Exantema", 
        "Queda de cabelo (alopecia)", 
        "Pelos faciais em mulheres (hirsutismo)", 
        "Alterações nas unhas (coiloníquia/unha em colher, onicólise, unhas de Terry/Lindsay, baqueteamento/hipocratismo, linhas de Mees/Beau)", 
        "Alterações de textura / ressecamento (xerodermia)",
        "Exposição a irritantes ou agentes químicos/tóxicos"
    ],
    'rev_cabeca': [
        "Cefaleia (dor de cabeça)", 
        "Vertigem / Tontura", 
        "Síncope (desmaio)", 
        "Lipotímia (sensação de desmaio iminente)", 
        "Traumatismos cranianos prévios", 
        "Sequelas neurológicas / paralisia facial"
    ],
    'rev_olhos': [
        "Alteração da acuidade visual / embaçamento", 
        "Uso de lentes corretoras", 
        "Fotofobia (sensibilidade à luz)", 
        "Diplopia (visão dupla)", 
        "Escotomas (pontos cegos ou manchas na visão)", 
        "Amaurose (perda temporária/completa da visão)", 
        "Dor ocular", 
        "Vermelhidão (congestão de vasos na esclerótica)", 
        "Prurido ocular", 
        "Ardência ocular", 
        "Ressecamento (sensação de olho seco)", 
        "Lacrimejamento excessivo", 
        "Edema palpebral", 
        "Alucinações visuais (luzes, cores)"
    ],
    'rev_ouvido': [
        "Alteração da acuidade auditiva (hipoacusia/anacusia)", 
        "Otalgia (dor no ouvido)", 
        "Otorreia (saída de líquido)", 
        "Otorragia (perda de sangue pelo ouvido)", 
        "Zumbidos (chiado, apito, campainha, grilos)", 
        "Prurido no canal auditivo", 
        "Tontura / Vertigem labiríntica"
    ],
    'rev_nariz': [
        "Anosmia (perda completa do olfato)", 
        "Hiposmia (perda parcial do olfato)", 
        "Parosmia / Cacosmia (distorção / percepção de cheiro ruim)", 
        "Epistaxe (sangramento nasal)", 
        "Rinorreia / Coriza (secreção nasal)", 
        "Obstrução nasal", 
        "Dor nasal ou nos seios paranasais", 
        "Prurido nasal",
        "Ressecamento nasal"
    ],
    'rev_boca': [
        "Alteração do paladar (disgeusia)", 
        "Gengivorragia (sangramento na gengiva)", 
        "Lesões bucais / aftas / ulcerações", 
        "Hemorragias bucais", 
        "Dor de garganta / odinofagia", 
        "Rouquidão / alteração do timbre (disfonia)", 
        "Língua dolorosa", 
        "Halitose (mau hálito)", 
        "Sialose / Sialorreia (excesso de saliva)", 
        "Mau estado dos dentes / ausência dentária (desdentado)"
    ],
    'rev_mama': [
        "Nódulos palpáveis nas mamas", 
        "Secreção mamilar espontânea ou provocada (galactorreia)", 
        "Dor nas mamas (mastalgia)", 
        "Ginecomastia (aumento das mamas em homens)"
    ],
    'rev_resp': [
        "Dor torácica (ventilatório-dependente ou pleurítica)", 
        "Tosse seca / improdutiva", 
        "Tosse produtiva (com expectoração)", 
        "Expectoração mucopurulenta / purulenta / serosa", 
        "Hemoptise (expectoração de sangue originário dos pulmões)", 
        "Dispneia (falta de ar / dificuldade respiratória)", 
        "Chieira / sibilância", 
        "Suores noturnos", 
        "Estridor (respiração ruidosa por obstrução alta)", 
        "Soluço persistente"
    ],
    'rev_circ': [
        "Dor precordial / dor retroesternal / aperto no peito", 
        "Dispneia aos esforços (grandes, médios ou pequenos)", 
        "Ortopneia (dificuldade de respirar ao deitar)", 
        "Dispneia paroxística noturna (falta de ar durante o sono)", 
        "Edema periférico bilateral nos membros inferiores", 
        "Palpitação (sensação de batimento cardíaco acelerado ou irregular)", 
        "Cianose periférica ou central", 
        "Claudicação intermitente (dor na panturrilha ao caminhar que melhora com repouso)", 
        "Cãibras frequentes", 
        "Diminuição da temperatura das extremidades (frialdade)", 
        "Varizes nos membros inferiores"
    ],
    'rev_digest': [
        "Dor abdominal (cólica, queimação, aperto, difusa ou localizada)", 
        "Anorexia / Hiporexia (perda ou diminuição do apetite)", 
        "Hiperorexia (aumento anormal de apetite)", 
        "Odinofagia (dor ao engolir)", 
        "Disfagia alta (bucofaringe) ou baixa (esofágica)", 
        "Pirose (sensação de queimação retroesternal)", 
        "Regurgitação ácida ou alimentar", 
        "Sialorreia (produção excessiva de saliva)", 
        "Eructação excessiva (arroto)", 
        "Náuseas / Vômitos", 
        "Hematêmese (vômito de sangue vivo ou escuro)", 
        "Distensão abdominal / meteorismo / flatulência", 
        "Diarreia aguda ou crônica", 
        "Esteatorreia (fezes gordurosas e de odor fétido)", 
        "Melena (fezes pretas em borra de café com forte mau cheiro)", 
        "Enterorragia / Hematoquezia (sangue vivo pelo ânus)", 
        "Obstipação intestinal (prisão de ventre)", 
        "Icterícia (pele/esclerótica amarelada)", 
        "Acolia fecal (fezes esbranquiçadas)", 
        "Tenesmo / Urgência retal", 
        "Incontinência fecal",
        "Prurido anal / perianal"
    ],
    'rev_urinario': [
        "Dor lombar ou em flanco (contínua ou em cólica)", 
        "Dor hipogástrica / vesical", 
        "Disúria (dor, ardência ou desconforto ao urinar)", 
        "Urina turva ou com mau cheiro", 
        "Colúria (urina escura cor de chá ou coca-cola)", 
        "Hematúria (sangue na urina)", 
        "Piúria (pus na urina)", 
        "Oligúria (diminuição importante do volume urinário)", 
        "Anúria (ausência quase total de produção de urina)", 
        "Poliúria (aumento excessivo do volume urinário diário)", 
        "Nictúria / Noctúria (necessidade frequente de urinar à noite)", 
        "Polaciúria (micção muito frequente em pequenas quantidades)", 
        "Urgência miccional",
        "Incontinência urinária de esforço ou urgência", 
        "Retenção urinária aguda ou crônica",
        "Modificações no jato urinário (calibre reduzido, jato fraco, gotejamento terminal)",
        "Corrimento uretral", 
        "Eliminação de cálculo renal", 
        "Edema bipalpebral, facial ou de membros inferiores"
    ],
    'rev_gen_masc': [
        "Lesões penianas (úlceras, vesículas, pápulas, verrugas)", 
        "Nódulos, tumorações ou aumento de volume nos testículos", 
        "Dor testicular / perineal / lombossacra", 
        "Priapismo (ereção involuntária, persistente e dolorosa)", 
        "Hemospermia (presença de sangue no esperma)", 
        "Corrimento uretral espontâneo", 
        "Disfunção erétil (impotência sexual)", 
        "Ejaculação precoce, retardada ou retrógada", 
        "Redução acentuada da libido", 
        "Criptorquidia ou alterações congênitas (hipospadia/epispadia)"
    ],
    'rev_gen_fem': [
        "Corrimento vaginal (aspecto, cor, odor)", 
        "Prurido vulvo-vaginal", 
        "Lesões vulvo-vaginais (úlceras, vesículas, pápulas)", 
        "Hemorragias uterinas anormais / sangramento intermenstrual", 
        "Ciclo menstrual irregular", 
        "Amenorreia (ausência de menstruação por mais de 3 meses)", 
        "Dismenorreia (cólica menstrual dolorosa e incapacitante)", 
        "Tensão Pré-Menstrual (TPM) grave", 
        "Dispareunia (dor na relação sexual)", 
        "Fogachos (ondas de calor) / sintomas do climatério", 
        "Redução acentuada da libido",
        "Polimenorreia (ciclos < 21 dias) ou Oligomenorreia (ciclos > 35 dias)",
        "Hipo ou hipermenorragia (fluxo reduzido ou muito aumentado)"
    ],
    'rev_musc': [
        "Dor articular espontânea ou ao movimento", 
        "Dores ósseas localizadas ou generalizadas", 
        "Espasmos musculares / contrações involuntárias", 
        "Fraqueza muscular segmentar ou generalizada", 
        "Edema articular (articulação inchada)", 
        "Articulação quente / vermelha (calor e rubor)", 
        "Limitação de movimentos articulares ativos ou passivos", 
        "Deformidades articulares (nódulos de Heberden/Bouchard, desvios, tofos)", 
        "Rigidez articular matinal", 
        "Crepitação articular audível ou palpável ao movimento", 
        "Fraturas espontâneas ou por trauma mínimo"
    ],
    'rev_linfatico': [
        "Palidez cutâneo-mucosa acentuada", 
        "Sangramentos fáceis (petéquias, equimoses, hematomas espontâneos)", 
        "Infecções frequentes e de repetição", 
        "Adenomegalias / ínguas localizadas ou generalizadas (cervicais, occipitais, retro/pré-auriculares, submaxilares, supraclaviculares, axilares, epitrocleares, inguinais)", 
        "Esplenomegalia (baço aumentado palpável)", 
        "Hepatomegalia (fígado aumentado palpável)",
        "Icterícia com colúria e acolia"
    ],
    'rev_endocrino': [
        "Alterações do desenvolvimento físico (nanismo, gigantismo, acromegalia)", 
        "Alterações do desenvolvimento sexual (puberdade precoce ou atrasada)", 
        "Intolerância importante ao frio (sugere hipotireoidismo)", 
        "Intolerância importante ao calor (sugere hipertireoidismo)", 
        "Sudorese excessiva (hiperidrose) ou pele excessivamente seca", 
        "Polidipsia (sede anormal, excessiva e constante)", 
        "Polifagia / Hiperorexia (fome anormal e excessiva)", 
        "Ganho de peso rápido inexplicado de base hormonal", 
        "Perda de peso rápida inexplicada de base hormonal", 
        "Bócio (aumento do volume ou presença de nódulos na tireoide)", 
        "Galactorreia (produção de leite fora do período de amamentação/lactação)", 
        "Fácies de lua cheia / giba dorsal / estrias purpúreas (sugere Cushing)"
    ],
    'rev_neuro': [
        "Alteração do nível de consciência / sonolência / torpor / coma", 
        "Cefaleia de início recente, grave ou progressiva", 
        "Tontura / Vertigem de origem central ou periférica", 
        "Crise convulsiva focal ou tônico-clônica generalizada", 
        "Amnésia recente (anterógrada), antiga (retrógrada) ou lacunar", 
        "Distúrbios visuais agudos (amaurose, diplopia, hemianopsia, escotomas)", 
        "Distúrbios auditivos (hipoacusia/anacusia, zumbidos)", 
        "Alterações de marcha (ceifante, ébria/ataxica, anserina, parkinsoniana, vestibular, escarvante, tabética, espástica)", 
        "Déficits motores (paresias/fraqueza, paralisias/plegias localizadas)", 
        "Déficits sensitivos (anestesia, hipoestesia, parestesias/formigamento)", 
        "Distúrbios esfincterianos (incontinência urinária/fecal ou retenção aguda)", 
        "Distúrbios de sono graves (insônia, sonolência excessiva diurna)", 
        "Alterações na fala/linguagem (disfonia/afonia, disartria, dislalia, disgrafia, dislexia, afasia/disfasia)", 
        "Alterações emocionais / de humor (ansiedade extrema, depressão, irritabilidade, delírios, alucinações)"
    ]
}

# Configuração da página do Streamlit
st.set_page_config(
    page_title="SemioCollect Pro - Aplicativo de Apoio à Anamnese",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo customizado para interface limpa, moderna e focado em OSCE/Prontuários
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
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
    .calculated-box {
        background-color: #e6f7ff;
        border-left: 5px solid #1890ff;
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
        
        # Dores/Sintomas adicionais dinâmicos
        'sintomas_adicionais': [],
        
        # Revisão dos Sistemas (17 subsistemas)
        'rev_pele': 'Sem Alterações (S.A.)',
        'rev_pele_sintomas': [],
        'rev_pele_detalhes': '',
        'rev_cabeca': 'Sem Alterações (S.A.)',
        'rev_cabeca_sintomas': [],
        'rev_cabeca_detalhes': '',
        'rev_olhos': 'Sem Alterações (S.A.)',
        'rev_olhos_sintomas': [],
        'rev_olhos_detalhes': '',
        'rev_ouvido': 'Sem Alterações (S.A.)',
        'rev_ouvido_sintomas': [],
        'rev_ouvido_detalhes': '',
        'rev_nariz': 'Sem Alterações (S.A.)',
        'rev_nariz_sintomas': [],
        'rev_nariz_detalhes': '',
        'rev_boca': 'Sem Alterações (S.A.)',
        'rev_boca_sintomas': [],
        'rev_boca_detalhes': '',
        'rev_mama': 'Sem Alterações (S.A.)',
        'rev_mama_sintomas': [],
        'rev_mama_detalhes': '',
        'rev_resp': 'Sem Alterações (S.A.)',
        'rev_resp_sintomas': [],
        'rev_resp_detalhes': '',
        'rev_circ': 'Sem Alterações (S.A.)',
        'rev_circ_sintomas': [],
        'rev_circ_detalhes': '',
        'rev_digest': 'Sem Alterações (S.A.)',
        'rev_digest_sintomas': [],
        'rev_digest_detalhes': '',
        'rev_urinario': 'Sem Alterações (S.A.)',
        'rev_urinario_sintomas': [],
        'rev_urinario_detalhes': '',
        'rev_gen_masc': 'Sem Alterações (S.A.)',
        'rev_gen_masc_sintomas': [],
        'rev_gen_masc_detalhes': '',
        'rev_gen_fem': 'Sem Alterações (S.A.)',
        'rev_gen_fem_sintomas': [],
        'rev_gen_fem_detalhes': '',
        'rev_musc': 'Sem Alterações (S.A.)',
        'rev_musc_sintomas': [],
        'rev_musc_detalhes': '',
        'rev_linfatico': 'Sem Alterações (S.A.)',
        'rev_linfatico_sintomas': [],
        'rev_linfatico_detalhes': '',
        'rev_endocrino': 'Sem Alterações (S.A.)',
        'rev_endocrino_sintomas': [],
        'rev_endocrino_detalhes': '',
        'rev_neuro': 'Sem Alterações (S.A.)',
        'rev_neuro_sintomas': [],
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
        
        # Glasgow 2018
        'glasgow_ao': "4 - Espontânea",
        'glasgow_rv': "5 - Orientado",
        'glasgow_rm': "6 - Obedece a comandos",
        'glasgow_pupilas': "0 - Completa (As duas pupilas reagem ao estímulo de luz)",
        'glasgow_resultado_texto': "ECG: 15/15 | ECG-P: 15/15 (Normal)",
        
        # Fidedignidade
        'fide_grau': 'Fidedigna',
        'fide_justificativa': []
    }

# Lógica defensiva para garantir que chaves novas sejam integradas mesmo se houver estados de sessão antigos
defaults = {
    'sintomas_adicionais': [],
    'glasgow_ao': "4 - Espontânea",
    'glasgow_rv': "5 - Orientado",
    'glasgow_rm': "6 - Obedece a comandos",
    'glasgow_pupilas': "0 - Completa (As duas pupilas reagem ao estímulo de luz)",
    'glasgow_resultado_texto': "ECG: 15/15 | ECG-P: 15/15 (Normal)"
}
for k, v in defaults.items():
    if k not in st.session_state.anamnese:
        st.session_state.anamnese[k] = v

for k in sistemas.keys():
    if f"{k}_sintomas" not in st.session_state.anamnese:
        st.session_state.anamnese[f"{k}_sintomas"] = []

# Menu lateral de Navegação por etapas
st.sidebar.title("🩺 SemioCollect Pro")
st.sidebar.caption("Suporte Avançado à Entrevista Clínica")

etapas_nomes = [
    "1. Identificação",
    "2. Queixa Principal (Q.P.)",
    "3. História da Moléstia Atual",
    "4. Revisão dos Sistemas",
    "5. História Pessoal Patológica",
    "6. Medicamentos em Uso",
    "7. História Não Patológica",
    "8. Histórico Familiar",
    "9. Fidedignidade e Glasgow (ECG-P)",
    "📋 Revisão e Exportação"
]

# Rádio no menu lateral para pular etapas de forma rápida
etapa_selecionada = st.sidebar.radio("Etapa ativa:", etapas_nomes, index=st.session_state.etapa - 1)
st.session_state.etapa = etapas_nomes.index(etapa_selecionada) + 1

# Título do Aplicativo principal
st.title("Coleta de Anamnese Estruturada e Prontuário")
st.caption("Alinhado com Celmo Celeno Porto, 8ª ed. e protocolos práticos de OSCE.")

# ETAPA 1: IDENTIFICAÇÃO
if st.session_state.etapa == 1:
    st.header("1. Identificação do Paciente")
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.anamnese['ident_nome'] = st.text_input(
                "Nome Completo / Nome Social:",
                value=st.session_state.anamnese['ident_nome']
            )
            st.session_state.anamnese['ident_idade'] = st.number_input(
                "Idade (Anos):",
                min_value=0, max_value=120, step=1,
                value=st.session_state.anamnese['ident_idade'] if st.session_state.anamnese['ident_idade'] is not None else 0
            )
            st.session_state.anamnese['ident_sexo'] = st.selectbox(
                "Sexo Biológico (Aspecto anatômico):",
                ["Não informado", "Masculino", "Feminino"],
                index=["Não informado", "Masculino", "Feminino"].index(st.session_state.anamnese['ident_sexo'])
            )
            st.session_state.anamnese['ident_genero'] = st.text_input(
                "Identidade de Gênero (Gênero autodeclarado):",
                value=st.session_state.anamnese['ident_genero']
            )
            st.session_state.anamnese['ident_cor'] = st.selectbox(
                "Cor/Etnia (Categorias Oficiais IBGE):",
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
                "Profissão / Ocupação / Trabalho:",
                value=st.session_state.anamnese['ident_profissao']
            )
            st.session_state.anamnese['ident_naturalidade'] = st.text_input(
                "Naturalidade (Local de nascimento):",
                value=st.session_state.anamnese['ident_naturalidade']
            )
            st.session_state.anamnese['ident_procedencia'] = st.text_input(
                "Procedência / Residência Atual:",
                value=st.session_state.anamnese['ident_procedencia']
            )
            st.session_state.anamnese['ident_religiao'] = st.text_input(
                "Religião / Crença espiritual:",
                value=st.session_state.anamnese['ident_religiao']
            )
            st.session_state.anamnese['ident_leito'] = st.text_input(
                "Número do Leito (Se internado em enfermaria):",
                value=st.session_state.anamnese['ident_leito']
            )
            st.session_state.anamnese['ident_informante'] = st.text_input(
                "Fonte / Informante:",
                value=st.session_state.anamnese['ident_informante'],
                placeholder="Ex: O próprio paciente / Cônjuge (mãe/pai)"
            )
            st.session_state.anamnese['ident_acompanhante'] = st.text_input(
                "Acompanhante / Cuidador / Responsável:",
                value=st.session_state.anamnese['ident_acompanhante']
            )

# ETAPA 2: QUEIXA PRINCIPAL
elif st.session_state.etapa == 2:
    st.header("2. Queixa Principal (Q.P.)")
    with st.container(border=True):
        st.session_state.anamnese['qp_atendimento'] = st.selectbox(
            "Regime ou Foco do Atendimento:",
            ["Consulta Direta", "Encaminhamento"],
            index=["Consulta Direta", "Encaminhamento"].index(st.session_state.anamnese['qp_atendimento'])
        )
        
        if st.session_state.anamnese['qp_atendimento'] == "Consulta Direta":
            st.info("Registre o motivo principal entre aspas usando as palavras literais descritas pelo paciente.")
            st.session_state.anamnese['qp_queixa'] = st.text_area(
                "O que o paciente relatou que está sentindo / incomodando? (Aspas automáticas):",
                value=st.session_state.anamnese['qp_queixa'],
                placeholder="Ex: dor de cabeça e vômitos"
            )
        else:
            st.info("Para encaminhamentos ou avaliações de prontuário, registre o motivo em linguagem técnica.")
            st.session_state.anamnese['qp_queixa'] = st.text_area(
                "Descrição do encaminhamento clínico ou cirúrgico:",
                value=st.session_state.anamnese['qp_queixa'],
                placeholder="Ex: Avaliação pré-operatória cardíaca..."
            )
            
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.anamnese['qp_duracao_num'] = st.number_input(
                "Duração aproximada do sintoma-guia:",
                min_value=1, step=1,
                value=st.session_state.anamnese['qp_duracao_num']
            )
        with col2:
            st.session_state.anamnese['qp_duracao_unidade'] = st.selectbox(
                "Unidade de tempo correspondente:",
                ["Minutos", "Horas", "Dias", "Semanas", "Meses", "Anos"],
                index=["Minutos", "Horas", "Dias", "Semanas", "Meses", "Anos"].index(st.session_state.anamnese['qp_duracao_unidade'])
            )

# ETAPA 3: HISTÓRIA DA MOLÉSTIA ATUAL
elif st.session_state.etapa == 3:
    st.header("3. História da Moléstia Atual (H.M.A.)")
    st.caption("Investigue de forma cronológica e detalhada o sintoma-guia e demais manifestações associadas.")
    
    with st.container(border=True):
        st.subheader("Os Sete Atributos Clínicos do Sintoma Principal")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.anamnese['hma_localizacao'] = st.text_input(
                "1. Localização e Irradiação:",
                value=st.session_state.anamnese['hma_localizacao'],
                placeholder="Onde começa? Para onde irradia?"
            )
            st.session_state.anamnese['hma_caracteristica'] = st.text_input(
                "2. Característica / Tipo da Dor ou Sintoma:",
                value=st.session_state.anamnese['hma_caracteristica'],
                placeholder="Queimação, aperto, pontada, cólica, etc."
            )
            st.session_state.anamnese['hma_intensidade'] = st.slider(
                "3. Intensidade do Sintoma (0 a 10):",
                min_value=0, max_value=10,
                value=st.session_state.anamnese['hma_intensidade']
            )
            st.session_state.anamnese['hma_cronologia'] = st.text_input(
                "4. Cronologia, Padrão Temporal e Frequência:",
                value=st.session_state.anamnese['hma_cronologia'],
                placeholder="Ex: Contínua, oscilante, pior à noite, etc."
            )
        with col2:
            st.session_state.anamnese['hma_desencadeantes'] = st.text_input(
                "5. Condições de Início / Fatores Desencadeantes:",
                value=st.session_state.anamnese['hma_desencadeantes'],
                placeholder="Iniciou ao repouso, após exercício, estresse, alimentação..."
            )
            st.session_state.anamnese['hma_melhora_piora'] = st.text_input(
                "6. Fatores de Melhora e de Piora:",
                value=st.session_state.anamnese['hma_melhora_piora'],
                placeholder="Melhora sentada, piora com luz e barulho, etc."
            )
            st.session_state.anamnese['hma_manifestacoes_assoc'] = st.text_input(
                "7. Manifestações Associadas / Concomitantes:",
                value=st.session_state.anamnese['hma_manifestacoes_assoc'],
                placeholder="Outros sintomas associados ao mesmo tempo (náuseas, tremores)..."
            )

    # NOVIDADE: SEÇÃO DE DORES E SINTOMAS ADICIONAIS DINÂMICOS
    st.markdown("---")
    st.subheader("📋 Dores ou Sintomas Adicionais (Classificação Dinâmica)")
    st.caption("Caso a queixa envolva mais de uma dor ou sintoma simultâneo relevante, caracterize-os abaixo usando os atributos clínicos clássicos.")
    
    sintomas_list = st.session_state.anamnese['sintomas_adicionais']
    
    if len(sintomas_list) > 0:
        for i, sint in enumerate(sintomas_list):
            with st.expander(f"Sintoma Adicional #{i+1}: {sint.get('nome', 'Sintoma s/ nome')}", expanded=True):
                col_s1, col_s2 = st.columns(2)
                with col_s1:
                    sint['nome'] = st.text_input("Nome do Sintoma/Dor:", value=sint.get('nome', ''), key=f"sint_nome_{i}")
                    sint['localizacao'] = st.text_input("Localização e Irradiação:", value=sint.get('localizacao', ''), key=f"sint_loc_{i}")
                    sint['caracteristica'] = st.text_input("Característica / Tipo:", value=sint.get('caracteristica', ''), key=f"sint_car_{i}")
                    sint['intensidade'] = st.slider("Intensidade (0 a 10):", min_value=0, max_value=10, value=sint.get('intensidade', 5), key=f"sint_int_{i}")
                with col_s2:
                    sint['cronologia'] = st.text_input("Cronologia e Início:", value=sint.get('cronologia', ''), key=f"sint_cro_{i}")
                    sint['desencadeantes'] = st.text_input("Fatores Desencadeantes:", value=sint.get('desencadeantes', ''), key=f"sint_des_{i}")
                    sint['melhora_piora'] = st.text_input("Fatores de Melhora/Piora:", value=sint.get('melhora_piora', ''), key=f"sint_mp_{i}")
                    sint['manifestacoes_assoc'] = st.text_input("Manifestações Associadas:", value=sint.get('manifestacoes_assoc', ''), key=f"sint_ma_{i}")
                
                if st.button("🗑️ Remover este Sintoma", key=f"remove_sint_{i}"):
                    st.session_state.anamnese['sintomas_adicionais'].pop(i)
                    st.toast("Sintoma removido.")
                    st.rerun()
                    
    if st.button("➕ Adicionar outro Sintoma ou outra Dor"):
        st.session_state.anamnese['sintomas_adicionais'].append({
            'nome': 'Nova Dor / Sintoma',
            'localizacao': '',
            'caracteristica': '',
            'intensidade': 5,
            'cronologia': '',
            'desencadeantes': '',
            'melhora_piora': '',
            'manifestacoes_assoc': ''
        })
        st.rerun()

    st.markdown("---")
    with st.container(border=True):
        st.subheader("Repercussões Clínicas Sistêmicas (H.M.A.)")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.anamnese['hma_anorexia'] = st.checkbox("Anorexia / Hiporexia (Falta de apetite)", value=st.session_state.anamnese['hma_anorexia'])
            st.session_state.anamnese['hma_astenia'] = st.checkbox("Astenia (Sensação de fraqueza generalizada)", value=st.session_state.anamnese['hma_astenia'])
            st.session_state.anamnese['hma_febre'] = st.checkbox("Febre / Calafrios", value=st.session_state.anamnese['hma_febre'])
            st.session_state.anamnese['hma_emagrecimento'] = st.checkbox("Emagrecimento involuntário espontâneo", value=st.session_state.anamnese['hma_emagrecimento'])
            
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
                        "Intervalo de tempo (Meses):",
                        min_value=1, max_value=120, step=1,
                        value=st.session_state.anamnese['hma_emagrecimento_tempo']
                    )
        with col2:
            st.session_state.anamnese['hma_repercussao_funcional'] = st.text_area(
                "Grau de comprometimento das atividades (Laborais e de vida diária):",
                value=st.session_state.anamnese['hma_repercussao_funcional']
            )
            st.session_state.anamnese['hma_investigacao_previa'] = st.text_area(
                "Investigações, exames anteriores e tratamentos já realizados:",
                value=st.session_state.anamnese['hma_investigacao_previa']
            )
            st.session_state.anamnese['hma_condicao_atual'] = st.text_area(
                "Condição Atual do paciente / Situação no momento da consulta:",
                value=st.session_state.anamnese['hma_condicao_atual']
            )

# ETAPA 4: REVISÃO DOS SISTEMAS
elif st.session_state.etapa == 4:
    st.header("4. Revisão dos Sistemas / Interrogatório Sintomatológico")
    st.caption("Investigue sistematicamente os sistemas biológicos não mencionados na H.M.A. para triagem clínica.")
    
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
                    # NOVIDADE: Multi-select com opções típicas/esperadas de sintomas
                    st.session_state.anamnese[f"{chave}_sintomas"] = st.multiselect(
                        "Principais alterações semiológicas esperadas neste sistema:",
                        sistemas_sintomas.get(chave, []),
                        default=st.session_state.anamnese.get(f"{chave}_sintomas", []),
                        key=f"multi_{chave}"
                    )
                    st.session_state.anamnese[f"{chave}_detalhes"] = st.text_input(
                        "Outros achados / Observações adicionais do profissional:",
                        value=st.session_state.anamnese.get(f"{chave}_detalhes", ""),
                        key=f"txt_{chave}"
                    )
                else:
                    st.session_state.anamnese[f"{chave}_sintomas"] = []
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
                "Doenças típicas da infância relatadas:",
                infancia_lista,
                default=st.session_state.anamnese['ant_infancia']
            )
            st.session_state.anamnese['ant_infancia_outras'] = st.text_input(
                "Outros antecedentes pessoais na infância:",
                value=st.session_state.anamnese['ant_infancia_outras']
            )
        with col2:
            adulto_lista = ["Hipertensão Arterial Sanguínea (HAS)", "Diabetes Mellitus (DM)", "Dislipidemia", "Doença Coronariana Isquêmica", "Insuficiência Cardíaca", "Acidente Vascular Cerebral (AVC)", "Doença Pulmonar Obstrutiva Crônica (DPOC)", "Asma brônquica", "Tuberculose", "Doença de Chagas", "Hanseníase", "Transtorno Depressivo / Ansioso", "Osteoartrose"]
            st.session_state.anamnese['ant_adulto'] = st.multiselect(
                "Doenças crônicas / Comorbidades do adulto:",
                adulto_lista,
                default=st.session_state.anamnese['ant_adulto']
            )
            st.session_state.anamnese['ant_adulto_outras'] = st.text_input(
                "Outros diagnósticos / Antecedentes na fase adulta:",
                value=st.session_state.anamnese['ant_adulto_outras']
            )
            
    with st.container(border=True):
        st.subheader("Alergias e Intolerâncias")
        st.session_state.anamnese['ant_alergias'] = st.text_area(
            "Descreva detalhadamente intolerâncias e alergias conhecidas (medicamentos, contraste, esparadrapo, alimentos...):",
            value=st.session_state.anamnese['ant_alergias'],
            placeholder="Nega alergias ou descreva o agente e tipo de reação..."
        )

    with st.container(border=True):
        st.subheader("Hábitos e Adições")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.anamnese['ant_tabagismo'] = st.selectbox(
                "Hábito de fumar (Tabagismo):",
                ["Não fumante", "Fumante atual", "Ex-fumante"],
                index=["Não fumante", "Fumante atual", "Ex-fumante"].index(st.session_state.anamnese['ant_tabagismo'])
            )
            if st.session_state.anamnese['ant_tabagismo'] != "Não fumante":
                col_tab1, col_tab2 = st.columns(2)
                with col_tab1:
                    st.session_state.anamnese['ant_tabaco_cigs_dia'] = st.number_input(
                        "Média de cigarros consumidos ao dia:",
                        min_value=1, max_value=100, step=1,
                        value=st.session_state.anamnese['ant_tabaco_cigs_dia'] if st.session_state.anamnese['ant_tabaco_cigs_dia'] > 0 else 10
                    )
                with col_tab2:
                    st.session_state.anamnese['ant_tabaco_anos'] = st.number_input(
                        "Anos de consumo ativo de tabaco:",
                        min_value=1, max_value=80, step=1,
                        value=st.session_state.anamnese['ant_tabaco_anos'] if st.session_state.anamnese['ant_tabaco_anos'] > 0 else 10
                    )
                carga = (st.session_state.anamnese['ant_tabaco_cigs_dia'] / 20.0) * st.session_state.anamnese['ant_tabaco_anos']
                st.metric("Carga Tabágica Calculada:", f"{carga:.2f} maços-ano")
                
            st.session_state.anamnese['ant_drogas'] = st.selectbox(
                "Uso de substâncias ilícitas / anabolizantes:",
                ["Não consome", "Uso ocasional", "Uso frequente / dependência", "Histórico de uso prévio"],
                index=["Não consome", "Uso ocasional", "Uso frequente / dependência", "Histórico de uso prévio"].index(st.session_state.anamnese['ant_drogas'])
            )
            if st.session_state.anamnese['ant_drogas'] != "Não consome":
                st.session_state.anamnese['ant_drogas_detalhes'] = st.text_input(
                    "Identifique o tipo, frequência e via de administração:",
                    value=st.session_state.anamnese['ant_drogas_detalhes']
                )

        with col2:
            st.session_state.anamnese['ant_etilismo'] = st.selectbox(
                "Hábito de beber (Etilismo):",
                ["Não consome", "Consumo social", "Consumo frequente", "Consumo diário abusivo"],
                index=["Não consome", "Consumo social", "Consumo frequente", "Consumo diário abusivo"].index(st.session_state.anamnese['ant_etilismo'])
            )
            if st.session_state.anamnese['ant_etilismo'] != "Não consome":
                st.session_state.anamnese['ant_etilismo_bebida'] = st.text_input(
                    "Tipo de bebida alcóolica preferencial:",
                    value=st.session_state.anamnese['ant_etilismo_bebida'],
                    placeholder="Ex: Cerveja / Destilados"
                )
                st.session_state.anamnese['ant_etilismo_vol'] = st.text_input(
                    "Frequência e volume semanal aproximado:",
                    value=st.session_state.anamnese['ant_etilismo_vol'],
                    placeholder="Ex: 5 latas de cerveja aos sábados"
                )
                
                st.caption("Rastreamento CAGE (Suspeita de abuso/dependência de álcool):")
                st.session_state.anamnese['ant_cage_1'] = st.checkbox(
                    "C (Cut down) - Já sentiu necessidade de reduzir o consumo de bebida?",
                    value=st.session_state.anamnese['ant_cage_1']
                )
                st.session_state.anamnese['ant_cage_2'] = st.checkbox(
                    "A (Annoyed) - Sente-se irritado ou incomodado quando pessoas criticam seu hábito de beber?",
                    value=st.session_state.anamnese['ant_cage_2']
                )
                st.session_state.anamnese['ant_cage_3'] = st.checkbox(
                    "G (Guilty) - Já sentiu culpa ou remorso por beber ou fazer algo sob efeito do álcool?",
                    value=st.session_state.anamnese['ant_cage_3']
                )
                st.session_state.anamnese['ant_cage_4'] = st.checkbox(
                    "E (Eye-opener) - Precisa beber pela manhã para 'abrir os olhos', acalmar os nervos ou aliviar a ressaca?",
                    value=st.session_state.anamnese['ant_cage_4']
                )
                
                pontos_cage = sum([
                    st.session_state.anamnese['ant_cage_1'],
                    st.session_state.anamnese['ant_cage_2'],
                    st.session_state.anamnese['ant_cage_3'],
                    st.session_state.anamnese['ant_cage_4']
                ])
                if pontos_cage >= 2:
                    st.warning(f"CAGE Positivo ({pontos_cage}/4): Triagem compatível com risco elevado de abuso ou dependência do álcool.")

    with st.container(border=True):
        st.subheader("Antecedentes Médicos de Risco")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.anamnese['ant_cirurgias'] = st.text_area(
                "Procedimentos cirúrgicos prévios (Tipo, ano e complicações se houver):",
                value=st.session_state.anamnese['ant_cirurgias'],
                placeholder="Nega intervenções cirúrgicas prévias ou especifique..."
            )
            st.session_state.anamnese['ant_hospitalizacoes'] = st.text_area(
                "Internações hospitalares anteriores e traumatismos graves:",
                value=st.session_state.anamnese['ant_hospitalizacoes']
            )
        with col2:
            st.session_state.anamnese['ant_transfusoes'] = st.text_area(
                "Transfusões sanguíneas prévias (Ano e motivo):",
                value=st.session_state.anamnese['ant_transfusoes'],
                placeholder="Nega transfusões sanguíneas..."
            )
            
            # Histórico obstétrico AGO (Apenas se o sexo biológico for feminino)
            if st.session_state.anamnese['ident_sexo'] == "Feminino":
                st.markdown("**Histórico Gineco-Obstétrico (AGO):**")
                col_obs1, col_obs2, col_obs3, col_obs4 = st.columns(4)
                with col_obs1:
                    st.session_state.anamnese['ant_obstetrico_gestas'] = st.number_input("Gestações (G):", min_value=0, step=1, value=st.session_state.anamnese['ant_obstetrico_gestas'])
                with col_obs2:
                    st.session_state.anamnese['ant_obstetrico_partos'] = st.number_input("Partos (P):", min_value=0, step=1, value=st.session_state.anamnese['ant_obstetrico_partos'])
                with col_obs3:
                    st.session_state.anamnese['ant_obstetrico_abortos'] = st.number_input("Abortos (A):", min_value=0, step=1, value=st.session_state.anamnese['ant_obstetrico_abortos'])
                with col_obs4:
                    st.session_state.anamnese['ant_obstetrico_cesareas'] = st.number_input("Cesáreas (C):", min_value=0, step=1, value=st.session_state.anamnese['ant_obstetrico_cesareas'])
                
                st.session_state.anamnese['ant_obstetrico_comp'] = st.text_input(
                    "Histórico de complicações em partos, puerpério ou amamentação:",
                    value=st.session_state.anamnese['ant_obstetrico_comp']
                )

# ETAPA 6: MEDICAMENTOS EM USO ATUAL
elif st.session_state.etapa == 6:
    st.header("6. Medicamentos em Uso Atual")
    st.caption("Cadastre todo o histórico terapêutico medicamentoso ativo em formato de lista estruturada.")
    
    with st.container(border=True):
        st.subheader("➕ Adicionar Novo Fármaco:")
        col_med1, col_med2, col_med3 = st.columns(3)
        with col_med1:
            med_nome = st.text_input("Nome da Droga / Substância:", key="add_med_nome")
        with col_med2:
            med_dose = st.text_input("Dosagem / Concentração:", key="add_med_dose", placeholder="Ex: 50 mg")
        with col_med3:
            med_poso = st.text_input("Esquema diário / Posologia:", key="add_med_poso", placeholder="Ex: 1-0-1 ou 1x ao dia pela manhã")
            
        if st.button("Adicionar Medicamento à Lista"):
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
        st.subheader("Fármacos em Uso Ativo Registrados:")
        if len(st.session_state.anamnese['meds_lista']) == 0:
            st.warning("Paciente nega uso ativo de medicações contínuas de forma voluntária.")
        else:
            df_meds = pd.DataFrame(st.session_state.anamnese['meds_lista'])
            st.table(df_meds)
            
            med_excluir = st.selectbox(
                "Selecione um item para remover caso haja erro de digitação:",
                [med['nome'] for med in st.session_state.anamnese['meds_lista']]
            )
            if st.button("🗑️ Remover Fármaco Selecionado"):
                st.session_state.anamnese['meds_lista'] = [med for med in st.session_state.anamnese['meds_lista'] if med['nome'] != med_excluir]
                st.toast(f"Fármaco {med_excluir} removido.")
                st.rerun()

# ETAPA 7: HISTÓRIA NÃO PATOLÓGICA (AMBIENTAL E SOCIAL)
elif st.session_state.etapa == 7:
    st.header("7. História Pessoal Não Patológica (Ambiental e Social)")
    
    with st.container(border=True):
        st.subheader("Desenvolvimento Fisiológico e Atividade Sexual")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.anamnese['np_desenv_psicomotor'] = st.text_area(
                "Marcos do desenvolvimento psicomotor, neurológico e cognitivo:",
                value=st.session_state.anamnese['np_desenv_psicomotor'],
                placeholder="Desenvolvimento de fala, marcha e cognição sem atrasos relatados..."
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
                "Idade da Menopausa / Início do Climatério (se aplicável):",
                value=st.session_state.anamnese['np_desenv_sexual_menopausa']
            )
            st.session_state.anamnese['np_orientacao_sexual'] = st.text_input(
                "Orientação e Práticas Sexuais (Opcional - Usar nomenclatura neutra):",
                value=st.session_state.anamnese['np_orientacao_sexual'],
                placeholder="Ex: MSH (Mulheres que fazem sexo com homens) / Parceria monogâmica ativa..."
            )

    with st.container(border=True):
        st.subheader("Condições Habitacionais e Saneamento Básico")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.anamnese['np_proc_remota'] = st.text_input(
                "Procedência Remota (Cidades onde morou por mais de 6 meses no passado):",
                value=st.session_state.anamnese['np_proc_remota']
            )
            st.session_state.anamnese['np_hab_tipo'] = st.selectbox(
                "Tipo de Construção de Habitação:",
                ["Alvenaria", "Madeira", "Taipa / Adobe", "Outro"],
                index=["Alvenaria", "Madeira", "Taipa / Adobe", "Outro"].index(st.session_state.anamnese['np_hab_tipo'])
            )
        with col2:
            saneamento_opcoes = ["Água tratada", "Rede de esgoto", "Fossa séptica", "Coleta regular de lixo"]
            st.session_state.anamnese['np_hab_saneamento'] = st.multiselect(
                "Estruturas de Saneamento Básico Ativas:",
                saneamento_opcoes,
                default=st.session_state.anamnese['np_hab_saneamento']
            )
            st.session_state.anamnese['np_hab_vetores'] = st.text_input(
                "Presença de vetores epidemiológicos ou animais peçonhentos no domicílio/entorno:",
                value=st.session_state.anamnese['np_hab_vetores'],
                placeholder="Ex: Vetor triatomíneo (barbeiro), roedores, focos de mosquitos, escorpiões..."
            )

    with st.container(border=True):
        st.subheader("Hábitos Gerais e Fatores Socioeconômicos")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.anamnese['np_escolaridade'] = st.selectbox(
                "Grau de Escolaridade:",
                ["Não informado", "Analfabeto(a)", "Alfabetizado(a)", "Ensino Fundamental", "Ensino Médio", "Ensino Superior (Graduação)", "Pós-graduação"],
                index=["Não informado", "Analfabeto(a)", "Alfabetizado(a)", "Ensino Fundamental", "Ensino Médio", "Ensino Superior (Graduação)", "Pós-graduação"].index(st.session_state.anamnese['np_escolaridade'])
            )
            st.session_state.anamnese['np_renda'] = st.text_input(
                "Renda Familiar Mensal aproximada (Opcional):",
                value=st.session_state.anamnese['np_renda']
            )
            st.session_state.anamnese['np_alimentacao'] = st.selectbox(
                "Hábitos Alimentares Gerais:",
                [
                    "Alimentação quantitativa e qualitativamente adequada",
                    "Reduzida ingesta de fibras",
                    "Insuficiente consumo de proteínas (à base de carboidratos)",
                    "Consumo de calorias acima das necessidades",
                    "Alimentação com alto teor de gorduras e sódio",
                    "Baixa ingestão de líquidos diários"
                ],
                index=[
                    "Alimentação quantitativa e qualitativamente adequada",
                    "Reduzida ingesta de fibras",
                    "Insuficiente consumo de proteínas (à base de carboidratos)",
                    "Consumo de calorias acima das necessidades",
                    "Alimentação com alto teor de gorduras e sódio",
                    "Baixa ingestão de líquidos diários"
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
                placeholder="Ex: Nega atividade física estruturada / Caminhada 3x na semana por 30 minutos..."
            )
            st.session_state.anamnese['np_viagens'] = st.text_area(
                "Viagens recentes para áreas de risco sanitário ou endemias rurais:",
                value=st.session_state.anamnese['np_viagens']
            )
            st.session_state.anamnese['np_imunizacao'] = st.selectbox(
                "Situação Imunológica / Carteira de Vacinas:",
                ["Não informada", "Completa / Em dia", "Atrasada / Incompleta"],
                index=["Não informada", "Completa / Em dia", "Atrasada / Incompleta"].index(st.session_state.anamnese['np_imunizacao'])
            )

# ETAPA 8: HISTÓRICO FAMILIAR
elif st.session_state.etapa == 8:
    st.header("8. Histórico Familiar")
    
    with st.container(border=True):
        st.subheader("Estado de Saúde de Parentes Próximos")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.anamnese['fam_pai'] = st.text_area(
                "Genitor (Pai - Idade e estado de saúde se vivo, ou causa da morte e idade se falecido):",
                value=st.session_state.anamnese['fam_pai']
            )
            st.session_state.anamnese['fam_mae'] = st.text_area(
                "Genitora (Mãe - Idade e estado de saúde se vivo, ou causa da morte e idade se falecido):",
                value=st.session_state.anamnese['fam_mae']
            )
        with col2:
            st.session_state.anamnese['fam_irmaos'] = st.text_area(
                "Irmãos (Número de irmãos, idades e condições clínicas gerais):",
                value=st.session_state.anamnese['fam_irmaos']
            )
            st.session_state.anamnese['fam_filhos'] = st.text_area(
                "Filhos / Cônjuge (Descendentes e parceiro - condições clínicas):",
                value=st.session_state.anamnese['fam_filhos']
            )
            
    with st.container(border=True):
        st.subheader("Investigação de Patologias Heredofamiliares prevalentes")
        doencas_fam = ["Hipertensão Arterial Sanguínea (HAS)", "Diabetes Mellitus", "Tuberculose", "Neoplasias (Câncer de Mama/Próstata/Cólon)", "Doença Arterial Coronariana (Infarto/Angina)", "Acidente Vascular Cerebral (AVC)", "Dislipidemias", "Transtornos Psiquiátricos (ex: Bipolaridade, Esquizofrenia)", "Alcoolismo Crônico"]
        st.session_state.anamnese['fam_heredo'] = st.multiselect(
            "Selecione as comorbidades de base presentes no histórico familiar:",
            doencas_fam,
            default=st.session_state.anamnese['fam_heredo']
        )
        st.session_state.anamnese['fam_heredo_outros'] = st.text_input(
            "Outras doenças familiares importantes detectedas:",
            value=st.session_state.anamnese['fam_heredo_outros']
        )

# ETAPA 9: FIDEDIGNIDADE E GLASGOW
elif st.session_state.etapa == 9:
    st.header("9. Fidedignidade e Escala de Glasgow (ECG-P)")
    st.caption("Avaliação subjetiva da fidedignidade da anamnese e automatização do cálculo do nível de consciência.")
    
    col_fid, col_gla = st.columns([1, 1])
    
    with col_fid:
        st.subheader("🔒 Grau de Fidedignidade")
        st.session_state.anamnese['fide_grau'] = st.selectbox(
            "Classificação da Fidedignidade das informações prestadas:",
            ["Fidedigna", "Parcialmente Fidedigna", "Não Fidedigna"],
            index=["Fidedigna", "Parcialmente Fidedigna", "Não Fidedigna"].index(st.session_state.anamnese['fide_grau'])
        )
        
        justificativa_opcoes = [
            "Coerência lógica e cronológica do relato espontâneo",
            "Paciente calmo, focado e orientado no tempo e espaço",
            "Déficits de memória ou de cognição relatados/observados de forma clara",
            "Barreiras severas de linguagem ou de comunicação",
            "Relato conflitante ou confuso na cronologia",
            "Informações validadas por terceiros (acompanhante/cuidador)"
        ]
        st.session_state.anamnese['fide_justificativa'] = st.multiselect(
            "Parâmetros de justificativa clínica do profissional:",
            justificativa_opcoes,
            default=st.session_state.anamnese['fide_justificativa']
        )

    # NOVIDADE: CALCULADORA AUTOMATIZADA DA ESCALA DE COMA DE GLASGOW COM REATIVIDADE PUPILAR (2018)
    with col_gla:
        st.subheader("🧠 Escala de Glasgow com Avaliação Pupilar (ECG-P - 2018)")
        st.caption("Aferição objetiva do nível de consciência conforme diretriz da atualização de 2018.")
        
        ao_options = ["4 - Espontânea", "3 - Ao comando verbal", "2 - À dor/pressão", "1 - Sem resposta", "NT - Não testável"]
        rv_options = ["5 - Orientado", "4 - Confuso", "3 - Palavras inadequadas", "2 - Sons incompreensíveis", "1 - Sem resposta", "NT - Não testável"]
        rm_options = ["6 - Obedece a comandos", "5 - Localiza estímulo doloroso", "4 - Flexão normal (retirada)", "3 - Flexão anormal (decorticação)", "2 - Extensão (descerebração)", "1 - Sem resposta", "NT - Não testável"]
        pupilas_options = ["0 - Completa (As duas pupilas reagem ao estímulo de luz)", "1 - Parcial (Apenas uma pupila reage ao estímulo de luz)", "2 - Inexistente (Nenhuma pupila reage ao estímulo de luz)"]
        
        st.session_state.anamnese['glasgow_ao'] = st.selectbox(
            "Abertura Ocular (AO):", ao_options,
            index=ao_options.index(st.session_state.anamnese['glasgow_ao'])
        )
        st.session_state.anamnese['glasgow_rv'] = st.selectbox(
            "Resposta Verbal (RV):", rv_options,
            index=rv_options.index(st.session_state.anamnese['glasgow_rv'])
        )
        st.session_state.anamnese['glasgow_rm'] = st.selectbox(
            "Resposta Motora (RM):", rm_options,
            index=rm_options.index(st.session_state.anamnese['glasgow_rm'])
        )
        st.session_state.anamnese['glasgow_pupilas'] = st.selectbox(
            "Reatividade Pupilar (P):", pupilas_options,
            index=pupilas_options.index(st.session_state.anamnese['glasgow_pupilas'])
        )
        
        # Lógica de cálculo automatizado
        ao_val = st.session_state.anamnese['glasgow_ao'].split(" - ")[0]
        rv_val = st.session_state.anamnese['glasgow_rv'].split(" - ")[0]
        rm_val = st.session_state.anamnese['glasgow_rm'].split(" - ")[0]
        p_val = st.session_state.anamnese['glasgow_pupilas'].split(" - ")[0]
        
        if ao_val == "NT" or rv_val == "NT" or rm_val == "NT":
            gla_text = f"O{ao_val} V{rv_val} M{rm_val}"
            p_text = f"Reatividade pupilar: P{p_val}"
            st.info(f"**Glasgow por componentes:** {gla_text} | {p_text}")
            st.warning("Escore total numérico não calculável devido a componente não testável (NT).")
            st.session_state.anamnese['glasgow_resultado_texto'] = f"Componentes individuais: {gla_text} | Reatividade Pupilar: {p_text}"
        else:
            ao_score = int(ao_val)
            rv_score = int(rv_val)
            rm_score = int(rm_val)
            p_score = int(p_val)
            
            ecg_total = ao_score + rv_score + rm_score
            ecg_p_total = max(1, ecg_total - p_score)
            
            st.markdown(f"""
                <div class="calculated-box">
                    <h4>Escores de Glasgow Calculados:</h4>
                    <p><b>Escore Glasgow Padrão (ECG):</b> {ecg_total}/15</p>
                    <p><b>Escore com Reatividade Pupilar (ECG-P - 2018):</b> {ecg_p_total}/15</p>
                </div>
            """, unsafe_allow_html=True)
            
            estado_consciencia = "Vigília / Alerta"
            if ecg_total <= 8:
                estado_consciencia = "Coma"
                st.error("🚨 Alerta Clínico: Paciente em estado de coma (ECG ≤ 8). Necessidade de proteção de via aérea.")
            elif ecg_total <= 12:
                estado_consciencia = "Rebaixamento Moderado (Sonolência / Torpor / Confusão)"
                st.warning("⚠️ Alerta Clínico: Paciente apresenta rebaixamento moderado do nível de consciência.")
                
            st.session_state.anamnese['glasgow_resultado_texto'] = f"ECG: {ecg_total}/15 | ECG-P (2018): {ecg_p_total}/15 (AO: {ao_score}, RV: {rv_score}, RM: {rm_score}, P: {p_score}) - Classificação: {estado_consciencia}"

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
        st.error(f"⚠️ Atenção: Detectamos {len(lacunas)} lacunas/informações incompletas que exigem investigação complementar na próxima entrevista:")
        for lac in lacunas:
            st.markdown(f"- {lac}")
    else:
        st.success("✅ Excelente! Todas as seções e campos obrigatórios estruturados de forma robusta e sem lacunas.")

    # 2. CONSTRUÇÃO DO MARKDOWN FINAL
    # Formatação da Queixa Principal
    qp_formatada = st.session_state.anamnese['qp_queixa']
    if st.session_state.anamnese['qp_atendimento'] == "Consulta Direta" and qp_formatada:
        qp_formatada = f'"{qp_formatada}"'
    duracao = f" há {st.session_state.anamnese['qp_duracao_num']} {st.session_state.anamnese['qp_duracao_unidade'].lower()}"
    qp_final = f"{qp_formatada}{duracao}" if qp_formatada else "Não preenchida"

    # Formatação de Revisão de Sistemas com pre-defined symptoms
    is_text = ""
    for k, v in sistemas.items():
        sub_nome = v.split("(")[0].strip()
        status = st.session_state.anamnese[k]
        sintomas_selecionados = st.session_state.anamnese.get(f"{k}_sintomas", [])
        outros_detalhes = st.session_state.anamnese.get(f"{k}_detalhes", "")
        
        if status == "Com Alterações":
            detalhes_partes = []
            if sintomas_selecionados:
                detalhes_partes.append(f"Alterações relatadas: {', '.join(sintomas_selecionados)}")
            if outros_detalhes:
                detalhes_partes.append(f"Observações: {outros_detalhes}")
            
            final_detalhes = " | ".join(detalhes_partes) if detalhes_partes else "Alterações não especificadas"
            is_text += f"* **{sub_nome}:** Com Alterações ({final_detalhes})\n"
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
            etilismo_relato += f" | Rastreamento CAGE Positivo para: {', '.join(cage_itens)}"

    # Carga Tabágica
    tabagismo_relato = st.session_state.anamnese['ant_tabagismo']
    if tabagismo_relato != "Não fumante":
        carga_calc = (st.session_state.anamnese['ant_tabaco_cigs_dia'] / 20.0) * st.session_state.anamnese['ant_tabaco_anos']
        tabagismo_relato += f" ({st.session_state.anamnese['ant_tabaco_cigs_dia']} cigs/dia por {st.session_state.anamnese['ant_tabaco_anos']} anos | Carga Tabágica: {carga_calc:.2f} maços-ano)"

    # Formatação dos Medicamentos
    meds_text = ""
    if len(st.session_state.anamnese['meds_lista']) == 0:
        meds_text = "Nega uso de medicamentos de uso contínuo de forma ativa."
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

    # Formatação de Sintomas Adicionais Dinâmicos
    sintomas_adicionais_text = ""
    if len(st.session_state.anamnese['sintomas_adicionais']) > 0:
        sintomas_adicionais_text += "\n### Dores e Sintomas Adicionais Caracterizados:\n"
        for idx, sint in enumerate(st.session_state.anamnese['sintomas_adicionais']):
            sintomas_adicionais_text += f"""
#### {idx+1}. Sintoma/Dor: {sint.get('nome', 'Sem nome')}
* **Localização e Irradiação:** {sint.get('localizacao', 'Não informada')}
* **Característica / Tipo:** {sint.get('caracteristica', 'Não informada')}
* **Intensidade:** {sint.get('intensidade', 5)}/10 (Escala Analógica)
* **Cronologia / Padrão:** {sint.get('cronologia', 'Não informada')}
* **Condições de Início:** {sint.get('desencadeantes', 'Não informadas')}
* **Fatores de Melhora/Piora:** {sint.get('melhora_piora', 'Não informados')}
* **Manifestações Associadas:** {sint.get('manifestacoes_assoc', 'Não informadas')}
"""

    glasgow_text_final = st.session_state.anamnese.get('glasgow_resultado_texto', 'Não avaliada')

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
{sintomas_adicionais_text}

### Repercussões Clínicas e Gerais:
* **Estado Geral (Sintomas Gerais):** Astenia: {"Sim" if st.session_state.anamnese['hma_astenia'] else "Não"} | Anorexia: {"Sim" if st.session_state.anamnese['hma_anorexia'] else "Não"} | Febre: {"Sim" if st.session_state.anamnese['hma_febre'] else "Não"}
* **Perda Ponderal:** {"Sim, de " + str(st.session_state.anamnese['hma_emagrecimento_kg']) + " kg em " + str(st.session_state.anamnese['hma_emagrecimento_tempo']) + " meses" if st.session_state.anamnese['hma_emagrecimento'] else "Nega emagrecimento involuntário"}
* **Repercussão Funcional:** {st.session_state.anamnese['hma_repercussao_funcional'] if st.session_state.anamnese['hma_repercussao_funcional'] else 'Sem prejuízo funcional relatado'}
* **Investigações e Condutas Anteriores:** {st.session_state.anamnese['hma_investigacao_previa'] if st.session_state.anamnese['hma_investigacao_previa'] else 'Sem exames ou tratamentos prévios realizados'}
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
* **Habitação e Saneamento:** Casa de {st.session_state.anamnese['np_hab_tipo'].lower()} | Saneamento básico: {', '.join(st.session_state.anamnese['np_hab_saneamento']) if len(st.session_state.anamnese['np_hab_saneamento']) > 0 else 'Sem saneamento básico relatado'} | Vetores: {st.session_state.anamnese['np_hab_vetores'] if st.session_state.anamnese['np_hab_vetores'] else 'Sem registro de vetores no domicílio'}
* **Escolaridade / Renda:** Escolaridade: {st.session_state.anamnese['np_escolaridade']} | Renda familiar mensal: {st.session_state.anamnese['np_renda'] if st.session_state.anamnese['np_renda'] else 'Não informada'}
* **Hábitos Alimentares:** {st.session_state.anamnese['np_alimentacao']} | Detalhes: {st.session_state.anamnese['np_alimentacao_detalhes']}
* **Atividades de Lazer e Exercícios Físicos:** {st.session_state.anamnese['np_lazer_exercicio'] if st.session_state.anamnese['np_lazer_exercicio'] else 'Não realiza atividade física estruturada'}
* **Viagens Recentes:** {st.session_state.anamnese['np_viagens'] if st.session_state.anamnese['np_viagens'] else 'Não relata viagens recentes de risco epidemiológico'}
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

## 9. FIDEDIGNIDADE E EXAME NEUROLÓGICO (GLASGOW)
* **Classificação da Fidedignidade:** **{st.session_state.anamnese['fide_grau']}**
* **Fatores de validação / justificativas:** {', '.join(st.session_state.anamnese['fide_justificativa']) if len(st.session_state.anamnese['fide_justificativa']) > 0 else 'Critérios de justificativa não especificados'}
* **Escala de Coma de Glasgow com Reatividade Pupilar (ECG-P - 2018):** {glasgow_text_final}
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
