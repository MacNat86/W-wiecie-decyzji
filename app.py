import streamlit as st
import random

# --- KONFIGURACJA ---
st.set_page_config(page_title="Projekt: Przyszłość", page_icon="⚖️")

# --- STYLE ---
st.markdown("""
    <style>
    .stProgress > div > div > div > div { background-color: #4CAF50; }
    .reportview-container .main .block-container { max-width: 800px; }
    </style>
    """, unsafe_content_code=True)

# --- INICJALIZACJA ---
if 'etap' not in st.session_state:
    st.session_state.update({
        'etap': 'start',
        'plec': None,
        'punkty_wiedzy': 0,
        'punkty_spoleczne': 0,
        'zdrowie_psychiczne': 100,
        'finanse': 300,
        'doswiadczenie': 0,
        'decyzje': []
    })

def przejdz_dalej(nowy_etap):
    st.session_state.etap = nowy_etap
    st.rerun()

# --- SIDEBAR (STATYSTYKI JAKO WYZWANIE) ---
st.sidebar.title("📊 Twój Status")
st.sidebar.metric("Konto", f"{st.session_state.finanse} PLN")
st.sidebar.write(f"🧠 Wiedza: {st.session_state.punkty_wiedzy}")
st.sidebar.write(f"🤝 Relacje: {st.session_state.punkty_spoleczne}")
st.sidebar.write(f"🛠️ Doświadczenie: {st.session_state.doswiadczenie}")
st.sidebar.progress(st.session_state.zdrowie_psychiczne, text=f"Kondycja psychiczna: {st.session_state.zdrowie_psychiczne}%")

# --- LOGIKA ROZGRYWKI ---

if st.session_state.etap == 'start':
    st.title("⚖️ Projekt: Przyszłość")
    st.write("To nie jest zwykły quiz. Każda decyzja zamyka jedne drzwi, a otwiera inne. Masz przed sobą 5 lat kluczowych decyzji.")
    c1, c2 = st.columns(2)
    with c1: 
        if st.button("Uczeń"): st.session_state.plec = "Uczeń"; przejdz_dalej('wybor_profilu')
    with c2: 
        if st.button("Uczennica"): st.session_state.plec = "Uczennica"; przejdz_dalej('wybor_profilu')

elif st.session_state.etap == 'wybor_profilu':
    st.header("📍 Krok 1: Strategia Edukacyjna")
    st.write("Szkoła to tylko baza. Musisz wybrać swój główny 'filar'. Gdzie zainwestujesz najwięcej czasu w 1. klasie?")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Ścisły")
        st.write("Ciężka nauka, mało czasu na życie towarzyskie.")
        if st.button("Wybieram Ścisły"):
            st.session_state.punkty_wiedzy += 15
            st.session_state.zdrowie_psychiczne -= 10
            st.session_state.decyzje.append("Profil ścisły")
            przejdz_dalej('trudny_wybor')
    with col2:
        st.subheader("Human / Relacje")
        st.write("Dużo projektów grupowych, średnie perspektywy finansowe na start.")
        if st.button("Wybieram Human"):
            st.session_state.punkty_spoleczne += 15
            st.session_state.decyzje.append("Profil humanistyczny")
            przejdz_dalej('trudny_wybor')
    with col3:
        st.subheader("Zawodowy / Tech")
        st.write("Szybkie wejście w fach, ale ryzyko wypalenia fizycznego.")
        if st.button("Wybieram Tech"):
            st.session_state.doswiadczenie += 15
            st.session_state.finanse += 100
            st.session_state.decyzje.append("Profil techniczny")
            przejdz_dalej('trudny_wybor')

elif st.session_state.etap == 'trudny_wybor':
    st.header("⌛ Dylemat 2. Klasy: Czas to pieniądz")
    st.write("Masz 20 'jednostek czasu'. Jak je rozdzielisz w tym roku?")
    
    nauka = st.slider("Czas na naukę i korepetycje", 0, 20, 10)
    praca = st.slider("Czas na pracę dorywczą / staż", 0, 20 - nauka, 0)
    zycie = 20 - nauka - praca
    
    st.write(f"Pozostały czas na regenerację i znajomych: **{zycie}**")
    
    if st.button("Zatwierdź podział"):
        st.session_state.punkty_wiedzy += nauka * 2
        st.session_state.finanse += praca * 50
        st.session_state.punkty_spoleczne += zycie
        if zycie < 4:
            st.session_state.zdrowie_psychiczne -= 20
            st.warning("Jesteś skrajnie zmęczony! Twoja kondycja psychiczna drastycznie spadła.")
        przejdz_dalej('kryzys')

elif st.session_state.etap == 'kryzys':
    st.header("⚡ Kryzys: Nieoczekiwane zdarzenie")
    zdarzenie = random.choice([
        "Masz okazję wyjechać na prestiżową wymianę, ale kosztuje ona 1000 PLN. Pożyczasz czy rezygnujesz?",
        "Twoja pasja zaczyna przynosić dochody, ale zawalasz oceny. Co wybierasz?",
        "Wypalenie. Musisz wydać 300 PLN na terapię/odpoczynek lub stracisz punkty wiedzy."
    ])
    st.subheader(zdarzenie)
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Inwestuję w przyszłość / Pasję"):
            if st.session_state.finanse >= 300:
                st.session_state.finanse -= 300
                st.session_state.doswiadczenie += 20
            else:
                st.error("Nie stać Cię na to! Musisz wybrać drugą opcję.")
    with c2:
        if st.button("Skupiam się na stabilizacji / Szkole"):
            st.session_state.punkty_wiedzy += 10
            st.session_state.zdrowie_psychiczne += 5
    
    if st.button("Idź do podsumowania kariery"):
        przejdz_dalej('rynek_pracy')

elif st.session_state.etap == 'rynek_pracy':
    st.header("🌍 Rynek Pracy: 5 lat później")
    st.write("Analizujemy Twój profil...")
    
    w = st.session_state.punkty_wiedzy
    s = st.session_state.punkty_spoleczne
    d = st.session_state.doswiadczenie
    p = st.session_state.zdrowie_psychiczne
    
    if p < 30:
        st.error("🚨 Zakończenie: Wypalenie zawodowe. Masz wiedzę, ale nie masz siły jej użyć. Nauczka: Pamiętaj o odpoczynku!")
    elif w > 40 and s > 30:
        st.success("💎 Zakończenie: Manager / Lider Zespołu. Świetny balans!")
    elif w > 50:
        st.success("🔬 Zakończenie: Ekspert / Naukowiec. Twoja wiedza jest Twoją walutą.")
    elif d > 40:
        st.success("🏗️ Zakończenie: Wysokiej klasy Specjalista. Praktyka czyni mistrza.")
    else:
        st.warning("⚠️ Zakończenie: Praca poniżej kwalifikacji. Zabrakło Ci konkretnego kierunku.")
        
    st.write("Podjęte przez Ciebie decyzje:", ", ".join(st.session_state.decyzje))
    if st.button("Spróbuj innej strategii (Restart)"):
        st.session_state.clear()
        st.rerun()
