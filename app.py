import streamlit as st
import sqlite3
import pandas as pd

# Sayfa Ayarları
st.set_page_config(page_title="GTS - Tez Sistemi", layout="wide")

st.title("🎓 Graduate Thesis System (GTS)")
st.write("Hoşgeldiniz! Sistemdeki tezleri aşağıda inceleyebilirsiniz.")

# 1. Veritabanına Bağlan (Django'nun kullandığı db.sqlite3 dosyası)
def get_data():
    # db.sqlite3 dosyası manage.py ile aynı yerde olmalı
    conn = sqlite3.connect('db.sqlite3')
    
    # SQL Sorgusu (Tablo isimleri genelde app_model şeklindedir: gts_thesis)
    # Eğer hata alırsan tablo ismini kontrol ederiz
    query = """
    SELECT 
        t.thesis_no, 
        t.title, 
        t.year,
        a.name as Author,
        l.name as Language,
        ty.name as Type
    FROM gts_thesis t
    LEFT JOIN gts_author a ON t.author_id = a.id
    LEFT JOIN gts_language l ON t.language_id = l.id
    LEFT JOIN gts_thesistype ty ON t.type_id = ty.id
    """
    
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# 2. Veriyi Çek ve Göster
try:
    df = get_data()
    
    # İstatistikler (Opsiyonel - Havalı görünür)
    col1, col2 = st.columns(2)
    col1.metric("Toplam Tez", len(df))
    col2.metric("Son Eklenen Yıl", df['year'].max())

    # Tabloyu Göster
    st.subheader("📚 Tez Listesi")
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Bir hata oluştu: {e}")
    st.info("İpucu: Veritabanında henüz veri olmayabilir veya tablo isimleri farklı olabilir.")