from typing import Any, Dict, List
import streamlit as st

from frontend.components.detailed_feedback import render_issue


def display_strengths(strengths: List[str]) -> None:
    st.markdown("### 💪 Strengths")
    if not strengths:
        st.info("Keep improving your resume to unlock strengths!")
        return
    for item in strengths:
        st.markdown(f"- {item}")


def display_critical_issues(analysis: Dict[str, Any]) -> None:
    feedback = analysis.get("detailed_feedback") or []
    high_issues = [
        f for f in feedback
        if (f.get("severity_level") or "").lower() in ("high", "critical")
    ]
    # Score-derived one-liners - used only as a fallback when the parser produced
    # no detailed High/Critical entries (e.g. a strong resume with minor gaps).
    score_critical = [
        c.strip() for c in (analysis.get("critical_issues") or []) if c and c.strip()
    ]

    if not high_issues and not score_critical:
        st.success("### ✅ No Critical Issues Found!")
        st.markdown("Your resume doesn't have any urgent issues. Nice work.")
        return

    st.markdown("### 🚨 Critical Issues")
    st.error("These high-impact issues should be addressed first for better ATS performance.")

    if high_issues:
        st.caption(f"{len(high_issues)} high-impact issue(s) - expand each for how to fix it.")
        for issue in high_issues:
            render_issue(issue)
    else:
        for item in score_critical:
            st.markdown(f"- 🔴 **{item}**")