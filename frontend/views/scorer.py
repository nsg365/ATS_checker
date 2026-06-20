from typing import Optional

import requests
import streamlit as st

from frontend.services import api_client
from frontend.components.dashboard import display_results_dashboard


def _styles() -> str:
    return """
    <style>
        /* ---- Hero ---- */
        .sc-hero {
            position: relative;
            padding: 2.2rem 2rem;
            background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 50%, #9333EA 100%);
            color: #ffffff;
            border-radius: 20px;
            margin-bottom: 1.4rem;
            overflow: hidden;
            box-shadow: 0 14px 40px rgba(79, 70, 229, 0.32);
        }
        .sc-hero::after {
            content: "";
            position: absolute;
            inset: 0;
            background: radial-gradient(circle at 12% 18%, rgba(255,255,255,0.18), transparent 38%),
                        radial-gradient(circle at 88% 0%, rgba(255,255,255,0.12), transparent 35%);
            pointer-events: none;
        }
        .sc-badge {
            display: inline-block;
            font-size: 0.74rem; font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase;
            padding: 0.3rem 0.8rem; border-radius: 999px;
            background: rgba(255,255,255,0.16); border: 1px solid rgba(255,255,255,0.25);
            margin-bottom: 0.8rem;
        }
        .sc-hero h1 { font-size: 2.1rem; font-weight: 800; margin: 0 0 0.3rem; color: #ffffff; }
        .sc-hero p { margin: 0; color: rgba(255,255,255,0.92); font-size: 1.02rem; }

        /* ---- Mode cards ---- */
        .sc-modes { display: grid; grid-template-columns: 1fr 1fr; gap: 1.1rem; margin-bottom: 0.4rem; }
        @media (max-width: 820px) { .sc-modes { grid-template-columns: 1fr; } }
        .sc-mode {
            background: var(--background-light, #F9FAFB);
            border: 1px solid var(--border-color, #E5E7EB);
            border-radius: 14px;
            padding: 1rem 1.2rem;
        }
        .sc-mode h4 { margin: 0 0 0.3rem; font-size: 1rem; color: var(--text-primary, #1F2937); }
        .sc-mode p { margin: 0; font-size: 0.88rem; color: var(--text-secondary, #6B7280); }
        .sc-mode .sc-tag {
            display: inline-block; font-size: 0.7rem; font-weight: 700; letter-spacing: 0.03em;
            text-transform: uppercase; padding: 0.18rem 0.55rem; border-radius: 999px;
            margin-bottom: 0.5rem; color: #fff;
        }

        /* ---- Section titles ---- */
        .sc-section-title {
            font-size: 1.15rem; font-weight: 750;
            color: var(--text-primary, #1F2937);
            margin: 0.2rem 0 0.7rem;
        }
    </style>
    """


def _read_jd(jd_file, jd_text: str) -> str:
    """
    Turn whatever the user provided into a plain JD string for the backend.

    For .txt files we decode in-process - that's a trivial operation, no need
    for a backend round-trip. For PDF/DOCX, we'd need the backend's parser;
    we don't have a public endpoint for that, so we ask the user to paste text
    instead for non-txt JDs.
    """
    if jd_text:
        return jd_text.strip()
    if jd_file is None:
        return ""
    if jd_file.name.lower().endswith(".txt"):
        return jd_file.getvalue().decode("utf-8", errors="ignore")
    st.warning(
        "Job description files must be `.txt` for now - paste the JD text instead "
        "if you have a PDF or DOCX."
    )
    return ""


def _show_backend_error(exc: Exception) -> None:
    """Translate a `requests` exception into a friendly Streamlit error."""
    if isinstance(exc, requests.ConnectionError):
        st.error("Could not reach the backend. Is `uvicorn backend.main:app` running on port 8000?")
    elif isinstance(exc, requests.Timeout):
        st.error("The backend took too long to respond. Try a smaller resume or check the server logs.")
    elif isinstance(exc, requests.HTTPError) and exc.response is not None:
        try:
            detail = exc.response.json().get("detail", exc.response.text)
        except ValueError:
            detail = exc.response.text
        st.error(f"Backend returned {exc.response.status_code}: {detail}")
    else:
        st.error(f"Unexpected error: {exc}")


def _summary_text(analysis: dict) -> str:
    """Tiny client-side text summary for the Download button."""
    score = analysis.get("ATS_score", analysis.get("ats_score", 0))
    lines = [f"ATS Score: {score:.0f}/100", ""]
    if analysis.get("strengths"):
        lines.append("STRENGTHS:")
        lines.extend(f"  - {s}" for s in analysis["strengths"])
        lines.append("")
    if analysis.get("critical_issues"):
        lines.append("CRITICAL ISSUES:")
        lines.extend(f"  - {s}" for s in analysis["critical_issues"])
        lines.append("")
    if analysis.get("suggestions"):
        lines.append("SUGGESTIONS:")
        lines.extend(f"  - {s}" for s in analysis["suggestions"])
    return "\n".join(lines)


def _render_upload_area(analysis_mode: str):
    """Two-column upload widgets. Returns (resume_file, jd_file, jd_text)."""
    left, right = st.columns(2)

    with left:
        st.markdown('<div class="sc-section-title">📄 Upload Resume</div>', unsafe_allow_html=True)
        resume_file = st.file_uploader(
            "Choose your resume file",
            type=["pdf", "doc", "docx"],
            help="Supported: PDF, DOC, DOCX (max 10 MB)",
            key="resume_upload",
        )
        if resume_file:
            st.success(f"✅ {resume_file.name} ({resume_file.size / 1024:.1f} KB)")

    jd_file: Optional[object] = None
    jd_text = ""

    with right:
        if analysis_mode == "Job Description Comparison":
            st.markdown('<div class="sc-section-title">📋 Job Description</div>', unsafe_allow_html=True)
            jd_method = st.radio(
                "Input method:",
                ["Paste Text", "Upload .txt File"],
                horizontal=True,
                key="jd_input_method",
            )
            if jd_method == "Upload .txt File":
                jd_file = st.file_uploader(
                    "Choose JD file (.txt only)",
                    type=["txt"],
                    key="jd_upload",
                )
                if jd_file:
                    st.success(f"✅ {jd_file.name}")
            else:
                jd_text = st.text_area(
                    "Paste job description text:",
                    height=200,
                    placeholder="Paste the JD here...",
                    key="jd_text",
                )
                if jd_text:
                    st.success(f"✅ {len(jd_text)} characters")
        else:
            st.markdown('<div class="sc-section-title">📋 Job Description</div>', unsafe_allow_html=True)
            st.info("Switch to 'Job Description Comparison' mode to enable JD matching.")

    return resume_file, jd_file, jd_text


def _render_export_buttons(analysis: dict) -> None:
    st.markdown('<div class="sc-section-title">📥 Export Results</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        # Lazy: only call the backend the first time the user clicks expand.
        if st.button("📑 Generate PDF Report", use_container_width=True, type="primary"):
            try:
                with st.spinner("Generating PDF on backend..."):
                    pdf_bytes = api_client.generate_pdf(
                        analysis,
                        access_token=st.session_state["access_token"],
                    )
                st.session_state["scorer_pdf_bytes"] = pdf_bytes
            except requests.RequestException as exc:
                _show_backend_error(exc)

        if "scorer_pdf_bytes" in st.session_state:
            st.download_button(
                "⬇️ Download PDF",
                data=st.session_state["scorer_pdf_bytes"],
                file_name="ats_resume_report.pdf",
                mime="application/pdf",
                use_container_width=True,
                key="download_pdf_report",
            )

    with c2:
        st.download_button(
            "📄 Download Summary (.txt)",
            data=_summary_text(analysis),
            file_name="ats_summary.txt",
            mime="text/plain",
            use_container_width=True,
            key="download_summary",
        )


def render() -> None:
    st.markdown(_styles(), unsafe_allow_html=True)

    st.markdown(
        """
        <div class="sc-hero">
          <span class="sc-badge">🐒 ResumeLens</span>
          <h1>Score your resume</h1>
          <p>Upload your resume - and optionally a job description - for a comprehensive,
          0–100 ATS analysis with prioritized fixes.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sc-modes">
          <div class="sc-mode">
            <span class="sc-tag" style="background:#4F46E5;">General</span>
            <h4>General ATS Score</h4>
            <p>Resume only - overall ATS compatibility across all dimensions.</p>
          </div>
          <div class="sc-mode">
            <span class="sc-tag" style="background:#9333EA;">Targeted</span>
            <h4>JD Comparison</h4>
            <p>Resume + job description - match %, missing keywords and skills gap.</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    analysis_mode = st.radio(
        "Select Analysis Mode:",
        ["General ATS Score", "Job Description Comparison"],
        horizontal=True,
    )

    st.markdown("---")

    resume_file, jd_file, jd_text = _render_upload_area(analysis_mode)

    st.markdown("---")

    if not resume_file:
        st.info("👆 Upload your resume to begin.")
        # If we have a prior result in session, render it again.
        if st.session_state.get("scorer_analysis"):
            display_results_dashboard(st.session_state["scorer_analysis"])
        return

    access_token = st.session_state.get("access_token")
    if not access_token:
        st.warning("⚠️ Sign in from the top account panel to analyze a resume.")
        return

    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        analyze = st.button("🚀 Analyze Resume", use_container_width=True, type="primary")

    if not analyze:
        # Re-show previous result on rerun (e.g. after PDF generation).
        if st.session_state.get("scorer_analysis"):
            display_results_dashboard(st.session_state["scorer_analysis"])
            _render_export_buttons(st.session_state["scorer_analysis"])
        return

    # Fresh analysis - drop any cached PDF/result.
    st.session_state.pop("scorer_pdf_bytes", None)
    st.session_state.pop("scorer_analysis", None)

    job_description = _read_jd(jd_file, jd_text) if analysis_mode == "Job Description Comparison" else ""

    try:
        with st.spinner("Analyzing your resume... this can take 10–30 seconds."):
            analysis = api_client.analyze_resume(
                resume_file=resume_file,
                access_token=access_token,
                job_description=job_description,
            )
    except requests.RequestException as exc:
        _show_backend_error(exc)
        return

    st.session_state["scorer_analysis"] = analysis
    st.success("✅ Analysis complete!")
    display_results_dashboard(analysis)
    _render_export_buttons(analysis)
