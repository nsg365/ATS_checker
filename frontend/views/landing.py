import streamlit as st


def _styles() -> str:
    return """
    <style>
        .lp-wrap { max-width: 1040px; margin: 0 auto; }

        /* ---- Hero ---- */
        .lp-hero {
            position: relative;
            text-align: center;
            padding: 3.5rem 2rem 3rem;
            background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 50%, #9333EA 100%);
            color: #ffffff;
            border-radius: 22px;
            margin-bottom: 1rem;
            box-shadow: 0 18px 50px rgba(79, 70, 229, 0.35);
            overflow: hidden;
        }
        .lp-hero::after {
            content: "";
            position: absolute;
            inset: 0;
            background: radial-gradient(circle at 20% 20%, rgba(255,255,255,0.18), transparent 40%),
                        radial-gradient(circle at 80% 0%, rgba(255,255,255,0.12), transparent 35%);
            pointer-events: none;
        }
        .lp-badge {
            display: inline-block;
            font-size: 0.8rem;
            font-weight: 600;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            padding: 0.35rem 0.85rem;
            border-radius: 999px;
            background: rgba(255,255,255,0.16);
            border: 1px solid rgba(255,255,255,0.25);
            margin-bottom: 1.1rem;
        }
        .lp-hero h1 {
            font-size: 3rem;
            line-height: 1.05;
            font-weight: 800;
            margin: 0 0 0.6rem;
            color: #ffffff;
        }
        .lp-hero p {
            font-size: 1.15rem;
            color: rgba(255,255,255,0.92);
            max-width: 620px;
            margin: 0 auto;
        }
        .lp-hero .lp-hint {
            font-size: 0.9rem;
            color: rgba(255,255,255,0.8);
            margin-top: 1.4rem;
        }

        /* ---- Section heading ---- */
        .lp-section-title {
            text-align: center;
            font-size: 1.6rem;
            font-weight: 800;
            margin: 2.4rem 0 0.3rem;
            color: var(--text-primary, #1F2937);
        }
        .lp-section-sub {
            text-align: center;
            color: var(--text-secondary, #6B7280);
            margin-bottom: 1.6rem;
        }

        /* ---- Card grid ---- */
        .lp-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1.1rem;
        }
        @media (max-width: 820px) { .lp-grid { grid-template-columns: 1fr; } }

        .lp-card {
            background: var(--background-white, #ffffff);
            border: 1px solid var(--border-color, #E5E7EB);
            border-top: 4px solid var(--accent, #4F46E5);
            border-radius: 18px;
            padding: 1.5rem 1.35rem;
            box-shadow: 0 4px 14px rgba(0,0,0,0.06);
            transition: transform 0.18s ease, box-shadow 0.18s ease;
            height: 100%;
        }
        .lp-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 16px 34px rgba(79,70,229,0.18);
        }
        .lp-icon {
            width: 46px; height: 46px;
            display: flex; align-items: center; justify-content: center;
            border-radius: 12px;
            font-size: 1.4rem;
            margin-bottom: 0.9rem;
            background: var(--accent-soft, rgba(79,70,229,0.12));
        }
        .lp-card h3 {
            font-size: 1.12rem;
            font-weight: 750;
            margin: 0 0 0.45rem;
            color: var(--text-primary, #1F2937);
        }
        .lp-card p {
            font-size: 0.93rem;
            line-height: 1.5;
            color: var(--text-secondary, #6B7280);
            margin: 0;
        }
        .lp-card .lp-weights {
            margin-top: 0.7rem;
            font-size: 0.8rem;
            color: var(--text-muted, #9CA3AF);
        }

        /* ---- Two modes ---- */
        .lp-modes { display: grid; grid-template-columns: 1fr 1fr; gap: 1.1rem; }
        @media (max-width: 820px) { .lp-modes { grid-template-columns: 1fr; } }
        .lp-mode {
            background: var(--background-light, #F9FAFB);
            border: 1px solid var(--border-color, #E5E7EB);
            border-radius: 16px;
            padding: 1.3rem 1.4rem;
        }
        .lp-mode h4 { margin: 0 0 0.35rem; font-size: 1.05rem; color: var(--text-primary, #1F2937); }
        .lp-mode p { margin: 0; font-size: 0.92rem; color: var(--text-secondary, #6B7280); }
        .lp-mode .lp-tag {
            display:inline-block; font-size:0.72rem; font-weight:700; letter-spacing:0.03em;
            text-transform:uppercase; padding:0.2rem 0.6rem; border-radius:999px; margin-bottom:0.6rem;
            color:#fff;
        }

        /* ---- Chips ---- */
        .lp-chips { display:flex; flex-wrap:wrap; gap:0.6rem; justify-content:center; }
        .lp-chip {
            background: var(--background-white, #ffffff);
            border: 1px solid var(--border-color, #E5E7EB);
            border-radius: 999px;
            padding: 0.5rem 1rem;
            font-size: 0.88rem;
            font-weight: 600;
            color: var(--text-primary, #1F2937);
            box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        }

        /* ---- Steps ---- */
        .lp-steps { display:grid; grid-template-columns: repeat(3,1fr); gap:1.1rem; }
        @media (max-width: 820px) { .lp-steps { grid-template-columns: 1fr; } }
        .lp-step {
            background: var(--background-white, #ffffff);
            border: 1px solid var(--border-color, #E5E7EB);
            border-radius: 16px;
            padding: 1.3rem;
            text-align: center;
        }
        .lp-step .lp-num {
            width: 38px; height: 38px; margin: 0 auto 0.7rem;
            display:flex; align-items:center; justify-content:center;
            border-radius: 50%;
            font-weight: 800; color:#fff;
            background: linear-gradient(135deg, #4F46E5, #9333EA);
        }
        .lp-step h4 { margin:0 0 0.3rem; font-size:1rem; color: var(--text-primary, #1F2937); }
        .lp-step p { margin:0; font-size:0.88rem; color: var(--text-secondary, #6B7280); }

        /* ---- Footer ---- */
        .lp-footer {
            text-align:center; color: var(--text-muted, #9CA3AF);
            font-size: 0.83rem; margin: 2.6rem 0 0.5rem;
        }
    </style>
    """


def _cta(key: str, label: str = "🚀 Analyze My Resume") -> None:
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        if st.button(label, use_container_width=True, type="primary", key=key):
            st.session_state.current_view = "scorer"
            st.rerun()


def render():
    st.markdown(_styles(), unsafe_allow_html=True)

    # ---- Hero ----
    st.markdown(
        """
        <div class="lp-wrap">
          <div class="lp-hero">
            <span class="lp-badge">🐒 ResumeLens · Free</span>
            <h1>Know your resume's<br>ATS score in 30 seconds</h1>
            <p>Upload your resume - and optionally a job description - to get a 0–100
            compatibility score with specific, prioritized fixes.</p>
            <div class="lp-hint">Sign in from the top bar to analyze · PDF report & saved history included</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    _cta("cta_hero")

    # ---- Two analysis modes ----
    st.markdown('<div class="lp-section-title">Two ways to analyze</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="lp-section-sub">Pick the mode that matches where you are in your search.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="lp-wrap">
          <div class="lp-modes">
            <div class="lp-mode">
              <span class="lp-tag" style="background:#4F46E5;">General</span>
              <h4>General ATS Score</h4>
              <p>Resume only. Get your overall ATS compatibility across formatting,
              keywords, content quality, skill validation and parse-ability.</p>
            </div>
            <div class="lp-mode">
              <span class="lp-tag" style="background:#9333EA;">Targeted</span>
              <h4>Job Description Comparison</h4>
              <p>Resume + a job description. See your match percentage, the exact
              keywords you're missing, and your skills gap for that specific role.</p>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---- Key features ----
    st.markdown('<div class="lp-section-title">✨ What you get</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="lp-section-sub">More than a score - a clear plan to improve.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="lp-wrap">
          <div class="lp-grid">
            <div class="lp-card" style="--accent:#4F46E5; --accent-soft:rgba(79,70,229,0.12);">
              <div class="lp-icon">📊</div>
              <h3>5-Dimension Scoring</h3>
              <p>A breakdown across the factors ATS systems actually weigh, so you know
              exactly where you stand.</p>
              <div class="lp-weights">Formatting 20 · Keywords 25 · Content 25 · Skills 15 · ATS 15</div>
            </div>
            <div class="lp-card" style="--accent:#10B981; --accent-soft:rgba(16,185,129,0.14);">
              <div class="lp-icon">✅</div>
              <h3>Semantic Skill Validation</h3>
              <p>We check that each skill you list is actually backed by a project or
              experience bullet - no more empty claims.</p>
            </div>
            <div class="lp-card" style="--accent:#F59E0B; --accent-soft:rgba(245,158,11,0.16);">
              <div class="lp-icon">🔍</div>
              <h3>Keyword & Skills Gap</h3>
              <p>Compare against any job description to surface the missing keywords and
              skills that cost you interviews.</p>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---- Payoff chips ----
    st.markdown('<div style="height:1.4rem;"></div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="lp-wrap">
          <div class="lp-chips">
            <span class="lp-chip">🎯 Overall ATS score</span>
            <span class="lp-chip">🚨 Critical issues, ranked</span>
            <span class="lp-chip">💡 Prioritized recommendations</span>
            <span class="lp-chip">📑 Downloadable PDF report</span>
            <span class="lp-chip">📊 Saved analysis history</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---- How it works ----
    st.markdown('<div class="lp-section-title">How it works</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="lp-wrap">
          <div class="lp-steps">
            <div class="lp-step">
              <div class="lp-num">1</div>
              <h4>Upload your resume</h4>
              <p>PDF or DOCX, up to 10 MB. Optionally paste a job description.</p>
            </div>
            <div class="lp-step">
              <div class="lp-num">2</div>
              <h4>AI analysis</h4>
              <p>Your resume is parsed and scored across multiple dimensions in seconds.</p>
            </div>
            <div class="lp-step">
              <div class="lp-num">3</div>
              <h4>Get actionable fixes</h4>
              <p>Review ranked issues, recommendations, and export a PDF report.</p>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---- Closing CTA + footer ----
    st.markdown('<div style="height:1.8rem;"></div>', unsafe_allow_html=True)
    _cta("cta_footer", "Start Analyzing - It's Free")
    st.markdown(
        """
        <div class="lp-footer">
          ResumeLens · Analyses are private to your account and deletable anytime from History.
        </div>
        """,
        unsafe_allow_html=True,
    )
