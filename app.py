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
        password='BURAYA_MYSQL_SIFRENİ_YAZ',  # <--- ŞİFRENİ BURAYA YAZ
        database='gts_db',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

# --- Verileri Çekme Fonksiyonu ---
def get_data():
    try:
        conn = get_connection()
        query = """
        SELECT 
            t.thesis_no as 'Tez No',
            t.title as 'Başlık',
            t.year as 'Yıl',
            a.name as 'Yazar',
            l.name as 'Dil',
            ty.name as 'Tür'
        FROM gts_thesis t
        LEFT JOIN gts_author a ON t.author_id = a.id
        LEFT JOIN gts_language l ON t.language_id = l.id
        LEFT JOIN gts_thesistype ty ON t.type_id = ty.id
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Veritabanı bağlantı hatası: {e}")
        return pd.DataFrame()

# --- ARAYÜZ ---
st.title("🎓 Graduate Thesis System (MySQL Versiyonu)")
st.markdown("---")

df = get_data()

if not df.empty:
    # Sidebar Filtreleri
    st.sidebar.header("🔍 Filtreleme")
    
    # Yıl Filtresi
    years = sorted(df['Yıl'].unique())
    selected_year = st.sidebar.multiselect("Yıl Seçiniz", years, default=years)
    
    # Dil Filtresi
    langs = sorted(df['Dil'].astype(str).unique())
    selected_lang = st.sidebar.multiselect("Dil Seçiniz", langs, default=langs)

    # Filtreleme Mantığı
    mask = (df['Yıl'].isin(selected_year)) & (df['Dil'].isin(selected_lang))
    df_filtered = df[mask]

    # Arama Çubuğu
    search_term = st.text_input("🔎 Arama (Başlık veya Yazar):", placeholder="Örn: Yapay Zeka...")
    if search_term:
        df_filtered = df_filtered[
            df_filtered['Başlık'].str.contains(search_term, case=False) | 
            df_filtered['Yazar'].str.contains(search_term, case=False)
        ]

    st.success(f"Toplam **{len(df_filtered)}** tez listeleniyor.")
    st.dataframe(df_filtered, use_container_width=True)

else:
    st.warning("⚠️ Sistemde veri yok. Lütfen Admin panelinden tez ekleyin.")