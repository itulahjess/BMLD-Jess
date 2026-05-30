import pandas as pd
import streamlit as st
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

/* Fonts importieren */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&display=swap');

/* Hauptschrift */
html, body {
    font-family: 'Playfair Display', serif;
}

.stApp {
    font-family: 'Playfair Display', serif !important;
}

/* Alle Streamlit Container */
div, p, label {
    font-family: 'Playfair Display', serif;
}

/* Titel */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Playfair Display', serif !important;
}

/* Text */
p, label {
    font-family: 'Playfair Display', serif !important;
}

/* Inputs & Buttons */
button, input, textarea {
    font-family: 'Playfair Display', serif !important;
}

/* Streamlit Textcontainer */
.stMarkdown p,
.stText p,
.stText,
.stMarkdown {
    font-family: 'Playfair Display', serif !important;
}

/* Sidebar NUR TEXT */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label {
    font-family: 'Playfair Display', serif !important;
}

/* Navigation Labels */
section[data-testid="stSidebarNav"] a {
    font-family: 'Playfair Display', serif !important;
}
            
/* Sidebar Navigation Text */
[data-testid="stSidebarNav"] a,
[data-testid="stSidebarNav"] {
    font-family: 'Playfair Display', serif !important;
}

/* Allgemeiner Streamlit Text */
[data-testid="stMarkdownContainer"] p,
[data-testid="stText"] {
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

/* Logout Button in Sidebar */
section[data-testid="stSidebar"] .stButton > button {
    background-color: rgba(255, 255, 255, 0.82) !important;
    color: #054033 !important;
    padding: 6px 12px !important;
    font-size: 12px !important;
    font-weight: 400 !important;
    border: 1px solid rgba(95, 208, 173, 0.18) !important;
    height: auto !important;
    width: auto !important;
}

section[data-testid="stSidebar"] .stButton > button p {
    font-weight: 400 !important;
    font-size: 12px !important;
}

section[data-testid="stSidebar"] .stButton > button p::first-line {
    font-weight: 400 !important;
    font-size: 12px !important;
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
            
p, label {
    font-size: 20px;
}
            
[data-testid="stMetric"] * {
    font-size: 18px !important;
    font-weight: 500 !important;
}
            
[data-testid="stMetricValue"] {
    font-size: 36px !important;
    font-weight: 700 !important;
}

/* METRIC BOX */
div[data-testid="stMetric"] {
    background-color: #e8fff5;
    padding: 20px;
    border-radius: 18px;
}

</style>
""", unsafe_allow_html=True)


def show_logo_header(logo_path="views/assets/Bild.png", logo_width=700):
    p = Path(logo_path)

    if not p.exists():
        st.warning("Logo nicht gefunden: " + str(p))
        return

    st.image(
        str(p),
        width=logo_width
    )


show_logo_header(logo_width=700)


data_manager = DataManager(
    fs_protocol='webdav',
    fs_root_folder="bmldjm"
)

login_manager = LoginManager(data_manager)
login_manager.login_register()


if 'data_df' not in st.session_state:
    st.session_state['data_df'] = data_manager.load_user_data(
        'data.csv',
        initial_value=pd.DataFrame(),
        parse_dates=['timestamp']
    )


pg_home = st.Page("views/home.py", title="Home", icon=":material/home:", default=True)
pg_second = st.Page("views/Aboverwaltung.py", title="Abo-Verwaltung", icon=":material/subscriptions:")
pg_overview = st.Page("views/Aboubersicht.py", title="Aboübersicht", icon=":material/overview:")
pg_budget = st.Page("views/Budgetplaner.py", title="Budgetplaner", icon=":material/attach_money:")
pg_savings = st.Page("views/Sparziele.py", title="Sparziele", icon=":material/savings:")

pg = st.navigation([pg_home, pg_second, pg_overview, pg_budget, pg_savings])
pg.run()
