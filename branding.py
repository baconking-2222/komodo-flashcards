"""Komodo brand styling + shared layout helpers."""

from __future__ import annotations

import html
from pathlib import Path

import streamlit as st

from activities import Activity
import widgets

ASSETS_DIR = Path(__file__).parent / "assets"
LOGO_PATH = ASSETS_DIR / "logo-primary.png"
ICON_PATH = ASSETS_DIR / "icon-blue.png"


COLOURS = {
    "pale_blue": "#ebf9ff",
    "pastel_blue": "#a5daff",
    "komodo_blue": "#55b5f2",
    "vibrant_blue": "#3d92e6",
    "komodo_navy": "#064471",
    "light_green": "#77eed6",
    "pastel_green": "#d2ffe6",
    "white": "#ffffff",
    "black_blue": "#001f34",
}


# Display labels for age tabs.
AGE_LABELS = {
    "Jr": "Primary",
    "Sr": "Secondary",
    "All": "All ages",
}
# Filter options shown to users → internal codes.
AGE_FILTER_OPTIONS = ["All ages", "Primary", "Secondary"]
AGE_DISPLAY_TO_CODE = {
    "All ages": "All",
    "Primary": "Jr",
    "Secondary": "Sr",
}


def set_brand(page_title: str) -> None:
    """Call once at the top of every page."""
    st.set_page_config(
        page_title=f"{page_title} • Komodo Wellbeing",
        page_icon=str(ICON_PATH) if ICON_PATH.exists() else "🌿",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    if LOGO_PATH.exists():
        try:
            st.logo(
                str(LOGO_PATH),
                icon_image=str(ICON_PATH) if ICON_PATH.exists() else None,
                size="large",
                link=None,
            )
        except TypeError:
            st.logo(str(LOGO_PATH))

    try:
        st.html(_GLOBAL_CSS)
    except AttributeError:
        st.markdown(_GLOBAL_CSS, unsafe_allow_html=True)
    _render_sidebar_nav()


def _render_sidebar_nav() -> None:
    """Custom branded nav at the top of the sidebar."""
    with st.sidebar:
        st.markdown("<div class='kb-nav-label'>Navigate</div>", unsafe_allow_html=True)
        st.page_link("Browse_all.py", label="Browse all activities", icon="🔍")
        st.page_link("pages/1_Themed_Sets.py", label="Themed sets", icon="🎨")
        st.page_link("pages/2_Random_Picker.py", label="Random picker", icon="🎲")
        st.markdown("<div class='kb-nav-divider'></div>", unsafe_allow_html=True)


def scroll_to_top() -> None:
    """Inject JS to scroll the Streamlit main area to the top. Call once at the
    top of a page (e.g. when entering presentation mode) to avoid landing the
    user halfway down the page after a rerun."""
    import streamlit.components.v1 as components

    components.html(
        """
        <script>
            (function() {
                let tries = 0;
                const tick = setInterval(function() {
                    try {
                        const doc = window.parent.document;
                        const targets = [
                            doc.querySelector('[data-testid="stMain"]'),
                            doc.querySelector('section.main'),
                            doc.scrollingElement,
                        ].filter(Boolean);
                        targets.forEach(t => t.scrollTo({top: 0, behavior: 'instant'}));
                        clearInterval(tick);
                    } catch (e) { /* sandbox: ignore */ }
                    if (++tries > 8) clearInterval(tick);
                }, 60);
            })();
        </script>
        """,
        height=0,
    )


def page_title(text: str) -> None:
    st.markdown(f"<h1 style='margin: 6px 0 4px;'>{html.escape(text)}</h1>", unsafe_allow_html=True)


def page_subtitle(text: str) -> None:
    st.markdown(
        f"<p style='color:#2a4458; margin: 0 0 14px; font-size:1.02rem;'>{html.escape(text)}</p>"
        "<hr style='border:none; border-top:2px solid #55b5f2; margin: 6px 0 18px;'>",
        unsafe_allow_html=True,
    )


def _age_pill(activity: Activity) -> str:
    label = AGE_LABELS.get(activity.age, activity.age)
    return f"<span class='pill age-{activity.age}'>{label}</span>"


def pills_html(activity: Activity, *, primary_only: bool = True) -> str:
    """Pills row. By default: age + duration + ONE primary purpose."""
    parts = [
        _age_pill(activity),
        f"<span class='pill duration'>⏱ {activity.duration_minutes} min</span>",
    ]
    if primary_only:
        if activity.purposes:
            parts.append(f"<span class='pill purpose'>{html.escape(activity.purposes[0])}</span>")
    else:
        for p in activity.purposes:
            parts.append(f"<span class='pill purpose'>{html.escape(p)}</span>")
    return " ".join(parts)


def _short_objective(text: str, *, max_sentences: int = 2, max_chars: int = 260) -> str:
    """Trim objective to a fixed number of sentences for uniform card sizing."""
    if not text:
        return ""
    # Split on ". " to preserve sentences; ignore empty fragments.
    parts = [p.strip() for p in text.split(". ") if p.strip()]
    chosen = parts[:max_sentences]
    result = ". ".join(p.rstrip(".") for p in chosen) + "."
    if len(result) > max_chars:
        result = result[: max_chars - 1].rstrip(", ;") + "…"
    return result


def _card_body_html(activity: Activity) -> str:
    """Compact browse card body — emoji, title, ONE wellbeing tag, short objective.
    No instructions preview (users open the card to see them)."""
    return (
        "<div class='kb-card-body'>"
        "<div class='kb-card-head'>"
        f"<div class='kb-card-emoji'>{activity.emoji}</div>"
        "<div class='kb-card-headtext'>"
        f"<h3>{html.escape(activity.name)}</h3>"
        f"<div class='pills-row'>{pills_html(activity, primary_only=True)}</div>"
        "</div>"
        "</div>"
        f"<div class='kb-card-objective'>{html.escape(_short_objective(activity.objective))}</div>"
        "</div>"
    )


def render_browse_card(activity: Activity, *, on_open_key: str) -> bool:
    """Compact card with title/objective on the left and a small Open pill top-right.
    Returns True if the Open button was clicked.

    Uses keyed Streamlit elements so CSS can reliably target them across
    Streamlit versions (the default stVerticalBlock DOM has no distinguishing
    testid for bordered containers).
    """
    clicked = False
    with st.container(key=f"kbcard_{activity.id}"):
        cols = st.columns([7, 1.2], vertical_alignment="top")
        with cols[0]:
            st.markdown(_card_body_html(activity), unsafe_allow_html=True)
        with cols[1]:
            if st.button("Open", key=f"kbopen_{activity.id}"):
                clicked = True
    return clicked


def render_themed_card(themed, *, on_open_key: str) -> bool:
    """Themed-set card — same compact treatment."""
    clicked = False
    with st.container(key=f"kbcard_set_{themed.id}"):
        cols = st.columns([7, 1.2], vertical_alignment="top")
        with cols[0]:
            st.markdown(
                "<div class='kb-card-body'>"
                "<div class='kb-card-head'>"
                f"<div class='kb-card-emoji'>{themed.icon}</div>"
                "<div class='kb-card-headtext'>"
                f"<h3>{html.escape(themed.name)}</h3>"
                f"<div style='color:#064471; font-weight:700; font-size:0.85rem; margin-top:2px;'>"
                f"{len(themed.activity_ids)} cards"
                "</div>"
                "</div>"
                "</div>"
                f"<div class='kb-card-objective'>{html.escape(_short_objective(themed.description, max_chars=160))}</div>"
                f"<div class='kb-card-when'>📅 {html.escape(themed.when_to_use)}</div>"
                "</div>",
                unsafe_allow_html=True,
            )
        with cols[1]:
            if st.button("Open", key=f"kbopen_set_{themed.id}"):
                clicked = True
    return clicked


def render_present_card(activity: Activity, header_eyebrow: str = "") -> None:
    """Big presentation card + interactive widget below."""
    eyebrow_html = ""
    if header_eyebrow:
        eyebrow_html = f"<div class='eyebrow'>{html.escape(header_eyebrow)}</div>"
    props_block = ""
    if activity.props_needed:
        props_block = (
            "<div class='props-block'>"
            f"<span class='props-icon'>🧰</span> "
            f"<strong>You'll need:</strong> {html.escape(activity.props_description)}"
            "</div>"
        )

    st.markdown(
        "<div class='present-card'>"
        f"{eyebrow_html}"
        "<div class='present-head'>"
        f"<div class='present-emoji'>{activity.emoji}</div>"
        "<div class='present-text'>"
        f"<h1>{html.escape(activity.name)}</h1>"
        # Show full pill set on the presentation page (still useful context).
        f"<div class='pills-row'>{pills_html(activity, primary_only=False)}</div>"
        "</div>"
        "</div>"
        f"<div class='objective'><strong>Objective:</strong> {html.escape(activity.objective)}</div>"
        f"{props_block}"
        "<div class='instructions-block'>"
        "<div class='instructions-label'>📋 Instructions</div>"
        f"<div class='instructions-body'>{html.escape(activity.instructions)}</div>"
        "</div>"
        "</div>",
        unsafe_allow_html=True,
    )

    widgets.render(activity)


_GLOBAL_CSS = """
<link href="https://fonts.googleapis.com/css2?family=Epilogue:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  :root {
    --pale-blue: #ebf9ff;
    --pastel-blue: #a5daff;
    --komodo-blue: #55b5f2;
    --vibrant-blue: #3d92e6;
    --komodo-navy: #064471;
    --light-green: #77eed6;
    --pastel-green: #d2ffe6;
    --white: #ffffff;
    --black-blue: #001f34;
  }
  html, body, [class*="css"], .stApp {
    font-family: 'Epilogue', 'Inter', 'Open Sans', sans-serif !important;
    color: var(--black-blue);
  }
  .stApp {
    background:
      radial-gradient(circle at 10% 15%, rgba(165,218,255,0.35) 0%, transparent 28%),
      radial-gradient(circle at 90% 85%, rgba(119,238,214,0.22) 0%, transparent 28%),
      var(--pale-blue);
  }
  h1, h2, h3, h4, h5 {
    color: var(--black-blue);
    font-family: 'Epilogue', sans-serif !important;
    font-weight: 700;
  }

  /* Hide Streamlit's default multipage nav */
  [data-testid="stSidebarNav"] { display: none !important; }

  /* Sidebar */
  section[data-testid="stSidebar"] {
    background: var(--white);
    border-right: 2px solid var(--black-blue);
  }
  img[data-testid="stSidebarLogo"],
  img[data-testid="stLogo"],
  [data-testid="stSidebarHeader"] img,
  [data-testid="stHeader"] img[alt="Logo"] {
    max-height: 64px !important;
    height: 64px !important;
    width: auto !important;
    object-fit: contain !important;
    image-rendering: -webkit-optimize-contrast;
    image-rendering: crisp-edges;
  }
  [data-testid="stSidebarHeader"] {
    padding: 16px 14px 8px !important;
  }
  .kb-nav-label {
    color: var(--komodo-navy);
    font-weight: 700;
    font-size: 0.78rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin: 8px 4px 8px;
  }
  section[data-testid="stSidebar"] [data-testid="stPageLink"] a,
  section[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"] {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 14px !important;
    margin: 4px 0;
    background: var(--pale-blue);
    border: 2px solid var(--black-blue);
    border-radius: 12px;
    font-weight: 700;
    color: var(--komodo-navy) !important;
    text-decoration: none !important;
    transition: background 0.15s ease, transform 0.1s ease;
  }
  section[data-testid="stSidebar"] [data-testid="stPageLink"] a:hover,
  section[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"]:hover {
    background: var(--light-green);
    transform: translateX(2px);
  }
  .kb-nav-divider {
    height: 2px;
    background: var(--pastel-blue);
    border-radius: 1px;
    margin: 14px 0 10px;
  }

  /* Primary buttons */
  .stButton > button {
    background: var(--vibrant-blue);
    color: var(--white) !important;
    border: 3px solid var(--black-blue);
    border-radius: 30px;
    font-weight: 700;
    font-family: 'Epilogue', sans-serif !important;
    padding: 8px 22px;
    transition: background 0.15s ease;
  }
  .stButton > button:hover {
    background: var(--light-green);
    color: var(--black-blue) !important;
    border-color: var(--black-blue);
  }

  /* ----- BROWSE / THEMED CARDS -----
     Each card wraps in a Streamlit container with a stable key ("kbcard_*"),
     which becomes a CSS class "st-key-kbcard_*" on the stElementContainer.
     We style that wrapper to look like a Komodo brand card. */
  [class*="st-key-kbcard_"] {
    background: #ffffff !important;
    border: 2px solid var(--black-blue) !important;
    border-radius: 16px !important;
    padding: 22px 24px !important;
    box-shadow: 0 4px 14px rgba(0,31,52,0.10) !important;
    min-height: 240px;
    height: 100%;
    margin-bottom: 14px;
    display: flex;
    flex-direction: column;
  }
  /* Make the inner block fill the card so content is evenly distributed */
  [class*="st-key-kbcard_"] > [data-testid="stVerticalBlock"] {
    flex: 1;
  }
  /* Stretch sibling cards in a row to match heights */
  [data-testid="stHorizontalBlock"] { align-items: stretch; }
  [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
    display: flex; flex-direction: column;
  }
  [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] > [data-testid="stVerticalBlock"] {
    flex: 1;
  }
  /* Compact Open pill inside cards, aligned to top-right of its column */
  [class*="st-key-kbopen_"] {
    text-align: right;
  }
  [class*="st-key-kbopen_"] button {
    background: var(--light-green) !important;
    color: var(--black-blue) !important;
    border: 2px solid var(--black-blue) !important;
    border-radius: 999px !important;
    padding: 3px 14px !important;
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    white-space: nowrap !important;
    min-width: 0 !important;
    min-height: 0 !important;
    line-height: 1.4 !important;
    box-shadow: none !important;
    width: auto !important;
  }
  [class*="st-key-kbopen_"] button:hover {
    background: var(--pastel-green) !important;
  }
  /* Card body */
  .kb-card-body { padding: 0; }
  .kb-card-head { display: flex; align-items: flex-start; gap: 12px; margin-bottom: 6px; }
  .kb-card-emoji { font-size: 2.2rem; line-height: 1; flex-shrink: 0; padding-top: 2px; }
  .kb-card-headtext { flex: 1; min-width: 0; }
  .kb-card-headtext h3 { margin: 0 0 6px; font-size: 1.15rem; line-height: 1.2; }
  .kb-card-objective {
    color: #2a4458;
    font-size: 0.92rem;
    line-height: 1.45;
    margin: 8px 0 4px;
  }
  .kb-card-when {
    margin-top: 6px;
    color: #2a4458;
    font-size: 0.85rem;
    font-style: italic;
  }

  /* ----- PILLS ----- */
  .pill {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 999px;
    font-weight: 700;
    font-size: 0.74rem;
    margin-right: 4px;
    margin-bottom: 4px;
    border: 2px solid var(--black-blue);
    color: var(--black-blue);
    line-height: 1.4;
  }
  .pill.age-Jr   { background: #77eed6; }
  .pill.age-Sr   { background: #a5daff; }
  .pill.age-All  { background: #55b5f2; color: #ffffff; }
  .pill.purpose  { background: var(--white); }
  .pill.duration { background: var(--pastel-blue); }

  /* ----- PRESENTATION CARD ----- */
  .present-card {
    background: var(--white);
    border: 3px solid var(--black-blue);
    border-radius: 20px;
    padding: 28px 36px 24px;
    margin: 12px 0 18px;
    box-shadow: 0 4px 16px rgba(0,31,52,0.12);
    position: relative;
    overflow: hidden;
  }
  .present-card::before {
    content: '';
    position: absolute; top: -40px; right: -40px;
    width: 160px; height: 160px; border-radius: 50%;
    background: var(--pastel-blue); opacity: 0.4; z-index: 0;
  }
  .present-card::after {
    content: '';
    position: absolute; bottom: -50px; left: -50px;
    width: 180px; height: 180px; border-radius: 50%;
    background: var(--light-green); opacity: 0.25; z-index: 0;
  }
  .present-card > * { position: relative; z-index: 1; }
  .present-card .eyebrow {
    color: var(--komodo-navy);
    font-weight: 700;
    font-size: 0.85rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 4px;
  }
  .present-card .present-head { display:flex; align-items:center; gap: 22px; margin-bottom: 12px; }
  .present-card .present-emoji {
    font-size: 5rem;
    line-height: 1;
    flex-shrink: 0;
    filter: drop-shadow(0 2px 6px rgba(0,31,52,0.15));
  }
  .present-card h1 {
    color: var(--komodo-navy);
    font-size: 2.4rem;
    margin: 0 0 8px;
    line-height: 1.1;
  }
  .present-card .objective {
    font-size: 1rem;
    color: #2a4458;
    margin: 14px 0 10px;
    padding: 12px 16px;
    background: var(--pale-blue);
    border-left: 4px solid var(--komodo-blue);
    border-radius: 6px;
    line-height: 1.5;
  }
  .present-card .props-block {
    margin: 10px 0;
    padding: 10px 14px;
    background: var(--pastel-green);
    border-radius: 10px;
    border: 2px solid var(--black-blue);
    font-size: 0.95rem;
  }
  .present-card .instructions-block {
    margin-top: 14px;
    padding: 14px 18px;
    background: var(--white);
    border: 2px dashed var(--komodo-blue);
    border-radius: 10px;
  }
  .present-card .instructions-label {
    font-weight: 700; color: var(--komodo-navy);
    font-size: 0.92rem; margin-bottom: 6px;
    letter-spacing: 0.04em;
  }
  .present-card .instructions-body {
    font-size: 1.08rem;
    line-height: 1.55;
    white-space: pre-line;
  }

  /* ----- RANDOM PICKER HERO ----- */
  .draw-hero {
    text-align: center;
    padding: 30px 20px;
    background: var(--white);
    border: 3px solid var(--black-blue);
    border-radius: 20px;
    margin: 20px 0 24px;
    box-shadow: 0 4px 16px rgba(0,31,52,0.10);
  }
  .draw-hero .deck-emoji {
    font-size: 5rem;
    margin-bottom: 8px;
    line-height: 1;
  }
  .draw-hero h2 { margin: 4px 0 16px; color: var(--komodo-navy); }

  footer { visibility: hidden; }
</style>
"""
