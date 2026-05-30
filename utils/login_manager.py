import secrets
from pathlib import Path
import streamlit as st
import streamlit_authenticator as stauth
from utils.data_manager import DataManager


class LoginManager:
    """
    Singleton class that manages user authentication for the application.

    Handles user login, registration, and session management using
    streamlit-authenticator. Credentials are stored in a YAML file via
    the DataManager.
    """

    def __new__(cls, *args, **kwargs):
        """
        Singleton: returns existing instance from session state if available.

        Returns:
            LoginManager: The singleton instance, either existing or newly created.
        """
        if 'login_manager' in st.session_state:
            return st.session_state.login_manager
        instance = super(LoginManager, cls).__new__(cls)
        st.session_state.login_manager = instance
        return instance

    def __init__(self, data_manager: DataManager = None,
                 auth_credentials_file: str = 'credentials.yaml',
                 auth_cookie_name: str = 'bmld_inf2_streamlit_app'):
        """
        Initializes authentication components if not already initialized.

        Args:
            data_manager (DataManager): The DataManager instance to use for credential storage.
            auth_credentials_file (str): Filename for storing user credentials.
            auth_cookie_name (str): Cookie name for session management.
        """
        if hasattr(self, 'authenticator'):
            return
        if data_manager is None:
            return

        self.data_manager = data_manager
        self.auth_credentials_file = auth_credentials_file
        self.auth_cookie_name = auth_cookie_name
        if 'auth_cookie_key' not in st.session_state:
            st.session_state.auth_cookie_key = secrets.token_urlsafe(32)
        self.auth_cookie_key = st.session_state.auth_cookie_key
        self.auth_credentials = self._load_auth_credentials()
        self.authenticator = stauth.Authenticate(
            self.auth_credentials, self.auth_cookie_name, self.auth_cookie_key
        )

    def _load_auth_credentials(self):
        """
        Loads user credentials from the configured credentials file.

        Returns:
            dict: User credentials, defaulting to empty usernames dict if file not found.
        """
        return self.data_manager.load_app_data(self.auth_credentials_file, initial_value={"usernames": {}})

    def _save_auth_credentials(self):
        """Saves current user credentials to the credentials file."""
        self.data_manager.save_app_data(self.auth_credentials, self.auth_credentials_file)

    def login_register(self, login_title='Login', register_title='Registrieren'):
        """
        Handles authentication. When not logged in, shows the login/register page
        and stops further execution. When logged in, adds the logout button to the
        sidebar and returns, allowing app.py to set up its own navigation.

        Args:
            login_title (str): Label for the login tab.
            register_title (str): Label for the registration tab.
        """
        if st.session_state.get("authentication_status") is True:
            with st.sidebar:
                st.write(f"Angemeldet als: **{st.session_state.get('name')}**")
                self.authenticator.logout()
        else:
            page_fn = lambda: self._login_register_page(login_title, register_title)
            pg = st.navigation([st.Page(page_fn, title="Login", icon=":material/login:")])
            pg.run()
            st.stop()

    def _login_register_page(self, login_title, register_title):
        """Page function shown when the user is not authenticated."""
        # inject a mint-green theme and a centered card header
        self._inject_mint_styles()

        # show logo if present (views/assets/logo.png)
        logo_path = Path(__file__).parent.parent / "views" / "assets" / "logo.png"
        if logo_path.exists():
            try:
                st.image(str(logo_path), width=260)
            except Exception:
                pass

        st.markdown(
            """
        <div class="login-header">
          <h1 class="login-title">Willkommen zurück</h1>
          <div class="login-sub">Melde dich an, um Zugriff auf die Aboverwaltung zu erhalten</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        login_tab, register_tab = st.tabs((login_title, register_title))
        with login_tab:
            with st.container():
                self._login()
        with register_tab:
            with st.container():
                self._register()

    def _inject_mint_styles(self):
        """Inject CSS to style the login/register page with the app's mint theme and card layout."""
        css = """
        <style>
        :root{--mint:#c8f1e0;--mint-strong:#7bd7bd;--card:#ffffff;--text-dark:#054033;--text-muted:#52796f;--border:#8be0c8}

        .stApp{background-color:#f7fffb;}
        .stApp .block-container{max-width:760px;margin:28px auto;padding-left:16px;padding-right:16px;}

        .login-header{
            max-width:760px;
            margin:0 auto 20px;
            padding:30px 24px;
            border-radius:22px;
            background:#ffffff;
            box-shadow:0 14px 34px rgba(31,122,99,0.06);
            text-align:center;
        }
        .login-title{
            font-size:44px;
            font-weight:700;
            color:var(--text-dark);
            margin:0;
        }
        .login-sub{
            font-size:20px;
            color:var(--text-muted);
            margin-top:10px;
            line-height:1.55;
        }

        .stContainer{
            background:#ffffff;
            border-radius:22px;
            padding:20px 24px 24px;
            box-shadow:0 14px 34px rgba(31,122,99,0.06);
        }

        .stTabs [role='tablist']{
            margin-bottom:14px;
        }

        .stTextInput input,
        .stPasswordInput input,
        .stNumberInput input,
        .stDateInput input,
        .stSelectbox div[data-baseweb="select"] {
            border-radius:14px !important;
            border:2px solid rgba(95,208,173,0.22) !important;
            background:rgba(255,255,255,0.85) !important;
            color:#2f3038 !important;
            padding:10px !important;
        }
        .stTextInput input:focus,
        .stPasswordInput input:focus,
        .stNumberInput input:focus,
        .stDateInput input:focus {
            border-color:#5fd0ad !important;
            box-shadow:0 0 0 3px rgba(95,208,173,0.16) !important;
        }

        .stButton > button {
            border-radius:16px !important;
            border:1px solid rgba(95,208,173,0.26) !important;
            background:#d9f2e8 !important;
            color:var(--text-dark) !important;
            font-weight:800 !important;
            box-shadow:0 8px 20px rgba(31,122,99,0.08) !important;
            transition:all 0.2s ease !important;
        }
        .stButton > button:hover {
            transform:translateY(-2px) !important;
            border:1px solid rgba(95,208,173,0.48) !important;
            box-shadow:0 14px 28px rgba(31,122,99,0.13) !important;
            background:#e8fff5 !important;
            color:var(--text-dark) !important;
        }

        button[data-baseweb="tab"] {
            font-size:16px;
            font-weight:700;
            color:#52796f;
            padding:12px 18px;
            border-radius:999px;
            margin-right:8px;
            transition:all 0.2s ease;
        }
        button[data-baseweb="tab"]:hover {
            background:rgba(95,208,173,0.12);
            color:var(--text-dark);
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            background: var(--mint-strong);
            color:white;
        }
        div[data-baseweb="tab-highlight"] {
            display:none;
        }
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
    def _login(self):
        """Renders the login form and handles authentication status messages."""
        self.authenticator.login(fields={
            'Form name': 'Login',
            'Username': 'Benutzername',
            'Password': 'Passwort',
            'Login': 'Anmelden',
            'Captcha': 'Captcha'
        })
        if st.session_state["authentication_status"] is False:
            st.error("Benutzername oder Passwort ist falsch")
        else:
            st.warning("Bitte gib deinen Benutzernamen und dein Passwort ein")

    def _register(self):
        """
        Renders the registration form and handles user registration flow.

        Displays password requirements, processes registration attempts,
        and saves credentials on successful registration.
        """
        st.info("""
        Das Passwort muss 8-20 Zeichen lang sein und mindestens einen Großbuchstaben,
        einen Kleinbuchstaben, eine Zahl und ein Sonderzeichen aus @$!%*?& enthalten.
        """)
        res = self.authenticator.register_user(fields={
            'Form name': 'Registrieren',
            'First name': 'Vorname',
            'Last name': 'Nachname',
            'Email': 'E-Mail',
            'Username': 'Benutzername',
            'Password': 'Passwort',
            'Repeat password': 'Passwort wiederholen',
            'Password hint': 'Passworthinweis',
            'Captcha': 'Captcha',
            'Register': 'Registrieren',
            'Dialog name': 'Verifizierungscode',
            'Code': 'Code',
            'Submit': 'Senden',
            'Error': 'Code ist falsch'
        })
        if res[1] is not None:
            st.success(f"Benutzer {res[1]} erfolgreich registriert")
            try:
                self._save_auth_credentials()
                st.success("Anmeldedaten erfolgreich gespeichert")
            except Exception as e:
                st.error(f"Speichern der Anmeldedaten fehlgeschlagen: {e}")
