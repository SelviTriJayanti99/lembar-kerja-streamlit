import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pydeck as pdk
from PIL import Image
import base64
import requests

# Mengatur Title dan Header
st.set_page_config(page_title="Survey Penggemar Anime UNM", layout="wide")

# Title Aplikasi
st.title("Formulir Survey Penggemar Anime di Kampus UNM")
st.markdown("Selamat datang di aplikasi survey anime! Isi formulir ini untuk berbagi pengalaman dan anime favoritmu.")

# Sidebar Navigasi
st.sidebar.title("Navigasi Aplikasi")
menu = st.sidebar.radio("Pilih Menu", ["Formulir", "Data Anime", "Grafik", "Peta Lokasi", "Tentang"])

# Main Section
if menu == "Formulir":
    st.header("Formulir Survey Penggemar Anime")

    # Formulir Input Data
    with st.form(key="anime_form"):
        # Input Data Pengguna
        nama = st.text_input("Nama Lengkap")
        nim = st.text_input("NIM")
        fakultas_list = [
            "Fakultas Teknik", "Fakultas Ilmu Sosial", "Fakultas Bahasa dan Sastra",
            "Fakultas Matematika dan Ilmu Pengetahuan Alam", "Fakultas Ekonomi dan Bisnis",
            "Fakultas Psikologi", "Fakultas Seni dan Desain", "Fakultas Ilmu Pendidikan"
        ]
        fakultas = st.selectbox("Pilih Fakultas", fakultas_list)
        jurusan = st.text_input("Jurusan")
        # Input Data Anime
        anime_favorit = st.text_input("Anime Favorit")
        karakter_favorit = st.text_input("Karakter Favorit")
        genre_favorit = st.selectbox("Genre Anime Favorit", [
            "Action", "Adventure", "Comedy", "Drama", "Fantasy", "Romance", "Slice of Life", "Horror", "Sci-Fi", "Sports"
        ])
        tanggal_mulai_nonton = st.date_input("Kapan kamu mulai menonton anime?")
        foto_karakter = st.file_uploader("Upload Gambar Karakter Favorit", type=["jpg", "jpeg", "png"])
        
        # Tombol Submit
        submit_button = st.form_submit_button("Kirim Formulir")
        
        if submit_button:
            st.success("Formulir berhasil dikirim!")
            st.write(f"**Nama:** {nama}")
            st.write(f"**Anime Favorit:** {anime_favorit}")
            st.write(f"**Karakter Favorit:** {karakter_favorit}")
            st.write(f"**Genre Favorit:** {genre_favorit}")
            st.write(f"**Mulai Menonton Sejak:** {tanggal_mulai_nonton}")
            if foto_karakter:
                st.image(foto_karakter, caption="Karakter Favorit", use_column_width=True)

elif menu == "Data Anime":
    st.header("Data Anime dari MyAnimeList API")

    url_base = "https://api.jikan.moe/v4/anime"
    anime_data = []
    page = 1
    data_per_page = 50  # Jumlah data per halaman

    # Mengambil data anime
    while len(anime_data) < 100:
        url = f"{url_base}?page={page}"
        response = requests.get(url)
        if response.status_code == 200:
            api_data = response.json()
            if 'data' in api_data:
                anime_data.extend(api_data['data'])
                if len(anime_data) >= 100:
                    break
                page += 1
            else:
                st.warning("Tidak ada data anime yang ditemukan.")
                break
        else:
            st.error("Gagal mengambil data dari API Jikan.")
            break
        
    # Menampilkan data anime dalam tabel
    anime_list = pd.DataFrame([{
        'Title': anime['title'],
        'Score': anime.get('score', 'N/A'),
        'Genres': ', '.join([genre['name'] for genre in anime.get('genres', [])]),
        'Year': anime.get('year', 'Unknown'),
        'Episodes': anime.get('episodes', 'N/A'),
        'Type': anime.get('type', 'N/A'),
        'Status': anime.get('status', 'N/A')
    } for anime in anime_data[:100]])

    st.dataframe(anime_list)

    st.subheader("Statistik tentang Anime")
    if not anime_list.empty:
        avg_score = anime_list['Score'].mean()
        oldest_year = anime_list['Year'].min()
        avg_episodes = anime_list['Episodes'].mean()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Skor Rata-Rata", f"{avg_score:.2f}")
        col2.metric("Tahun Rilis Tertua", oldest_year)
        col3.metric("Rata-rata Episode", f"{avg_episodes:.1f}")

    # Menambahkan fitur upload file CSV
    st.header("Upload File Data")
    uploaded_file = st.file_uploader("Unggah Data (CSV)", type=["csv"])

    if uploaded_file is not None:
        # Membaca file CSV yang diunggah
        anime_data_uploaded = pd.read_csv(uploaded_file)

elif menu == "Grafik":
    st.header("Grafik Visualisasi Anime")

    # Data Dummy untuk Grafik
    data_chart = pd.DataFrame(np.random.randn(100, 3), columns=['a', 'b', 'c'])

    # Grafik Line
    st.subheader("Line Chart")
    st.line_chart(data_chart)

    # Grafik Bar dengan Plotly
    st.subheader("Bar Chart dengan Plotly")
    fig = px.bar(data_chart, x=data_chart.index, y=['a', 'b', 'c'], title='Bar Chart per Kolom A, B, C')
    st.plotly_chart(fig)

    # Grafik Pie
    st.subheader("Pie Chart")
    labels = ['Action', 'Comedy', 'Drama', 'Fantasy', 'Sci-Fi']
    sizes = [25, 30, 20, 15, 10]
    fig_pie = plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0'])
    plt.title('Distribusi Genre Anime')
    st.pyplot(fig_pie)

    # Grafik Histogram
    st.subheader("Histogram")
    data_hist = np.random.randn(1000)
    plt.figure(figsize=(10, 6))
    plt.hist(data_hist, bins=30, color='purple', edgecolor='black')
    plt.title('Distribusi Data dengan Histogram')
    plt.xlabel('Nilai')
    plt.ylabel('Frekuensi')
    st.pyplot(plt.gcf())

    # Grafik Box Plot
    st.subheader("Box Plot")
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=data_chart)
    plt.title('Box Plot Data Kolom A, B, C')
    plt.xlabel('Kolom')
    plt.ylabel('Nilai')
    st.pyplot(plt.gcf())

    # Grafik Scatter Plot
    st.subheader("Scatter Plot")
    plt.figure(figsize=(10, 6))
    plt.scatter(data_chart['a'], data_chart['b'], color='red')
    plt.title('Scatter Plot Kolom A vs Kolom B')
    plt.xlabel('Kolom A')
    plt.ylabel('Kolom B')
    st.pyplot(plt.gcf())

    # Grafik Heatmap
    st.subheader("Heatmap")
    correlation_matrix = data_chart.corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
    plt.title('Heatmap Korelasi')
    st.pyplot(plt.gcf())

    # Grafik Violin Plot
    st.subheader("Violin Plot")
    plt.figure(figsize=(10, 6))
    sns.violinplot(data=data_chart)
    plt.title('Violin Plot Data Kolom A, B, C')
    st.pyplot(plt.gcf())

    # Grafik Area Chart
    st.subheader("Area Chart")
    data_area = pd.DataFrame(np.random.randn(100, 1), columns=['Area'])
    st.area_chart(data_area)

    # Grafik Stacked Bar Chart
    st.subheader("Stacked Bar Chart")
    data_stacked = pd.DataFrame(np.random.randn(10, 3), columns=['X', 'Y', 'Z'])
    st.bar_chart(data_stacked)

    # Grafik Bubble Chart
    st.subheader("Bubble Chart")
    bubble_data = pd.DataFrame({
        'x': np.random.rand(50),
        'y': np.random.rand(50),
        'size': np.random.rand(50)*1000,
    })
    fig_bubble = px.scatter(bubble_data, x='x', y='y', size='size', title="Bubble Chart")
    st.plotly_chart(fig_bubble)

elif menu == "Peta Lokasi":
    st.header("Peta Lokasi Wibu di Makassar")

    # Data Lokasi Dummy
    locations = pd.DataFrame({
        'latitude': np.random.uniform(-5.136, -5.126, size=100),
        'longitude': np.random.uniform(119.413, 119.433, size=100)
    })

    # Membuat peta interaktif dengan PyDeck
    layer = pdk.Layer(
        'ScatterplotLayer',
        data=locations,
        get_position='[longitude, latitude]',
        get_color='[0, 100, 255, 160]',
        get_radius=50,
    )

    view_state = pdk.ViewState(
        latitude=-5.131593,
        longitude=119.421982,
        zoom=14,
        pitch=0,
    )

    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
    )
    st.pydeck_chart(deck)

elif menu == "Tentang":
    st.header("Tentang Aplikasi")
    st.caption("Trailer Kimetsu No Yaiba")
    # Menampilkan Video atau Trailer Anime
    st.video("https://youtu.be/wyiZWYMilgk?si=Mix-7xZtgtx3Q2m-")
    st.markdown(""" 
        Aplikasi ini saya kembangkan sebagai **formulir survey** untuk penggemar anime yang ada di Kampus UNM.
        Formulir ini untuk mengetahui seberapa banyak penggemar anime yang ada, untuk membuat suatu komunitas di Kampus. 
        Saya membuat ini karena saya juga merupakan penggemar anime, Terimakasih sudah berkunjung dan mengisi formulir ini! Arigatouu.
    """)

# Background Musik
st.markdown(
    """
    <audio autoplay loop>
        <source src="https://www.bensound.com/bensound-music/bensound-sunny.mp3" type="audio/mpeg">
        Your browser does not support the audio element.
    </audio>
    """,
    unsafe_allow_html=True
)
