import streamlit as st
from datetime import date

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Perio-Compass", page_icon="🦷", layout="centered")

# --- 1. SISTEMA DI PROTEZIONE (LOGIN) ---
def check_password():
    """Ritorna True se l'utente ha inserito la password corretta."""
    def password_entered():
        if st.session_state["password"] == "perio2026": 
            st.session_state["password_correct"] = True
            del st.session_state["password"]  
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Inserisci la Chiave di Accesso", type="password", on_change=password_entered, key="password")
        st.warning("🔒 Accesso riservato ai professionisti abilitati.")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Inserisci la Chiave di Accesso", type="password", on_change=password_entered, key="password")
        st.error("😕 Password errata. Riprova.")
        return False
    else:
        return True

if check_password():
    # --- QUI INIZIA L'APP ---
    st.title("🦷 Perio-Compass")
    st.markdown("Generatore di Report Clinico - *Versione MVP 1.1*")
    st.markdown("---")

    # --- 2. INPUT DATI (SIDEBAR) ---
    st.sidebar.header("Dati Paziente")
    
    # MODIFICA: Ora i campi sono vuoti
    nome_paziente = st.sidebar.text_input("Nome e Cognome Paziente", value="")
    eta = st.sidebar.number_input("Età", min_value=0, max_value=110, value=0)
    
    st.sidebar.markdown("---")
    st.sidebar.header("Parametri Clinici")
    
    cal_peggiore = st.sidebar.number_input("CAL Peggiore (mm)", min_value=0, value=0)
    denti_persi = st.sidebar.selectbox("Denti persi per parodontite", ["Nessuno", "1-3 denti", "4 o più"])
    tasche_profonde = st.sidebar.slider("Profondità Tasche (PPD Max)", 3, 12, 4)
    
    st.sidebar.markdown("---")
    st.sidebar.header("Fattori di Rischio")
    
    fumo = st.sidebar.radio("Fumo", ["Non fumatore", "< 10 sigarette", "≥ 10 sigarette"])
    diabete = st.sidebar.radio("Diabete", ["No", "Sì (Controllato)", "Sì (Non controllato / HbA1c >7)"])

    # --- 3. CERVELLO (LOGICA) ---
    
    # CONTROLLO DI SICUREZZA: Se non hai messo l'età, fermati qui.
    if eta == 0:
        st.info("👈 Inserisci l'età del paziente nella barra laterale per iniziare.")
    else:
        # Calcolo Stadio
        stadio = "I"
        if denti_persi == "4 o più":
            stadio = "IV"
        elif cal_peggiore >= 5:
            stadio = "III"
        elif cal_peggiore >= 3:
            stadio = "II"
            
        # Calcolo Grado
        grado = "B" 
        # Evitiamo divisione per zero
        if eta > 0:
            ratio = (cal_peggiore / eta) 
        else:
            ratio = 0
            
        if ratio < 0.25: grado = "A"
        
        # Modificatori
        if fumo == "≥ 10 sigarette" or diabete == "Sì (Non controllato / HbA1c >7)":
            grado = "C"
        
        # --- 4. GENERAZIONE TESTO ---
        testo_fumo = ""
        testo_diabete = ""
        
        if "sigarette" in fumo and fumo != "Non fumatore":
            testo_fumo = "Nel tuo caso, il fumo agisce mascherando alcuni sintomi (come il sanguinamento) e riducendo la capacità di difesa del tuo organismo."
        
        if diabete != "No":
            testo_diabete = "Nel tuo caso, lo squilibrio metabolico mantiene uno stato infiammatorio costante e rallenta la naturale capacità di guarigione."

        if testo_fumo == "" and testo_diabete == "":
            testo_rischio = "Non sono presenti fattori di rischio sistemici maggiori (Fumo/Diabete), il che ci aiuta nella prognosi."
        else:
            testo_rischio = f"{testo_fumo} {testo_diabete}"

        # --- 5. OUTPUT A SCHERMO ---
        
        if st.button("📝 Genera Progetto di Salute"):
            st.success("Report Generato!")
            
            st.markdown(f"""
            ### 📄 DOCUMENTO PAZIENTE: IL PROGETTO DI SALUTE
            
            **Paziente:** {nome_paziente}  
            **Età:** {eta} anni  
            **Data:** {date.today().strftime("%d.%m.%Y")}  
            **Clinico:** Dott./Igienista [Il Tuo Nome]
            
            ---
            
            #### 1. LA DIAGNOSI
            Abbiamo rilevato una condizione di **Parodontite (Stadio {stadio})**.
            
            * **Cosa sta succedendo:**
                I tessuti di sostegno del dente hanno subito un danno importante. Si sono create delle **tasche profonde** (fino a {tasche_profonde}mm) dove l'infiammazione è presente, mettendo a rischio la stabilità dei denti.
            * **La situazione:**
                La terapia ha l'obiettivo di conservare i denti e arrestare la progressione del danno. La presenza di queste tasche richiede un intervento professionale **mirato** per stabilizzare la situazione.
            
            #### 2. IL PROFILO DI RISCHIO
            Abbiamo valutato l'aggressività con cui la malattia si comporta nel tuo organismo: **Grado {grado}**.
            
            * **Il fattore chiave:**
                {testo_rischio}
            * **Conseguenza:**
                Questo rende la bocca meno reattiva alle cure. Per ottenere il successo, dovremo monitorare la situazione con un'attenzione superiore alla media.
            
            ---
            
            #### 3. LA NOSTRA ALLEANZA
            Il risultato dipende dalla solidità della nostra collaborazione.
            
            **TERAPIA PROFESSIONALE (Il mio compito):**
            Il mio obiettivo è fare **tabula rasa** dei batteri dove tu non puoi arrivare.
            * **Metodo:** Utilizzerò tecnologie avanzate e protocolli delicati per decontaminare le radici dei denti, garantendo il massimo comfort.
            * **Obiettivo:** Far guarire i tessuti infiammati e ridurre la profondità delle tasche, creando un ambiente che tu possa riuscire a mantenere pulito.
            
            **TERAPIA DOMICILIARE (Il tuo compito):**
            La guarigione avviene **anche a casa**, giorno per giorno. La terapia professionale crea le condizioni, tu mantieni la salute.
            * **Strumenti Prescritti:**
                L'utilizzo quotidiano e rigoroso degli strumenti di igiene domiciliare che abbiamo selezionato insieme è l'unico modo per disgregare i batteri e prevenire le recidive.
            * **Stile di vita:** È fondamentale la consapevolezza che i fattori di rischio contrastano attivamente gli effetti benefici della cura.
            
            ---
            
            > *"Lavoriamo insieme per fermare la malattia e proteggere il tuo sorriso nel tempo."*
            """)
