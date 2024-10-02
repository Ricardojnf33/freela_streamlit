import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Configurações do Streamlit
st.set_page_config(page_title="Dashboard de Plantio", layout="wide")

# Carregar os dados
@st.cache_data
def load_data():
    # Substitua o caminho do arquivo pelo local onde seu arquivo CSV está armazenado
    file_path = 'Controle_Plantio_set_2024.csv'
    data = pd.read_csv(file_path)

    # Remove a última linha
    data = data.iloc[:-1]

    # Remover colunas desnecessárias
    data = data.drop(columns=['Unnamed: 13', 'Unnamed: 14', 'Unnamed: 15'], errors='ignore')

    # Converter a coluna ANO para tipo numérico (se necessário)
    if 'ANO' in data.columns:
        data['ANO'] = pd.to_numeric(data['ANO'], errors='coerce')

    # Remover espaços em branco extras nos nomes das colunas
    data.columns = data.columns.str.strip()

    # Remover espaços extras da coluna 'DESCRIÇÃO DO PRF'
    if 'DESCRIÇÃO DO PRF' in data.columns:
        data['DESCRIÇÃO DO PRF'] = data['DESCRIÇÃO DO PRF'].str.strip()

    # Calcular 'Área Sem Plantio (%)'
    data['Área Sem Plantio (%)'] = 100 - data['Plantio (%)']

    # Calcular 'Mortalidade (Qtd.)' usando a taxa de mortalidade de 8,26%
    data['Mortalidade (Qtd.)'] = data['QDE de Mudas (UND)'] * 0.0826

    return data

data = load_data()

# Separar os dataframes por divisão
assetco_data = data[data['DIVISÃO'] == 'ASSETco']
devco_data = data[data['DIVISÃO'] == 'DEVco']

# Configurar as páginas
st.sidebar.title("Navegação")
page = st.sidebar.radio("Ir para", ["Home", "ASSETco", "DEVco", "Projetos"])

# ------------------ Página Home ------------------
if page == "Home":
    st.title("Dashboard de Plantio - Home")
    st.write("Visualização geral dos dados de plantio.")

    def quebra_nome_em_tres_partes(nome):
        # Remover espaços extras
        nome = nome.strip()

        # Ajustes manuais para os nomes longos
        if nome == "CE - RVE":
            return "CE\n- RVE"
        elif nome == "ASV COMPLEMENTAR - RDV":
            return "ASV\nCOMPLEMENTAR\n- RDV"
        elif nome == "BAY DE CONEXÃO - RDV":
            return "BAY\nDE CONEXÃO\n- RDV"
        elif nome == "CO SE - RVE":
            return "CO SE\n- RVE"
        elif nome == "CO SJ23 - RDV":
            return "CO\nSJ23\n- RDV"
        elif nome == "LT - RDV":
            return "LT\n- RDV"
        elif nome == "LT - RVE":
            return "LT\n- RVE"
        elif nome == "RMT SJ23 - RDV":
            return "RMT\nSJ23\n- RDV"
        elif nome == "PARQUE EÓLICO SJ23 - RDV":
            return "PARQUE\nEÓLICO\nSJ23\n- RDV"
        elif nome == "UMARI - LT - BLOCO NORTE/SUL":
            return "UMARI\n- LT - BLOCO\nNORTE/SUL"
        elif nome == "UMARI - CE - BLOCO SUL":
            return "UMARI\n- CE - BLOCO\nSUL"
        elif nome == "UMARI - CE - BLOCO NORTE":
            return "UMARI\n- CE - BLOCO\nNORTE"
        elif nome == "UMARI - ASV COMPLEMENTAR - BLOCO NORTE":
            return "UMARI\n- ASV COMPLEM.\nBLOCO NORTE"
        elif nome == "UMARI - CO CIVIL - BLOCO NORTE":
            return "UMARI\n- CO CIVIL\nBLOCO NORTE"
        elif nome == "REASSENTAMENTO - RVE":
            return "REASSENT.\n- RVE"
        elif nome == "SE - RVE":
            return "SE\n- RVE"
        elif nome == "SONDAGEM DA LT - RDV":
            return "SONDAGEM\nDA LT\n- RDV"
        elif nome == "CANTEIRO DE OBRAS CIVIL - RVE":
            return "CANTEIRO\nDE OBRAS\nCIVIL - RVE"
        elif nome == "SONDAGEM LT PARTE 1 - RVE":
            return "SONDAGEM\nLT PARTE 1\n- RVE"
        elif nome == "SONDAGEM LT PARTE 2 - RVE":
            return "SONDAGEM\nLT PARTE 2\n- RVE"
        
        # Para os códigos de PRF que não precisam de ajustes (VA84103, VA84113, etc.)
        return nome

    # Gráfico 1: Percentual de Aproveitamento das Áreas de Plantio por PRF
    
    st.markdown("<h2 style='text-align: center; color: #1C4E80; font-family: DejaVu Sans;'>Percentual de Aproveitamento das Áreas de Plantio por PRF</h2>", unsafe_allow_html=True)

    # Preparar os dados para plotagem
    plot_data = data[['DESCRIÇÃO DO PRF', 'Plantio (%)', 'Área Sem Plantio (%)']].copy()
    plot_data.set_index('DESCRIÇÃO DO PRF', inplace=True)
    plot_data.sort_values('Plantio (%)', inplace=True)

    # Plotagem
    fig, ax = plt.subplots(figsize=(20, 12))

    ind = range(len(plot_data))
    bar_width = 0.975

    # Gráfico de barras empilhadas com as cores especificadas
    p1 = ax.bar(ind, plot_data['Plantio (%)'], bar_width, color='#6AB187', label='Área Plantada (%)')
    p2 = ax.bar(ind, plot_data['Área Sem Plantio (%)'], bar_width, bottom=plot_data['Plantio (%)'], color='#D8AE58', label='Área Sem Plantio (%)')

    # Linha de mortalidade
    ax.axhline(y=8.26, color='#EA6A47', linestyle='--', linewidth=1, label='Taxa de Mortalidade')
    ax.text(len(ind) - 0.5, 8.26 + 1, '8,26%', color='#EA6A47', ha='right', va='bottom', fontsize=12, fontweight='bold', fontname='DejaVu Sans')

    # Customizações do gráfico
    ax.set_ylabel('Percentual (%)', fontname='DejaVu Sans', fontsize=12, color='#1C4E80')
    ax.set_title('Percentual de Aproveitamento das Áreas de Plantio por PRF', color='#1C4E80', fontname='DejaVu Sans', fontsize=18)

    # Definir os nomes do eixo X com a função de quebra e rotação de 90 graus
    ax.set_xticks(ind)
    ax.set_xticklabels([quebra_nome_em_tres_partes(nome) for nome in plot_data.index], rotation=90, fontname='DejaVu Sans', color='#4D4D4D', fontsize=8)

    # Ajustar o eixo Y com cor de linha em tom cinza mais escuro
    ax.tick_params(axis='y', colors='#4D4D4D')  # Cor das linhas do eixo Y
    ax.spines['left'].set_color('#4D4D4D')      # Bordas do eixo Y em cinza escuro
    ax.spines['left'].set_linewidth(1.5)

    # Limites e ajustes do gráfico
    ax.set_ylim(0, 110)
    ax.margins(x=0)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3, fontsize=12)

    # Adicionar valores percentuais nas barras
    for idx in ind:
        plantio_pct = plot_data['Plantio (%)'].iloc[idx]
        sem_plantio_pct = plot_data['Área Sem Plantio (%)'].iloc[idx]

        # Exibir percentuais dentro das barras
        if plantio_pct > 0:
            ax.text(idx, plantio_pct / 2, f"{plantio_pct:.1f}%", ha='center', va='center', color='white', fontsize=8, fontweight='bold', fontname='DejaVu Sans')

        if sem_plantio_pct > 0:
            ax.text(idx, plantio_pct + sem_plantio_pct / 2, f"{sem_plantio_pct:.1f}%", ha='center', va='center', color='black', fontsize=8, fontweight='bold', fontname='DejaVu Sans')

    # Exibir o gráfico no Streamlit
    st.pyplot(fig)

# ------------------------------------------------------------------------------------------------------------------------------------------------------

    # Gráfico 2: Resumo das Áreas de Plantio
    st.markdown("<h2 style='text-align: center; color: #1C4E80; font-family: DejaVu Sans;'>Resumo das Áreas de Plantio</h2>", unsafe_allow_html=True)

    # Dados para o resumo
    summary_data = pd.DataFrame({
        'DESCRIÇÃO DO PRF': ['CE - RVE', 'ASV COMPLEMENTAR - RDV', 'BAY DE CONEXÃO - RDV', 'CO SE - RVE', 'CO SJ23 - RDV',
                             'LT - RDV', 'LT - RVE', 'RMT SJ23 - RDV', 'PARQUE EÓLICO SJ23 - RDV', 'VA84103', 'VA84113',
                             'VA84131', 'VA84132', 'VA84134', 'VA84135', 'VA84138', 'VA84141', 'VA84142', 'VA84143',
                             'VA84157', 'VA84164', 'VA84165', 'VA8457', 'VA8481', 'WLS71069-09', 'CE - RDV',
                             'UMARI - LT - BLOCO NORTE/SUL', 'UMARI - CE - BLOCO SUL', 'UMARI - CE - BLOCO NORTE',
                             'UMARI - ASV COMPLEMENTAR - BLOCO NORTE', 'UMARI - CO CIVIL - BLOCO NORTE', 'REASSENTAMENTO - RVE',
                             'SE - RVE', 'SONDAGEM DA LT - RDV', 'CANTEIRO DE OBRAS CIVIL - RVE',
                             'SONDAGEM LT PARTE 1 - RVE', 'SONDAGEM LT PARTE 2 - RVE'],
        'Plantio (ha)': [35.180000, 13.507200, 0.039342, 0.109200, 0.030180, 3.231384, 0.495200, 3.511925, 4.785835,
                         0.088400, 0.287337, 0.202010, 0.034488, 0.097194, 0.508002, 0.013319, 0.113500, 0.382392,
                         0.437960, 0.035570, 0.132475, 0.039096, 0.032900, 0.083000, 0.008400, 43.101100,
                         1.010300, 1.554900, 3.770900, 0.656900, 0.067900, 0.161100, 0.571800, 0.258200,
                         0.302900, 0.518700, 3.188000],
        'QDE de Mudas (UND)': [87950.0000, 33768.0000, 98.3550, 273.0000, 75.4500, 8078.4600, 1238.0000, 8779.8125,
                               11964.5875, 221.0000, 718.3425, 505.0250, 86.2200, 242.9850, 1270.0050, 33.2975,
                               283.7500, 955.9800, 1094.9000, 88.9250, 331.1875, 97.7400, 82.2500, 207.5000,
                               21.0000, 107752.7500, 2525.7500, 3887.2500, 9427.2500, 1642.2500, 169.7500,
                               402.7500, 1429.5000, 645.5000, 757.2500, 1296.7500, 7970.0000],
        'Mortalidade (Qtd.)': [7264.670000, 2789.236800, 8.124123, 22.549800, 6.232170, 667.280796, 102.258800,
                               725.212513, 988.274928, 18.254600, 59.335090, 41.715065, 7.121772, 20.070561,
                               104.902413, 2.750374, 23.437750, 78.963948, 90.438740, 7.345205, 27.356088,
                               8.073324, 6.793850, 17.139500, 1.734600, 8900.377150, 208.626950, 321.086850,
                               778.690850, 135.649850, 14.021350, 33.267150, 118.076700, 53.318300, 62.548850,
                               107.111550, 658.322000]
    })

    # Normalização dos valores para o gráfico
    summary_data_normalized = summary_data.copy()
    summary_data_normalized[['Plantio (ha)', 'QDE de Mudas (UND)', 'Mortalidade (Qtd.)']] = summary_data[['Plantio (ha)', 'QDE de Mudas (UND)', 'Mortalidade (Qtd.)']].apply(lambda x: (x - x.min()) / (x.max() - x.min()))

    # Configurar os subplots
    fig, axs = plt.subplots(3, 1, figsize=(18, 14), sharex=True)

    # Definir a largura das barras
    bar_width = 1.0  # Aumente este valor para barras mais grossas

    # Plot 1: Área Plantada
    axs[0].bar(summary_data['DESCRIÇÃO DO PRF'], summary_data_normalized['Plantio (ha)'], width=bar_width, color='#1F3F49')
    axs[0].set_title('RESUMO DAS ÁREAS DE PLANTIO POR PRF', fontsize=16, fontname='DejaVu Sans', color='#1C4E80')
    axs[0].set_ylabel('Área Plantada (ha)', fontname='DejaVu Sans', color='#1C4E80')
    for i, v in enumerate(summary_data_normalized['Plantio (ha)']):
        axs[0].text(i, v + 0.01, f'{summary_data["Plantio (ha)"].iloc[i]:.2f}', ha='center', fontsize=8, fontname='DejaVu Sans')

    # Plot 2: Quantidade de Mudas
    axs[1].bar(summary_data['DESCRIÇÃO DO PRF'], summary_data_normalized['QDE de Mudas (UND)'], width=bar_width, color='#6AB187')
    axs[1].set_ylabel('Qtd. Mudas (UND)', fontname='DejaVu Sans', color='#1C4E80')
    for i, v in enumerate(summary_data_normalized['QDE de Mudas (UND)']):
        axs[1].text(i, v + 0.01, f'{summary_data["QDE de Mudas (UND)"].iloc[i]:.1f}', ha='center', fontsize=8, fontname='DejaVu Sans')

    # Plot 3: Mortalidade
    axs[2].bar(summary_data['DESCRIÇÃO DO PRF'], summary_data_normalized['Mortalidade (Qtd.)'], width=bar_width, color='#488A99')
    axs[2].set_ylabel('Mortalidade (Qtd.)', fontname='DejaVu Sans', color='#1C4E80')
    for i, v in enumerate(summary_data_normalized['Mortalidade (Qtd.)']):
        axs[2].text(i, v + 0.01, f'{summary_data["Mortalidade (Qtd.)"].iloc[i]:.1f}', ha='center', fontsize=8, fontname='DejaVu Sans')

    # Ajustar o eixo X com a função de quebra de nome e personalização
    for ax in axs:
        ax.set_xticks(range(len(summary_data['DESCRIÇÃO DO PRF'])))
        ax.set_xticklabels([quebra_nome_em_tres_partes(nome) for nome in summary_data['DESCRIÇÃO DO PRF']], rotation=90, ha='center', fontsize=8, fontname='DejaVu Sans', color='#4D4D4D')
        ax.tick_params(axis='y', colors='#4D4D4D')  # Cor das linhas do eixo Y
        ax.spines['left'].set_color('#4D4D4D')      # Bordas do eixo Y em cinza escuro
        ax.spines['left'].set_linewidth(1.5)

    # Ajustar o layout
    plt.tight_layout()
    st.pyplot(fig)

    # ------------------ Gráficos Adicionados ------------------

    # Função de categorização
    def categorize_aproveitamento(plantio_pct):
        if plantio_pct == 100:
            return '100%'
        elif 90 <= plantio_pct < 100:
            return '90%-99%'
        elif 80 <= plantio_pct < 90:
            return '80%-89%'
        elif 70 <= plantio_pct < 80:
            return '70%-79%'
        elif 60 <= plantio_pct < 70:
            return '60%-69%'
        else:
            return '<60%'

    # Aplicar a categorização
    data['Classe de Aproveitamento'] = data['Plantio (%)'].apply(categorize_aproveitamento)

    # Contagem de PRFs em cada classe
    aproveitamento_counts = data['Classe de Aproveitamento'].value_counts()

    # Definir as cores para o pie chart
    colors_aproveitamento = ['#8FD3A9', '#B1D7B0', '#74B781', '#74B7E0', '#2F5263', '#5B94C4']  # Cores mais diferenciadas

    # Gráfico de Pizza: Aproveitamento por Projeto
    
    st.markdown("<h2 style='text-align: center; color: #1C4E80; font-family: DejaVu Sans;'>Aproveitamento por Projeto</h2>", unsafe_allow_html=True)    

    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(aproveitamento_counts, colors=colors_aproveitamento, autopct='', startangle=90, wedgeprops=dict(width=0.3, edgecolor='w'))
                                        
    # Centralizar o texto no gráfico
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig.gca().add_artist(centre_circle)
    ax.set_title('APROVEITAMENTO POR PROJETO', pad=30, fontname='DejaVu Sans', color='#1C4E80')

    # Adicionar o número total no centro
    ax.text(0, 0, f'{aproveitamento_counts.sum()}', ha='center', va='center', fontsize=27, color='#1C4E80')

    # Adicionar os percentuais fora da pizza e os valores inteiros acima dos percentuais
    for i, (wedge, count) in enumerate(zip(wedges, aproveitamento_counts)):
        angle = (wedge.theta2 - wedge.theta1) / 2. + wedge.theta1
        x = 1.1 * np.cos(np.radians(angle))
        y = 1.1 * np.sin(np.radians(angle))

        # Percentual fora, entre parênteses e na cor cinza
        ax.text(x, y, f'({count / aproveitamento_counts.sum() * 100:.2f}%)', ha='center', va='center', fontsize=8, color='gray', fontname='DejaVu Sans')

        # Valor inteiro acima do percentual em preto
        ax.text(x, y + 0.15, f'{count}', ha='center', va='center', fontsize=9, color='#1C4E80', fontname='DejaVu Sans')

    # Legenda
    ax.legend(wedges, aproveitamento_counts.index, title='CLASSES DE APROVEITAMENTO:', loc='center left', 
            bbox_to_anchor=(1, 0, 0.5, 1), prop={'family': 'DejaVu Sans', 'size': 10}, 
            title_fontproperties={'family': 'DejaVu Sans', 'size': 12}, labelcolor='#1C4E80')

    # Aplicar cor ao título da legenda diretamente
    legend = ax.get_legend()
    plt.setp(legend.get_title(), color='#1C4E80')



    plt.tight_layout()
    st.pyplot(fig)

# ------------------------------------------------------------------------------------------------------------------------------------------------------

    # Contagem de divisões para ASSETco e DEVco
    divisao_counts = data['DIVISÃO'].value_counts()

    # Definir as cores para o donut chart
    colors_divisao = ['#8AB8A8', '#476B8A']  # Cores solicitadas

    # Gráfico de Donut: Gestão por Quantidade de Projetos
    st.markdown("<h2 style='text-align: center; color: #1C4E80; font-family: DejaVu Sans;'>Gestão por Quantidade de Projetos</h2>", unsafe_allow_html=True)
    
    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(divisao_counts, colors=colors_divisao, autopct='', startangle=90, wedgeprops=dict(width=0.3, edgecolor='w'))

    # Centralizar o texto no gráfico
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig.gca().add_artist(centre_circle)
    ax.set_title('GESTÃO POR QUANTIDADE DE PROJETOS', fontname='DejaVu Sans', color='#1C4E80')


    # Adicionar o número total no centro
    ax.text(0, 0, f'{aproveitamento_counts.sum()}', ha='center', va='center', fontsize=27, color='#1C4E80')

    # Adicionar os percentuais fora da pizza e os valores inteiros acima dos percentuais
    for i, (wedge, count) in enumerate(zip(wedges, aproveitamento_counts)):
        angle = (wedge.theta2 - wedge.theta1) / 2. + wedge.theta1
        x = 1.1 * np.cos(np.radians(angle))
        y = 1.1 * np.sin(np.radians(angle))

        # Percentual fora, entre parênteses e na cor cinza
        ax.text(x, y, f'({count / aproveitamento_counts.sum() * 100:.2f}%)', ha='center', va='center', fontsize=8, color='gray', fontname='DejaVu Sans')

        # Valor inteiro acima do percentual em preto
        ax.text(x, y + 0.15, f'{count}', ha='center', va='center', fontsize=9, color='#1C4E80', fontname='DejaVu Sans')


    # Legenda
    ax.legend(wedges, divisao_counts.index, title='Divisão', loc='center left', 
            bbox_to_anchor=(1, 0, 0.5, 1), prop={'family': 'DejaVu Sans', 'size': 10}, 
            title_fontproperties={'family': 'DejaVu Sans', 'size': 12}, labelcolor='#1C4E80')

    # Aplicar cor ao título da legenda diretamente
    legend = ax.get_legend()
    plt.setp(legend.get_title(), color='#1C4E80')

    plt.tight_layout()
    st.pyplot(fig)

# ------------------------------------------------------------------------------------------------------------------------------------------------------

    # Agrupando os dados por 'DIVISÃO' e somando os valores de 'Total (ha)', 'QDE de Mudas (UND)', 'Mortalidade (Qtd.)'
    division_summary = data.groupby('DIVISÃO').agg({
        'Total (ha)': 'sum',
        'QDE de Mudas (UND)': 'sum',
        'Mortalidade (Qtd.)': 'sum'
    })

    # Substituindo st.header() por st.markdown() com HTML para customização
    st.markdown("<h2 style='text-align: center; color: #1C4E80; font-family: DejaVu Sans;'>Gestão por Métricas</h2>", unsafe_allow_html=True)

    # Função para plotar os gráficos de donut
    def plot_donut_chart(column, title, division_summary, colors):
        fig, ax = plt.subplots(figsize=(8, 8))
        wedges, texts, autotexts = ax.pie(division_summary[column], colors=colors, autopct='', startangle=90, wedgeprops=dict(width=0.3, edgecolor='w'))

        # Centralizar o texto no gráfico
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig.gca().add_artist(centre_circle)
        ax.set_title(title, pad=35, fontname='DejaVu Sans', color='#1C4E80')

        # Adicionar o número total no centro
        ax.text(0, 0, f'{int(division_summary[column].sum())}', ha='center', va='center', fontsize=27, color='#1C4E80', fontname='DejaVu Sans')

        # Adicionar os percentuais fora do donut e os valores inteiros acima dos percentuais
        for i, (wedge, count) in enumerate(zip(wedges, division_summary[column])):
            angle = (wedge.theta2 - wedge.theta1) / 2. + wedge.theta1
            x = 1.2 * np.cos(np.radians(angle))
            y = 1.2 * np.sin(np.radians(angle))

            # Percentual fora, entre parênteses e na cor cinza
            ax.text(x, y, f'({count / division_summary[column].sum() * 100:.2f}%)', ha='center', va='center', fontsize=10, color='gray', fontname='DejaVu Sans')

            # Valor inteiro acima do percentual em preto
            ax.text(x, y + 0.15, f'{int(count)}', ha='center', va='center', fontsize=10, color='#1C4E80', fontname='DejaVu Sans')

        # Legenda
        ax.legend(wedges, division_summary.index, title='Divisão', loc='center left', bbox_to_anchor=(1, 0, 0.5, 1),
                prop={'family': 'DejaVu Sans', 'size': 10}, title_fontproperties={'family': 'DejaVu Sans', 'size': 12}, labelcolor='#1C4E80')

        # Aplicar cor ao título da legenda diretamente
        legend = ax.get_legend()
        plt.setp(legend.get_title(), color='#1C4E80')

        plt.tight_layout()
        st.pyplot(fig)



    # Gráfico de Donut: Gestão por Total de Hectares
    plot_donut_chart('Total (ha)', 'Gestão por Total de Hectares', division_summary, colors_divisao)

    # Gráfico de Donut: Gestão por Número de Mudas
    plot_donut_chart('QDE de Mudas (UND)', 'Gestão por Número de Mudas', division_summary, colors_divisao)

    # Gráfico de Donut: Gestão por Número de Mudas Mortas
    plot_donut_chart('Mortalidade (Qtd.)', 'Gestão por Número de Mudas Mortas', division_summary, ['#EA6A47', '#DBAE58'])

# ------------------------------------------------------------------------------------------------------------------------------------------------------

    # Agrupando os dados por 'DIVISÃO' e somando os valores de uso do solo
    land_use = data.groupby('DIVISÃO').agg({
        'Estrada(ha)': 'sum',
        'Vegetação Nativa(ha)': 'sum',
        'Plantio (ha)': 'sum',
        'Total (ha)': 'sum'
    })

    # Gráfico de Barras Horizontais: Uso do Solo
    st.markdown("<h2 style='text-align: center; color: #1C4E80; font-family: DejaVu Sans;'>Uso do Solo</h2>", unsafe_allow_html=True)

    # Definir as cores para as barras
    colors = ['#488A99', '#6AB187']  # Devco com #488A99 (azul), Assetco com #6AB187 (verde)

    # Definir a posição das barras
    y_labels = ['Estrada(ha)', 'Vegetação Nativa(ha)', 'Plantio (ha)', 'Total (ha)']
    y = np.arange(len(y_labels))

    fig, ax = plt.subplots(figsize=(10, 6))

    # Largura das barras
    height = 0.35

    # Valores para Assetco e Devco
    assetco_values = land_use.loc['ASSETco', y_labels]
    devco_values = land_use.loc['DEVco', y_labels]

    # Plotando as barras para Assetco com a cor especificada
    ax.barh(y - height/2, assetco_values, height, color=colors[1], label='ASSETco')
    for i, v in enumerate(assetco_values):
        ax.text(v + 0.5, y[i] - height/2, f'{v:.2f}', va='center', ha='left', fontsize=10, color='#1C4E80')

    # Plotando as barras para Devco com a cor especificada
    ax.barh(y + height/2, devco_values, height, color=colors[0], label='DEVco')
    for i, v in enumerate(devco_values):
        ax.text(v + 0.5, y[i] + height/2, f'{v:.2f}', va='center', ha='left', fontsize=10, color='#1C4E80')

    # Personalizar o gráfico
    ax.set_title('USO DO SOLO', fontsize=16, pad=20, fontname='DejaVu Sans', color='#1C4E80')
    ax.set_xlabel('Área (ha)', fontname='DejaVu Sans', color='#1C4E80')
    ax.set_yticks(y)
    ax.set_yticklabels(y_labels, fontname='DejaVu Sans', color='#1C4E80')

    # Configurar o estilo dos eixos
    ax.spines['left'].set_color('#4D4D4D')  # Bordas do eixo Y em cinza escuro
    ax.spines['left'].set_linewidth(1.5)
    ax.spines['bottom'].set_color('#4D4D4D')  # Bordas do eixo X em cinza escuro
    ax.spines['bottom'].set_linewidth(1.5)
    ax.tick_params(axis='x', colors='#1C4E80')  # Cor das linhas do eixo X
    ax.tick_params(axis='y', colors='#1C4E80')  # Cor das linhas do eixo Y

    # Legenda sem usar 'color' no FontProperties
    ax.legend(prop={'family': 'DejaVu Sans', 'size': 10}, labelcolor='#1C4E80')

    plt.tight_layout()
    st.pyplot(fig)

# ------------------ Página ASSETco ------------------
elif page == "ASSETco":
    st.title("Dashboard de Plantio - ASSETco")
    st.write("Visualização dos dados de plantio para a divisão ASSETco.")

    # Preparar os dados para ASSETco
    assetco_data['Área Sem Plantio (%)'] = 100 - assetco_data['Plantio (%)']
    assetco_data['Mortalidade (Qtd.)'] = assetco_data['QDE de Mudas (UND)'] * 0.0826

    # Gráfico de Barras Empilhadas - Percentual de Aproveitamento das Áreas de Plantio
    
    st.markdown("<h2 style='text-align: center; color: #1C4E80; font-family: DejaVu Sans;'>Percentual de Aproveitamento das Áreas de Plantio por PRF - ASSETco</h2>", unsafe_allow_html=True)

    plot_data_assetco = assetco_data[['DESCRIÇÃO DO PRF', 'Plantio (%)', 'Área Sem Plantio (%)']].copy()
    plot_data_assetco.set_index('DESCRIÇÃO DO PRF', inplace=True)
    plot_data_assetco.sort_values('Plantio (%)', inplace=True)

    def quebra_nome_em_tres_partes(nome):
        # Verifica se o nome pode ser dividido por '/'

        # # Remove espaços extras
        # nome = nome.strip()

        if '/' in nome:
            partes = nome.split('/')
            return '\n'.join(partes)
        
        # Ajustes manuais para nomes longos conforme a estratégia especificada
        if nome == "CE - RVE":
            return "CE\n- RVE"
        elif nome == "ASV COMPLEMENTAR - RDV":
            return "ASV\nCOMPLEMENTAR\n- RDV"
        elif nome == "BAY DE CONEXÃO - RDV":
            return "BAY\n DE\nCONEXÃO\n- RDV"
        elif nome == "CO SE - RVE":
            return "CO SE\n- RVE"
        elif nome == "CO SJ23 - RDV":
            return "CO\nSJ23\n- RDV"
        elif nome == "LT - RDV":
            return "LT\n- RDV"
        elif nome == "LT - RVE":
            return "LT\n- RVE"
        elif nome == "RMT SJ23 - RDV":
            return "RMT\nSJ23\n- RDV"
        elif nome == "PARQUE EÓLICO SJ23 - RDV":
            return "PARQUE\nEÓLICO\nSJ23\n- RDV"
        elif nome == "CE - RDV":
            return "CE\n- RDV"        
        elif nome == "UMARI - LT - BLOCO NORTE/SUL":
            return "UMARI\n- LT - BLOCO\nNORTE/SUL"
        elif nome == "UMARI - CE - BLOCO SUL":
            return "UMARI\n- CE\n - BLOCO\nSUL"
        elif nome == "UMARI - CE - BLOCO NORTE":
            return "UMARI\n- CE\n - BLOCO\nNORTE"
        elif nome == "UMARI - ASV COMPLEMENTAR - BLOCO NORTE":
            return "UMARI\n- ASV \nCOMPLEM.\nBLOCO \nNORTE"
        elif nome == "UMARI - CO CIVIL - BLOCO NORTE":
            return "UMARI\n- CO \nCIVIL\nBLOCO \nNORTE"
        elif nome == "REASSENTAMENTO - RVE":
            return "REASSENT.\n- RVE"
        elif nome == "SE - RVE":
            return "SE\n- RVE"
        elif nome == "SONDAGEM DA LT - RDV":
            return "SONDAGEM\nDA LT\n- RDV"
        elif nome == "CANTEIRO DE OBRAS CIVIL - RVE":
            return "CANTEIRO\nDE \nOBRAS\nCIVIL - \nRVE"
        elif nome == "SONDAGEM LT PARTE 1 - RVE":
            return "SONDAGEM\nLT PARTE 1\n- RVE"
        elif nome == "SONDAGEM LT PARTE 2 - RVE":
            return "SONDAGEM\nLT PARTE 2\n- RVE"
        
        # Caso nenhum ajuste seja necessário, retorna o nome original
        return nome


    # Criar a visualização
    fig, ax = plt.subplots(figsize=(18, 10))
    ind = range(len(plot_data_assetco))
    bar_width = 0.9

    # Gráfico de barras empilhadas com as cores especificadas
    p1 = ax.bar(ind, plot_data_assetco['Plantio (%)'], bar_width, color='#6AB187', label='Área Plantada (%)')
    p2 = ax.bar(ind, plot_data_assetco['Área Sem Plantio (%)'], bar_width, bottom=plot_data_assetco['Plantio (%)'], color='#D8AE58', label='Área Sem Plantio (%)')

    # Adicionar linha de mortalidade com a cor especificada
    ax.axhline(y=8.26, color='#EA6A47', linestyle='--', linewidth=1, label='Taxa de Mortalidade')
    ax.text(len(ind) - 0.5, 8.26 + 1, '8,26%', color='#EA6A47', ha='right', va='bottom', fontsize=12, fontweight='bold', fontname='DejaVu Sans')

    # Customizações do gráfico
    ax.set_ylabel('Percentual (%)', fontname='DejaVu Sans', fontsize=12, color='#1C4E80')
    ax.set_title('ASSETco - Percentual de Aproveitamento das Áreas de Plantio por PRF', color='#1C4E80', fontname='DejaVu Sans', fontsize=18)

    # Definir os nomes do eixo X com quebra de linha para descrições longas em até três partes
    ax.set_xticks(ind)
    ax.set_xticklabels([quebra_nome_em_tres_partes(label) for label in plot_data_assetco.index], rotation=0, fontname='DejaVu Sans', color='#4D4D4D', fontsize=8)

    # Ajustar o eixo Y com cor de linha em tom cinza mais escuro
    ax.tick_params(axis='y', colors='#4D4D4D')  # Tom cinza mais escuro
    ax.spines['left'].set_color('#4D4D4D')      # Bordas do eixo Y em cinza escuro
    ax.spines['left'].set_linewidth(1.5)

    # Limites e ajustes do gráfico
    ax.set_ylim(0, 110)
    ax.margins(x=0)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.10), ncol=3, fontsize=12)

    # Adicionar valores percentuais nas barras
    for idx in ind:
        plantio_pct = plot_data_assetco['Plantio (%)'].iloc[idx]
        sem_plantio_pct = plot_data_assetco['Área Sem Plantio (%)'].iloc[idx]

        # Exibir percentuais dentro das barras
        if plantio_pct > 0:
            ax.text(idx, plantio_pct / 2, f"{plantio_pct:.1f}%", ha='center', va='center', color='white', fontsize=10, fontweight='bold', fontname='DejaVu Sans')

        if sem_plantio_pct > 0:
            ax.text(idx, plantio_pct + sem_plantio_pct / 2, f"{sem_plantio_pct:.1f}%", ha='center', va='center', color='black', fontsize=10, fontweight='bold', fontname='DejaVu Sans')

    # Ajustes finais no layout
    plt.tight_layout()
    st.pyplot(fig)

# ------------------------------------------------------------------------------------------------------------

    # Gráficos de Barras - Resumo das Áreas de Plantio
    
    st.markdown("<h2 style='text-align: center; color: #1C4E80; font-family: DejaVu Sans;'>Resumo das Áreas de Plantio - ASSETco</h2>", unsafe_allow_html=True)

    # summary_data_assetco = assetco_data[['DESCRIÇÃO DO PRF', 'Plantio (ha)', 'QDE de Mudas (UND)', 'Mortalidade (Qtd.)']].copy()
    # summary_data_assetco.set_index('DESCRIÇÃO DO PRF', inplace=True)

    # # Normalização dos valores para o gráfico
    # summary_data_normalized = summary_data_assetco.copy()
    # summary_data_normalized[['Plantio (ha)', 'QDE de Mudas (UND)', 'Mortalidade (Qtd.)']] = summary_data_assetco[['Plantio (ha)', 'QDE de Mudas (UND)', 'Mortalidade (Qtd.)']].apply(lambda x: (x - x.min()) / (x.max() - x.min()))

    # fig, axs = plt.subplots(3, 1, figsize=(16, 12), sharex=True)

    # # Plot 1: Área Plantada
    # axs[0].bar(summary_data_assetco.index, summary_data_normalized['Plantio (ha)'], color='sandybrown')
    # axs[0].set_ylabel('Área Plantada (ha)')
    # axs[0].set_title('ASSETco - RESUMO DAS ÁREAS DE PLANTIO POR PRF')
    # for i, v in enumerate(summary_data_normalized['Plantio (ha)']):
    #     axs[0].text(i, v + 0.01, f'{summary_data_assetco["Plantio (ha)"].iloc[i]:.2f}', ha='center')

    # # Plot 2: Quantidade de Mudas
    # axs[1].bar(summary_data_assetco.index, summary_data_normalized['QDE de Mudas (UND)'], color='lightgreen')
    # axs[1].set_ylabel('Quantidade de Mudas (UND)')
    # for i, v in enumerate(summary_data_normalized['QDE de Mudas (UND)']):
    #     axs[1].text(i, v + 0.01, f'{summary_data_assetco["QDE de Mudas (UND)"].iloc[i]:.0f}', ha='center')

    # # Plot 3: Mortalidade
    # axs[2].bar(summary_data_assetco.index, summary_data_normalized['Mortalidade (Qtd.)'], color='lightcoral')
    # axs[2].set_ylabel('Mortalidade (Qtd.)')
    # for i, v in enumerate(summary_data_normalized['Mortalidade (Qtd.)']):
    #     axs[2].text(i, v + 0.01, f'{summary_data_assetco["Mortalidade (Qtd.)"].iloc[i]:.2f}', ha='center')

    # plt.xticks(rotation=90, ha='center')
    # plt.tight_layout()
    # st.pyplot(fig)

    # Copiar e configurar os dados
    summary_data_assetco = assetco_data[['DESCRIÇÃO DO PRF', 'Plantio (ha)', 'QDE de Mudas (UND)', 'Mortalidade (Qtd.)']].copy()
    summary_data_assetco.set_index('DESCRIÇÃO DO PRF', inplace=True)

    # Normalizar os valores para o gráfico
    summary_data_normalized = summary_data_assetco.copy()
    summary_data_normalized[['Plantio (ha)', 'QDE de Mudas (UND)', 'Mortalidade (Qtd.)']] = summary_data_assetco[['Plantio (ha)', 'QDE de Mudas (UND)', 'Mortalidade (Qtd.)']].apply(lambda x: (x - x.min()) / (x.max() - x.min()))

    fig, axs = plt.subplots(3, 1, figsize=(16, 12), sharex=True)

    # Plot 1: Área Plantada
    axs[0].bar(summary_data_assetco.index, summary_data_normalized['Plantio (ha)'], color='#1F3F49')
    axs[0].set_ylabel('Área Plantada (ha)', fontname='DejaVu Sans', color='#1C4E80')
    axs[0].set_title('ASSETco - RESUMO DAS ÁREAS DE PLANTIO POR PRF', fontname='DejaVu Sans', color='#1C4E80')
    for i, v in enumerate(summary_data_normalized['Plantio (ha)']):
        axs[0].text(i, v + 0.01, f'{summary_data_assetco["Plantio (ha)"].iloc[i]:.2f}', ha='center')

    # Plot 2: Quantidade de Mudas
    axs[1].bar(summary_data_assetco.index, summary_data_normalized['QDE de Mudas (UND)'], color='#6AB187')
    axs[1].set_ylabel('Quantidade de Mudas (UND)', fontname='DejaVu Sans', color='#1C4E80')
    for i, v in enumerate(summary_data_normalized['QDE de Mudas (UND)']):
        axs[1].text(i, v + 0.01, f'{summary_data_assetco["QDE de Mudas (UND)"].iloc[i]:.0f}', ha='center')

    # Plot 3: Mortalidade
    axs[2].bar(summary_data_assetco.index, summary_data_normalized['Mortalidade (Qtd.)'], color='#488A99')
    axs[2].set_ylabel('Mortalidade (Qtd.)', fontname='DejaVu Sans', color='#1C4E80')
    for i, v in enumerate(summary_data_normalized['Mortalidade (Qtd.)']):
        axs[2].text(i, v + 0.01, f'{summary_data_assetco["Mortalidade (Qtd.)"].iloc[i]:.2f}', ha='center')

    # Ajustes no eixo X com a função de quebra de nome e customizações
    axs[2].set_xticklabels([quebra_nome_em_tres_partes(nome) for nome in summary_data_assetco.index], rotation=0, ha='center', fontname='DejaVu Sans', color='#4D4D4D', fontsize=7)

    # Configurar o estilo dos eixos Y
    for ax in axs:
        ax.spines['left'].set_color('#4D4D4D')  # Bordas do eixo Y em cinza escuro
        ax.spines['left'].set_linewidth(1.5)
        ax.tick_params(axis='y', colors='#1C4E80')  # Cor das linhas do eixo Y

    plt.tight_layout()
    st.pyplot(fig)

# ------------------ Página DEVco ------------------
elif page == "DEVco":
    st.title("Dashboard de Plantio - DEVco")
    st.write("Visualização dos dados de plantio para a divisão DEVco.")

    # Preparar os dados para DEVco
    devco_data['Área Sem Plantio (%)'] = 100 - devco_data['Plantio (%)']
    devco_data['Mortalidade (Qtd.)'] = devco_data['QDE de Mudas (UND)'] * 0.0826

    # Gráfico de Barras Empilhadas - Percentual de Aproveitamento das Áreas de Plantio
    st.markdown("<h2 style='text-align: center; color: #1C4E80; font-family: DejaVu Sans;'>Percentual de Aproveitamento das Áreas de Plantio por PRF - DEVco</h2>", unsafe_allow_html=True)    


    plot_data_devco = devco_data[['DESCRIÇÃO DO PRF', 'Plantio (%)', 'Área Sem Plantio (%)']].copy()
    plot_data_devco.set_index('DESCRIÇÃO DO PRF', inplace=True)
    plot_data_devco.sort_values('Plantio (%)', inplace=True)

    # Criar a visualização
    fig, ax = plt.subplots(figsize=(18, 10))
    ind = range(len(plot_data_devco))
    bar_width = 0.9

    # Gráfico de barras empilhadas com as cores especificadas
    p1 = ax.bar(ind, plot_data_devco['Plantio (%)'], bar_width, color='#6AB187', label='Área Plantada (%)')
    p2 = ax.bar(ind, plot_data_devco['Área Sem Plantio (%)'], bar_width, bottom=plot_data_devco['Plantio (%)'], color='#D8AE58', label='Área Sem Plantio (%)')

    # Adicionar linha de mortalidade com a cor especificada
    ax.axhline(y=8.26, color='#EA6A47', linestyle='--', linewidth=1, label='Taxa de Mortalidade')
    ax.text(len(ind) - 0.5, 8.26 + 1, '8,26%', color='#EA6A47', ha='right', va='bottom', fontsize=12, fontweight='bold', fontname='DejaVu Sans')

    # Customizações do gráfico
    ax.set_ylabel('Percentual (%)', fontname='DejaVu Sans', fontsize=12, color='#1C4E80')
    ax.set_title('DEVco - Percentual de Aproveitamento das Áreas de Plantio por PRF', color='#1C4E80', fontname='DejaVu Sans', fontsize=18)

    # Definir os nomes do eixo X com a nova fonte e rotação
    ax.set_xticks(ind)
    ax.set_xticklabels([f'{label[:15]}\n{label[15:]}' if len(label) > 15 else label for label in plot_data_devco.index], rotation=0, fontname='DejaVu Sans', color='#4D4D4D', fontsize=10)

    # Ajustar o eixo Y com cor de linha em tom cinza mais escuro
    ax.tick_params(axis='y', colors='#4D4D4D')  # Tom cinza mais escuro
    ax.spines['left'].set_color('#4D4D4D')      # Bordas do eixo Y em cinza escuro
    ax.spines['left'].set_linewidth(1.5)

    # Limites e ajustes do gráfico
    ax.set_ylim(0, 110)
    ax.margins(x=0)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3, fontsize=12)

    # Adicionar valores percentuais nas barras
    for idx in ind:
        plantio_pct = plot_data_devco['Plantio (%)'].iloc[idx]
        sem_plantio_pct = plot_data_devco['Área Sem Plantio (%)'].iloc[idx]

        # Exibir percentuais dentro das barras
        if plantio_pct > 0:
            ax.text(idx, plantio_pct / 2, f"{plantio_pct:.1f}%", ha='center', va='center', color='white', fontsize=10, fontweight='bold', fontname='DejaVu Sans')

        if sem_plantio_pct > 0:
            ax.text(idx, plantio_pct + sem_plantio_pct / 2, f"{sem_plantio_pct:.1f}%", ha='center', va='center', color='black', fontsize=10, fontweight='bold', fontname='DejaVu Sans')

    # Ajustes finais no layout
    plt.tight_layout()
    st.pyplot(fig)

# ----------------------------------------------------------------------------------------

    # Gráficos de Barras - Resumo das Áreas de Plantio
    st.markdown("<h2 style='text-align: center; color: #1C4E80; font-family: DejaVu Sans;'>Resumo das Áreas de Plantio - DEVco</h2>", unsafe_allow_html=True)

    summary_data_devco = devco_data[['DESCRIÇÃO DO PRF', 'Plantio (ha)', 'QDE de Mudas (UND)', 'Mortalidade (Qtd.)']].copy()
    summary_data_devco.set_index('DESCRIÇÃO DO PRF', inplace=True)

    # Normalização dos valores para o gráfico
    summary_data_normalized = summary_data_devco.copy()
    summary_data_normalized[['Plantio (ha)', 'QDE de Mudas (UND)', 'Mortalidade (Qtd.)']] = summary_data_devco[['Plantio (ha)', 'QDE de Mudas (UND)', 'Mortalidade (Qtd.)']].apply(lambda x: (x - x.min()) / (x.max() - x.min()))

    fig, axs = plt.subplots(3, 1, figsize=(16, 12), sharex=True)

    # Plot 1: Área Plantada
    axs[0].bar(summary_data_devco.index, summary_data_normalized['Plantio (ha)'], color='#1F3F49')
    axs[0].set_ylabel('Área Plantada (ha)', fontname='DejaVu Sans', color='#1C4E80')
    axs[0].set_title('DEVco - RESUMO DAS ÁREAS DE PLANTIO POR PRF', fontname='DejaVu Sans', color='#1C4E80')
    for i, v in enumerate(summary_data_normalized['Plantio (ha)']):
        axs[0].text(i, v + 0.01, f'{summary_data_devco["Plantio (ha)"].iloc[i]:.2f}', ha='center')

    # Plot 2: Quantidade de Mudas
    axs[1].bar(summary_data_devco.index, summary_data_normalized['QDE de Mudas (UND)'], color='#6AB187')
    axs[1].set_ylabel('Quantidade de Mudas (UND)', fontname='DejaVu Sans', color='#1C4E80')
    for i, v in enumerate(summary_data_normalized['QDE de Mudas (UND)']):
        axs[1].text(i, v + 0.01, f'{summary_data_devco["QDE de Mudas (UND)"].iloc[i]:.0f}', ha='center')

    # Plot 3: Mortalidade
    axs[2].bar(summary_data_devco.index, summary_data_normalized['Mortalidade (Qtd.)'], color='#488A99')
    axs[2].set_ylabel('Mortalidade (Qtd.)', fontname='DejaVu Sans', color='#1C4E80')
    for i, v in enumerate(summary_data_normalized['Mortalidade (Qtd.)']):
        axs[2].text(i, v + 0.01, f'{summary_data_devco["Mortalidade (Qtd.)"].iloc[i]:.2f}', ha='center')

    # Ajustes no eixo X com as customizações
    axs[2].set_xticklabels(summary_data_devco.index, rotation=0, ha='center', fontname='DejaVu Sans', color='#4D4D4D', fontsize=9)  # Ajuste o 'fontsize' conforme necessário


    # Configurar o estilo dos eixos Y
    for ax in axs:
        ax.spines['left'].set_color('#4D4D4D')  # Bordas do eixo Y em cinza escuro
        ax.spines['left'].set_linewidth(1.5)
        ax.tick_params(axis='y', colors='#1C4E80')  # Cor das linhas do eixo Y

    plt.tight_layout()
    st.pyplot(fig)

    # ------------------ Página Projetos ------------------

elif page == "Projetos":
    st.title("Dashboard de Plantio - Projetos")
    st.write("Visualização dos dados de plantio para diferentes projetos.")

    # Assetco: Separar em dataframes para os projetos dentro da divisão ASSETco
    rio_vento_expansao_assetco = assetco_data[assetco_data['PROJETO'] == 'Rio do Vento Expansão']
    rio_vento_assetco = assetco_data[assetco_data['PROJETO'] == 'Rio do Vento']
    umari_assetco = assetco_data[assetco_data['PROJETO'] == 'UMARI']

    # Devco: Separar em dataframes para os projetos dentro da divisão DEVco
    torre_anemometrica_devco = devco_data[devco_data['PROJETO'] == 'Torre Anemométrica']

# --------------------------------------------------------------------------------------------
    # 1. Rio do Vento Expansão Assetco
    st.markdown("<h2 style='text-align: center; color: #1C4E80; font-family: DejaVu Sans;'>Rio do Vento Expansão - Assetco</h2>", unsafe_allow_html=True)

    # Preparar os dados para rio_vento_expansao_assetco
    rio_vento_expansao_assetco['Área Sem Plantio (%)'] = 100 - rio_vento_expansao_assetco['Plantio (%)']
    rio_vento_expansao_assetco['Mortalidade (Qtd.)'] = rio_vento_expansao_assetco['QDE de Mudas (UND)'] * 0.0826

    # Selecionar e organizar os dados
    plot_rio_vento_expansao_assetco = rio_vento_expansao_assetco[['DESCRIÇÃO DO PRF', 'Plantio (%)', 'Área Sem Plantio (%)']].copy()
    plot_rio_vento_expansao_assetco.set_index('DESCRIÇÃO DO PRF', inplace=True)
    plot_rio_vento_expansao_assetco.sort_values('Plantio (%)', inplace=True)

    # Criar a visualização
    fig, ax = plt.subplots(figsize=(18, 10))
    ind = range(len(plot_rio_vento_expansao_assetco))
    bar_width = 0.9

    # Gráfico de barras empilhadas com novas paletas de cores
    p1 = ax.bar(ind, plot_rio_vento_expansao_assetco['Plantio (%)'], bar_width, color='#6AB187', label='Área Plantada (%)')
    p2 = ax.bar(ind, plot_rio_vento_expansao_assetco['Área Sem Plantio (%)'], bar_width, bottom=plot_rio_vento_expansao_assetco['Plantio (%)'], color='#D8AE58', label='Área Sem Plantio (%)')

    # Adicionar linha de mortalidade com nova cor e fonte
    ax.axhline(y=8.26, color='#EA6A47', linestyle='--', linewidth=1, label='Taxa de Mortalidade')
    ax.text(len(ind) - 0.5, 8.26 + 1, '8,26%', color='#EA6A47', ha='right', va='bottom', fontsize=12, fontweight='bold', fontname='DejaVu Sans')

    # Customizações do gráfico
    ax.set_ylabel('Percentual (%)', fontname='DejaVu Sans', fontsize=12, color='#1C4E80')
    ax.set_title('Rio Vento Expansão ASSETco - Percentual de Aproveitamento das Áreas de Plantio - Rio do Vento Expansão', color='#1C4E80', fontname='DejaVu Sans', fontsize=18)

    # Definir os nomes do eixo X com a quebra de linha e nova fonte
    ax.set_xticks(ind)
    ax.set_xticklabels([f'{label[:15]}\n{label[15:]}' if len(label) > 15 else label for label in plot_rio_vento_expansao_assetco.index], rotation=0, fontname='DejaVu Sans', color='#4D4D4D', fontsize=10)

    # Ajustar o eixo Y com cor de linha em tom cinza mais escuro
    ax.tick_params(axis='y', colors='#4D4D4D')  # Tom cinza mais escuro
    ax.spines['left'].set_color('#4D4D4D')      # Bordas do eixo Y em cinza escuro
    ax.spines['left'].set_linewidth(1.5)

    # Limites e ajustes do gráfico
    ax.set_ylim(0, 110)
    ax.margins(x=0)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.10), ncol=3, fontsize=12)

    # Adicionar valores percentuais nas barras
    for idx in ind:
        plantio_pct = plot_rio_vento_expansao_assetco['Plantio (%)'].iloc[idx]
        sem_plantio_pct = plot_rio_vento_expansao_assetco['Área Sem Plantio (%)'].iloc[idx]

        # Exibir percentuais dentro das barras
        if plantio_pct > 0:
            ax.text(idx, plantio_pct / 2, f"{plantio_pct:.1f}%", ha='center', va='center', color='white', fontsize=10, fontweight='bold', fontname='DejaVu Sans')

        if sem_plantio_pct > 0:
            ax.text(idx, plantio_pct + sem_plantio_pct / 2, f"{sem_plantio_pct:.1f}%", ha='center', va='center', color='black', fontsize=10, fontweight='bold', fontname='DejaVu Sans')

    # Ajustes finais no layout
    plt.tight_layout()
    st.pyplot(fig)


# --------------------------------------------------------------------------------------------
    # Novo gráfico de resumo das áreas de plantio
    st.markdown("<h2 style='text-align: center; color: #1C4E80; font-family: DejaVu Sans;'>Resumo das Áreas de Plantio por PRF - Rio do Vento Expansão</h2>", unsafe_allow_html=True)

    fig, axs = plt.subplots(3, 1, figsize=(16, 12), sharex=True)
    rio_vento_expansao_assetco.set_index('DESCRIÇÃO DO PRF', inplace=True)

    # Plot 1: Área Plantada
    axs[0].bar(rio_vento_expansao_assetco.index, rio_vento_expansao_assetco['Plantio (ha)'], color='#1F3F49')
    axs[0].set_ylabel('Área Plantada (ha)', fontname='DejaVu Sans', color='#1C4E80')
    axs[0].set_title('Resumo das Áreas de Plantio - Rio do Vento Expansão', fontname='DejaVu Sans', color='#1C4E80')
    for i, v in enumerate(rio_vento_expansao_assetco['Plantio (ha)']):
        axs[0].text(i, v + 0.01, f'{v:.2f}', ha='center')

    # Plot 2: Quantidade de Mudas
    axs[1].bar(rio_vento_expansao_assetco.index, rio_vento_expansao_assetco['QDE de Mudas (UND)'], color='#6AB187')
    axs[1].set_ylabel('Quantidade de Mudas (UND)', fontname='DejaVu Sans', color='#1C4E80')
    for i, v in enumerate(rio_vento_expansao_assetco['QDE de Mudas (UND)']):
        axs[1].text(i, v + 0.01, f'{v:.0f}', ha='center')

    # Plot 3: Mortalidade
    axs[2].bar(rio_vento_expansao_assetco.index, rio_vento_expansao_assetco['Mortalidade (Qtd.)'], color='#488A99')
    axs[2].set_ylabel('Mortalidade (Qtd.)', fontname='DejaVu Sans', color='#1C4E80')
    for i, v in enumerate(rio_vento_expansao_assetco['Mortalidade (Qtd.)']):
        axs[2].text(i, v + 0.01, f'{v:.2f}', ha='center')

    # # Ajustar os rótulos do eixo X
    # axs[2].set_xticklabels(rio_vento_expansao_assetco.index, rotation=90, ha='center', fontname='DejaVu Sans', color='#4D4D4D', fontsize=9)

    # Definir os nomes do eixo X com a quebra de linha e nova fonte
    axs[2].set_xticks(ind)
    axs[2].set_xticklabels([f'{label[:15]}\n{label[15:]}' if len(label) > 15 else label for label in plot_rio_vento_expansao_assetco.index], rotation=0, fontname='DejaVu Sans', color='#4D4D4D', fontsize=9)

    # Configurar estilo dos eixos Y
    for ax in axs:
        ax.spines['left'].set_color('#4D4D4D')  # Cor das bordas do eixo Y
        ax.spines['left'].set_linewidth(1.5)
        ax.tick_params(axis='y', colors='#1C4E80')  # Cor das linhas do eixo Y

    plt.tight_layout()
    st.pyplot(fig)


# --------------------------------------------------------------------------------------------
    # 2. Rio do Vento Assetco
    st.markdown("<h2 style='text-align: center; color: #1C4E80; font-family: DejaVu Sans;'>Rio do Vento - Assetco</h2>", unsafe_allow_html=True)

    # Preparar os dados para rio_vento_assetco
    rio_vento_assetco['Área Sem Plantio (%)'] = 100 - rio_vento_assetco['Plantio (%)']
    rio_vento_assetco['Mortalidade (Qtd.)'] = rio_vento_assetco['QDE de Mudas (UND)'] * 0.0826

    # Selecionar e organizar os dados
    plot_rio_vento_assetco = rio_vento_assetco[['DESCRIÇÃO DO PRF', 'Plantio (%)', 'Área Sem Plantio (%)']].copy()
    plot_rio_vento_assetco.set_index('DESCRIÇÃO DO PRF', inplace=True)
    plot_rio_vento_assetco.sort_values('Plantio (%)', inplace=True)

    # Criar a visualização
    fig, ax = plt.subplots(figsize=(18, 10))
    ind = range(len(plot_rio_vento_assetco))
    bar_width = 0.9

    # Gráfico de barras empilhadas com as cores especificadas
    p1 = ax.bar(ind, plot_rio_vento_assetco['Plantio (%)'], bar_width, color='#6AB187', label='Área Plantada (%)')
    p2 = ax.bar(ind, plot_rio_vento_assetco['Área Sem Plantio (%)'], bar_width, bottom=plot_rio_vento_assetco['Plantio (%)'], color='#D8AE58', label='Área Sem Plantio (%)')

    # Adicionar linha de mortalidade com a cor especificada
    ax.axhline(y=8.26, color='#EA6A47', linestyle='--', linewidth=1, label='Taxa de Mortalidade')
    ax.text(len(ind) - 0.5, 8.26 + 1, '8,26%', color='#EA6A47', ha='right', va='bottom', fontsize=12, fontweight='bold', fontname='DejaVu Sans')

    # Customizações do gráfico
    ax.set_ylabel('Percentual (%)', fontname='DejaVu Sans', fontsize=12, color='#1C4E80')
    ax.set_title('Percentual de Aproveitamento das Áreas de Plantio - Rio do Vento ASSETco', color='#1C4E80', fontname='DejaVu Sans', fontsize=18)

    # Definir os nomes do eixo X com a quebra de linha e nova fonte
    ax.set_xticks(ind)
    ax.set_xticklabels([f'{label[:15]}\n{label[15:]}' if len(label) > 15 else label for label in plot_rio_vento_assetco.index], rotation=0, fontname='DejaVu Sans', color='#4D4D4D', fontsize=10)

    # Ajustar o eixo Y com cor de linha em tom cinza mais escuro
    ax.tick_params(axis='y', colors='#4D4D4D')  # Tom cinza mais escuro
    ax.spines['left'].set_color('#4D4D4D')      # Bordas do eixo Y em cinza escuro
    ax.spines['left'].set_linewidth(1.5)

    # Limites e ajustes do gráfico
    ax.set_ylim(0, 110)
    ax.margins(x=0)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.10), ncol=3, fontsize=12)

    # Adicionar valores percentuais nas barras
    for idx in ind:
        plantio_pct = plot_rio_vento_assetco['Plantio (%)'].iloc[idx]
        sem_plantio_pct = plot_rio_vento_assetco['Área Sem Plantio (%)'].iloc[idx]

        # Exibir percentuais dentro das barras
        if plantio_pct > 0:
            ax.text(idx, plantio_pct / 2, f"{plantio_pct:.1f}%", ha='center', va='center', color='white', fontsize=10, fontweight='bold', fontname='DejaVu Sans')

        if sem_plantio_pct > 0:
            ax.text(idx, plantio_pct + sem_plantio_pct / 2, f"{sem_plantio_pct:.1f}%", ha='center', va='center', color='black', fontsize=10, fontweight='bold', fontname='DejaVu Sans')

    # Ajustes finais no layout
    plt.tight_layout()
    st.pyplot(fig)

# --------------------------------------------------------------------------------------------
    # Novo gráfico de resumo das áreas de plantio para Rio do Vento
    st.markdown("<h2 style='text-align: center; color: #1C4E80; font-family: DejaVu Sans;'>Resumo das Áreas de Plantio - Rio do Vento</h2>", unsafe_allow_html=True)

    fig, axs = plt.subplots(3, 1, figsize=(16, 12), sharex=True)
    rio_vento_assetco.set_index('DESCRIÇÃO DO PRF', inplace=True)

    # Plot 1: Área Plantada
    axs[0].bar(rio_vento_assetco.index, rio_vento_assetco['Plantio (ha)'], color='#1F3F49')
    axs[0].set_ylabel('Área Plantada (ha)', fontname='DejaVu Sans', color='#1C4E80')
    axs[0].set_title('Resumo das Áreas de Plantio - Rio do Vento', fontname='DejaVu Sans', color='#1C4E80')
    for i, v in enumerate(rio_vento_assetco['Plantio (ha)']):
        axs[0].text(i, v + 0.01, f'{v:.2f}', ha='center')

    # Plot 2: Quantidade de Mudas
    axs[1].bar(rio_vento_assetco.index, rio_vento_assetco['QDE de Mudas (UND)'], color='#6AB187')
    axs[1].set_ylabel('Quantidade de Mudas (UND)', fontname='DejaVu Sans', color='#1C4E80')
    for i, v in enumerate(rio_vento_assetco['QDE de Mudas (UND)']):
        axs[1].text(i, v + 0.01, f'{v:.0f}', ha='center')

    # Plot 3: Mortalidade
    axs[2].bar(rio_vento_assetco.index, rio_vento_assetco['Mortalidade (Qtd.)'], color='#488A99')
    axs[2].set_ylabel('Mortalidade (Qtd.)', fontname='DejaVu Sans', color='#1C4E80')
    for i, v in enumerate(rio_vento_assetco['Mortalidade (Qtd.)']):
        axs[2].text(i, v + 0.01, f'{v:.2f}', ha='center')

    # Definir os nomes do eixo X com a quebra de linha e nova fonte
    axs[2].set_xticks(ind)
    axs[2].set_xticklabels([f'{label[:15]}\n{label[15:]}' if len(label) > 15 else label for label in rio_vento_assetco.index], rotation=0, fontname='DejaVu Sans', color='#4D4D4D', fontsize=9)

    # Configurar o estilo dos eixos Y
    for ax in axs:
        ax.spines['left'].set_color('#4D4D4D')  # Bordas do eixo Y em cinza escuro
        ax.spines['left'].set_linewidth(1.5)
        ax.tick_params(axis='y', colors='#1C4E80')  # Cor das linhas do eixo Y

    plt.tight_layout()
    st.pyplot(fig)


# --------------------------------------------------------------------------------------------

    # 3. Umari Assetco
    st.markdown("<h2 style='text-align: center; color: #1C4E80; font-family: DejaVu Sans;'>Umari Assetco</h2>", unsafe_allow_html=True)
    
    # Preparar os dados para umari_assetco
    umari_assetco['Área Sem Plantio (%)'] = 100 - umari_assetco['Plantio (%)']
    umari_assetco['Mortalidade (Qtd.)'] = umari_assetco['QDE de Mudas (UND)'] * 0.0826

    # Selecionar e organizar os dados
    plot_umari_assetco = umari_assetco[['DESCRIÇÃO DO PRF', 'Plantio (%)', 'Área Sem Plantio (%)']].copy()
    plot_umari_assetco.set_index('DESCRIÇÃO DO PRF', inplace=True)
    plot_umari_assetco.sort_values('Plantio (%)', inplace=True)

    # Criar a visualização
    fig, ax = plt.subplots(figsize=(18, 10))
    ind = range(len(plot_umari_assetco))
    bar_width = 0.9

    # Gráfico de barras empilhadas com as cores especificadas
    p1 = ax.bar(ind, plot_umari_assetco['Plantio (%)'], bar_width, color='#6AB187', label='Área Plantada (%)')
    p2 = ax.bar(ind, plot_umari_assetco['Área Sem Plantio (%)'], bar_width, bottom=plot_umari_assetco['Plantio (%)'], color='#D8AE58', label='Área Sem Plantio (%)')

    # Adicionar linha de mortalidade com a cor especificada
    ax.axhline(y=8.26, color='#EA6A47', linestyle='--', linewidth=1, label='Taxa de Mortalidade')
    ax.text(len(ind) - 0.5, 8.26 + 1, '8,26%', color='#EA6A47', ha='right', va='bottom', fontsize=12, fontweight='bold', fontname='DejaVu Sans')

    # Customizações do gráfico
    ax.set_ylabel('Percentual (%)', fontname='DejaVu Sans', fontsize=12, color='#1C4E80')
    ax.set_title('Percentual de Aproveitamento das Áreas de Plantio - Umari', color='#1C4E80', fontname='DejaVu Sans', fontsize=18)

    # Definir os nomes do eixo X com a quebra de linha e nova fonte
    ax.set_xticks(ind)
    ax.set_xticklabels([f'{label[:15]}\n{label[15:]}' if len(label) > 15 else label for label in plot_umari_assetco.index], rotation=0, fontname='DejaVu Sans', color='#4D4D4D', fontsize=10)

    # Ajustar o eixo Y com cor de linha em tom cinza mais escuro
    ax.tick_params(axis='y', colors='#4D4D4D')  # Tom cinza mais escuro
    ax.spines['left'].set_color('#4D4D4D')      # Bordas do eixo Y em cinza escuro
    ax.spines['left'].set_linewidth(1.5)

    # Limites e ajustes do gráfico
    ax.set_ylim(0, 110)
    ax.margins(x=0)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.10), ncol=3, fontsize=12)

    # Adicionar valores percentuais nas barras
    for idx in ind:
        plantio_pct = plot_umari_assetco['Plantio (%)'].iloc[idx]
        sem_plantio_pct = plot_umari_assetco['Área Sem Plantio (%)'].iloc[idx]

        # Exibir percentuais dentro das barras
        if plantio_pct > 0:
            ax.text(idx, plantio_pct / 2, f"{plantio_pct:.1f}%", ha='center', va='center', color='white', fontsize=10, fontweight='bold', fontname='DejaVu Sans')

        if sem_plantio_pct > 0:
            ax.text(idx, plantio_pct + sem_plantio_pct / 2, f"{sem_plantio_pct:.1f}%", ha='center', va='center', color='black', fontsize=10, fontweight='bold', fontname='DejaVu Sans')

    # Ajustes finais no layout
    plt.tight_layout()
    st.pyplot(fig)

# -------------------------------------------------------------------------------------------------------------

    # Novo gráfico de resumo das áreas de plantio
    st.markdown("<h2 style='text-align: center; color: #1C4E80; font-family: DejaVu Sans;'>Resumo das Áreas de Plantio por PRF - Umari</h2>", unsafe_allow_html=True)

    fig, axs = plt.subplots(3, 1, figsize=(16, 12), sharex=True)
    umari_assetco.set_index('DESCRIÇÃO DO PRF', inplace=True)

    # Plot 1: Área Plantada
    axs[0].bar(umari_assetco.index, umari_assetco['Plantio (ha)'], color='#1F3F49')
    axs[0].set_ylabel('Área Plantada (ha)', fontname='DejaVu Sans', color='#1C4E80')
    axs[0].set_title('Resumo das Áreas de Plantio - Umari', fontname='DejaVu Sans', color='#1C4E80')
    for i, v in enumerate(umari_assetco['Plantio (ha)']):
        axs[0].text(i, v + 0.01, f'{v:.2f}', ha='center')

    # Plot 2: Quantidade de Mudas
    axs[1].bar(umari_assetco.index, umari_assetco['QDE de Mudas (UND)'], color='#6AB187')
    axs[1].set_ylabel('Quantidade de Mudas (UND)', fontname='DejaVu Sans', color='#1C4E80')
    for i, v in enumerate(umari_assetco['QDE de Mudas (UND)']):
        axs[1].text(i, v + 0.01, f'{v:.0f}', ha='center')

    # Plot 3: Mortalidade
    axs[2].bar(umari_assetco.index, umari_assetco['Mortalidade (Qtd.)'], color='#488A99')
    axs[2].set_ylabel('Mortalidade (Qtd.)', fontname='DejaVu Sans', color='#1C4E80')
    for i, v in enumerate(umari_assetco['Mortalidade (Qtd.)']):
        axs[2].text(i, v + 0.01, f'{v:.2f}', ha='center')

    # Definir os nomes do eixo X com a quebra de linha e nova fonte
    axs[2].set_xticks(ind)
    axs[2].set_xticklabels([f'{label[:15]}\n{label[15:]}' if len(label) > 15 else label for label in umari_assetco.index], rotation=0, fontname='DejaVu Sans', color='#4D4D4D', fontsize=9)

    # Configurar o estilo dos eixos Y
    for ax in axs:
        ax.spines['left'].set_color('#4D4D4D')  # Bordas do eixo Y em cinza escuro
        ax.spines['left'].set_linewidth(1.5)
        ax.tick_params(axis='y', colors='#1C4E80')  # Cor das linhas do eixo Y

    plt.tight_layout()
    st.pyplot(fig)


# -----------------------------------------------------------------------------------------------

    # 4. Torre Anemométrica DEVco
    
    st.markdown("<h2 style='text-align: center; color: #1C4E80; font-family: DejaVu Sans;'>Torre Anemométrica DEVco</h2>", unsafe_allow_html=True)
    
    # Preparar os dados para torre_anemometrica_devco
    torre_anemometrica_devco['Área Sem Plantio (%)'] = 100 - torre_anemometrica_devco['Plantio (%)']
    torre_anemometrica_devco['Mortalidade (Qtd.)'] = torre_anemometrica_devco['QDE de Mudas (UND)'] * 0.0826

    # Selecionar e organizar os dados
    plot_torre_anemometrica_devco = torre_anemometrica_devco[['DESCRIÇÃO DO PRF', 'Plantio (%)', 'Área Sem Plantio (%)']].copy()
    plot_torre_anemometrica_devco.set_index('DESCRIÇÃO DO PRF', inplace=True)
    plot_torre_anemometrica_devco.sort_values('Plantio (%)', inplace=True)

    # Criar a visualização
    fig, ax = plt.subplots(figsize=(18, 10))
    ind = range(len(plot_torre_anemometrica_devco))
    bar_width = 0.9

    # Gráfico de barras empilhadas com as cores especificadas
    p1 = ax.bar(ind, plot_torre_anemometrica_devco['Plantio (%)'], bar_width, color='#6AB187', label='Área Plantada (%)')
    p2 = ax.bar(ind, plot_torre_anemometrica_devco['Área Sem Plantio (%)'], bar_width, bottom=plot_torre_anemometrica_devco['Plantio (%)'], color='#D8AE58', label='Área Sem Plantio (%)')

    # Adicionar linha de mortalidade com a cor especificada
    ax.axhline(y=8.26, color='#EA6A47', linestyle='--', linewidth=1, label='Taxa de Mortalidade')
    ax.text(len(ind) - 0.5, 8.26 + 1, '8,26%', color='#EA6A47', ha='right', va='bottom', fontsize=12, fontweight='bold', fontname='DejaVu Sans')

    # Customizações do gráfico
    ax.set_ylabel('Percentual (%)', fontname='DejaVu Sans', fontsize=12, color='#1C4E80')
    ax.set_title('Percentual de Aproveitamento das Áreas de Plantio - Torre Anemométrica', color='#1C4E80', fontname='DejaVu Sans', fontsize=18)

    # Definir os nomes do eixo X com a quebra de linha e nova fonte
    ax.set_xticks(ind)
    ax.set_xticklabels([f'{label[:15]}\n{label[15:]}' if len(label) > 15 else label for label in plot_torre_anemometrica_devco.index], rotation=0, fontname='DejaVu Sans', color='#4D4D4D', fontsize=10)

    # Ajustar o eixo Y com cor de linha em tom cinza mais escuro
    ax.tick_params(axis='y', colors='#4D4D4D')  # Tom cinza mais escuro
    ax.spines['left'].set_color('#4D4D4D')      # Bordas do eixo Y em cinza escuro
    ax.spines['left'].set_linewidth(1.5)

    # Limites e ajustes do gráfico
    ax.set_ylim(0, 110)
    ax.margins(x=0)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.10), ncol=3, fontsize=12)

    # Adicionar valores percentuais nas barras
    for idx in ind:
        plantio_pct = plot_torre_anemometrica_devco['Plantio (%)'].iloc[idx]
        sem_plantio_pct = plot_torre_anemometrica_devco['Área Sem Plantio (%)'].iloc[idx]

        # Exibir percentuais dentro das barras
        if plantio_pct > 0:
            ax.text(idx, plantio_pct / 2, f"{plantio_pct:.1f}%", ha='center', va='center', color='white', fontsize=10, fontweight='bold', fontname='DejaVu Sans')

        if sem_plantio_pct > 0:
            ax.text(idx, plantio_pct + sem_plantio_pct / 2, f"{sem_plantio_pct:.1f}%", ha='center', va='center', color='black', fontsize=10, fontweight='bold', fontname='DejaVu Sans')

    # Ajustes finais no layout
    plt.tight_layout()
    st.pyplot(fig)


    # Novo gráfico de resumo das áreas de plantio
    
    # Novo gráfico de resumo das áreas de plantio - Torre Anemométrica
    st.markdown("<h2 style='text-align: center; color: #1C4E80; font-family: DejaVu Sans;'>Resumo das Áreas de Plantio por PRF - Torre Anemométrica</h2>", unsafe_allow_html=True)

    fig, axs = plt.subplots(3, 1, figsize=(16, 12), sharex=True)
    torre_anemometrica_devco.set_index('DESCRIÇÃO DO PRF', inplace=True)

    # Plot 1: Área Plantada
    axs[0].bar(torre_anemometrica_devco.index, torre_anemometrica_devco['Plantio (ha)'], color='#1F3F49')
    axs[0].set_ylabel('Área Plantada (ha)', fontname='DejaVu Sans', color='#1C4E80')
    axs[0].set_title('Resumo das Áreas de Plantio - Torre Anemométrica', fontname='DejaVu Sans', color='#1C4E80')
    for i, v in enumerate(torre_anemometrica_devco['Plantio (ha)']):
        axs[0].text(i, v + 0.01, f'{v:.2f}', ha='center')

    # Plot 2: Quantidade de Mudas
    axs[1].bar(torre_anemometrica_devco.index, torre_anemometrica_devco['QDE de Mudas (UND)'], color='#6AB187')
    axs[1].set_ylabel('Quantidade de Mudas (UND)', fontname='DejaVu Sans', color='#1C4E80')
    for i, v in enumerate(torre_anemometrica_devco['QDE de Mudas (UND)']):
        axs[1].text(i, v + 0.01, f'{v:.0f}', ha='center')

    # Plot 3: Mortalidade
    axs[2].bar(torre_anemometrica_devco.index, torre_anemometrica_devco['Mortalidade (Qtd.)'], color='#488A99')
    axs[2].set_ylabel('Mortalidade (Qtd.)', fontname='DejaVu Sans', color='#1C4E80')
    for i, v in enumerate(torre_anemometrica_devco['Mortalidade (Qtd.)']):
        axs[2].text(i, v + 0.01, f'{v:.2f}', ha='center')

    # Ajustar os rótulos do eixo X
    axs[2].set_xticklabels(torre_anemometrica_devco.index, rotation=0, ha='center', fontname='DejaVu Sans', color='#4D4D4D', fontsize=9)

    # Configurar o estilo dos eixos Y
    for ax in axs:
        ax.spines['left'].set_color('#4D4D4D')  # Bordas do eixo Y em cinza escuro
        ax.spines['left'].set_linewidth(1.5)
        ax.tick_params(axis='y', colors='#1C4E80')  # Cor das linhas do eixo Y

    plt.tight_layout()
    st.pyplot(fig)
