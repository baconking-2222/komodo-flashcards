"""Random card picker — for live demo moments during training."""

from __future__ import annotations

import random

import streamlit as st

from activities import filter_activities, get_activity
from branding import (
    AGE_DISPLAY_TO_CODE,
    AGE_FILTER_OPTIONS,
    page_subtitle,
    page_title,
    render_present_card,
    set_brand,
)

set_brand("Random picker")
page_title("🎲 Random picker")
page_subtitle(
    "Draw a random card from the deck — useful for live demos with teachers, "
    "or as a wellbeing 'card of the day' ritual."
)

with st.sidebar:
    st.markdown("### 🔎 Narrow the pool")
    age_display = st.multiselect(
        "Age group",
        options=AGE_FILTER_OPTIONS,
        default=[],
    )
    age_filter = [AGE_DISPLAY_TO_CODE[a] for a in age_display]

pool = filter_activities(
    ages=age_filter if age_filter else None,
    props_filter="Any",
)

if not pool:
    st.info("No activities match those filters. Loosen the filters in the sidebar.")
    st.stop()


drawn_id = st.session_state.get("drawn_card")

# --- Hero draw area ---
if not drawn_id:
    st.markdown(
        "<div class='draw-hero'>"
        "<div class='deck-emoji'>🎴</div>"
        f"<h2>Drawing from {len(pool)} activities</h2>"
        f"<p style='margin:0 0 6px; color:#2a4458;'>Click below to pick one at random.</p>"
        "</div>",
        unsafe_allow_html=True,
    )
    centre = st.columns([2, 3, 2])
    with centre[1]:
        if st.button("🎲 Draw a card", use_container_width=True):
            st.session_state["drawn_card"] = random.choice(pool).id
            st.rerun()
    st.stop()


# --- Show drawn card ---
activity = get_activity(drawn_id)
if not activity:
    st.session_state.pop("drawn_card", None)
    st.rerun()

# Buttons row above the card.
btn_cols = st.columns([1, 1, 4])
with btn_cols[0]:
    if st.button("🎲 Draw again"):
        choices = [a for a in pool if a.id != drawn_id]
        st.session_state["drawn_card"] = random.choice(choices or pool).id
        st.rerun()
with btn_cols[1]:
    if st.button("↺ Clear"):
        st.session_state.pop("drawn_card", None)
        st.rerun()

render_present_card(activity, header_eyebrow="🎴 You drew this card")
