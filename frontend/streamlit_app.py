import streamlit as st
import sys
from pathlib import Path

# Put the repo root on sys.path so `from frontend.views import ...` resolves
# regardless of the directory streamlit was launched from.
sys.path.insert(0, str(Path(__file__).parent.parent))

# Configure page
st.set_page_config(
    page_title="ResumeLens",
    page_icon="🐒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Auth state. Populated by Supabase sign-in / sign-up / OAuth.
# All four are None when signed out, all four are set when signed in.
for key, default in [
    ("access_token", None),
    ("refresh_token", None),
    ("user_id", None),       # Supabase auth user id (uuid); also used by api_client
    ("user_email", None),
    ("auth_error", None),
    ("auth_info", None),
    ("dark_mode", True),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# If we just came back from Google OAuth, Supabase appends `?code=<authcode>`
# to the redirect URL. Exchange it for a session before rendering anything.
if (
    not st.session_state.access_token
    and "code" in st.query_params
):
    from frontend.services import supabase_client
    result = supabase_client.exchange_code_for_session(st.query_params["code"])

    #Always clear the ?code= param so a refresh doesn't try to re-exchange.
    st.query_params.clear()
    if "error" in result:
        st.session_state.auth_error = f"Google sign-in failed: {result['error']}"
    else:
        st.session_state.access_token  = result["access_token"]
        st.session_state.refresh_token = result["refresh_token"]
        st.session_state.user_id       = result["user_id"]
        st.session_state.user_email    = result["email"]
        st.rerun()

#Load custom CSS
def load_css():
    try:
        css_path = Path(__file__).parent / 'assets' / 'styles.css'
        with open(css_path, 'r') as f:
            return f'<style>{f.read()}</style>'
    except FileNotFoundError:
        return ''

st.markdown(load_css(), unsafe_allow_html=True)


def theme_css() -> str:
    if not st.session_state.dark_mode:
        return """
        <style>
            :root { color-scheme: light; }
        </style>
        """

    return """
    <style>
        :root {
            color-scheme: dark;
            --text-primary: #f8fafc;
            --text-secondary: #cbd5e1;
            --text-muted: #94a3b8;
            --background-light: #111827;
            --background-white: #1f2937;
            --border-color: #374151;
            --border-light: #273244;
            --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.35);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.45);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.55);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.65);
        }

        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stHeader"],
        [data-testid="stToolbar"] {
            background: #0f172a !important;
            color: var(--text-primary) !important;
        }

        [data-testid="stSidebar"],
        [data-testid="stSidebarContent"] {
            background: #111827 !important;
            color: var(--text-primary) !important;
        }

        h1, h2, h3, h4, h5, h6,
        p, label, span, div,
        [data-testid="stMarkdownContainer"] {
            color: inherit;
        }

        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li,
        [data-testid="stMarkdownContainer"] span {
            color: var(--text-secondary);
        }

        [data-testid="stMarkdownContainer"] h1,
        [data-testid="stMarkdownContainer"] h2,
        [data-testid="stMarkdownContainer"] h3,
        [data-testid="stMarkdownContainer"] h4 {
            color: var(--text-primary);
        }

        section[data-testid="stSidebar"] button,
        .stButton > button,
        .stDownloadButton > button,
        [data-testid="stBaseButton-secondary"] {
            background: #1f2937 !important;
            border-color: #374151 !important;
            color: var(--text-primary) !important;
        }

        section[data-testid="stSidebar"] button:hover,
        .stButton > button:hover,
        .stDownloadButton > button:hover {
            border-color: var(--primary-light) !important;
            color: #ffffff !important;
            background: #273244 !important;
        }

        [data-testid="stBaseButton-primary"] {
            background: linear-gradient(135deg, var(--primary-color), var(--primary-dark)) !important;
            border-color: var(--primary-color) !important;
            color: #ffffff !important;
        }

        input, textarea,
        [data-baseweb="input"],
        [data-baseweb="textarea"],
        [data-baseweb="select"] {
            background: #0b1220 !important;
            color: var(--text-primary) !important;
            border-color: #374151 !important;
        }

        [data-baseweb="input"] input,
        [data-baseweb="textarea"] textarea {
            color: var(--text-primary) !important;
            -webkit-text-fill-color: var(--text-primary) !important;
        }

        [data-testid="stFileUploader"],
        [data-testid="stExpander"],
        [data-testid="stMetric"],
        [data-testid="stForm"],
        [data-testid="stVerticalBlockBorderWrapper"] {
            background: #1f2937 !important;
            border-color: #374151 !important;
            color: var(--text-primary) !important;
        }

        /* Expander header bar (Streamlit paints this with the light
           secondaryBackgroundColor by default - force it dark and readable). */
        [data-testid="stExpander"] details,
        [data-testid="stExpander"] summary,
        [data-testid="stExpander"] .streamlit-expanderHeader {
            background: #1f2937 !important;
            color: var(--text-primary) !important;
        }
        [data-testid="stExpander"] summary:hover {
            background: #273244 !important;
            color: #ffffff !important;
        }
        [data-testid="stExpander"] summary p,
        [data-testid="stExpander"] summary span,
        [data-testid="stExpander"] summary div { color: var(--text-primary) !important; }
        [data-testid="stExpander"] summary svg { fill: var(--text-secondary) !important; }

        [data-testid="stAlert"] {
            background: #1e293b !important;
            border-color: #334155 !important;
            color: var(--text-primary) !important;
        }

        hr {
            border-color: #334155 !important;
        }

        code, pre {
            background: #020617 !important;
            color: #e2e8f0 !important;
        }
    </style>
    """


st.markdown(theme_css(), unsafe_allow_html=True)

# Initialize session state for view management
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'landing'

from frontend.services import supabase_client


def set_view(view: str) -> None:
    # No st.rerun() here: current_view is read by the main content block further
    # down in this same script run, so the new view renders in one pass. Calling
    # st.rerun() would abort before the "Dark mode" toggle (rendered later in
    # render_top_bar) is instantiated, and Streamlit would then drop its widget
    # state - which is what made dark mode revert on every navigation click.
    st.session_state.current_view = view


def render_top_bar() -> None:
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {
                display: none;
            }
            [data-testid="stAppViewContainer"] > .main {
                margin-left: 0;
            }
            .block-container {
                padding-top: 1.5rem;
            }
            .top-bar {
                border: 1px solid var(--border-color);
                border-radius: 18px;
                padding: 1rem 1.25rem;
                margin-bottom: 1.5rem;
                background: var(--background-white);
                box-shadow: var(--shadow-sm);
            }
            .top-bar-title {
                font-size: 1.1rem;
                font-weight: 800;
                color: var(--text-primary);
            }
        </style>
        <div class="top-bar">
            <div class="top-bar-title">🐒 ResumeLens</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    title_col, home_col, scorer_col, history_col, resources_col, theme_col, account_col = st.columns(
        [1.4, 0.9, 1.1, 0.9, 1.0, 1.1, 1.5]
    )

    with title_col:
        st.markdown("### Navigation")
    with home_col:
        if st.button("🛖 Home", use_container_width=True):
            set_view("landing")
    with scorer_col:
        if st.button("🐒 ATS Scorer", use_container_width=True):
            set_view("scorer")
    with history_col:
        if st.button("📊 History", use_container_width=True):
            set_view("history")
    with resources_col:
        if st.button("📚 Resources", use_container_width=True):
            set_view("resources")
    with theme_col:
        st.toggle("Dark mode", key="dark_mode")
    with account_col:
        if st.session_state.access_token:
            st.caption(f"Signed in as {st.session_state.user_email}")
            if st.button("Sign out", use_container_width=True):
                supabase_client.sign_out()
                for k in ("access_token", "refresh_token", "user_id", "user_email"):
                    st.session_state[k] = None
                st.rerun()
        else:
            st.caption("Not signed in")


def _auth_styles() -> str:
    return """
    <style>
        /* Attention banner that points users to the sign-in expander */
        .auth-cta {
            display: flex; align-items: center; gap: 0.9rem;
            background: linear-gradient(135deg, rgba(79,70,229,0.14), rgba(147,51,234,0.14));
            border: 1.5px solid #7C3AED;
            border-radius: 14px;
            padding: 0.9rem 1.15rem;
            margin-bottom: 0.55rem;
            box-shadow: 0 4px 16px rgba(124,58,237,0.18);
        }
        .auth-cta-icon { font-size: 1.7rem; line-height: 1; }
        .auth-cta-title { font-weight: 800; font-size: 1.04rem; color: var(--text-primary, #1F2937); }
        .auth-cta-sub { font-size: 0.86rem; color: var(--text-secondary, #6B7280); margin-top: 1px; }

        /* Primary submit buttons: Sign in / Create account */
        [data-testid="stFormSubmitButton"] button {
            background: linear-gradient(135deg, #4F46E5, #7C3AED) !important;
            color: #ffffff !important;
            border: none !important;
            font-weight: 700 !important;
            box-shadow: 0 4px 14px rgba(79,70,229,0.35) !important;
            transition: transform .15s ease, box-shadow .15s ease !important;
        }
        [data-testid="stFormSubmitButton"] button:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 8px 22px rgba(79,70,229,0.45) !important;
        }
        [data-testid="stFormSubmitButton"] button p,
        [data-testid="stFormSubmitButton"] button div { color: #ffffff !important; }

        /* Google sign-in button (same-tab anchor) - readable in light and dark */
        .google-oauth-btn {
            display: block;
            width: 100%;
            text-align: center;
            padding: 0.55rem 1rem;
            border-radius: 8px;
            background: var(--background-white, #ffffff);
            color: var(--text-primary, #1F2937) !important;
            border: 1px solid var(--border-color, #E5E7EB);
            font-weight: 600;
            text-decoration: none !important;
            transition: border-color .15s ease, color .15s ease;
        }
        .google-oauth-btn:hover {
            border-color: #7C3AED;
            color: #7C3AED !important;
        }

        /* Password reveal toggle shouldn't render as a white block */
        [data-baseweb="input"] button {
            background: transparent !important;
            border: none !important;
        }
    </style>
    """


def render_auth_panel() -> None:
    if st.session_state.access_token:
        return

    st.markdown(_auth_styles(), unsafe_allow_html=True)
    st.markdown(
        """
        <div class="auth-cta">
          <span class="auth-cta-icon">🔐</span>
          <div>
            <div class="auth-cta-title">Sign in to analyze your resume</div>
            <div class="auth-cta-sub"></div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Auto-open the panel when there's a message to show, so feedback isn't hidden.
    open_panel = bool(st.session_state.auth_error or st.session_state.auth_info)

    with st.expander("🔐  Account sign in / sign up", expanded=open_panel):
        if st.session_state.auth_error:
            st.error(st.session_state.auth_error)
            st.session_state.auth_error = None
        if st.session_state.auth_info:
            st.info(st.session_state.auth_info)
            st.session_state.auth_info = None

        tab_in, tab_up = st.tabs(["Sign in", "Sign up"])

        with tab_in:
            with st.form("signin_form", clear_on_submit=False):
                email = st.text_input("Email", key="signin_email")
                password = st.text_input("Password", type="password", key="signin_pw")
                submitted = st.form_submit_button("Sign in", use_container_width=True)
            if submitted:
                result = supabase_client.sign_in_with_password(email, password)
                if "error" in result:
                    st.session_state.auth_error = result["error"]
                else:
                    st.session_state.access_token = result["access_token"]
                    st.session_state.refresh_token = result["refresh_token"]
                    st.session_state.user_id = result["user_id"]
                    st.session_state.user_email = result["email"]
                st.rerun()

        with tab_up:
            with st.form("signup_form", clear_on_submit=False):
                email_up = st.text_input("Email", key="signup_email")
                password_up = st.text_input("Password (min 6 chars)", type="password", key="signup_pw")
                submitted_up = st.form_submit_button("Create account", use_container_width=True)
            if submitted_up:
                result = supabase_client.sign_up_with_password(email_up, password_up)
                if "error" in result:
                    st.session_state.auth_error = result["error"]
                elif result.get("pending_confirmation"):
                    st.session_state.auth_info = (
                        f"Check your inbox - confirmation email sent to {result['email']}."
                    )
                else:
                    st.session_state.access_token = result["access_token"]
                    st.session_state.refresh_token = result["refresh_token"]
                    st.session_state.user_id = result["user_id"]
                    st.session_state.user_email = result["email"]
                st.rerun()

        st.markdown(
            """
            <div style="display:flex; align-items:center; gap:0.75rem; margin:0.7rem 0;
                        color:var(--text-muted, #9CA3AF);">
              <div style="flex:1; height:1px; background:var(--border-color, #E5E7EB);"></div>
              <span style="font-size:0.82rem;">or</span>
              <div style="flex:1; height:1px; background:var(--border-color, #E5E7EB);"></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        oauth = supabase_client.google_oauth_url()
        if "error" in oauth:
            st.caption(f"Google sign-in unavailable: {oauth['error']}")
        else:
            # target="_self" keeps OAuth in the SAME tab. st.link_button renders
            # target="_blank", which opened Google in a new window and left two
            # tabs of the app open (one signed in, one signed out).
            st.markdown(
                f'<a href="{oauth["url"]}" target="_self" class="google-oauth-btn">'
                f'Continue with Google</a>',
                unsafe_allow_html=True,
            )


render_top_bar()
render_auth_panel()

# Main content area - render based on current view
if st.session_state.current_view == 'landing':
    # Import and render landing page
    from frontend.views import landing
    landing.render()

elif st.session_state.current_view == 'scorer':
    # Import and render scorer page
    from frontend.views import scorer
    scorer.render()

elif st.session_state.current_view == 'history':
    # Import and render history page
    from frontend.views import history
    history.render()

elif st.session_state.current_view == 'resources':
    # Import and render resources page
    from frontend.views import resources
    resources.render()
