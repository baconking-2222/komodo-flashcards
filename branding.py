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


def set_brand(page_title: str) -> None:
    """Call once at the top of every page. Sets config, logo, CSS, and the
    branded sidebar nav. Hides Streamlit's default multipage nav."""
    st.set_page_config(
        page_title=f"{page_title} • Komodo Wellbeing",
        page_icon=str(ICON_PATH) if ICON_PATH.exists() else "🌿",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Streamlit's brand logo helper — handles sidebar + collapsed-navbar placement.
    if LOGO_PATH.exists():
        try:
            st.logo(
                str(LOGO_PATH),
                icon_image=str(ICON_PATH) if ICON_PATH.exists() else None,
                size="large",
                link=None,
            )
        except TypeError:
            # Older Streamlit signature
            st.logo(str(LOGO_PATH))

    # Use st.html for raw CSS — st.markdown double-renders <style> content as text.
    try:
        st.html(_GLOBAL_CSS)
    except AttributeError:
        # Fallback for older Streamlit
        st.markdown(_GLOBAL_CSS, unsafe_allow_html=True)
    _render_sidebar_nav()


def _render_sidebar_nav() -> None:
    """Custom branded nav at the top of the sidebar (replaces default page list)."""
    with st.sidebar:
        st.markdown(
            "<div class='kb-nav-label'>Navigate</div>",
            unsafe_allow_html=True,
        )
        # st.page_link accepts the path to the page file.
        st.page_link("Browse_all.py", label="Browse all activities", icon="🔍")
        st.page_link("pages/1_Themed_Sets.py", label="Themed sets", icon="🎨")
        st.page_link("pages/2_Random_Picker.py", label="Random picker", icon="🎲")
        st.page_link("pages/3_Training_Guide.py", label="Training guide", icon="📘")
        st.markdown("<div class='kb-nav-divider'></div>", unsafe_allow_html=True)


def page_title(text: str) -> None:
    """Big page title (no inline logo — st.logo handles that)."""
    st.markdown(
        f"<h1 style='margin: 6px 0 4px;'>{html.escape(text)}</h1>",
        unsafe_allow_html=True,
    )


def page_subtitle(text: str) -> None:
    st.markdown(
        f"<p style='color:#2a4458; margin: 0 0 14px; font-size:1.02rem;'>{html.escape(text)}</p>"
        "<hr style='border:none; border-top:2px solid #55b5f2; margin: 6px 0 18px;'>",
        unsafe_allow_html=True,
    )


def pills_html(activity: Activity, *, include_purposes: bool = True) -> str:
    """Pills shown on every card. NO body-only / props pill (per design)."""
    parts = [
        f"<span class='pill age-{activity.age}'>{activity.age}</span>",
        f"<span class='pill duration'>⏱ {activity.duration_minutes} min</span>",
    ]
    if include_purposes:
        for p in activity.purposes:
            parts.append(f"<span class='pill purpose'>{html.escape(p)}</span>")
    return " ".join(parts)


def _card_body_html(activity: Activity) -> str:
    """The content of a browse card — emoji, title, pills, objective, instructions
    preview. Designed to be placed inside an `st.container(border=True)`."""
    return (
        "<div class='kb-card-body'>"
        "<div class='kb-card-head'>"
        f"<div class='kb-card-emoji'>{activity.emoji}</div>"
        "<div class='kb-card-headtext'>"
        f"<h3>{html.escape(activity.name)}</h3>"
        f"<div class='pills-row'>{pills_html(activity)}</div>"
        "</div>"
        "</div>"
        f"<div class='kb-card-objective'><strong>Objective:</strong> {html.escape(activity.objective)}</div>"
        f"<div class='kb-card-instructions'><strong>📋 Instructions:</strong> {html.escape(activity.instructions)}</div>"
        "</div>"
    )


def render_browse_card(activity: Activity, *, on_open_key: str) -> bool:
    """Render a card with an Open button INSIDE (top-right). Returns True if clicked."""
    clicked = False
    with st.container(border=True):
        cols = st.columns([4, 1.4], vertical_alignment="top")
        with cols[0]:
            st.markdown(_card_body_html(activity), unsafe_allow_html=True)
        with cols[1]:
            st.markdown("<div class='kb-open-spacer'></div>", unsafe_allow_html=True)
            if st.button("Open ▶", key=on_open_key, use_container_width=True):
                clicked = True
    return clicked


def render_themed_card(themed, *, on_open_key: str) -> bool:
    """Themed-set card with Open button top-right (Komodo green)."""
    clicked = False
    with st.container(border=True):
        cols = st.columns([4, 1.4], vertical_alignment="top")
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
                f"<div class='kb-card-objective'>{html.escape(themed.description)}</div>"
                f"<div class='kb-card-when'><strong>When to use:</strong> {html.escape(themed.when_to_use)}</div>"
                "</div>",
                unsafe_allow_html=True,
            )
        with cols[1]:
            st.markdown("<div class='kb-open-spacer'></div>", unsafe_allow_html=True)
            if st.button("Open ▶", key=on_open_key, use_container_width=True):
                clicked = True
    return clicked


def render_present_card(activity: Activity, header_eyebrow: str = "") -> None:
    """Big presentation card + the interactive widget below."""
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
        f"<div class='pills-row'>{pills_html(activity)}</div>"
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
      radial-gradient(circle at 10% 15%, rgba(165,218,255,0.4) 0%, transparent 28%),
      radial-gradient(circle at 90% 85%, rgba(119,238,214,0.3) 0%, transparent 28%),
      var(--pale-blue);
  }
  h1, h2, h3, h4, h5 {
    color: var(--black-blue);
    font-family: 'Epilogue', sans-serif !important;
    font-weight: 700;
  }

  /* ---- HIDE Streamlit's default multipage nav (we render our own) ---- */
  [data-testid="stSidebarNav"] { display: none !important; }

  /* ---- Sidebar styling ---- */
  section[data-testid="stSidebar"] {
    background: var(--white);
    border-right: 2px solid var(--black-blue);
  }
  /* Make st.logo render the wordmark larger and crisp */
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
  /* Sidebar header should give the logo room to breathe */
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
  /* Branded sidebar nav links (st.page_link) */
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

  /* ---- Primary buttons (global) ---- */
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

  /* ---- Cards: st.container(border=True) styled as Komodo brand cards ---- */
  [data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--white);
    border: 2px solid var(--black-blue) !important;
    border-radius: 14px !important;
    padding: 14px 18px !important;
    box-shadow: 0 2px 8px rgba(0,31,52,0.08);
    height: 100%;
    margin-bottom: 14px;
  }
  /* Make columns stretch their bordered children to equal height for uniform cards */
  [data-testid="stHorizontalBlock"] {
    align-items: stretch;
  }
  [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
    display: flex;
    flex-direction: column;
  }
  [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] > [data-testid="stVerticalBlock"] {
    flex: 1;
  }
  /* Open buttons inside bordered cards = Komodo green pill, compact */
  [data-testid="stVerticalBlockBorderWrapper"] .stButton > button {
    background: var(--light-green);
    color: var(--black-blue) !important;
    border: 2.5px solid var(--black-blue);
    border-radius: 30px;
    padding: 6px 8px;
    font-size: 0.82rem;
    font-weight: 700;
    white-space: nowrap;
    min-width: 0;
  }
  [data-testid="stVerticalBlockBorderWrapper"] .stButton > button:hover {
    background: var(--pastel-green);
  }
  /* Card body */
  .kb-card-body { padding: 0; }
  .kb-card-head { display: flex; align-items: flex-start; gap: 14px; margin-bottom: 6px; }
  .kb-card-emoji { font-size: 2.4rem; line-height: 1; flex-shrink: 0; padding-top: 2px; }
  .kb-card-headtext { flex: 1; min-width: 0; }
  .kb-card-headtext h3 { margin: 0 0 6px; font-size: 1.2rem; }
  .kb-card-objective {
    color: #2a4458;
    font-size: 0.9rem;
    line-height: 1.45;
    margin: 8px 0 10px;
  }
  .kb-card-instructions {
    background: var(--pale-blue);
    border-left: 4px solid var(--komodo-blue);
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 0.93rem;
    line-height: 1.5;
  }
  .kb-card-when {
    margin-top: 8px;
    color: #2a4458;
    font-size: 0.88rem;
    font-style: italic;
  }
  .kb-open-spacer { height: 4px; }

  /* ---- Pills ---- */
  .pill {
    display: inline-block;
    padding: 3px 11px;
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

  /* ---- Presentation card ---- */
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

  /* ---- Random picker hero ---- */
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

  /* Hide Streamlit footer */
  footer { visibility: hidden; }
</style>
"""
