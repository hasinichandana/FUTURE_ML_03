import pandas as pd

skills = pd.read_csv("data/skills.csv", header=None)[0].tolist()


def extract_skills(text):

    found_skills = []

    text = text.lower()

    for skill in skills:

        if skill.lower() in text:
            found_skills.append(skill)

    return list(set(found_skills))