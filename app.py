import pandas as pd
import streamlit as st
# --- NEW CODE: import and initialize data manager and login manager ---
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

from pathlib import Path

# Seitenlayout
st.set_page_config(
    page_title="Meine Aboverwaltung",
    page_icon="💳",
    layout="wide"
)

# Mintgrünes CSS Design
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&display=swap');

/* Nur Texte */
h1, h2, h3, h4, h5, h6,
p,
label,
button,
input,
textarea {
    font-family: 'Playfair Display', serif !important;
}

/* Hintergrund */
.stApp {
    background-color: #f7fffb;
}

/* Titel */
h1, h2, h3 {
    color: #1b5e54;
    font-family: 'Playfair Display', serif;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #e8fff5;
}

/* Buttons */
.stButton > button {
    background-color: #66d9b8;
    color: white;
    border-radius: 12px;
    border: none;
    padding: 10px 20px;
    font-size: 16px;
    transition: 0.3s;
}

.stButton > button:hover {
    background-color: #45c9a5;
    color: white;
}

/* Inputfelder */
.stTextInput input {
    border-radius: 10px;
    border: 2px solid #8be0c8;
    padding: 10px;
}

/* Selectbox */
.stSelectbox div[data-baseweb="select"] {
    border-radius: 10px;
    border: 2px solid #8be0c8;
}

/* Kartenstil */
.custom-box {
    background-color: white;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

/* Metric Container */
[data-testid="metric-container"] {
    background-color: white;
    border-radius: 15px;
    padding: 15px;
    border-left: 8px solid #66d9b8;
}


/* Titel optional grösser */
h1 {
    font-size: 44px;
    font-weight: 700;
}

h2 {
    font-size: 32px;
}
            
p, div, label {
    font-size: 20px;
}
            
[data-testid="stMetric"] * {
    font-size: 18px !important;
    font-weight: 500 !important;
}
            
[data-testid="stMetricValue"] {
    font-size: 18px !important;
    font-weight: 300 !important;
}

/* METRIC BOX */
div[data-testid="stMetric"] {
    background-color: #e8fff5;
    padding: 20px;
    border-radius: 18px;
}


</style>
""", unsafe_allow_html=True)

def show_logo_header(logo_path="views/assets/Bild.png", logo_width=140, title="Meine Aboverwaltung", title_font_family="Playfair Display", title_font_size=40):
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
login_manager.login_register() 
          # stops if not logged in
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
