import pandas as pd
import streamlit as st
# --- NEW CODE: import and initialize data manager and login manager ---
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

from pathlib import Path

st.markdown("""
<style>
.app-title { font-family: 'Times New Roman', Arial, sans-serif; font-size:20px; font-weight:600; margin:8px 0 0 10px; }
</style>
<link href="https://fonts.googleapis.com/css2?family=Times+New+Roman:wght@300;400;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

def show_logo_header(logo_path="views/assets/Bild.png", logo_width=140, title="Deine Aboverwaltung", title_font_family="Times New Roman", title_font_size=40):
    # logo_path: relativer Pfad aus Repo-Root oder __file__-bezogen anpassen
    p = Path(logo_path)
    if not p.exists():
        st.warning("Logo nicht gefunden: " + str(p))
        return
    
     

    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(str(p), width=logo_width)
    with col2:
        st.markdown(
            f"<div style='display:flex;align-items:center;height:100%'>"
            f"<h1 style='font-family: \"{title_font_family}\", Arial, sans-serif; "
            f"font-size: {title_font_size}px; margin:8px 0 0 10px; font-weight:600;'>"
            f"{title}</h1></div>",
            unsafe_allow_html=True,
        )

# Beispiel-Aufruf
show_logo_header(logo_width=500)
data_manager = DataManager(       # initialize data manager
    fs_protocol='webdav',         # protocol for the filesystem, use webdav for switch drive
    fs_root_folder="bmldjm"  # folder on switch drive where the data is stored
    ) 
login_manager = LoginManager(data_manager) # handles user login and registration
login_manager.login_register()             # stops if not logged in
# --- END OF NEW CODE ---

# --- CODE UPDATE: load user data from data manager if not already present in session state --
if 'data_df' not in st.session_state:
    st.session_state['data_df'] = data_manager.load_user_data(
        'data.csv',                     # The file on switch drive where the data is stored
        initial_value=pd.DataFrame(),   # Initial value if the file does not exist
        parse_dates=['timestamp']       # Parse timestamp as datetime
    )
# --- END OF CODE UPDATE ---


pg_home = st.Page("views/home.py", title="Home", icon=":material/home:", default=True)
pg_second = st.Page("views/Aboverwaltung.py", title="Abo-Verwaltung", icon=":material/subscriptions:")
pg_overview = st.Page("views/Aboubersicht.py", title="Aboübersicht", icon=":material/overview:")
pg_budget = st.Page("views/Budgetplaner.py", title="Budgetplaner", icon=":material/attach_money:")
pg_savings = st.Page("views/Sparziele.py", title="Sparziele", icon=":material/savings:")

pg = st.navigation([pg_home, pg_second, pg_overview, pg_budget, pg_savings])
pg.run()
