import streamlit as st
import pandas as pd
import pymysql

# --- Sayfa Ayarları ---
st.set_page_config(page_title="GTS - Tez Sistemi", layout="wide", page_icon="🎓")

# --- MySQL Bağlantı Fonksiyonu ---
def get_connection():
    return pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='',  # <--- ŞİFRENİ UNUTMA
        database='gts_db',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

# --- Verileri Çekme Fonksiyonu ---
def get_data():
    try:
        conn = get_connection()
        # DÜZELTME: Senin ekran görüntündeki gerçek tablo isimlerine göre ayarlandı!
        query = """
        SELECT 
            t.thesis_no as 'Tez No',
            t.title as 'Başlık',
            t.year as 'Yıl',
            a.name as 'Yazar',
            l.name as 'Dil',
            ty.name as 'Tür',
            i.name as 'Enstitü'
        FROM gts_thesis t
        LEFT JOIN author a ON t.author_id = a.author_id
        LEFT JOIN language l ON t.language_id = l.language_id
        LEFT JOIN thesis_type ty ON t.type_id = ty.type_id
        LEFT JOIN institute i ON t.institute_id = i.institute_id
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"⚠️ Veritabanı Hatası: {e}")
        return pd.DataFrame()

# --- ARAYÜZ ---
st.title("🎓 Graduate Thesis System")
st.markdown("### Gelişmiş Arama ve Filtreleme Paneli")
st.markdown("---")

# Veriyi Çek
df = get_data()

if not df.empty:
    # --- Sidebar (Sol Menü) ---
    st.sidebar.header("🔍 Filtreleme Seçenekleri")
    
    # 1. Yıl Filtresi
    years = sorted(df['Yıl'].unique())
    selected_year = st.sidebar.multiselect("Yıl Seçiniz", years, default=years)
    
    # 2. Dil Filtresi
    langs = sorted(df['Dil'].astype(str).unique())
    selected_lang = st.sidebar.multiselect("Dil Seçiniz", langs, default=langs)

    # 3. Tür Filtresi
    types = sorted(df['Tür'].astype(str).unique())
    selected_type = st.sidebar.multiselect("Tez Türü", types, default=types)

    # Filtreleme Mantığı
    mask = (df['Yıl'].isin(selected_year)) & (df['Dil'].isin(selected_lang)) & (df['Tür'].isin(selected_type))
    df_filtered = df[mask]

    # --- Ana Sayfa Arama Çubuğu ---
    col1, col2 = st.columns([3, 1])
    with col1:
        search_term = st.text_input("🔎 Detaylı Arama:", placeholder="Başlık, Yazar veya Enstitü...")

    if search_term:
        df_filtered = df_filtered[
            df_filtered['Başlık'].str.contains(search_term, case=False) | 
            df_filtered['Yazar'].str.contains(search_term, case=False) |
            df_filtered['Enstitü'].str.contains(search_term, case=False)
        ]

    # --- Sonuç Tablosu ---
    st.info(f"Toplam **{len(df_filtered)}** tez listeleniyor.")
    
    st.dataframe(
        df_filtered, 
        use_container_width=True,
        hide_index=True,
        column_config={
            "Tez No": st.column_config.NumberColumn(format="%d"),
            "Yıl": st.column_config.NumberColumn(format="%d"),
        }
    )

else:
    st.warning("⚠️ Sistemde veri yok veya bağlantı kurulamadı. Lütfen Admin panelinden veri ekleyiniz.")