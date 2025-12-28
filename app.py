import streamlit as st
import sqlite3
import pandas as pd

# --- Sayfa Ayarları ---
st.set_page_config(page_title="GTS - Tez Sistemi", layout="wide", page_icon="🎓")

# --- Başlık ---
st.title("🎓 Graduate Thesis System")
st.markdown("---")

# --- Veritabanı Bağlantısı ---
def get_data():
    conn = sqlite3.connect('db.sqlite3')
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
    try:
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        st.error(f"Veritabanı hatası: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

# Veriyi Çek
df = get_data()

if not df.empty:
    # --- YAN PANEL (Filtreleme) ---
    st.sidebar.header("🔍 Filtreleme Seçenekleri")
    
    # 1. Yıla Göre Filtre
    years = sorted(df['Yıl'].unique())
    selected_year = st.sidebar.multiselect("Yıl Seçiniz", years, default=years)
    
    # 2. Türe Göre Filtre (Master/PhD)
    types = sorted(df['Tür'].astype(str).unique())
    selected_type = st.sidebar.multiselect("Tez Türü", types, default=types)

    # 3. Dile Göre Filtre
    languages = sorted(df['Dil'].astype(str).unique())
    selected_lang = st.sidebar.multiselect("Dil Seçiniz", languages, default=languages)

    # --- ANA SAYFA (Arama Çubuğu) ---
    search_term = st.text_input("🔎 Tez Başlığı veya Yazar Ara:", placeholder="Örn: Yapay Zeka...")

    # --- FİLTRELEME MANTIĞI ---
    # Önce Yan Panel Filtrelerini Uygula
    mask = (df['Yıl'].isin(selected_year)) & (df['Tür'].isin(selected_type)) & (df['Dil'].isin(selected_lang))
    df_filtered = df[mask]

    # Sonra Arama Çubuğunu Uygula (Büyük/küçük harf duyarsız)
    if search_term:
        df_filtered = df_filtered[
            df_filtered['Başlık'].str.contains(search_term, case=False) | 
            df_filtered['Yazar'].str.contains(search_term, case=False)
        ]

    # --- SONUÇLARI GÖSTER ---
    col1, col2 = st.columns(2)
    col1.metric("Bulunan Tez Sayısı", len(df_filtered))
    
    st.table(df_filtered)

else:
    st.warning("⚠️ Veri bulunamadı. Lütfen Admin panelinden tez ekleyin.")