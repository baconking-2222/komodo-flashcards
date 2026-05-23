"""Themed sets — curated playlists of activities for specific situations."""

from __future__ import annotations

import html

import streamlit as st

from activities import get_activity
from branding import (
    page_subtitle,
    page_title,
    render_browse_card,
    render_present_card,
    render_themed_card,
    scroll_to_top,
    set_brand,
)
from themed_sets import THEMED_SETS, get_themed_set

set_brand("Themed sets")


selected_set_id: str | None = st.session_state.get("selected_set")
selected_activity_id: str | None = st.session_state.get("set_active_card")


# ---------- Drill-down 2: presenting a single card from a set ----------
if selected_set_id and selected_activity_id:
    activity = get_activity(selected_activity_id)
    themed = get_themed_set(selected_set_id)
    if not activity or not themed:
        st.session_state.pop("set_active_card", None)
        st.rerun()

    ids = list(themed.activity_ids)
    pos = ids.index(activity.id)

    scroll_to_top()

    nav_cols = st.columns([1, 1, 4])
    with nav_cols[0]:
        if st.button("← Back to set"):
            st.session_state.pop("set_active_card", None)
            st.session_state["_kb_scroll_top"] = True
            st.rerun()
    with nav_cols[1]:
        st.markdown(f"**Card {pos + 1} of {len(ids)}**")

    render_present_card(activity, header_eyebrow=f"{themed.icon} {themed.name}")

    nav2 = st.columns([1, 1, 3, 1])
    with nav2[0]:
        if pos > 0:
            if st.button("◀ Previous card"):
                st.session_state["set_active_card"] = ids[pos - 1]
                st.session_state["_kb_scroll_top"] = True
                st.rerun()
    with nav2[1]:
        if pos < len(ids) - 1:
            if st.button("Next card ▶"):
                st.session_state["set_active_card"] = ids[pos + 1]
                st.session_state["_kb_scroll_top"] = True
                st.rerun()

    st.stop()

# Scroll to top when nav state changes from another card opening.
if st.session_state.pop("_kb_scroll_top", False):
    scroll_to_top()


# ---------- Drill-down 1: inside a chosen set ----------
if selected_set_id:
    themed = get_themed_set(selected_set_id)
    if not themed:
        st.session_state.pop("selected_set", None)
        st.rerun()

    if st.button("← Back to all sets"):
        st.session_state.pop("selected_set", None)
        st.rerun()

    page_title(f"{themed.icon} {themed.name}")
    page_subtitle(themed.description)

    st.markdown(
        f"<div style='margin-bottom:14px; color:#2a4458;'><em>When to use:</em> {html.escape(themed.when_to_use)}</div>",
        unsafe_allow_html=True,
    )

    st.markdown(f"### Activities in this set ({len(themed.activity_ids)})")
    st.caption("Click an activity to open it for training.")

    # 2-column grid of activities in this set
    aids = list(themed.activity_ids)
    for row_start in range(0, len(aids), 2):
        cols = st.columns(2, gap="medium")
        for i, col in enumerate(cols):
            idx = row_start + i
            if idx >= len(aids):
                continue
            a = get_activity(aids[idx])
            if not a:
                continue
            with col:
                if render_browse_card(a, on_open_key=f"open_set_card_{a.id}"):
                    st.session_state["set_active_card"] = a.id
                    st.rerun()

    st.stop()


# ---------- Top level: gallery of all themed sets ----------
page_title("Themed sets")
page_subtitle(
    "Curated playlists of activities for common classroom moments. "
    "Pick a set, then walk through the cards in order."
)

for row_start in range(0, len(THEMED_SETS), 2):
    cols = st.columns(2, gap="medium")
    for i, col in enumerate(cols):
        idx = row_start + i
        if idx >= len(THEMED_SETS):
            continue
        s = THEMED_SETS[idx]
        with col:
            if render_themed_card(s, on_open_key=f"set_{s.id}"):
                st.session_state["selected_set"] = s.id
                st.rerun()
