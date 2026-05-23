import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from simulation import simule_et

# 1. Sayfa Ayarları ve Geniş Ekran Modu
st.set_page_config(page_title="Gelişmiş Eczane Simülasyonu", layout="wide", initial_sidebar_state="expanded")

# 2. Custom CSS ile Premium Görünüm ve Kart Tasarımları
st.markdown("""
    <style>
    /* Ana arka plan ve genel font yapısı */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Dijital Gösterge Kartları (KPI Cards) Tasarımı */
    .kpi-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border-left: 5px solid #4CAF50;
        text-align: center;
        transition: transform 0.3s;
    }
    .kpi-card:hover {
        transform: translateY(-5px);
    }
    .kpi-title {
        font-size: 14px;
        color: #666;
        text-transform: uppercase;
        font-weight: bold;
    }
    .kpi-value {
        font-size: 28px;
        color: #2c3e50;
        font-weight: bold;
        margin-top: 5px;
    }
    
    /* Simülasyon Başlat Butonu Tasarımı */
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #00b4db, #0083b0);
        color: white !important;
        border-radius: 10px;
        padding: 12px;
        font-size: 18px;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 15px rgba(0,131,176,0.3);
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background: linear-gradient(45deg, #0083b0, #00b4db);
        transform: scale(1.02);
    }
    </style>
""", unsafe_allow_html=True)

# Üst Başlık Alanı (Banner)
st.markdown("""
    <div style="background: linear-gradient(45deg, #2c3e50, #3498db); padding: 25px; border-radius: 15px; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.1)">
        <h1 style="color: white; margin: 0; font-size: 32px; text-align: center;">🏥 Akıllı Eczane Kuyruk Yönetimi ve Dijital İkiz Paneli</h1>
        <p style="color: #e0e0e0; margin: 10px 0 0 0; font-size: 16px; text-align: center;">TÜİK Yoğunluk Verileri, SGK Entegrasyonu ve Stok Parametreli Gelişmiş Model</p>
    </div>
""", unsafe_allow_html=True)

# Yan Menü Kontrol Alanı (Sidebar Layout)
st.sidebar.markdown("<h2 style='color: #2c3e50; text-align: center;'>⚙️ Kontrol Paneli</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# Dinamik Parametre Girişleri (Geliştirilmiş Seçenekler)
st.sidebar.subheader("👨‍⚕️ Personel Ayarları")
eczaci = st.sidebar.slider("Eczacı Sayısı (Onay & Teslimat)", 1, 3, 1)
kalfa = st.sidebar.slider("Kalfa Sayısı (İlaç Arama)", 1, 5, 2)

st.sidebar.subheader("📦 Stok Parametreleri")
stok_bulma = st.sidebar.slider("İlaç Stokta Bulunma Oranı (%)", 50, 100, 90)

st.sidebar.subheader("⏰ Zaman Yönetimi")
sure = st.sidebar.selectbox("Simülasyon Süresi (Saat)", [8, 12, 24])

st.sidebar.markdown("---")

# Simülasyon Tetikleme Mekanizması
if st.sidebar.button("🚀 SİMÜLASYONU BAŞLAT"):
    df_sonuc = simule_et(eczaci, kalfa, stok_bulma, sure)
    
    if not df_sonuc.empty:
        # Metriklerin Ekran Kartları ile Gösterilmesi (KPI Paneli)
        st.markdown("### 📊 Genel Performans Göstergeleri (KPIs)")
        c1, c2, c3 = st.columns(3)
        
        with c1:
            st.markdown(f"""
                <div class="kpi-card" style="border-left-color: #2196F3;">
                    <div class="kpi-title">Toplam Hizmet Verilen Hasta</div>
                    <div class="kpi-value">{len(df_sonuc)} Hasta</div>
                </div>
            """, unsafe_allow_html=True)
            
        with c2:
            st.markdown(f"""
                <div class="kpi-card" style="border-left-color: #4CAF50;">
                    <div class="kpi-title">Ortalama Bekleme Süresi</div>
                    <div class="kpi-value">{df_sonuc['Bekleme Süresi'].mean():.2f} dk</div>
                </div>
            """, unsafe_allow_html=True)
            
        with c3:
            st.markdown(f"""
                <div class="kpi-card" style="border-left-color: #f44336;">
                    <div class="kpi-title">Maksimum Kuyruk Beklemesi</div>
                    <div class="kpi-value">{df_sonuc['Bekleme Süresi'].max():.2f} dk</div>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Çıktıların Multi-Column Düzeni ile Gösterilmesi
        col_left, col_right = st.columns([1, 1])
        
        # Sol Kolon: Reçete Türü Analiz Verileri
        with col_left:
            st.markdown("### 📋 Hasta Türlerine Göre Bekleme Analizi")
            tur_analiz = df_sonuc.groupby("Tür")["Bekleme Süresi"].mean().reset_index()
            tur_analiz.columns = ["Hasta Türü", "Ort. Bekleme (Dakika)"]
            st.dataframe(tur_analiz.style.background_gradient(cmap="Blues"), use_container_width=True)
            
        # Sağ Kolon: Ödeme Dağılım Grafiği
        with col_right:
            st.markdown("### 💳 Ödeme Türlerine Göre Dağılım")
            fig2, ax2 = plt.subplots(figsize=(5, 3))
            fig2.patch.set_facecolor('#f5f7fa')
            df_sonuc['Ödeme'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax2, colors=['#3498db','#2ecc71','#e67e22'])
            ax2.set_ylabel("")
            st.pyplot(fig2)
            
        # Alt Geniş Alan: Günlük Zaman Yoğunluk Eğrisi (TÜİK Yapısı)
        st.markdown("### ⏰ Gün İçindeki Saatlik Bekleme Süresi Değişimi (TÜİK Yoğunluk Eğrisi)")
        fig, ax = plt.subplots(figsize=(12, 4))
        fig.patch.set_facecolor('#f5f7fa')
        ax.plot(df_sonuc.sort_values('Saat')['Saat'], df_sonuc.sort_values('Saat')['Bekleme Süresi'].rolling(window=5, min_periods=1).mean(), color='#e74c3c', linewidth=2, label="Yoğunluk Trendi")
        ax.scatter(df_sonuc['Saat'], df_sonuc['Bekleme Süresi'], alpha=0.3, color='#34495e')
        ax.set_xlabel("Günlük Saat (8:00 - 24:00)")
        ax.set_ylabel("Bekleme Süresi (Dakika)")
        ax.grid(True, linestyle='--', alpha=0.5)
        st.pyplot(fig)
        
        # Resmi ve ciddi başarı bildirimi box'ı
        st.success("Simülasyon başarıyla tamamlandı. Tüm parametreler TÜİK standartlarında analiz edilerek raporlandı.")