import pandas as pd
import streamlit as st
import plotly.express as px

st.title('Base de datos de programas internacionales')

df = pd.read_csv('DF_int_final.csv')

st.caption('En esta página se muestra una serie de gráficas descriptivas de la información de la base de datos de programas internacionales del tecnológico de monterrey, dentro de las cuales se le da respuesta a dos hipótesis.')
#Filtros
year_options = df['Año'].unique().tolist()

# Alumnos aceptados en primera opcion:
st.header('1. ¿El 96"%" de los estudiantes que aplican a un programa académico en el extranjero quedan en su primera opción?')

year = st.selectbox('Año a visualizar', year_options, 0)
df_flt = df[df['Año']==year]


# Figura 1
df_acep = df_flt.loc[:,['Escuela','1ra_op','no_1ra_op']]
df_acep = df_acep.groupby(['Escuela']).sum()
sums = df_acep.select_dtypes(pd.np.number).sum().rename('total')
df_acep.append(sums)
df_acep.loc['total'] = df_acep.select_dtypes(pd.np.number).sum()
df_acep['Porcentaje_si'] = round(df_acep['1ra_op']/(df_acep['1ra_op'] + df_acep['no_1ra_op']),2)
df_acep['Porcentaje_no'] = [1-i for i in df_acep['Porcentaje_si']]
df_acep = df_acep.iloc[:8]

fig1 = px.bar(df_acep, x= df_acep.index, y=["Porcentaje_si", 'Porcentaje_no'], title="Indice anual de alumnos aceptados en su primera opción de intercambo"
,width=800, height=500)
st.write(fig1)

# Figura 2
df_acep_tot = df_flt.loc[:,['Escuela','1ra_op','no_1ra_op']]
df_acep_tot = df_acep_tot.groupby(['Escuela']).sum()
sums = df_acep_tot.select_dtypes(pd.np.number).sum().rename('total')
df_acep_tot.append(sums)
df_acep_tot.loc['total'] = df_acep_tot.select_dtypes(pd.np.number).sum()
df_acep_tot['Aceptados'] = round(df_acep_tot['1ra_op']/(df_acep_tot['1ra_op'] + df_acep_tot['no_1ra_op']),2)
df_acep_tot['No aceptados'] = [1-i for i in df_acep_tot['Aceptados']]
df_acep_tot = df_acep_tot.loc['total':]
df_acep_tot.drop(columns = ['1ra_op','no_1ra_op'], inplace= True)
df_acep_tot = df_acep_tot.transpose()

fig2 = px.pie(df_acep_tot, values = 'total', names = df_acep_tot.index, title="Indice anual total de alumnos aceptados en su primera opción de intercambo")
st.write(fig2)

# Figura 3
df_acep_tot2 = df.loc[:,['Escuela','Posición','Continente','Promedio']]
df_acep_tot2.rename({'Prom_ran':'Promedio'}, inplace = True)

fig3 = px.parallel_categories(df_acep_tot2,dimensions=['Escuela','Posición','Continente'], title = 'Histórico de alumnos aceptados y rechazados en su primera opción por promedio y continente de intercambio', color_continuous_scale=px.colors.sequential.Sunset, color = 'Promedio'
,width=900, height=500
)
st.plotly_chart(fig3, use_container_width=True)
fig3.update_layout(coloraxis_colorbar_x=+1.1)
st.write(fig3)

st.header('2. ¿Cada periodo el 80"%" de los alumnos se internacionalizan vía intercambio y solo el 20"%" se internacionaliza con un study abroad, certificación, verano o invierno?')

#Figura 4
escuela = df['Escuela'].unique().tolist()
escuela_op = st.selectbox('Escuela/s que se desean ver',escuela , 0)
df_flt2 = df[df['Escuela'] == escuela_op]

prog_año = df_flt2.loc[:,['Año', 'INT', 'SA']]
prog_año = prog_año.groupby('Año').sum()
sums = prog_año.select_dtypes(pd.np.number).sum().rename('total')
prog_año.append(sums)
prog_año.loc['total'] = prog_año.select_dtypes(pd.np.number).sum()

prog_año['Intercambios'] = round(prog_año['INT']/(prog_año['INT'] + prog_año['SA']),2)
prog_año['Study Abroad'] = [1-i for i in prog_año['Intercambios']]

fig4 = px.bar(prog_año, x= prog_año.index, y=['Study Abroad',"Intercambios"], title="Proporción de intercambios vs proporción de programas 'Study Abroad' por año escolar")
st.write(fig4)

# Figura 5

fig5 = px.parallel_categories(df,dimensions=['Escuela','Tipo de programa','Continente'],title="Total histórico de programas de intercambio y Study Abroad por escuela y continente", color_continuous_scale=px.colors.sequential.Peach, color = 'Promedio')
fig5.update_layout(coloraxis_colorbar_x=+1.1)
st.write(fig5)
#Sitio de programas int: Debe de tener un titulo, descripcion y graficas
