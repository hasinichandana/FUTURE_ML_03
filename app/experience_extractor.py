import re


def extract_experience(
    text
):

    patterns = [

        r'(\\d+)\\+?\\s+years',

        r'(\\d+)\\+?\\s+yrs',

        r'(\\d+)\\+?\\s+year'
    ]

    experiences = []

    for pattern in patterns:

        matches = re.findall(
            pattern,
            text.lower()
        )

        experiences.extend(
            matches
        )

    if experiences:

        max_exp = max(
            [
                int(exp)
                for exp in experiences
            ]
        )

        return (
            f"{max_exp} years"
        )

    return "Not Detected"