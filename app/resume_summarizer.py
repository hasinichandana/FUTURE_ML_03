def generate_summary(
    skills,
    score
):

    if len(skills) == 0:

        return (
            "Candidate profile contains "
            "limited matching technical skills."
        )

    top_skills = ", ".join(
        skills[:5]
    )

    summary = (
        f"Candidate demonstrates experience "
        f"in {top_skills}. "
        f"Overall candidate relevance score "
        f"is {score}%."
    )

    return summary