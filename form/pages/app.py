import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from io import BytesIO
from PIL import Image, ImageEnhance

def main():
    st.title("Questionário Socioeconômico")
    
    # Inicialização do estado
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 1

    def next_step():
        st.session_state.current_step += 1

    def previous_step():
        st.session_state.current_step -= 1

    # Executa a etapa atual com base no estado
    if st.session_state.current_step == 1:
        step_1(next_step)
    elif st.session_state.current_step == 2:
        step_2(next_step)
    elif st.session_state.current_step == 3:
        step_3(next_step, previous_step)
    elif st.session_state.current_step == 4:
        step_4(next_step, previous_step)

def step_1(next_step):
    st.title("Bem vindos")
    st.markdown("""

    <p>Lorem Ipsum é simplesmente um texto modelo da indústria tipográfica e de impressão. Lorem Ipsum tem sido o texto modelo padrão da indústria desde os anos 1500, quando um impressor desconhecido pegou uma galera de tipos e os embaralhou para fazer um livro de espécimes de tipos.</p>


""", unsafe_allow_html=True)
    leigeral = st.checkbox( "Aceito os termos da lei geral de proteção de dados", value=st.session_state.get('leigeral', False))
    declaracaoMaior = st.checkbox("Declaro de que sou maior de idade!", value=st.session_state.get('declaracaoMaior', False))
    
    st.session_state.leigeral = "Sim" if leigeral else "Não"
    st.session_state.declaracaoMaior = "Sim" if declaracaoMaior else "Não"
            
    
    if st.button("Avançar"):
        if leigeral and declaracaoMaior:
            st.session_state.leigeral = leigeral
            st.session_state.declaracaoMaior = declaracaoMaior
            
            next_step()
        else:
            st.error("Aceite os termos e a declaração de maioridade")

def step_2(next_step):
    st.header("Dados Pessoais")
    name = st.text_input("Digite o seu nome", value=st.session_state.get('name', ''))
    email = st.text_input("Digite o seu email", value=st.session_state.get('email', ''))
    telefone = st.text_input("Digite o telefone", value=st.session_state.get('telefone', ''))
    setor = st.text_input("Digite o seu setor", value=st.session_state.get('setor', ''))

    if st.button("Avançar"):
        if name and email:
            st.session_state.name = name
            st.session_state.email = email
            st.session_state.telefone = telefone
            st.session_state.setor = setor
            next_step()
        else:
            st.error("Preencha os campos obrigatórios")

def step_3(next_step, previous_step):
    st.header("Escolha do Curso")
    curso = st.selectbox("Escolha a primeira opção de curso", ["", "Administração", "Análise e Desenvolvimento de Sistemas", "Direito", "Pedagogia", "Enfermagem"], index=["", "Administração", "Análise e Desenvolvimento de Sistemas", "Direito", "Pedagogia", "Enfermagem"].index(st.session_state.get('curso', '')))
    turnoum = st.selectbox("Escolha o turno da primeira opção", ["", "Matutino", "Vespertino", "EAD"], index=["", "Matutino", "Vespertino", "EAD"].index(st.session_state.get('turnoum', '')))
    curso2 = st.selectbox("Escolha a segunda opção de curso", ["", "Administração", "Análise e Desenvolvimento de Sistemas", "Direito", "Pedagogia", "Enfermagem"], index=["", "Administração", "Análise e Desenvolvimento de Sistemas", "Direito", "Pedagogia", "Enfermagem"].index(st.session_state.get('curso2', '')))
    turnodois = st.selectbox("Escolha o turno da segunda opção", ["", "Matutino", "Vespertino", "EAD"], index=["", "Matutino", "Vespertino", "EAD"].index(st.session_state.get('turnodois', '')))
    unidade = st.selectbox("Escolha sua unidade", ["", "Asa Norte", "Asa Sul", "Cruzeiro", "Taguatinga", "Samambaia", "Ceilândia"], index=["", "Asa Norte", "Asa Sul", "Cruzeiro", "Taguatinga", "Samambaia", "Ceilândia"].index(st.session_state.get('unidade', '')))

    if st.button("Avançar"):
        if curso and turnoum and curso2 and turnodois and unidade:
            st.session_state.curso = curso
            st.session_state.turnoum = turnoum
            st.session_state.curso2 = curso2
            st.session_state.turnodois = turnodois
            st.session_state.unidade = unidade
            next_step()
        else:
            st.error("Preencha os campos obrigatórios")

    if st.button("Voltar"):
        previous_step()

def step_4(next_step, previous_step):
    st.header("Confirmar Dados")
    localprova = st.selectbox("Escolha o local da prova", ["", "Ceilândia", "Taguatinga", "Cruzeiro"], index=["", "Ceilândia", "Taguatinga", "Cruzeiro"].index(st.session_state.get('localprova', '')))
    data_prova = st.selectbox("Escolha a data da prova", ["", "14/08/2024 às 18:00", "15/08/2024 às 19:00", "17/08/2024 às 20:00"], index=["", "14/08/2024 às 18:00", "15/08/2024 às 19:00", "17/08/2024 às 20:00"].index(st.session_state.get('data_prova', '')))
  

    if st.button("Enviar"):
        if localprova and data_prova:
            st.session_state.localprova = localprova
            st.session_state.data_prova = data_prova
            st.success("Sua inscrição foi realizada com sucesso!")
            generate_pdf()
        else:
            st.error("Preencha todos os campos obrigatórios")

    if st.button("Voltar"):
        previous_step()

def generate_pdf():
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Adiciona a imagem
    c.drawImage('logo.png', 50, height - 100, width=50, height=50)  # Ajuste as coordenadas e o tamanho conforme necessário

    # Cabeçalho
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 100, "Questionário Socioeconômico")

    # Adiciona informações do formulário
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, height - 200, "Nome:")
    c.setFont("Helvetica", 12)
    c.drawString(150, height - 200, st.session_state.get('name', ''))

    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, height - 220, "Email:")
    c.setFont("Helvetica", 12)
    c.drawString(150, height - 220, st.session_state.get('email', ''))

    # Adiciona tabela com as informações
    data = [
        ['Campo', 'Valor'],
        ['Nome', st.session_state.get('name', '')],
        ['Email', st.session_state.get('email', '')],
        ['Telefone', st.session_state.get('telefone', '')],
        ['Setor', st.session_state.get('setor', '')],
        ['Curso 1', st.session_state.get('curso', '')],
        ['Turno 1', st.session_state.get('turnoum', '')],
        ['Curso 2', st.session_state.get('curso2', '')],
        ['Turno 2', st.session_state.get('turnodois', '')],
        ['Unidade', st.session_state.get('unidade', '')],
        ['Local da Prova', st.session_state.get('localprova', '')],
        ['Data da Prova', st.session_state.get('data_prova', '')],
        ['Declaração Maiooridade Penal', st.session_state.get('declaracaoMaior', '')],
        ['Termo de aceite', st.session_state.get('leigeral', '')],
    ]

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    table.wrapOn(c, width, height)
    table.drawOn(c, 100, height - 350)

    # Rodapé
    c.setFont("Helvetica", 10)
    c.drawString(100, 50, "Página 1")

    c.save()

    buffer.seek(0)
    st.download_button(
        label="Baixar PDF",
        data=buffer,
        file_name="inscricao_customizada.pdf",
        mime="application/pdf"
    )

if __name__ == "__main__":
    main()
