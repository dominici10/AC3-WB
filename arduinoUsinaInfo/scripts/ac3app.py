import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Lendo o arquivo CSV
data = pd.read_csv('../bases_de_upload/dados_upload.csv', delimiter=';')

top_precos = 50
top_titulos = 50

# título do aplicativo
st.title('Visualizações Gráficas - Produtos Arduino|Preços')

# primeira visualização usando o Streamlit
st.header('1 - Top 20 Produtos por Preço')

# Adicione um slider para permitir ao usuário escolher o número de produtos para exibir
num_produtos = st.slider('Selecione o número de produtos para exibir', min_value=1, max_value=top_precos, value=10)

mean_price = data.groupby('titulo')['preco'].mean().reset_index()
mean_price = mean_price.sort_values('preco', ascending=False).head(num_produtos)
st.bar_chart(mean_price, x='titulo', y='preco')
st.write('Este Gráfico mostra os {} produtos com os maiores preços médios.'.format(num_produtos))


# segunda visualização usando o Streamlit
st.header('2 - Preço Mínimo e Máximo por Produto')
min_max_price = data.groupby('titulo')['preco'].agg(['min', 'max']).reset_index()
min_max_price = min_max_price.sort_values('max', ascending=False).head(top_precos)
st.bar_chart(min_max_price, x='titulo', y=['min', 'max'])
st.write('Este Grafico mostra os {} produtos com os maiores preços máximos.'.format(top_precos))



# terceira visualização usando o Plotly
st.header('3 - Box Plot')
fig = px.box(data.groupby('titulo')['preco'].mean().reset_index(), y='preco')
fig.update_layout(xaxis=dict(showticklabels=False), hovermode='closest')

# Personalizando a informação mostrada ao passar o mouse em cima dos pontos
fig.update_traces(hovertemplate='<b>Preço:</b> R$%{y:.2f}<extra></extra>')


st.plotly_chart(fig)



# quarta visualização usando o Plotly
st.header('4 - Scatter Plot')

# Criando o multiselect para selecionar os títulos
selected_titles = st.multiselect('Selecione os títulos desejados', data['titulo'].unique())

# Filtrando o DataFrame com base nos títulos selecionados
filtered_data = data[data['titulo'].isin(selected_titles)]

# Criando o gráfico scatter plot com os dados filtrados
fig = px.scatter(filtered_data.groupby('titulo')['preco'].mean().reset_index(), x='preco', y='titulo')
fig.update_layout(yaxis=dict(showticklabels=False))

# Plotando o gráfico
st.plotly_chart(fig)

st.write('Taxa de variação de preço dos produtos.')

# criando o gráfico de linha com o Plotly
st.header('5 - Preço Médio por Produto')
# Adicionando barra de seleção para escolher a quantidade de produtos a serem exibidos
top_titulos_slider = st.slider('Selecione a quantidade de produtos a serem exibidos', 1, len(mean_price), top_titulos)

# Ordenando os valores por preço médio e selecionando a quantidade de produtos escolhida pelo usuário
mean_price = mean_price.sort_values(by='preco', ascending=False)[:top_titulos_slider]

# Criando o gráfico
fig = go.Figure()
fig.add_trace(go.Scatter(x=mean_price['titulo'], y=mean_price['preco'], mode='lines+markers'))

# Adicionando título e rótulos aos eixos
fig.update_layout(title='Preço Médio por Produto (Top {})'.format(top_titulos_slider),
                  xaxis_title='Produto',
                  yaxis_title='Preço Médio')

st.plotly_chart(fig)
st.write('Este gráfico mostra os {} produtos com os maiores preços médios.'.format(top_titulos_slider))




# Criando o gráfico de pizza
st.header('6 - Gráfico de Pizza (Top {})'.format(top_titulos))

# Adicione um slider para permitir ao usuário escolher o limite mínimo de preço
limite_minimo = st.slider('Selecione o limite mínimo de preço', min_value=0, max_value=142, value=130)

# Adicione um botão para permitir ao usuário diminuir o valor do limite mínimo de preço
if st.button('Diminuir limite mínimo'):
    limite_minimo = 0


# Adicione um slider para permitir ao usuário escolher o limite máximo de preço
limite_maximo = st.slider('Selecione o limite máximo de preço', min_value=0, max_value=142, value=140)

# Adicione um botão para permitir ao usuário diminuir o valor do limite máximo de preço
if st.button('Diminuir limite máximo'):
    limite_maximo = 142
above_min = data[(data['preco'] > limite_minimo) & (data['preco'] < limite_maximo)]
below_max = data['preco'] < limite_maximo
pie_chart = above_min[below_max].groupby('titulo')['preco'].sum().reset_index()
pie_chart = pie_chart.sort_values('preco', ascending=False).head(top_titulos)

fig = go.Figure(data=[go.Pie(labels=pie_chart['titulo'], values=pie_chart['preco'])])
fig.update_layout(title='Top {} Produtos com Preço Acima de R$ {} e Abaixo de R$ {}'.format(top_titulos, limite_minimo, limite_maximo),
                  font=dict(size=16),
                  title_font=dict(size=20),
                  width=800,
                  height=600)
fig.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig)
st.write('Este Gráfico de pizza mostra os {} produtos com os maiores preços médios acima de R$ {} e abaixo de R$ {}.'.format(top_titulos, limite_minimo, limite_maximo))
