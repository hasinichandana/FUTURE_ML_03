from resume_parser import extract_text_from_pdf
from utils import clean_text
from skill_extractor import extract_skills
from similarity_engine import calculate_similarity


# Resume path
pdf_path = r"data/resumes/categories/INFORMATION-TECHNOLOGY/10089434.pdf"

# Read resume
resume_text = extract_text_from_pdf(pdf_path)

# Clean resume
cleaned_resume = clean_text(resume_text)

# Read job description
with open(
    "data/job_descriptions/ml_engineer.txt",
    "r",
    encoding="utf-8"
) as file:

    jd_text = file.read()

# Clean JD
cleaned_jd = clean_text(jd_text)

# Extract skills
resume_skills = extract_skills(cleaned_resume)

# Extract JD skills
jd_skills = extract_skills(cleaned_jd)

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

# Results
print("\nEXTRACTED RESUME SKILLS:\n")
print(resume_skills)

print("\nJOB DESCRIPTION SKILLS:\n")
print(jd_skills)

print("\nMISSING SKILLS:\n")
print(missing_skills)

print("\nSIMILARITY SCORE:\n")
print(f"{score}%")



