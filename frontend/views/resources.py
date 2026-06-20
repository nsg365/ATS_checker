import streamlit as st


def _styles() -> str:
    return """
    <style>
        /* ---- Hero ---- */
        .rs-hero {
            position: relative;
            padding: 2.2rem 2rem;
            background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 50%, #9333EA 100%);
            color: #ffffff;
            border-radius: 20px;
            margin-bottom: 1.4rem;
            overflow: hidden;
            box-shadow: 0 14px 40px rgba(79, 70, 229, 0.32);
        }
        .rs-hero::after {
            content: "";
            position: absolute; inset: 0;
            background: radial-gradient(circle at 12% 18%, rgba(255,255,255,0.18), transparent 38%),
                        radial-gradient(circle at 88% 0%, rgba(255,255,255,0.12), transparent 35%);
            pointer-events: none;
        }
        .rs-badge {
            display: inline-block;
            font-size: 0.74rem; font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase;
            padding: 0.3rem 0.8rem; border-radius: 999px;
            background: rgba(255,255,255,0.16); border: 1px solid rgba(255,255,255,0.25);
            margin-bottom: 0.8rem;
        }
        .rs-hero h1 { font-size: 2.1rem; font-weight: 800; margin: 0 0 0.3rem; color: #ffffff; }
        .rs-hero p { margin: 0; color: rgba(255,255,255,0.92); font-size: 1.02rem; max-width: 640px; }

        .rs-section-title {
            font-size: 1.45rem; font-weight: 800; margin: 2rem 0 0.3rem;
            color: var(--text-primary, #1F2937);
        }
        .rs-section-sub { color: var(--text-secondary, #6B7280); margin-bottom: 1.1rem; }

        /* ---- Generic cards ---- */
        .rs-grid3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.1rem; }
        @media (max-width: 820px) { .rs-grid3 { grid-template-columns: 1fr; } }
        .rs-grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 1.1rem; }
        @media (max-width: 820px) { .rs-grid2 { grid-template-columns: 1fr; } }

        .rs-card {
            background: var(--background-white, #ffffff);
            border: 1px solid var(--border-color, #E5E7EB);
            border-top: 4px solid var(--accent, #4F46E5);
            border-radius: 16px;
            padding: 1.25rem 1.3rem;
            box-shadow: 0 4px 14px rgba(0,0,0,0.06);
            height: 100%;
        }
        .rs-card h3 { margin: 0 0 0.55rem; font-size: 1.05rem; color: var(--text-primary, #1F2937); }
        .rs-card ul { margin: 0; padding-left: 1.1rem; }
        .rs-card li { font-size: 0.92rem; line-height: 1.65; color: var(--text-secondary, #6B7280); }
        .rs-card p { font-size: 0.92rem; line-height: 1.55; color: var(--text-secondary, #6B7280); margin: 0; }
        .rs-step-n { color: var(--accent, #4F46E5); font-weight: 800; }

        /* ---- Before / after ---- */
        .rs-ba { display: grid; grid-template-columns: 1fr 1fr; gap: 1.1rem; }
        @media (max-width: 820px) { .rs-ba { grid-template-columns: 1fr; } }
        .rs-ba-box { border-radius: 14px; padding: 1rem 1.15rem; border: 1px solid var(--border-color, #E5E7EB); }
        .rs-ba-bad  { background: rgba(239,68,68,0.08);  border-color: rgba(239,68,68,0.35); }
        .rs-ba-good { background: rgba(16,185,129,0.10); border-color: rgba(16,185,129,0.4); }
        .rs-ba-box .rs-ba-tag { font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.03em; }
        .rs-ba-box p { margin: 0.4rem 0 0; color: var(--text-primary, #1F2937); font-size: 0.93rem; }
    </style>
    """


def render():
    st.markdown(_styles(), unsafe_allow_html=True)

    # ---- Hero ----
    st.markdown(
        """
        <div class="rs-hero">
          <span class="rs-badge">📚 Resources</span>
          <h1>Write a resume the bots can read</h1>
          <p>Most applications are filtered by software before a human sees them.
          Here's how to make sure yours gets through - and still impresses the recruiter on the other side.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---- How ATS reads your resume ----
    st.markdown('<div class="rs-section-title">How an ATS actually reads your resume</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="rs-section-sub">Three things happen before a recruiter ever opens your file.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="rs-grid3">
          <div class="rs-card" style="--accent:#4F46E5;">
            <h3><span class="rs-step-n">1.</span> It extracts plain text</h3>
            <p>The parser strips your layout down to raw text. Anything trapped in a
            table, column, image, or text box can be scrambled or dropped entirely.</p>
          </div>
          <div class="rs-card" style="--accent:#7C3AED;">
            <h3><span class="rs-step-n">2.</span> It maps your sections</h3>
            <p>It looks for standard headings - Experience, Education, Skills - to slot
            your content into a structured profile. Creative headings confuse it.</p>
          </div>
          <div class="rs-card" style="--accent:#9333EA;">
            <h3><span class="rs-step-n">3.</span> It matches keywords</h3>
            <p>Your text is scored against the job description. Missing the exact terms
            the role asks for is the fastest way to get filtered out.</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---- Do / Don't ----
    st.markdown('<div class="rs-section-title">The rules that move your score</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="rs-grid2">
          <div class="rs-card" style="--accent:#10B981;">
            <h3>✅ Do</h3>
            <ul>
              <li>Mirror the job post's exact wording (write "React.js" if they did)</li>
              <li>Keep a plain-text Skills section near the top</li>
              <li>Start bullets with strong past-tense verbs - Built, Led, Reduced</li>
              <li>Back every skill you list with a project or experience bullet</li>
              <li>Add numbers: %, $, users, hours saved, team size</li>
              <li>Use a single-column layout with standard section headings</li>
              <li>Export as a text-selectable PDF or DOCX</li>
            </ul>
          </div>
          <div class="rs-card" style="--accent:#EF4444;">
            <h3>❌ Don't</h3>
            <ul>
              <li>Bury text in tables, columns, text boxes, or images</li>
              <li>Put your name or contact info in the header/footer region</li>
              <li>Rely on icons or graphics to convey skills or ratings</li>
              <li>Keyword-stuff or list skills you can't demonstrate</li>
              <li>Use exotic fonts or sub-10pt text</li>
              <li>Submit a scanned or image-only PDF (no selectable text)</li>
              <li>Use an acronym without spelling it out at least once</li>
            </ul>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---- Quantify ----
    st.markdown('<div class="rs-section-title">Quantify everything</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="rs-section-sub">Numbers turn a vague duty into proof of impact. Same bullet, very different signal:</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="rs-ba">
          <div class="rs-ba-box rs-ba-bad">
            <span class="rs-ba-tag" style="color:#EF4444;">❌ Before</span>
            <p>Responsible for improving the checkout page and helping the team ship features.</p>
          </div>
          <div class="rs-ba-box rs-ba-good">
            <span class="rs-ba-tag" style="color:#10B981;">✅ After</span>
            <p>Rebuilt the checkout flow, cutting drop-off 32% and lifting conversion for ~8K monthly users.</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---- Keywords by field ----
    st.markdown('<div class="rs-section-title">Keyword starting points by field</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="rs-section-sub">A prompt, not a checklist - only include what you can actually back up.</div>',
        unsafe_allow_html=True,
    )
    tab1, tab2, tab3 = st.tabs(["💻 Tech", "💼 Business", "🎨 Creative"])
    with tab1:
        st.markdown("""
        - **Languages:** Python, JavaScript/TypeScript, Java, Go, SQL
        - **Frameworks & libraries:** React, Next.js, FastAPI, Django, Node.js
        - **Cloud & DevOps:** AWS, Docker, Kubernetes, CI/CD, Terraform
        - **Data & ML:** Pandas, PyTorch, scikit-learn, ETL, model evaluation
        - **Practices:** REST APIs, testing, code review, Agile/Scrum
        """)
    with tab2:
        st.markdown("""
        - **Delivery:** Agile, Scrum, roadmapping, OKRs, stakeholder management
        - **Finance:** budgeting, forecasting, P&L ownership, cost reduction
        - **Analytics:** Excel, SQL, Tableau, Power BI, A/B testing
        - **Leadership:** cross-functional teams, mentoring, hiring
        - **Domain:** GTM strategy, vendor negotiation, process improvement
        """)
    with tab3:
        st.markdown("""
        - **Tools:** Figma, Adobe Creative Suite, Sketch, Webflow
        - **UX methods:** user research, wireframing, prototyping, usability testing
        - **Deliverables:** design systems, responsive UI, accessibility (WCAG)
        - **Brand:** identity, typography, motion, art direction
        - **Collaboration:** design hand-off, working with engineering, Storybook
        """)

    # ---- FAQ ----
    st.markdown('<div class="rs-section-title">Quick answers</div>', unsafe_allow_html=True)
    with st.expander("What counts as a good ATS score?"):
        st.markdown(
            "Aim for **80+**. Below ~60 usually means structural problems - missing sections, "
            "few keywords, or skills with no supporting evidence. Use the breakdown to see which "
            "dimension is dragging you down."
        )
    with st.expander("Does a high score guarantee an interview?"):
        st.markdown(
            "No. The score measures how well your resume passes automated screening and matches a role - "
            "it clears the first gate. A human still decides based on the substance behind your bullets."
        )
    with st.expander("PDF or DOCX - which should I submit?"):
        st.markdown(
            "Either works as long as the text is **selectable** (try highlighting it). When a posting "
            "specifies a format, follow it. Never upload a scanned image saved as a PDF."
        )
    with st.expander("How many job-description keywords should I add?"):
        st.markdown(
            "Cover the **must-have** skills and the terms repeated across the posting, worded the way they "
            "wrote them. Don't pad with keywords you can't defend in an interview - relevance beats volume."
        )

    st.markdown("---")
    st.caption("Ready to test your resume? Head to the ATS Scorer from the top bar.")
