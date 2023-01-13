import pandas as pd
import streamlit as st
import plotly.express as px 
from PIL import Image
import pip
pip.main(["install", "openpyxl"])

st.set_page_config(page_title ="Survey_Results")
st.header('Survey_Results 2023')
st.subheader('I hope to Convert Excel File into a WebApp')


excel_file = 'Survey_Results.xlsx'
sheet_name = 'DATA'

df = pd.read_excel(excel_file,
                   sheet_name = sheet_name,
                   usecols='B:D',
                   header=3)
df_participants = pd.read_excel(excel_file,
                   sheet_name = sheet_name,
                   usecols='F:G',
                   header=3)
df_participants.dropna(inplace=True)

# ---SELECTION ON MY APP

department = df['Department'].unique().tolist()
ages = df['Age'].unique().tolist()
age_selection = st.slider('Age:',
                           min_value = min(ages),
                           max_value = max(ages),

                           
                           value = (min(ages),max(ages)))

department_selection = st.multiselect('Department:',
                                        department,
                                        default=department)

#---FILTER DATAFRAME BASED ON SELECTION
mask = (df['Age'].between(*age_selection)) & (df['Department']).isin(department_selection)
number_of_results = df[mask].shape[0]
st.markdown (f'*Available Results: {number_of_results}*')

#-- GROUP DATAFRAME AFTER SELECTION
df_grouped = df[mask].groupby(by=['Rating']).count()[['Age']]
df_grouped = df_grouped.rename(columns={'Age':'Votes'})
df_grouped = df_grouped.reset_index()


#---LET US PLOT OUR CHART
bar_chart = px.bar(df_grouped,
                    x='Rating',
                    y='Votes',
                    text='Votes',
                    color_discrete_sequence =  ['#F63366']*len(df_grouped),
                    template = 'plotly_white')
st.plotly_chart(bar_chart)

#----DISPLAY IMAGE AND DATAFRAME
col1,col2 = st.columns(2)
image1 = Image.open('Images\surveyanim.png')
col1.image(image1,
         caption= 'Freepik Images',
         use_column_width=True)


col2.dataframe(df[mask])
#--PIE CHART
pie_chart = px.pie(df_participants,
                title='Total No. of Participants',
                values='Participants',
                names='Departments')
st.plotly_chart(pie_chart)

