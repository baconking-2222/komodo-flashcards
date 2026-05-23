"""Komodo Wellbeing Flash Cards — Browse all activities.

Entry point. Run locally:  streamlit run Browse_all.py
"""

from __future__ import annotations

import streamlit as st

from activities import ACTIVITIES, ALL_PURPOSES, filter_activities, get_activity
from branding import (
    AGE_DISPLAY_TO_CODE,
    AGE_FILTER_OPTIONS,
    page_subtitle,
    page_title,
    render_browse_card,
    render_present_card,
    set_brand,
)

set_brand("Browse activities")

# ---------- Presentation mode ----------
selected_id: str | None = st.session_state.get("selected_activity")

if selected_id:
    activity = get_activity(selected_id)
    if activity is None:
        st.session_state.pop("selected_activity", None)
        st.rerun()

    back_col, _ = st.columns([1, 5])
    with back_col:
        if st.button("← Back to deck"):
            st.session_state.pop("selected_activity", None)
            st.rerun()

    render_present_card(activity)
    st.stop()


# ---------- Browse mode (grid) ----------
page_title("Wellbeing Flash Cards")
page_subtitle(
    "Interactive deck of 23 research-backed wellbeing activities — for live use in school training."
)

with st.sidebar:
    st.markdown("### 🔎 Filters")

    age_display = st.multiselect(
        "Age group",
        options=AGE_FILTER_OPTIONS,
        default=[],
        help="Primary = 5–12. Secondary = 13–18. Cards tagged 'All ages' always appear.",
    )
    age_filter = [AGE_DISPLAY_TO_CODE[a] for a in age_display]

    purpose_filter = st.multiselect(
        "Purpose",
        options=ALL_PURPOSES,
        default=[],
        help="What the activity is designed to do.",
    )

    search = st.text_input("Search", placeholder="e.g. 'breathing', 'gratitude'")


filtered = filter_activities(
    ages=age_filter if age_filter else None,
    purposes=purpose_filter if purpose_filter else None,
    props_filter="Any",
    search=search,
)

st.markdown(
    f"<div style='margin-bottom:10px;'><strong>Showing {len(filtered)} of {len(ACTIVITIES)} activities</strong>"
    + (" — clear filters in the sidebar to see all." if len(filtered) < len(ACTIVITIES) else "")
    + "</div>",
    unsafe_allow_html=True,
)

if not filtered:
    st.info("No activities match these filters. Try clearing one of the filters in the sidebar.")
    st.stop()


# Grid layout — 2 columns of equal-height cards.
for row_start in range(0, len(filtered), 2):
    cols = st.columns(2, gap="medium")
    for i, col in enumerate(cols):
        idx = row_start + i
        if idx >= len(filtered):
            continue
        a = filtered[idx]
        with col:
            if render_browse_card(a, on_open_key=f"open_{a.id}"):
                st.session_state["selected_activity"] = a.id
                st.rerun()
