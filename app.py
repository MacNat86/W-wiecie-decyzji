import streamlit as st
import random

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="Architekt Kariery - Symulator", page_icon="🎓", layout="centered")

# --- INICJALIZACJA STANU GRY ---
if 'etap' not in st.session_state:
    st.session_state.update({
        'etap': 'start',
        'plec': None,
        'soft_skills': 0,
        'hard_skills': 0,
        'finanse': 1000,
        'log': [],
        'historia': ""
    })

def zmien_etap(nowy_etap):
    st.session_state.etap = nowy_etap
    st.rerun()

# --- PASEK BOCZNY ---
st.sidebar.title("📊 Twój Profil")
if st.session_state.plec:
    st.sidebar.write(f"Postać: **{st.session_state.plec}**")
st.sidebar.metric("Budżet", f"{st.session_state.finanse} PLN")
st.sidebar.write(f"🤝 Miękkie: {st.session_state.soft_skills} | ⚙️ Twarde: {st.session_state.hard_skills}")

# --- LOGIKA GRY ---

# 0. WYBÓR POSTACI
if st.session_state.etap == 'start':
    st.title("🚀 Architekt Kariery")
    st.write("Witaj w symulatorze wyborów zawodowych. Twoja przyszłość zaczyna się dzisiaj!")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Chcę grać jako Uczeń"):
            st.session_state.plec = "Uczeń"
            zmien_etap('wybor_szkoly')
    with col2:
        if st.button("Chcę grać jako Uczennica"):
            st.session_state.plec = "Uczennica"
            zmien_etap('wybor_szkoly')

# 1. WYBÓR ŚCIEŻKI EDUKACYJNEJ
elif st.session_state.etap == 'wybor_szkoly':
    st.header("📍 Wybór Ścieżki")
    st.write(f"Jako **{st.session_state.plec}**, musisz zdecydować o swojej edukacji:")
    
    opcje = {
        "Liceum (Studia i Teoria)": "liceum",
        "Technikum (Zawód i Matura)": "technikum",
        "Szkoła Branżowa (Szybki Fach)": "branzowa",
        "Własna ścieżka (Pasja i Kursy)": "freelance"
    }
    
    for tekst, klucz in opcje.items():
        if st.button(tekst):
            if klucz == "liceum": st.session_state.soft_skills += 3
            if klucz == "technikum": st.session_state.hard_skills += 3
            if klucz == "branzowa": st.session_state.finanse += 200; st.session_state.hard_skills += 5
            zmien_etap(klucz)

# 2. DETALE ŚCIEŻEK (Przykład dla Liceum)
elif st.session_state.etap == 'liceum':
    st.header("🎓 Ścieżka Akademicka")
    st.write("W liceum skupiasz się na teorii. Pojawia się okazja zapisu do samorządu uczniowskiego.")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Wchodzę w to! (+Soft Skills)"):
            st.session_state.soft_skills += 7
            zmien_etap('wydarzenie_losowe')
    with col2:
        if st.button("Wolę kółko fizyczne (+Hard Skills)"):
            st.session_state.hard_skills += 7
            zmien_etap('wydarzenie_losowe')

# 3. ŚCIEŻKA TECHNIKUM / BRANŻOWA
elif st.session_state.etap in ['technikum', 'branzowa']:
    st.header("🛠️ Ścieżka Praktyczna")
    st.write("Dostajesz propozycję płatnych praktyk w wakacje.")
    if st.button("Biorę praktyki (+400 PLN, +5 Hard Skills)"):
        st.session_state.finanse += 400
        st.session_state.hard_skills += 5
        zmien_etap('wydarzenie_losowe')
    if st.button("Odpoczywam (Nic nie zyskujesz)"):
        zmien_etap('wydarzenie_losowe')

# 4. ŚCIEŻKA FREELANCE
elif st.session_state.etap == 'freelance':
    st.header("🎨 Pasja i Samodzielność")
    st.write("Zamiast szkoły, stawiasz na kursy online i budowanie portfolio.")
    wybor = st.slider("Ile czasu poświęcasz na naukę codziennie?", 0, 12, 4)
    if st.button("Zatwierdź"):
        st.session_state.hard_skills += wybor
        st.session_state.finanse -= (wybor * 10)
        zmien_etap('wydarzenie_losowe')

# 5. WYDARZENIE LOSOWE (Dla wszystkich)
elif st.session_state.etap == 'wydarzenie_losowe':
    st.header("🎲 Karta Losu")
    zdarzenie = random.choice([
        ("Wygrałeś grant edukacyjny!", 0, 0, 500),
        ("Twój projekt na YouTube stał się hitem!", 5, 2, 100),
        ("Zepsuł Ci się komputer...", 0, 0, -400),
        ("Brałeś udział w debacie oksfordzkiej.", 6, 0, 0)
    ])
    st.info(zdarzenie[0])
    st.session_state.soft_skills += zdarzenie[1]
    st.session_state.hard_skills += zdarzenie[2]
    st.session_state.finanse += zdarzenie[3]
    
    if st.button("Idź do finału"):
        zmien_etap('final')

# 6. FINAŁ I GENERATOR ZAWODÓW
elif st.session_state.etap == 'final':
    st.header("🏁 Twoja Przyszłość")
    s = st.session_state.soft_skills
    h = st.session_state.hard_skills
    f = st.session_state.finanse

    # Rozbudowana logika zawodów
    if s > 15 and h > 15: wynik = "Dyrektor Innowacji"
    elif h > 20: wynik = "Główny Inżynier / Programista"
    elif s > 20: wynik = "Specjalista PR / Dyplomata"
    elif f > 1500: wynik = "Inwestor / Właściciel Firmy"
    elif h > 10 and s > 10: wynik = "Analityk Biznesowy"
    else: wynik = "Wszechstronny Specjalista (Junior)"

    st.success(f"Twój zawód: **{wynik}**")
    st.write(f"Osiągnięcia: Miękkie ({s}), Twarde ({h}), Budżet ({f} PLN)")
    
    if st.button("Zacznij od nowa"):
        st.session_state.clear()
        st.rerun()