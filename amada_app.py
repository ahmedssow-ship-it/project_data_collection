
import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup as bs
from requests import get
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
import os



st.markdown("<h1 style='text-align: center; color: white;'>CoinAfrique Data Explorer</h1>", unsafe_allow_html=True)

st.markdown("""
Welcome to **CoinAfrique Data Explorer**, a user-friendly app for analyzing marketplace listings from [CoinAfrique](https://sn.coinafrique.com/).  
With this app, you can:

- **Scrape product data** across multiple pages automatically  
- **Download cleaned datasets** directly in CSV format  
- **Visualize trends and insights** with interactive charts  

**Python libraries used:** `pandas`, `streamlit`, `requests`, `beautifulsoup4`, `matplotlib`, `seaborn`, `base64`  
**Data source:** [CoinAfrique](https://sn.coinafrique.com/)
""")

# Background function
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

# Web scraping of Clothes-Shoes data on coinafrique
@st.cache_data

def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


def load(dataframe, title, key, key1) :
    # Créer 3 colonnes avec celle du milieu plus large
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button(title, key1):
            st.subheader('Display data dimension')
            st.write('Data dimension: ' + str(dataframe.shape[0]) + ' rows and ' + str(dataframe.shape[1]) + ' columns.')
            st.dataframe(dataframe)

            csv = convert_df(dataframe)

            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name='Data.csv',
                mime='text/csv',
                key = key)




def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)



# Background function
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

# Web scraping of Vehicles data on expat-dakar
@st.cache_data

def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')



def load(dataframe, title, key, key1) :
    # Créer 3 colonnes avec celle du milieu plus large
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button(title, key1):
            st.subheader('Display data dimension')
            st.write('Data dimension: ' + str(dataframe.shape[0]) + ' rows and ' + str(dataframe.shape[1]) + ' columns.')
            st.dataframe(dataframe)

            csv = convert_df(dataframe)

            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name='Data.csv',
                mime='text/csv',
                key = key)
            
            
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


        
        
# Fonction for web scraping vetements-homme
def load_vetements_hommes(mul_page):
    data = []
    # create a empty dataframe df
    df = pd.DataFrame()
    # loop over pages indexes
    for p in range(1, int(mul_page)+1):  
        url = f'https://sn.coinafrique.com/categorie/vetements-homme?page={p}'
        res = get(url)
        soup = bs(res.content, 'html.parser')
        containers = soup.find_all('div','col s6 m4 l3')
        for container in containers:
            try:
                type_clothes = container.find('p', 'ad__card-description').text
                price = container.find('p', 'ad__card-price').text
                adress = container.find('p', 'ad__card-location').span.text
                image_link = container.find('img','ad__card-img')['src'] 
            
                dic = {
                'type_clothes':type_clothes,
                'price':price,
                'adress':adress,
                'image_link':image_link
                      }
                data.append(dic)
            except: 
                pass
        
        DF = pd.DataFrame(data)
        df= pd.concat([df, DF], axis =0).reset_index(drop = True)
        
        # Clean data
        df_clean = df.drop_duplicates()
        df_clean = df_clean[df_clean['price'] != 'Prix sur demande']
        df_clean['price'] = df_clean['price'].str.replace('CFA', '')
        df_clean['price'] = df_clean['price'].str.replace(' ', '')
        df_clean['price'] = pd.to_numeric(df_clean['price'])
        df_clean.to_csv("vetements_hommes_clean.csv", index = False)
        
    return df 


# Fonction for web scraping chaussures-homme
def load_chaussures_hommes(mul_page):
    data = []
    # create a empty dataframe df
    df = pd.DataFrame()
    # loop over pages indexes
    for p in range(1, int(mul_page)+1):  
        url = f'https://sn.coinafrique.com/categorie/chaussures-homme?page={p}'
        res = get(url)
        soup = bs(res.content, 'html.parser')
        containers = soup.find_all('div','col s6 m4 l3')
        for container in containers:
            try:
                type_shoes = container.find('p', 'ad__card-description').text
                price = container.find('p', 'ad__card-price').text
                adress = container.find('p', 'ad__card-location').span.text
                image_link = container.find('img','ad__card-img')['src'] 
            
                dic = {
                'type_shoes':type_shoes,
                'price':price,
                'adress':adress,
                'image_link':image_link
                      }
                data.append(dic)
            except: 
                pass
        
        DF = pd.DataFrame(data)
        df= pd.concat([df, DF], axis =0).reset_index(drop = True)
        
        # Clean data
        df_clean = df.drop_duplicates()
        df_clean = df_clean[df_clean['price'] != 'Prix sur demande']
        df_clean['price'] = df_clean['price'].str.replace('CFA', '')
        df_clean['price'] = df_clean['price'].str.replace(' ', '')
        df_clean['price'] = pd.to_numeric(df_clean['price'])
        df_clean.to_csv("chaussures_hommes_clean.csv", index = False)
    return df

# Fonction for web scraping vetements-enfants
def load_vetements_enfants(mul_page):
    # create a empty dataframe df
    data = []
    df = pd.DataFrame()
    # loop over pages indexes
    for p in range(1, int(mul_page)+1):  
        url = f'https://sn.coinafrique.com/categorie/vetements-enfants?page={p}'
        res = get(url)
        soup = bs(res.content, 'html.parser')
        containers = soup.find_all('div','col s6 m4 l3')
        for container in containers:
            try:
                type_clothes = container.find('p', 'ad__card-description').text
                price = container.find('p', 'ad__card-price').text
                adress = container.find('p', 'ad__card-location').span.text
                image_link = container.find('img','ad__card-img')['src'] 
            
                dic = {
                'type_clothes':type_clothes,
                'price':price,
                'adress':adress,
                'image_link':image_link
                      }
                data.append(dic)
            except: 
                pass
        
        DF = pd.DataFrame(data)
        df= pd.concat([df, DF], axis =0).reset_index(drop = True)
        
        # Clean data
        df_clean = df.drop_duplicates()
        df_clean = df_clean[df_clean['price'] != 'Prix sur demande']
        df_clean['price'] = df_clean['price'].str.replace('CFA', '')
        df_clean['price'] = df_clean['price'].str.replace(' ', '')
        df_clean['price'] = pd.to_numeric(df_clean['price'])
        df_clean.to_csv("vetements_enfants_clean.csv", index = False)
    return df


# Fonction for web scraping chaussures-enfants
def load_chaussures_enfants(mul_page):
    # create a empty dataframe df
    data = []
    df = pd.DataFrame()
    # loop over pages indexes
    for p in range(1, int(mul_page)+1):  
        url = f'https://sn.coinafrique.com/categorie/chaussures-enfants?page={p}'
        res = get(url)
        soup = bs(res.content, 'html.parser')
        containers = soup.find_all('div','col s6 m4 l3')
        for container in containers:
            try:
                type_shoes = container.find('p', 'ad__card-description').text
                price = container.find('p', 'ad__card-price').text
                adress = container.find('p', 'ad__card-location').span.text
                image_link = container.find('img','ad__card-img')['src'] 
            
                dic = {
                'type_shoes':type_shoes,
                'price':price,
                'adress':adress,
                'image_link':image_link
                      }
                data.append(dic)
            except: 
                pass
        
        DF = pd.DataFrame(data)
        df= pd.concat([df, DF], axis =0).reset_index(drop = True)
        
        # Clean data
        df_clean = df.drop_duplicates()
        df_clean = df_clean[df_clean['price'] != 'Prix sur demande']
        df_clean['price'] = df_clean['price'].str.replace('CFA', '')
        df_clean['price'] = df_clean['price'].str.replace(' ', '')
        df_clean['price'] = pd.to_numeric(df_clean['price'])
        df_clean.to_csv("chaussures_enfants_clean.csv", index = False)
    return df 


st.sidebar.header('User Input Features')
Pages = st.sidebar.selectbox('Pages indexes', list([int(p) for p in np.arange(2, 600)]))
Choices = st.sidebar.selectbox('Options', ['Scrape data using Wed Scraper','Scrape data using beautifulSoup', 'Download scraped data', 'Dashbord of the data', 'Evaluate the App'])


add_bg_from_local('img_fil2.jpg') 

local_css('style.css') 

if Choices=='Scrape data using Wed Scraper':
    # load the data
    load(pd.read_csv('data/vetements_hommes.csv'), 'vetements_hommes', '1','101')
    load(pd.read_csv('data/vetements_enfants.csv'), 'vetements_enfants', '2', '102')
    load(pd.read_csv('data/chaussures_hommes.csv'), 'chaussures_hommes', '3', '103')
    load(pd.read_csv('data/chaussures_enfants.csv'), 'chaussures_enfants', '4', '104')


elif Choices=='Scrape data using beautifulSoup':
    vetements_hommes_data_mul_pag=load_vetements_hommes(Pages)
    chaussures_hommes_data_mul_pag=load_chaussures_hommes(Pages)
    vetements_enfants_data_mul_pag=load_vetements_enfants(Pages)
    chaussures_enfants_data_mul_pag=load_chaussures_enfants(Pages)
    
    load(vetements_hommes_data_mul_pag, 'vetements hommes data', '1', '101')
    load(chaussures_hommes_data_mul_pag, 'chaussures hommes data', '2', '102')
    load(vetements_enfants_data_mul_pag, 'vetements enfants data', '3', '103')
    load(chaussures_enfants_data_mul_pag, 'chaussures enfants data', '4', '104')

    
elif Choices == 'Download scraped data': 
    vetements_hommes = pd.read_csv('vetements_hommes_clean.csv')
    chaussures_hommes = pd.read_csv('chaussures_hommes_clean.csv')
    vetements_enfants = pd.read_csv('vetements_enfants_clean.csv')
    chaussures_enfants = pd.read_csv('chaussures_enfants_clean.csv')
    
    load(vetements_hommes, 'vetements hommes data', '1', '101')
    load(chaussures_hommes, 'chaussures hommes data', '2', '102')
    load(vetements_enfants, 'vetements enfants data', '3', '103')
    load(chaussures_enfants, 'chaussures enfants data', '4', '104')
    

elif  Choices == 'Dashbord of the data':
    data1 = pd.read_csv('vetements_hommes_clean.csv')
    data2 = pd.read_csv('chaussures_hommes_clean.csv')
    data3 = pd.read_csv('vetements_enfants_clean.csv')
    data4 = pd.read_csv('chaussures_enfants_clean.csv')
    
    st.subheader(" Dashboard — Analysis of the 4 categories")


    st.markdown("###  Top 5 most common articles")

    col1, col2 = st.columns(2)

    with col1:
        fig1 = plt.figure(figsize=(10,6))
        sns.barplot(x=data1['type_clothes'].value_counts()[:5].values,
                    y=data1['type_clothes'].value_counts()[:5].index)
        plt.title("Top 5 men's clothing items")
        plt.xlabel("Nombre")
        st.pyplot(fig1)

    with col2:
        fig2 = plt.figure(figsize=(10,6))
        sns.barplot(x=data2['type_shoes'].value_counts()[:5].values,
                    y=data2['type_shoes'].value_counts()[:5].index)
        plt.title("Top 5 men's shoes")
        plt.xlabel("Number")
        st.pyplot(fig2)



    st.markdown("###  Average price per item type")

    col3, col4 = st.columns(2)

    with col3:
        fig3 = plt.figure(figsize=(10,6))
        sns.barplot(data=data1, x="type_clothes", y="price", errorbar=None)
        plt.xticks(rotation=45)
        plt.title("Average price — Men's clothing")
        st.pyplot(fig3)

    with col4:
        fig4 = plt.figure(figsize=(10,6))
        sns.barplot(data=data2, x="type_shoes", y="price", errorbar=None)
        plt.xticks(rotation=45)
        plt.title("Average price — Men's shoes")
        st.pyplot(fig4)




    st.markdown("###  Award ceremony")

    col5, col6 = st.columns(2)

    with col5:
        fig5 = plt.figure(figsize=(10,6))
        sns.histplot(data1["price"], kde=True)
        plt.title("Award Ceremony — Men's Clothing")
        st.pyplot(fig5)

    with col6:
        fig6 = plt.figure(figsize=(10,6))
        sns.histplot(data2["price"], kde=True)
        plt.title("Award ceremony — Men's shoes")
        st.pyplot(fig6)




    st.markdown("###  Analysis — Children")

    col7, col8 = st.columns(2)

    with col7:
        fig7 = plt.figure(figsize=(10,6))

        top5_clothes_children = data3['type_clothes'].value_counts().head(5)

        plt.pie(
            top5_clothes_children.values,
            labels=top5_clothes_children.index,
            autopct='%1.1f%%',
            startangle=140
        )
    plt.title("Top 5 children's clothing items")
    plt.tight_layout()
    st.pyplot(fig7)
    with col8:
        fig8 = plt.figure(figsize=(10,6))
        sns.barplot(x=data4['type_shoes'].value_counts()[:5].values,
                    y=data4['type_shoes'].value_counts()[:5].index)
        plt.title("Top 5 children's shoes")
        st.pyplot(fig8)


else :

    st.markdown("<h3 style='text-align: center;'>Give your Feedback</h3>", unsafe_allow_html=True)

    # centrer les deux boutons
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Kobo Evaluation Form"):
            st.markdown(
                '<meta http-equiv="refresh" content="0; url=https://ee.kobotoolbox.org/x/4ep3EmZb">',
                unsafe_allow_html=True
            )

    with col2:
        if st.button("Google Forms Evaluation"):
            st.markdown(
                '<meta http-equiv="refresh" content="0; url=https://forms.gle/gTg77pn8rnFrfoEd6">',
                unsafe_allow_html=True
            )



