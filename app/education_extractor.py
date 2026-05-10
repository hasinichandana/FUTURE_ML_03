import re


def extract_education(text):

    education_keywords = [

        "b.tech",
        "bachelor",
        "master",
        "m.tech",
        "mba",
        "mca",
        "bca",
        "computer science",
        "engineering",
        "phd"
    ]

    found_education = []

    text = text.lower()

    for keyword in education_keywords:

        if keyword in text:

            found_education.append(
                keyword
            )

    if found_education:

        return ", ".join(
            found_education
        )

    return "Not Detected"