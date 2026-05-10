import os

from resume_parser import extract_text_from_pdf
from utils import clean_text
from skill_extractor import extract_skills
from similarity_engine import calculate_similarity
from ranking import rank_candidates


# Job description file
jd_path = "data/job_descriptions/ml_engineer.txt"

# Read JD
with open(jd_path, "r", encoding="utf-8") as file:
    jd_text = file.read()

cleaned_jd = clean_text(jd_text)

# Extract JD skills
jd_skills = extract_skills(cleaned_jd)

# Resume folder
resume_folder = "data/resumes/categories/INFORMATION-TECHNOLOGY"

results = []

# Loop through all resumes
for file_name in os.listdir(resume_folder):
    print(f"Processing: {file_name}")
    if file_name.endswith(".pdf"):

        pdf_path = os.path.join(
            resume_folder,
            file_name
        )

        # Extract resume text
        resume_text = extract_text_from_pdf(pdf_path)

        # Clean text
        cleaned_resume = clean_text(resume_text)

        # Extract skills
        resume_skills = extract_skills(cleaned_resume)

        # Similarity score
        score = calculate_similarity(
            cleaned_resume,
            cleaned_jd
        )

        # Missing skills
        missing_skills = []

        for skill in jd_skills:

            if skill not in resume_skills:
                missing_skills.append(skill)

        # Save results
        results.append({
            "resume": file_name,
            "score": score,
            "skills": resume_skills,
            "missing_skills": missing_skills
        })

# Rank candidates
ranked_candidates = rank_candidates(results)

# Print rankings
print("\n========== CANDIDATE RANKING ==========\n")

for rank, candidate in enumerate(
    ranked_candidates,
    start=1
):

    print(f"Rank #{rank}")
    print(f"Resume: {candidate['resume']}")
    print(f"Score: {candidate['score']}%")

    print(f"Skills: {candidate['skills']}")

    print(
        f"Missing Skills: "
        f"{candidate['missing_skills']}"
    )

    print("\n-----------------------------------\n")


