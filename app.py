import streamlit as st
import time

# Sayfa ayarlarını geniş (tam ekran hissiyatı için) yapıyoruz
st.set_page_config(page_title="Diş Hekimi Simülatörü", layout="wide", initial_sidebar_state="collapsed")

# Streamlit varsayılan UI elemanlarını gizleyerek "oyun" hissiyatını artıralım
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- OYUN DURUMU (STATE) YÖNETİMİ ---
if 'sahne' not in st.session_state:
    st.session_state.sahne = 'muayenehane'

def sahne_degistir(yeni_sahne):
    st.session_state.sahne = yeni_sahne

# --- SAHNELER ---

# 1. Sahne: Muayenehane ve Diyalog
if st.session_state.sahne == 'muayenehane':
    st.title("🦷 Muayenehane")
    st.markdown("---")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("https://api.dicebear.com/7.x/avataaars/svg?seed=Ahmet", width=200) # Temsili hasta avatarı
    with col2:
        st.subheader("Hasta: Ahmet Bey")
        st.info("💬 'Merhaba doktor bey. İki gündür sağ alt dişimde sıcak bir şey içtiğimde inanılmaz bir sızı oluyor. Gece ağrıdan uyutmadı resmen.'")
        
        if st.button("📸 Hastayı Panoramik Röntgene Yönlendir", use_container_width=True):
            sahne_degistir('rontgen')

# 2. Sahne: Röntgen Odası
elif st.session_state.sahne == 'rontgen':
    st.title("☢️ Röntgen Odası")
    st.markdown("---")
    
    with st.spinner("Röntgen çekiliyor..."):
        time.sleep(1.5) # Küçük bir simülasyon gecikmesi
        
    st.success("Röntgen filmi hazır.")
    # Temsili bir röntgen görseli
    st.image("https://upload.wikimedia.org/wikipedia/commons/4/46/Panoramic_radiograph.jpg", use_column_width=True)
    
    st.warning("📋 **Teşhis Notu:** Sağ alt 6 numaralı dişte (1. büyük azı) derin bir çürük başlangıcı ve pulpaya (sinire) yakın lezyon görünüyor.")
    
    if st.button("👄 Hastayı Koltuğa Al ve Ağzını Açtır", type="primary", use_container_width=True):
        sahne_degistir('agiz_ici')

# 3. Sahne: Ağız İçi (Tam Ekran Müdahale)
elif st.session_state.sahne == 'agiz_ici':
    # Bu aşamada ekranı tamamen dişlere ayırıyoruz
    st.markdown("<h1 style='text-align: center;'>👄 Ağız İçi Görünümü</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.write("Müdahale edilecek dişi seçin:")
    
    # Ağız içi dizilimi için kolonlar oluşturuyoruz
    ust_Cene, alt_Cene = st.container(), st.container()
    
    with ust_Cene:
        st.markdown("### Üst Çene")
        u1, u2, u3, u4 = st.columns(4)
        u1.button("Sağ Üst Azılar", use_container_width=True)
        u2.button("Sağ Üst Kesiciler", use_container_width=True)
        u3.button("Sol Üst Kesiciler", use_container_width=True)
        u4.button("Sol Üst Azılar", use_container_width=True)
        
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    with alt_Cene:
        st.markdown("### Alt Çene")
        a1, a2, a3, a4 = st.columns(4)
        
        # Sorunlu diş a1 kolonunda (Sağ Alt)
        if a1.button("Sağ Alt Azılar (⚠️ Sorunlu Bölge)", use_container_width=True):
            st.balloons()
            st.success("💉 **Doğru Tespit!** Anestezi uygulandı ve çürük temizleme işlemine başlandı.")
            time.sleep(2)
            sahne_degistir('bitis')
            st.rerun()
            
        a2.button("Sağ Alt Kesiciler", use_container_width=True)
        a3.button("Sol Alt Kesiciler", use_container_width=True)
        a4.button("Sol Alt Azılar", use_container_width=True)

# 4. Sahne: Bitiş ve Döngü
elif st.session_state.sahne == 'bitis':
    st.title("✅ Tedavi Başarılı!")
    st.write("Hastanın dolgusu başarıyla tamamlandı. Şikayetleri sona erdi.")
    
    if st.button("Sıradaki Hastayı Çağır", use_container_width=True):
        # Durumu sıfırlayıp başa dönüyoruz
        sahne_degistir('muayenehane')
        st.rerun()
