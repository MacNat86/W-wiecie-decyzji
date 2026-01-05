import streamlit as st
import random

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="Architekt Kariery: Symulator", page_icon="⚖️", layout="centered")

# --- STYLE CSS (NAPRAWIONE) ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; font-weight: bold; }
    .stProgress > div > div > div > div { background-color: #2E86C1; }
    .css-10trblm { font-size: 1.2rem; }
    </style>
    """, unsafe_allow_html=True)

# --- INICJALIZACJA STANU GRY ---
if 'etap' not in st.session_state:
    st.session_state.update({
        'etap': 'start',
        'plec': None,
        'branża': None,
        'wiedza': 10,
        'relacje': 10,
        'zdrowie': 100,
        'finanse': 500,
        'exp': 0,
        'historia': []
    })

def zmien_etap(nowy_etap):
    st.session_state.etap = nowy_etap
    st.rerun()

# --- PANEL BOCZNY (STATYSTYKI) ---
st.sidebar.title("📊 Twój Status")
if st.session_state.plec:
    st.sidebar.subheader(f"Rola: {st.session_state.plec}")
st.sidebar.divider()
st.sidebar.metric("Portfel", f"{st.session_state.finanse} PLN")
st.sidebar.write(f"🧠 Wiedza: {st.session_state.wiedza}")
st.sidebar.write(f"🤝 Relacje: {st.session_state.relacje}")
st.sidebar.write(f"🛠️ Doświadczenie: {st.session_state.exp}")
st.sidebar.progress(max(0, min(st.session_state.zdrowie, 100)), text=f"Energia życiowa: {st.session_state.zdrowie}%")

# --- LOGIKA GRY ---

# ETAP 0: START
if st.session_state.etap == 'start':
    st.title("🚀 Architekt Kariery: Symulator")
    st.write("Witaj w symulatorze decyzji zawodowych. To nie jest zwykły test – to gra o Twoją przyszłość. Każdy wybór niesie skutki, które zobaczysz za 5 lat.")
    st.info("Zadbaj o balans: wysoka wiedza przy zerowym zdrowiu psychicznym doprowadzi do porażki.")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Zacznij jako Uczeń"):
            st.session_state.plec = "Uczeń"
            zmien_etap('wybor_branzy')
    with c2:
        if st.button("Zacznij jako Uczennica"):
            st.session_state.plec = "Uczennica"
            zmien_etap('wybor_branzy')

# ETAP 1: WYBÓR BRANŻY
elif st.session_state.etap == 'wybor_branzy':
    st.header("🏢 Krok 1: Dominująca pasja")
    st.write("Wybierz obszar, w którym czujesz się najlepiej. To zdefiniuje Twoje trudności w nauce.")
    
    col = st.columns(2)
    with col[0]:
        if st.button("Inżynieria i Nowe Technologie"):
            st.session_state.branża = "Tech"
            st.session_state.wiedza += 10
            zmien_etap('edukacja_podstawowa')
        if st.button("Medycyna i Pomoc Ludziom"):
            st.session_state.branża = "Medycyna"
            st.session_state.relacje += 10
            zmien_etap('edukacja_podstawowa')
    with col[1]:
        if st.button("Biznes i Zarządzanie"):
            st.session_state.branża = "Biznes"
            st.session_state.finanse += 500
            zmien_etap('edukacja_podstawowa')
        if st.button("Rzemiosło i Sztuka"):
            st.session_state.branża = "Art"
            st.session_state.exp += 15
            zmien_etap('edukacja_podstawowa')

# ETAP 2: EDUKACJA I WYRZECZENIA
elif st.session_state.etap == 'edukacja_podstawowa':
    st.header("📚 Czas Szkoły Średniej")
    st.write(f"Jesteś na ścieżce: **{st.session_state.branża}**. Przed Tobą rok intensywnej nauki.")
    
    opcja = st.radio("Jak zarządzasz swoim czasem w tym roku?", [
        "Skupienie na ocenach (Wiedza ++, Zdrowie -20)",
        "Budowanie sieci kontaktów (Relacje ++, Finanse -200)",
        "Praca po lekcjach (Finanse ++, Wiedza -10)",
        "Balans (Małe bonusy do wszystkiego)"
    ])
    
    if st.button("Zatwierdź rok nauki"):
        if "ocenach" in opcja:
            st.session_state.wiedza += 25
            st.session_state.zdrowie -= 20
        elif "kontaktów" in opcja:
            st.session_state.relacje += 25
            st.session_state.finanse -= 200
        elif "Praca" in opcja:
            st.session_state.finanse += 600
            st.session_state.wiedza -= 10
            st.session_state.exp += 10
        else:
            st.session_state.wiedza += 10
            st.session_state.relacje += 10
            st.session_state.zdrowie += 5
        zmien_etap('dylemat_doroslosci')

# ETAP 3: DYLEMAT DOROSŁOŚCI (KOSZT ALTERNATYWNY)
elif st.session_state.etap == 'dylemat_doroslosci':
    st.header("⚖️ Poważna decyzja")
    st.write("Masz 19 lat. Otrzymujesz propozycję płatnego stażu za granicą, ale oznacza to rozłąkę z bliskimi i ogromny stres.")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Wyjeżdżam (Exp +30, Wiedza +20, Zdrowie -40)"):
            st.session_state.exp += 30
            st.session_state.wiedza += 20
            st.session_state.zdrowie -= 40
            st.session_state.historia.append("Wyjazd zagraniczny")
            zmien_etap('karta_losu')
    with c2:
        if st.button("Zostaję (Relacje +30, Zdrowie +20)"):
            st.session_state.relacje += 30
            st.session_state.zdrowie += 20
            st.session_state.historia.append("Stabilizacja w kraju")
            zmien_etap('karta_losu')

# ETAP 4: KARTA LOSU
elif st.session_state.etap == 'karta_losu':
    st.header("🎲 Losowy zwrot akcji")
    los = random.randint(1, 3)
    if los == 1:
        st.warning("Kryzys gospodarczy! Tracisz część oszczędności.")
        st.session_state.finanse -= 300
    elif los == 2:
        st.success("Wygrałeś konkurs branżowy! Twój prestiż rośnie.")
        st.session_state.exp += 20
    else:
        st.info("Niespodziewany spadek formy. Musisz zwolnić.")
        st.session_state.zdrowie -= 15
    
    if st.button("Sprawdź swój wynik końcowy"):
        zmien_etap('podsumowanie')

# ETAP 5: PODSUMOWANIE
elif st.session_state.etap == 'podsumowanie':
    st.header("🏁 Twoja Przyszłość Zawodowa")
    
    w = st.session_state.wiedza
    r = st.session_state.relacje
    e = st.session_state.exp
    z = st.session_state.zdrowie
    f = st.session_state.finanse
    
    # LOGIKA WYNIKÓW
    if z <= 0:
        st.error("🚨 PORAŻKA: WYPALENIE ZAWODOWE. Zbyt mocno parłeś do przodu, ignorując odpoczynek. Twoja kariera została przerwana przez problemy zdrowotne.")
        wynik = "Pacjent na regeneracji"
    elif w > 50 and r > 40 and e > 40:
        st.balloons()
        st.success("👑 WYBITNY SUKCES: Jesteś liderem w swojej branży! Masz wiedzę, ludzi i doświadczenie.")
        wynik = f"Top Manager / CEO ({st.session_state.branża})"
    elif w > 60:
        st.success("🔬 EKSPERT: Zostałeś wybitnym specjalistą. Firmy walczą o Twoją wiedzę.")
        wynik = f"Główny Analityk / Inżynier ({st.session_state.branża})"
    elif f > 1200:
        st.success("💰 PRZEDSIĘBIORCA: Może nie wiesz wszystkiego, ale wiesz jak zarabiać. Masz własną firmę.")
        wynik = "Właściciel Biznesu"
    else:
        st.info("👨‍💼 SOLIDNY PRACOWNIK: Masz stabilną pracę, ale nie wykorzystałeś w pełni swojego potencjału.")
        wynik = "Specjalista"

    st.subheader(f"Twój zawód: {wynik}")
    
    # Wykres kompetencji (tekstowy)
    st.code(f"""
    Wiedza:      {'█' * (w // 5)} ({w})
    Relacje:     {'█' * (r // 5)} ({r})
    Doświadczenie:{'█' * (e // 5)} ({e})
    Zdrowie:     {'█' * (max(0, z) // 5)} ({z}%)
    """)
    
    st.write("**Podjęte kluczowe decyzje:**", ", ".join(st.session_state.historia) if st.session_state.historia else "Brak")

    if st.button("Zagraj jeszcze raz - inna ścieżka"):
        st.session_state.clear()
        st.rerun()
