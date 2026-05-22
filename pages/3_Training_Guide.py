"""Training guide — a punchy TL;DR for trainers."""

from __future__ import annotations

import streamlit as st

from activities import ACTIVITIES
from branding import page_subtitle, page_title, set_brand
from themed_sets import THEMED_SETS

set_brand("Training guide")
page_title("📘 Training guide")
page_subtitle("The 60-second cheat sheet for running this with school staff.")


def _card(emoji: str, title: str, body_html: str) -> None:
    with st.container(border=True):
        st.markdown(
            f"<div style='display:flex; gap:14px; align-items:flex-start;'>"
            f"<div style='font-size:2rem; line-height:1;'>{emoji}</div>"
            f"<div style='flex:1;'>"
            f"<h3 style='margin:0 0 6px;'>{title}</h3>"
            f"<div style='font-size:0.96rem; line-height:1.55;'>{body_html}</div>"
            f"</div></div>",
            unsafe_allow_html=True,
        )


# --- TL;DR row of 3 ---
top = st.columns(3, gap="medium")
with top[0]:
    _card("⚡", "Pick a card", "Filter by age, purpose, or search. Click <strong>Open</strong> on any card.")
with top[1]:
    _card("📺", "Project it", "The card scales for a projector. Big text, big timer.")
with top[2]:
    _card("🤝", "Lead it live", "Run the activity with the room. The widget paces it for you.")

st.write("")

# --- Three ways to structure a session ---
st.markdown("### Three ways to run a session")
ways = st.columns(3, gap="medium")
with ways[0]:
    _card(
        "🎨",
        "By scenario",
        "Open <strong>Themed sets</strong> and walk through one playlist end-to-end "
        "(e.g. <em>Anxiety response</em>).",
    )
with ways[1]:
    _card(
        "👧",
        "By age group",
        "On <strong>Browse all</strong>, filter to <strong>Jr</strong> or <strong>Sr</strong> "
        "to match your audience.",
    )
with ways[2]:
    _card(
        "🎲",
        "By chance",
        "Use the <strong>Random picker</strong>. Get a participant to lead it. "
        "Great as a closing energiser.",
    )

st.write("")

# --- Themed set chips ---
st.markdown("### Themed sets at a glance")
set_cols = st.columns(4, gap="small")
for i, s in enumerate(THEMED_SETS):
    with set_cols[i % 4]:
        st.markdown(
            "<div style='background:#ffffff; border:2px solid #001f34; border-radius:12px; "
            "padding:12px; margin-bottom:10px; text-align:center; min-height:120px;'>"
            f"<div style='font-size:1.8rem; line-height:1;'>{s.icon}</div>"
            f"<div style='font-weight:700; color:#064471; margin:6px 0 4px;'>{s.name}</div>"
            f"<div style='color:#2a4458; font-size:0.8rem;'>{len(s.activity_ids)} cards</div>"
            "</div>",
            unsafe_allow_html=True,
        )

st.write("")

# --- 4 quick tips ---
st.markdown("### Pro tips")
tips = st.columns(2, gap="medium")
with tips[0]:
    _card("🪞", "Try it yourself first",
          "If you've done it once, you can lead it. Most cards are 2–5 minutes.")
    _card("⏱️", "Trust the widget",
          "The breath circle paces breathing. The timer counts down. Stay present with the room.")
with tips[1]:
    _card("🌡️", "Match the moment",
          "Jittery room → <em>Energy release</em>. Flat room → <em>Gratitude & connection</em>.")
    _card("🧑‍⚕️", "Source",
          "Activities written by Komodo's in-house Child & Family Psychologist.")

st.caption(f"Deck: {len(ACTIVITIES)} activities · {len(THEMED_SETS)} themed sets.")
