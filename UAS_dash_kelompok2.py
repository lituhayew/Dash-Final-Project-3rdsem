#!/usr/bin/env python
# coding: utf-8

# # **Dash**
# 
# ### Kelompok 2
#     1. Karin Emanuela
#     2. Boe, Felita
#     3. Samita Lituhayu

# ### Import Package dan Data

# In[1]:


# Import Packages
import pandas as pd
import numpy as np


# In[2]:


sales_df = pd.read_excel('AdventureWorksSales-individual project.xlsx', sheet_name='Sales_data')
product_df = pd.read_excel('AdventureWorksSales-individual project.xlsx', sheet_name='Product_data')
date_df = pd.read_excel('AdventureWorksSales-individual project.xlsx', sheet_name='Date_data')
cust_df = pd.read_excel('AdventureWorksSales-individual project.xlsx', sheet_name='Customer_data')
order_df = pd.read_excel('AdventureWorksSales-individual project.xlsx', sheet_name='Sales Order_data')

# Mengganti nama kolom DateKey menjadi OrderDateKey pada df date_df
date_df = date_df.rename(columns={'DateKey': 'OrderDateKey'})

# Left join berdasarkan kolom 'ProductKey'
datamart = pd.merge(sales_df, product_df, on='ProductKey', how='left')

# Left join berdasarkan kolom 'OrderDateKey'
datamart = pd.merge(datamart, date_df, on='OrderDateKey', how='left')

# Left join berdasarkan kolom 'CustomerKey'
datamart = pd.merge(datamart, cust_df, on='CustomerKey', how='left')

# Left join berdasarkan kolom 'SalesOrderLineKey'
datamart = pd.merge(datamart, order_df, on='SalesOrderLineKey', how='left')

# Menampilkan dataframe hasil left join
print(datamart)


# In[3]:


datamart = pd.merge(sales_df, product_df, on='ProductKey', how='left')
datamart.head(5)


# In[4]:


datamart.info()


# In[5]:


# Ubah tipe data kolom OrderDateKey menjadi datetime
datamart['OrderDateKey'] = pd.to_datetime(datamart['OrderDateKey'], format='%Y%m%d')

# Extract the quarter and year from the date column
datamart['quarter'] = datamart['OrderDateKey'].dt.quarter
datamart['year'] = datamart['OrderDateKey'].dt.year

# Group by year and quarter
datamart.head()


# ### Dash

# In[6]:


import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


# In[7]:


app = dash.Dash(__name__)


# In[8]:


# Most Ordered Category
most_ordered = datamart.groupby('Category')['Order Quantity'].sum().reset_index()
most_ordered_pie = px.pie(most_ordered, names='Category', values='Order Quantity', title='Most Ordered Items',
labels={'Category': 'Categories', 'Order Quantity': 'Items Ordered'})


most_ordered_pie.show()


# Karena Most Ordered Items adalah kategori Bikes, maka selanjutnya akan dianalisis Subcategory Bikes mana yang penjualannya paling tinggi

# In[9]:


subcat = datamart['Subcategory'].unique()
subcat


# In[10]:


bikes = datamart[datamart['Category']=='Bikes']
bikes.head()


# In[11]:


subcat_bike = bikes['Subcategory'].unique()
subcat_bike


# In[12]:


bike_color = bikes['Color'].unique()
bike_color


# In[13]:


qrt_sales_cat = datamart.groupby(['year', 'quarter', 'Category'])['Sales Amount'].mean().reset_index()
qrt_sales_cat


# In[14]:


# Multi line chart showing sales amount per category for each quarter
categories = datamart['Category'].unique()
filtered = qrt_sales_cat[qrt_sales_cat['Category'].isin(categories)]  
linechart = px.line(filtered, x='quarter', y='Sales Amount', color='Category', facet_col='year')
linechart.show()


# In[15]:


# Merge Sales Data dengan Customer Data
country_data = pd.merge(sales_df, cust_df, on='CustomerKey', how='left')
country_data.head(5)


# In[16]:


country_data.columns


# In[17]:


# Create Bar Chart that Shows Sales Amount on Each Country-Region
country_sales = country_data.groupby('Country-Region')['Sales Amount'].mean().sort_values(ascending=False).reset_index()
country_sales


# In[18]:


barchart_country = px.bar(country_sales, x='Country-Region', y='Sales Amount', title='Average Sales on Each Country-Region')
barchart_country


# In[27]:


import plotly.graph_objs as go
# Load data
df = datamart

# Create app
app = dash.Dash(__name__)

# Line Chart

# Define layout
app.layout = html.Div([
    html.H1("Adventure Works' Sales Data"),
    dcc.Markdown('''
        ### Introduction

        Dataset yang dianalisis adalah data penjualan milik Adventure Works, sebuah toko yang menjual berbagai peralatan
        olahraga. Dari dataset tersebut ditemukan bahwa terdapat 4 Category produk di toko mereka, yaitu Bikes, Clothing, Accessories, dan Components.
        
        Pertama tama, akan dilakukan analisis mengenai kategori produk mana yang paling diminati,
        melalui total Order Quantity.
                 
    '''),
    dcc.Graph(
        id='graph1',
        figure={
            'data':[
                go.Pie(
                    labels=most_ordered['Category'],
                    values=most_ordered['Order Quantity']
                )
            ],
            'layout': go.Layout(
                title='Most Ordered Category',
                hovermode='closest'
            )
        }
    ),
    dcc.Markdown('''
        ### Result:

        Berdasarkan analisis di atas, diketahui bahwa kategori produk yang paling diminati adalah kategori Bikes.
        Selanjutnya, akan dianalisis Sales Amount tiap warna pada Sub-category Bikes.
    '''),

    dcc.Markdown('''
                 

        ## Subcategory Sales and Overall Sales on Each Country
                 
        ### Sales per Subcategory
       Dalam analisis kali ini, kita akan melihat penjualan berdasarkan Subcategory. Di sini, user dapat memilih Category pada dropdown
                 untuk melihat sales Subcategory Category yang dipilih.
    '''),
    dcc.Dropdown(
        id='dropdown',
        options = [{'label':i, 'value': i} for i in df['Category'].unique()],
        value='Bikes'
    ),
    dcc.Graph(
        id='graph2'
    ),
    dcc.Markdown('''
        ### Result:

        Melalui graph di atas, untuk Category Bikes, Sales Amount tertinggi adalah Road Bikes dengan penjualan sebesar 43.87879M.
        
                 
        Sementara untuk Category Clothing, Sales Amount tertinggi adalah Jerseys diikuti dengan Shorts dengan penjualan sebesar 752.2594K dan 413.5225K. Dapat diasumsikan bahwa pengguna sepeda lebih nyaman menggunakan jersey dan shorts saja, tidak dilapisi vest mengingat mereka akan berkeringat cukup banyak ketika bersepeda
        
                 
        Untuk Category Accessories, Sales Amount tertinggi adalah Helmets (484.0485K), Tires and Tubes (246.4545K), dan Bike Racks (237.0962K). Bisa diasumsikan bahwa ketiga hal ini merupakan barang paling essential yang paling sering dibutuhkan oleh pesepeda.

        Pada Category Components, Sales Amount tertinggi merupakan pelengkap dari kategori Bikes, yaitu Bike Frames (Mountain Frames, Road Frames, dan Touring Frames) yang dapat disesuaikan dengan medan seperti apa yang sering dilewati oleh konsumen.
    '''),
    dcc.Markdown('''
        ### Sales on Each Country
                 
        Dalam analisis ini, akan dilihat negara mana dengan sales tertinggi
                 
    '''),
    dcc.Graph(
        id='graph3',
        figure=barchart_country
    ),
    dcc.Markdown('''
        ### Result:
        Berdasarkan bar chart di atas, diketahui bahwa sales tertinggi kedua adalah Australia, diikuti oleh Germany. Namun pada peringkat pertama adalah [Not Applicable]
                 yang bisa saja berarti bahwa toko tidak mendata negara mana yang membeli produk mereka. Maka dari itu, sebaiknya Adventure Works lebih menekankan pentingnya pendataan
                 konsumen tiap negara, supaya pemetaan pelanggan dapat dilakukan dengan lebih mudah.
                 
        '''),
    dcc.Markdown('''
        ### Category Sales for Each Quarter
                 
        Dalam analisis ini, akan dilihat bagaimana tren penjualan setiap kategori pada masing masing quarter dari tahun 2017 hingga 2020.
                 
    '''),
    dcc.Graph(
        id='graph4',
        figure=linechart
    ),
    dcc.Markdown('''
        ### Result:
        Grafik trend diatas menunjukkan penjualan berdasarkan kategori pada masing-masing quarter dari tahun 2017 hingga 2020. Penjualan tertinggi dari kategori Bikes mencapai 3.325 ada ditahun 2017 pada kuarter ke-4,
        dan mengalami penurunan yang drastis hingga akhir tahun 2019. Namun, penjualan Bikes mulai mengalami kenaikan di tahun 2020 akibat trend bersepeda yang kembali meningkat saat pandemi.
        Penjualan pada Components bisa dikatakan cukup stabil namun sempat mengalami penurunan penjualan di akhir tahun 2018 dan 2019. Sedangkan tingkat penjualan untuk kategori Clothing dan
        Accessories adalah yang paling rendah dan paling stabil jika dibandingkan dengan dua kategori lainnya, dengan penjualan tertinggi di kuarter ke-3 2018 lalu mengalami penurunan hingga 2019.
        Bisa disimpulkan bahwa dengan meningkatnya minat bersepeda dari masyarakat di awal 2020 akibat pandemi Covid-19, maka berdampak pada meningkatnya penjualan kategori-kategori lain seperti
        Accessories, Clothing, serta Components.
    '''),
    dcc.Markdown('''
        ## Kesimpulan
        Untuk dapat membantu Adventure Works dalam meningkatkan sales mereka setelah pandemi, berikut adalah beberapa saran yang dapat kami berikan:
                 
        1. Lebih gencar dalam menawarkan membership untuk membantu mempermudah pendataan konsumen agar toko bisa melakukan personalisasi penawaran produk yang lebih baik.
        2. Adventure Works dapat melakukan promosi di berbagai platform sosial media dengan mengikuti trend yang ada (diskon, website, dll)
        3. Meningkatkan shopping experience dengan memperbanyak penawaran jenis sepeda dan customisasi.
        4. Bekerja sama dengan komunitas sepeda di berbagai negara.
        5. Mengurangi penjualan Subcategory yang kurang menguntungkan, untuk mengurangi cost


            ''')
])    

# Define Callback for chart 1
@app.callback(
    dash.dependencies.Output('graph2', 'figure'),
    [dash.dependencies.Input('dropdown', 'value')]
)
def update_chart1(selected_category):
    # Bar chart Subcategory Sales
    filtered_df = df[df['Category']==selected_category]
    bar_chart = filtered_df.groupby('Subcategory')['Sales Amount'].sum().sort_values(ascending=False).reset_index()
    traces = px.bar(bar_chart, x='Subcategory', y='Sales Amount', title='Subcategory Sales for Each Category')
    
    return traces


if __name__ == '__main__':
    app.run_server(debug=True)


# 

# In[ ]:





# In[ ]:




