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

    def login_register(self, login_title='Login', register_title='Register new user'):
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
        """Inject CSS to style the login/register page with mint-green accents but without the boxed header."""
        css = """
        <style>
        :root{--mint:#c8f1e0;--mint-strong:#56c49d;--card:#ffffff}
        /* center the main column */
        .stApp .block-container{max-width:760px;margin:28px auto;padding-left:16px;padding-right:16px}
        /* Option A: remove the box around the header */
        .login-header{max-width:760px;margin:6px auto 18px;padding:0;border-radius:0;background:transparent;box-shadow:none;text-align:center}
    .login-title{font-size:16spx;font-weight:700;color:#054033;margin:0}
        .login-sub{color:#0f5132;margin-top:6px}
        /* inputs and buttons */
        input[type='text'], input[type='password'], input[type='number'], textarea{border-radius:8px;border:1px solid #e6f2ec;padding:10px;background:#f7fffb}
        button, .stButton>button{background:var(--mint-strong)!important;color:#ffffff!important;border-radius:8px!important;padding:8px 14px!important;border:none!important;box-shadow:0 6px 18px rgba(86,196,157,0.16)!important}
        /* subtle card for tabs content */
        .stTabs [role='tablist']{margin-bottom:6px}
        .stContainer{background:#ffffff;border-radius:10px;padding:12px}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
    def _login(self):
        """Renders the login form and handles authentication status messages."""
        self.authenticator.login()
        if st.session_state["authentication_status"] is False:
            st.error("Username/password is incorrect")
        else:
            st.warning("Please enter your username and password")

    def _register(self):
        """
        Renders the registration form and handles user registration flow.

        Displays password requirements, processes registration attempts,
        and saves credentials on successful registration.
        """
        st.info("""
        The password must be 8-20 characters long and include at least one uppercase letter,
        one lowercase letter, one digit, and one special character from @$!%*?&.
        """)
        res = self.authenticator.register_user()
        if res[1] is not None:
            st.success(f"User {res[1]} registered successfully")
            try:
                self._save_auth_credentials()
                st.success("Credentials saved successfully")
            except Exception as e:
                st.error(f"Failed to save credentials: {e}")
