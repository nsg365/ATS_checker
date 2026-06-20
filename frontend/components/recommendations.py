from typing import Any, Dict

import streamlit as st


def display_recommendations(analysis: Dict[str, Any]) -> None:
    recommendations = analysis.get("recommendations") or []

    # Fallback: older responses (or none generated) only carry a flat list.
    if not recommendations:
        suggestions = analysis.get("suggestions") or []
        if not suggestions:
            return
        st.markdown("### 💡 Recommendations")
        for suggestion in suggestions:
            st.markdown(f"- {suggestion}")
        return

    st.markdown("### 💡 Recommendations")

    summary = analysis.get("recommendation_summary")
    if summary:
        st.caption(summary)

    for rec in recommendations:
        icon = rec.get("priority_icon", "")
        label = rec.get("priority_label", "")
        title = rec.get("title", "")
        header = f"{icon} {title} - {label}" if label else f"{icon} {title}"

        with st.expander(header):
            if rec.get("description"):
                st.markdown(rec["description"])
            for item in rec.get("action_items") or []:
                st.markdown(f"- {item}")
