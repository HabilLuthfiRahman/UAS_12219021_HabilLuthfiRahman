# Import Library
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
import streamlit as st
import json
import urllib.request

from streamlit.elements import markdown



# Import Dataset and JSON file
dataset_minyak = pd.read_csv('https://raw.githubusercontent.com/HabilLuthfiRahman/UAS_12219021_HabilLuthfiRahman/main/produksi_minyak_mentah.csv')
with urllib.request.urlopen('https://raw.githubusercontent.com/HabilLuthfiRahman/UAS_12219021_HabilLuthfiRahman/main/kode_negara_lengkap.json') as url:
  json_data = json.loads(url.read().decode())
nama_negara_pair = dict()
kode_negara_pair = dict()
for i in range(len(json_data)):
  nama_negara_pair[json_data[i]['name']] = json_data[i]['alpha-3']
  kode_negara_pair[json_data[i]['alpha-3']] = json_data[i]['name']



############### Title ###############

st.set_page_config(layout="wide")  # this needs to be the first Streamlit command called
st.title("Tugas Besar")

############### Title ###############



############### Sidebar ###############

st.sidebar.title("Settings")
left_col, mid_col, right_col = st.columns(3)

# User inputs on the control panel
st.sidebar.subheader("Pengaturan konfigurasi tampilan")
list_negara = list(kode_negara_pair.values())
negara = st.sidebar.selectbox("A: Pilih Negara", list_negara)
b_negara = st.sidebar.number_input("B: Jumlah negara dengan jumlah produksi terbesar", min_value=1, max_value=20, value=10)
t_tahun = st.sidebar.number_input("B: Tahun  jumlah produksi terbesar", min_value=1970, max_value=2015, value=2015)
b_cummulative = st.sidebar.number_input("C: Jumlah negara dengan jumlah produksi kumulatif terbesar", min_value=1, max_value=20, value=10)
t_tahun_info = st.sidebar.number_input("D: Informasi Negara dengan Jumlah Produksi terbesa, terkecil bukan nol, dan nol", min_value=1970, max_value=2015, value=2015)
############### Sidebar ###############



############### upper left column ###############

# Soal A
# Fungsi ini berguna untuk menampilkan grafik produksi minyak terhadap tahun dari negara N
kode_negara = nama_negara_pair[negara]
df_n = dataset_minyak[dataset_minyak.kode_negara == kode_negara]

fig, ax = plt.subplots()
ax.plot(df_n['tahun'], df_n['produksi'])
ax.set_xlabel('Tahun', fontsize=12); ax.set_ylabel('Produksi', fontsize=12)

left_col.subheader('A: Produksi Minyak Negara ' + negara + ' Berdasarkan Tahun')
left_col.pyplot(fig)

############### upper left column ###############



############### upper mid column ###############

# Soal B
# Sort berdasarkan data dari tahun T kemudian tunjukkan
# data terbesar sebanyak B
df_year = dataset_minyak[dataset_minyak.tahun == t_tahun]
df_year = df_year.sort_values(by=['produksi'], ascending=False)

kode_negara = df_year['kode_negara']
nama_negara = list()
for item in kode_negara:
    try:
        nama_negara.append(kode_negara_pair[item])
    except:
        df_year[df_year.kode_negara == item] = None

df_year = df_year.dropna()
df_year = df_year.reset_index(drop=True)
df_year = df_year[:b_negara]

fig, ax = plt.subplots()
ax.bar(nama_negara[:b_negara], df_year['produksi'])
ax.set_xlabel('Negara', fontsize=12); ax.set_ylabel('Produksi', fontsize=12)
ax.set_xticklabels(nama_negara[:b_negara], rotation=90)

mid_col.subheader('B: Produksi Tertinggi pada Tahun ' + str(t_tahun))
mid_col.pyplot(fig)

############### upper mid column ###############



############### lower left column ###############

# Soal C
# Tampilkan B jumlah negara yang memiliki Produksi Kumulatif tertinggi
group_df = dataset_minyak.groupby(['kode_negara'])
cumm = group_df['produksi'].sum().to_frame(name ='cumm').reset_index()

kode_negara = cumm['kode_negara']
nama_negara = list()
for item in kode_negara:
    try:
        nama_negara.append(kode_negara_pair[item])
    except:
        cumm[cumm.kode_negara == item] = None

cumm = cumm.dropna()
cumm = cumm.reset_index(drop=True)
cumm = cumm.sort_values(by=['cumm'], ascending=False)
cumm = cumm[:b_cummulative]

nama_negara = list()
for item in cumm['kode_negara']:
    nama_negara.append(kode_negara_pair[item])


fig, ax = plt.subplots()
patches, labels = ax.pie(cumm['cumm'], labels=nama_negara)

display_data = {'nama_negara':nama_negara, 'produksi_kumulatif':cumm['cumm']}
display_table = pd.DataFrame(display_data)
display_table.reset_index(inplace=True,drop=True)
display_table.index = np.arange(1, len(display_table) + 1)


left_col.subheader('C: Tabel dan Diagram ' + str(b_cummulative) + ' Negara Tertinggi berdasarkan Produksi Kumulatif')
left_col.pyplot(fig)
left_col.dataframe(display_table)

############### lower left column ###############



############### lower mid column ###############

# Soal D
# Didapat dengan menggabungkan jawaban B dan C
# Filter untuk tahun T
df_year = dataset_minyak[dataset_minyak.tahun == t_tahun_info]
df_year = df_year.sort_values(by=['produksi'], ascending=False)

kode_negara = df_year['kode_negara']
nama_negara = list()
for item in kode_negara:
    try:
        nama_negara.append(kode_negara_pair[item])
    except:
        df_year[df_year.kode_negara == item] = None

df_year = df_year.dropna()
df_year = df_year.reset_index(drop=True)

# Data Max pada tahun T
max_year = df_year.iloc[0]

# Data Min pada tahun T
min_year = df_year[df_year.produksi > 0]
min_year = min_year.iloc[-1]

# Data Nol pada tahun T
zero_year = df_year[df_year.produksi == 0]
zero_year = list(zero_year['kode_negara'])

# Mencari data pada file json
max_year_data = None
min_year_data = None
zero_year_data = []

for data in json_data:
    if data['alpha-3'] == max_year['kode_negara']:
        max_year_data = data
    elif data['alpha-3'] == min_year['kode_negara']:
        min_year_data = data
    elif data['alpha-3'] in zero_year:
        zero_year_data.append(data)


# Filter untuk keseluruhan tahun
group_df = dataset_minyak.groupby(['kode_negara'])
cumm = group_df['produksi'].sum().to_frame(name ='produksi_kumulatif').reset_index()

kode_negara = cumm['kode_negara']
nama_negara = list()
for item in kode_negara:
    try:
        nama_negara.append(kode_negara_pair[item])
    except:
        cumm[cumm.kode_negara == item] = None

cumm = cumm.dropna()
cumm = cumm.sort_values(by=['produksi_kumulatif'], ascending=False)
cumm = cumm.reset_index(drop=True)

# Data Max keseluruhan
max_all = cumm.iloc[0]

# Data Min keseluruhan
min_all = cumm[cumm.produksi_kumulatif > 0]
min_all = min_all.iloc[-1]

# Data Nol keseluruhan
zero_all = cumm[cumm.produksi_kumulatif == 0]
zero_all = list(zero_all['kode_negara'])

# Mencari data pada file json
max_all_data = None
min_all_data = None
zero_all_data = []

for data in json_data:
    if data['alpha-3'] == max_all['kode_negara']:
        max_all_data = data
    elif data['alpha-3'] == min_all['kode_negara']:
        min_all_data = data
    elif data['alpha-3'] in zero_all:
        zero_all_data.append(data)



# Tampilkan Data
markdowns = []
markdowns.append('Negara dengan Produksi Tertinggi pada tahun ' + str(t_tahun_info) + ':')
markdowns.append('- Nama Negara: ' + max_year_data['name'])
markdowns.append('- Kode Negara: ' + max_year_data['country-code'])  
markdowns.append('- Region: ' + max_year_data['region'])
markdowns.append('- Sub-Region: ' + max_year_data['sub-region'])
markdowns.append('- Jumlah Produksi: ' + str(max_year['produksi']))
markdowns.append('\n')

markdowns.append('Negara dengan Produksi Tertinggi Keseluruhan')
markdowns.append('- Nama Negara: ' + max_all_data['name'])
markdowns.append('- Kode Negara: ' + max_all_data['country-code'])
markdowns.append('- Region: ' + max_all_data['region'])
markdowns.append('- Sub-Region: ' + max_all_data['sub-region'])
markdowns.append('- Jumlah Produksi: ' + str(max_all['produksi_kumulatif']))
markdowns.append('\n')

markdowns.append('Negara dengan Produksi Terendah pada tahun ' + str(t_tahun_info) + ':')
markdowns.append('- Nama Negara: ' + min_year_data['name'])
markdowns.append('- Kode Negara: ' + min_year_data['country-code'])
markdowns.append('- Region: ' + min_year_data['region'])
markdowns.append('- Sub-Region: ' + min_year_data['sub-region'])
markdowns.append('- Jumlah Produksi: ' + str(min_year['produksi']))
markdowns.append('\n')

markdowns.append('Negara dengan Produksi Terendah Keseluruhan')
markdowns.append('- Nama Negara: ' + min_all_data['name'])
markdowns.append('- Kode Negara: ' + min_all_data['country-code'])
markdowns.append('- Region: ' + min_all_data['region'])
markdowns.append('- Sub-Region: ' + min_all_data['sub-region'])
markdowns.append('- Jumlah Produksi: ' + str(min_all['produksi_kumulatif']))
markdowns.append('\n')

count = 1
markdowns.append('\nNegara dengan Produksi Nol pada tahun ' + str(t_tahun_info) + ':\n')
for item in zero_year_data:
    markdowns.append('    ' + str(count))
    markdowns.append('  - Nama Negara: ' + item['name'])
    markdowns.append('  - Kode Negara: ' + item['country-code'])
    markdowns.append('  - Region: ' + item['region'])
    markdowns.append('  - Sub-Region: ' + item['sub-region'])
    markdowns.append('\n')
    count += 1

count = 1
markdowns.append('\nNegara dengan Produksi Nol keseluruhan:\n')
for item in zero_all_data:
    markdowns.append('    ' + str(count))
    markdowns.append('  - Nama Negara: ' + item['name'])
    markdowns.append('  - Kode Negara: ' + item['country-code'])
    markdowns.append('  - Region: ' + item['region'])
    markdowns.append('  - Sub-Region: ' + item['sub-region'])
    markdowns.append('\n')
    count += 1

markdowns = "\n".join(markdowns)

right_col.subheader('D: Negara dengan Produksi Kumulatif Maksimum, Minimum, dan Nol berdasarkan Negara dan Keseluruhan')
right_col.markdown(markdowns)
############### upper right column ###############
