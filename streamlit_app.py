import streamlit as st
import pandas as pd
import tempfile
import os
import matplotlib.pyplot as plt

from collections import Counter

from app.resume_parser import extract_text_from_pdf
from app.utils import clean_text
from app.skill_extractor import extract_skills
from app.semantic_similarity import (
    calculate_semantic_similarity
)
from app.resume_summarizer import (
    generate_summary
)
from app.experience_extractor import (
    extract_experience
)
from app.education_extractor import (
    extract_education
)

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="📄",
    layout="wide"
)

# =====================================
# CUSTOM CSS
# =====================================

st.markdown(
    """
    <style>

    .main {
        padding-top: 1rem;
    }

    .stMetric {
        background-color: #1e1e1e;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #333333;
    }

    .big-title {
        font-size: 42px;
        font-weight: bold;
        color: #4CAF50;
    }

    .subtitle {
        font-size: 18px;
        color: #BBBBBB;
        margin-bottom: 30px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =====================================
# HEADER
# =====================================

st.markdown(
    """
    <div class="big-title">
        AI Resume Screening System
    </div>

    <div class="subtitle">
        Semantic AI-Powered ATS for Resume Ranking,
        Skill Matching & Recruiter Analytics
    </div>
    """,
    unsafe_allow_html=True
)

# =====================================
# SIDEBAR
# =====================================

st.sidebar.title(
    "Recruiter Dashboard"
)

st.sidebar.markdown(
    """
    Upload resumes and compare them
    against job descriptions using
    AI-powered semantic matching.
    """
)

# =====================================
# JOB DESCRIPTION
# =====================================

job_files = os.listdir(
    "data/job_descriptions"
)

selected_jd = st.selectbox(
    "Select Job Description",
    job_files
)

jd_path = os.path.join(
    "data/job_descriptions",
    selected_jd
)

with open(
    jd_path,
    "r",
    encoding="utf-8"
) as file:

    jd_text = file.read()

cleaned_jd = clean_text(
    jd_text
)

jd_skills = extract_skills(
    cleaned_jd
)

# =====================================
# FILE UPLOAD
# =====================================

uploaded_files = st.file_uploader(
    "Upload Resume PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

results = []

# =====================================
# MAIN PROCESSING
# =====================================

if uploaded_files:

    with st.spinner(
        "Screening resumes..."
    ):

        for uploaded_file in uploaded_files:

            # =====================================
            # SAVE TEMP PDF
            # =====================================

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ) as temp_file:

                temp_file.write(
                    uploaded_file.read()
                )

                temp_path = temp_file.name

            # =====================================
            # EXTRACT TEXT
            # =====================================

            resume_text = extract_text_from_pdf(
                temp_path
            )

            # =====================================
            # CLEAN TEXT
            # =====================================

            cleaned_resume = clean_text(
                resume_text
            )

            experience = extract_experience(
                cleaned_resume
            )

            # =====================================
            # EXTRACT SKILLS
            # =====================================

            resume_skills = extract_skills(
                cleaned_resume
            )

            # =====================================
            # SEMANTIC SIMILARITY
            # =====================================

            similarity_score = (
                calculate_semantic_similarity(
                    cleaned_resume,
                    cleaned_jd
                )
            )

            # =====================================
            # SKILL MATCH SCORE
            # =====================================

            matched_skills = []

            for skill in jd_skills:

                if skill in resume_skills:
                    matched_skills.append(
                        skill
                    )

            if len(jd_skills) > 0:

                skill_score = (
                    len(matched_skills)
                    / len(jd_skills)
                ) * 100

            else:

                skill_score = 0

            # =====================================
            # FINAL SCORE
            # =====================================

            final_score = round(
                (0.7 * skill_score)
                +
                (0.3 * similarity_score),
                2
            )

            # =====================================
            # MISSING SKILLS
            # =====================================

            missing_skills = []

            for skill in jd_skills:

                if skill not in resume_skills:

                    missing_skills.append(
                        skill
                    )

            # =====================================
            # AI SUMMARY
            # =====================================

            summary = generate_summary(
                resume_skills,
                final_score
            )

            # =====================================
            # STORE RESULTS
            # =====================================

            results.append({

                "Resume":
                uploaded_file.name,

                "Experience": 
                experience,

                "Semantic Score":
                similarity_score,

                "Skill Match Score":
                round(skill_score, 2),

                "Final Score":
                final_score,  

                "Skills":
                ", ".join(resume_skills),

                "Missing Skills":
                ", ".join(missing_skills),

                "Summary":
                summary  

                
            })

    # =====================================
    # RANK CANDIDATES
    # =====================================

    ranked = sorted(
        results,
        key=lambda x: x["Final Score"],
        reverse=True
    )

    df = pd.DataFrame(
        ranked
    )
    # =====================================
    # METRIC CARDS
    # =====================================

    total_candidates = len(df)

    average_score = round(
        df["Final Score"].mean(),
        2
    )

    top_score = round(
        df["Final Score"].max(),
        2
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Candidates",
        total_candidates
    )

    col2.metric(
        "Average Score",
        f"{average_score}%"
    )

    col3.metric(
        "Top Score",
        f"{top_score}%"
    )
    # =====================================
    # SIDEBAR FILTERS
    # =====================================

    st.sidebar.header(
        "Candidate Filters"
    )

    min_score = st.sidebar.slider(
        "Minimum Final Score",
        0,
        100,
        20
    )

    # Filter dataframe
    df = df[
        df["Final Score"] >= min_score
    ]

    # =====================================
    # CANDIDATE TABLE
    # =====================================

    st.subheader(
        "Candidate Rankings"
    )

    st.dataframe(
        df,
        use_container_width=True
    )

    # =====================================
    # TOP CANDIDATE
    # =====================================

    if len(df) > 0:

        top_candidate = df.iloc[0]

        st.success(
            f"""
            Top Candidate:
            {top_candidate['Resume']}

            Final Score:
            {top_candidate['Final Score']}%
            """
        )

    # =====================================
    # AI SUMMARIES
    # =====================================

    st.subheader(
        "AI Candidate Summaries"
    )

    for index, row in df.iterrows():

        st.markdown(
            f"""
            ### {row['Resume']}

            {row['Summary']}
            """
        )

    # =====================================
    # ANALYTICS DASHBOARD
    # =====================================

    st.subheader(
        "Recruiter Analytics"
    )

    # =====================================
    # SCORE CHART
    # =====================================

    st.markdown(
        "### Candidate Score Comparison"
    )

    fig, ax = plt.subplots(
        figsize=(10, 5)
    )

    ax.bar(
        df["Resume"],
        df["Final Score"]
    )

    ax.set_xlabel(
        "Candidates"
    )

    ax.set_ylabel(
        "Final Score"
    )

    plt.xticks(
        rotation=45
    )

    st.pyplot(fig)

    # =====================================
    # SKILL ANALYSIS
    # =====================================

    all_skills = []

    for skills in df["Skills"]:

        split_skills = skills.split(",")

        for skill in split_skills:

            cleaned_skill = skill.strip()

            if cleaned_skill:

                all_skills.append(
                    cleaned_skill
                )

    skill_counts = Counter(
        all_skills
    )

    top_skills = (
        skill_counts.most_common(10)
    )

    if top_skills:

        skill_names = [
            item[0]
            for item in top_skills
        ]

        skill_values = [
            item[1]
            for item in top_skills
        ]

        st.markdown(
            "### Most Common Skills"
        )

        fig2, ax2 = plt.subplots(
            figsize=(10, 5)
        )

        ax2.bar(
            skill_names,
            skill_values
        )

        ax2.set_xlabel(
            "Skills"
        )

        ax2.set_ylabel(
            "Frequency"
        )

        plt.xticks(
            rotation=45
        )

        st.pyplot(fig2)

    # =====================================
    # RECRUITER INSIGHTS
    # =====================================

    st.subheader(
        "Recruiter Insights"
    )

    average_score = round(
        df["Final Score"].mean(),
        2
    )

    highest_score = round(
        df["Final Score"].max(),
        2
    )

    lowest_score = round(
        df["Final Score"].min(),
        2
    )

    st.info(
        f"""
        Average Candidate Score:
        {average_score}%

        Highest Score:
        {highest_score}%

        Lowest Score:
        {lowest_score}%
        """
    )