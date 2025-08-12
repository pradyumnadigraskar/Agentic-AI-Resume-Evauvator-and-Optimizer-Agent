def calculate_ats_score(resume_text, job_description):
    resume_words = set(resume_text.lower().split())
    jd_words = set(job_description.lower().split())
    match_count = len(resume_words & jd_words)
    total_required = len(jd_words)
    score = (match_count / total_required) * 100 if total_required else 0
    return round(score, 2)