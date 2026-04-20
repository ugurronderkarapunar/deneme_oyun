import streamlit as st
import time
import random
import requests
from streamlit_lottie import st_lottie

# --- GENEL AYARLAR ---
st.set_page_config(page_title="Clinic Master: Dentist Edition", layout="wide", initial_sidebar_state="collapsed")

# --- GELİŞMİŞ CSS ---
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Acı Metresi Animasyonu */
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #4CAF50, #f44336);
    }
    
    /* Diş Üniti Tasarımı */
    .tooth-btn {
        height: 80px !important;
        width: 100% !important;
        font-size: 25px !important;
    }
    
    /* Animasyonlu Fade */
    .fade-in { animation: fadeIn 1s; }
    @keyframes fadeIn { from {opacity:0;} to {opacity:1;} }
    </style>
    """, unsafe_allow_html=True)

# --- YARDIMCI FONKSİYONLAR ---
def load_lottie(url):
    try:
        r = requests.get(url, timeout=5)
        return r.json() if r.status_code == 200 else None
    except: return None

# Animasyonları Önden Yükle
lottie_scan = load_lottie("https://lottie.host/82549a1e-8461-4191-8664-d2e831843b44/P22XqS8uS7.json")
lottie_win = load_lottie("https://lottie.host/801a6b0c-99f7-418d-8a21-72f53434685a/zZq7Vq7f7s.json")

# --- SESSION STATE (OYUN HAFIZASI) ---
if 'init' not in st.session_state:
    st.session_state.update({
        'init': True,
        'sahne': 'menu',
        'para': 1500,
        'itibar': 100,
        'aci_metresi': 0,
        'secili_alet': None,
        'hasta_tipi': None,
        'tedavi_asama': 0 # 0: Muayene, 1: Röntgen, 2: Operasyon
    })

def sahne_git(yeni_sahne):
    st.session_state.sahne = yeni_sahne
    st.rerun()

# --- OYUN MANTIĞI ---

# 1. SAHNE: ANA MENÜ
if st.session_state.sahne == 'menu':
    st.markdown("<h1 style='text-align: center;'>🦷 CLINIC MASTER: DENTIST</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        st.metric("Bütçe", f"{st.session_state.para} ₺")
        st.metric("Klinik İtibarı", f"%{st.session_state.itibar}")
        if st.button("🏥 YENİ HASTA KABUL ET", use_container_width=True, type="primary"):
            st.session_state.hasta_tipi = random.choice(["Çürük", "Kanal Tedavisi", "Temizlik"])
            st.session_state.aci_metresi = 0
            st.session_state.tedavi_asama = 0
            sahne_git('muayene')

# 2. SAHNE: MUAYENE VE DİALOG
elif st.session_state.sahne == 'muayene':
    st.title("👨‍⚕️ Muayene Koltuğu")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image(f"https://api.dicebear.com/7.x/avataaars/svg?seed={st.session_state.hasta_tipi}")
    
    with col2:
        if st.session_state.hasta_tipi == "Çürük":
            msg = "Ah doktor! Sağ tarafta bir dişim var, tatlı yiyince sızlıyor..."
        elif st.session_state.hasta_tipi == "Kanal Tedavisi":
            msg = "Üç gündür uyuyamıyorum, zonklayan bir ağrı var üstte!"
        else:
            msg = "Dişlerimin renginden memnun değilim, biraz parlasınlar istiyorum."
            
        st.chat_message("user").write(msg)
        
        if st.button("📸 Röntgen Odasına Gönder (-50 ₺)"):
            st.session_state.para -= 50
            sahne_git('rontgen')

# 3. SAHNE: RÖNTGEN (ANİMASYONLU)
elif st.session_state.sahne == 'rontgen':
    st.markdown("<h2 style='text-align: center;'>☢️ X-RAY TARANIYOR</h2>", unsafe_allow_html=True)
    if lottie_scan:
        st_lottie(lottie_scan, height=300)
    else:
        with st.spinner("Görüntü işleniyor..."): time.sleep(2)
    
    time.sleep(2)
    st.image("https://upload.wikimedia.org/wikipedia/commons/4/46/Panoramic_radiograph.jpg", caption="Röntgen Sonucu")
    st.info(f"Teşhis Onaylandı: {st.session_state.hasta_tipi}")
    
    if st.button("👄 OPERASYONA BAŞLA"):
        sahne_git('operasyon')

# 4. SAHNE: OPERASYON (FULL EKRAN AĞIZ)
elif st.session_state.sahne == 'operasyon':
    # Sidebar'ı Alet Çantasına Çevirelim
    with st.sidebar:
        st.title("🧰 Alet Çantası")
        if st.button("💉 Anestezi (Acıyı Azaltır)"): st.session_state.secili_alet = "anestezi"
        if st.button("⚙️ Elmas Frez (Çürük Temizler)"): st.session_state.secili_alet = "frez"
        if st.button("✨ Dolgu Tabancası"): st.session_state.secili_alet = "dolgu"
        st.markdown("---")
        st.write(f"Şu anki elin: **{st.session_state.secili_alet}**")

    # Üst Panel: Acı Metresi
    st.write("### 😫 Hastanın Acı Seviyesi")
    st.progress(st.session_state.aci_metresi / 100)
    
    if st.session_state.aci_metresi >= 100:
        st.error("HASTA KORKUDAN KAÇTI! İtibar kaybettin.")
        st.session_state.itibar -= 20
        time.sleep(2)
        sahne_git('menu')

    # FULL EKRAN AĞIZ TASARIMI
    st.markdown("<h2 style='text-align: center;'>AĞIZ İÇİ GÖRÜNÜMÜ</h2>", unsafe_allow_html=True)
    
    rows = [st.columns(8) for _ in range(2)] # 2 sıra diş
    
    for r_idx, row in enumerate(rows):
        for c_idx, col in enumerate(row):
            is_problem = (r_idx == 0 and c_idx == 5) # Hedef Diş
            label = "🦷" if not is_problem else "👾"
            
            if col.button(label, key=f"t_{r_idx}_{c_idx}", help="Dişe Müdahale Et"):
                if is_problem:
                    if st.session_state.secili_alet == "anestezi":
                        st.session_state.aci_metresi = max(0, st.session_state.aci_metresi - 30)
                        st.toast("Anestezi yapıldı, hasta rahatladı.")
                    elif st.session_state.secili_alet == "frez":
                        st.session_state.tedavi_asama += 1
                        st.session_state.aci_metresi += 25
                        st.toast("Çürük temizleniyor... (Acı arttı!)")
                    elif st.session_state.secili_alet == "dolgu" and st.session_state.tedavi_asama >= 2:
                        sahne_git('sonuc')
                    else:
                        st.error("Yanlış alet veya aşama!")
                        st.session_state.aci_metresi += 15
                else:
                    st.warning("Sağlam dişe dokunma!")
                    st.session_state.aci_metresi += 10

# 5. SAHNE: SONUÇ
elif st.session_state.sahne == 'sonuc':
    st.balloons()
    if lottie_win: st_lottie(lottie_win, height=300)
    
    kazanc = 500 if st.session_state.hasta_tipi != "Temizlik" else 200
    st.session_state.para += kazanc
    st.session_state.itibar = min(100, st.session_state.itibar + 5)
    
    st.success(f"Tebrikler! Tedavi başarılı. {kazanc} ₺ kazandın.")
    if st.button("KLİNİĞE DÖN"):
        sahne_git('menu')
