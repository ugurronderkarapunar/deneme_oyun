import streamlit as st
import time
import requests
from streamlit_lottie import st_lottie

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Dental Simulator Pro", layout="wide", initial_sidebar_state="collapsed")

# --- CUSTOM CSS (Animasyonlar ve Full Ekran Efekti) ---
st.markdown("""
    <style>
    /* Menü ve Header'ı Gizle */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Fade-in Sayfa Geçişi */
    .stApp {
        animation: fadeIn 1.5s;
    }
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }

    /* Diş Yanıp Sönme Efekti (Sorunlu Diş İçin) */
    .pulse-tooth {
        animation: pulse 1s infinite;
        border: 2px solid red !important;
        border-radius: 10px;
    }
    @keyframes pulse {
        0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 0, 0, 0.7); }
        70% { transform: scale(1.05); box-shadow: 0 0 0 10px rgba(255, 0, 0, 0); }
        100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 0, 0, 0); }
    }
    
    /* Butonları Güzelleştirme */
    .stButton>button {
        border-radius: 20px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- YARDIMCI FONKSİYONLAR ---
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Animasyon Linkleri
lottie_scanning = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_5n8y8y8y.json") # Tarama
lottie_success = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_xlmz9yl2.json") # Başarı

# --- OYUN MANTIĞI ---
if 'sahne' not in st.session_state:
    st.session_state.sahne = 'menu'

def sahne_degistir(yeni_sahne):
    st.session_state.sahne = yeni_sahne

# --- SAHNELER ---

# 1. SAHNE: ANA MENÜ
if st.session_state.sahne == 'menu':
    st.markdown("<h1 style='text-align: center; color: #2E86C1;'>🦷 DENTAL SIMULATOR 2026</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Klinik hazır, hasta bekliyor.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("🚀 OYUNA BAŞLA", use_container_width=True):
            sahne_degistir('hasta_gelisi')
            st.rerun()

# 2. SAHNE: HASTA VE ŞİKAYET
elif st.session_state.sahne == 'hasta_gelisi':
    st.subheader("👨‍💼 Yeni Hasta: Mehmet Bey")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("https://api.dicebear.com/7.x/avataaars/svg?seed=Mehmet&mood=sad", width=250)
    with col2:
        st.chat_message("user").write("Doktor bey, sol üstteki dişim soğuk bir şey değince zıplatıyor. Gece de sızladı...")
        if st.button("🔍 Muayene Et ve Röntgene Gönder"):
            sahne_degistir('rontgen_animasyon')
            st.rerun()

# 3. SAHNE: RÖNTGEN ANİMASYON (LOADING)
elif st.session_state.sahne == 'rontgen_animasyon':
    st.markdown("<h2 style='text-align: center;'>☢️ Röntgen Çekiliyor...</h2>", unsafe_allow_html=True)
    st_lottie(lottie_scanning, height=300, key="scan")
    time.sleep(3) # Oyuncuya tarama hissi ver
    sahne_degistir('rontgen_sonuc')
    st.rerun()

# 4. SAHNE: RÖNTGEN SONUCU
elif st.session_state.sahne == 'rontgen_sonuc':
    st.subheader("📋 Analiz Tamamlandı")
    st.image("https://upload.wikimedia.org/wikipedia/commons/4/46/Panoramic_radiograph.jpg")
    st.error("Tespit: Sol Üst 2. Azı dişinde derin çürük. Pulpa etkilenmiş olabilir.")
    if st.button("👄 Tedaviye Başla (Full Ekran Moda Geç)"):
        sahne_degistir('tedavi')
        st.rerun()

# 5. SAHNE: TEDAVİ (FULL EKRAN AĞIZ)
elif st.session_state.sahne == 'tedavi':
    st.markdown("<h1 style='text-align: center;'>🦷 HASTANIN AĞZI (OPERASYON ALANI)</h1>", unsafe_allow_html=True)
    
    # Üst Çene
    st.markdown("### ÜST ÇENE")
    u_col = st.columns(8)
    for i in range(8):
        if i == 6: # Sorunlu Diş (Sol Üst 2. Azı temsili)
            if u_col[i].button("🦷\nÇÜRÜK", key=f"dis_u_{i}", help="Operasyon Gerekiyor!"):
                sahne_degistir('basari')
                st.rerun()
        else:
            u_col[i].button("🦷", key=f"dis_u_{i}")

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Alt Çene
    st.markdown("### ALT ÇENE")
    a_col = st.columns(8)
    for i in range(8):
        a_col[i].button("🦷", key=f"dis_a_{i}")

    if st.button("⬅️ Geri Dön", type="secondary"):
        sahne_degistir('menu')
        st.rerun()

# 6. SAHNE: BAŞARI ANİMASYONU
elif st.session_state.sahne == 'basari':
    st.markdown("<h1 style='text-align: center; color: green;'>✅ TEDAVİ TAMAMLANDI!</h1>", unsafe_allow_html=True)
    st_lottie(lottie_success, height=400, key="success")
    st.balloons()
    time.sleep(4)
    sahne_degistir('menu')
    st.rerun()
