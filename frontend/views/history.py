import requests
import streamlit as st

from frontend.services import api_client


def _hero() -> str:
    return """
    <style>
        .hs-hero {
            position: relative;
            padding: 2.2rem 2rem;
            background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 50%, #9333EA 100%);
            color: #ffffff;
            border-radius: 20px;
            margin-bottom: 1.4rem;
            overflow: hidden;
            box-shadow: 0 14px 40px rgba(79, 70, 229, 0.32);
        }
        .hs-hero::after {
            content: "";
            position: absolute;
            inset: 0;
            background: radial-gradient(circle at 12% 18%, rgba(255,255,255,0.18), transparent 38%),
                        radial-gradient(circle at 88% 0%, rgba(255,255,255,0.12), transparent 35%);
            pointer-events: none;
        }
        .hs-badge {
            display: inline-block;
            font-size: 0.74rem; font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase;
            padding: 0.3rem 0.8rem; border-radius: 999px;
            background: rgba(255,255,255,0.16); border: 1px solid rgba(255,255,255,0.25);
            margin-bottom: 0.8rem;
        }
        .hs-hero h1 { font-size: 2.1rem; font-weight: 800; margin: 0 0 0.3rem; color: #ffffff; }
        .hs-hero p { margin: 0; color: rgba(255,255,255,0.92); font-size: 1.02rem; }
    </style>
    <div class="hs-hero">
      <span class="hs-badge">📊 History</span>
      <h1>Your analysis history</h1>
      <p>Every resume you've scored, saved to your account - reopen, download a PDF, or remove any entry.</p>
    </div>
    """


def _show_backend_error(exc: Exception) -> None:
    if isinstance(exc, requests.ConnectionError):
        st.error("Could not reach the backend. Is it running on port 8000?")
    elif isinstance(exc, requests.HTTPError) and exc.response is not None:
        st.error(f"Backend returned {exc.response.status_code}: {exc.response.text}")
    else:
        st.error(f"Unexpected error: {exc}")


def render() -> None:
    st.markdown(_hero(), unsafe_allow_html=True)

    access_token = st.session_state.get("access_token")
    if not access_token:
        st.warning("⚠️ Sign in from the top account panel to view your history.")
        return

    try:
        history = api_client.get_history(access_token)
    except requests.RequestException as exc:
        _show_backend_error(exc)
        return

    if not history:
        st.info("No analyses yet for this account. Run a scoring on the ATS Scorer page first.")
        if st.button("🎯 Go to ATS Scorer"):
            st.session_state.current_view = "scorer"
            st.rerun()
        return

    st.markdown(f"**Total analyses:** {len(history)}")
    st.markdown("---")

    for idx, entry in enumerate(history):
        filename = entry.get("filename", "resume")
        ats_score = float(entry.get("ats_score", 0))
        created_at = entry.get("created_at", "")
        analysis = entry.get("analysis_result", {}) or {}

        component_scores = analysis.get("component_scores", {}) or {}
        jd_comparison = analysis.get("jd_comparison") or analysis.get("jd_match_analysis")

        with st.expander(f"📄 {filename} - Score: {ats_score:.0f}/100 - {created_at}"):
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Overall", f"{ats_score:.0f}/100")
                st.metric("Formatting", f"{component_scores.get('formatting', 0):.0f}/20")
            with c2:
                st.metric("Keywords", f"{component_scores.get('keywords', 0):.0f}/25")
                st.metric("Content", f"{component_scores.get('content', 0):.0f}/25")
            with c3:
                st.metric("Skill Validation", f"{component_scores.get('skill_validation', 0):.0f}/15")
                st.metric("ATS Compatibility", f"{component_scores.get('ats_compatibility', 0):.0f}/15")

            if jd_comparison:
                st.markdown(f"**JD Match:** {jd_comparison.get('match_percentage', 0):.0f}%")

            entry_id = entry.get("id")
            if entry_id:
                pdf_col, delete_col = st.columns(2)

                with pdf_col:
                    pdf_key = f"hist_pdf_{entry_id}"
                    if st.button("📑 Generate PDF", key=f"pdf_{idx}", use_container_width=True):
                        try:
                            with st.spinner("Generating PDF on backend..."):
                                st.session_state[pdf_key] = api_client.get_history_pdf(
                                    str(entry_id), access_token
                                )
                        except requests.RequestException as exc:
                            _show_backend_error(exc)

                    if pdf_key in st.session_state:
                        st.download_button(
                            "⬇️ Download PDF",
                            data=st.session_state[pdf_key],
                            file_name=f"ats_report_{filename}.pdf",
                            mime="application/pdf",
                            use_container_width=True,
                            key=f"download_pdf_{idx}",
                        )

                with delete_col:
                    if st.button("🗑️ Delete", key=f"delete_{idx}", use_container_width=True):
                        try:
                            api_client.delete_history_entry(str(entry_id), access_token)
                            st.session_state.pop(f"hist_pdf_{entry_id}", None)
                            st.success("Deleted.")
                            st.rerun()
                        except requests.RequestException as exc:
                            _show_backend_error(exc)
