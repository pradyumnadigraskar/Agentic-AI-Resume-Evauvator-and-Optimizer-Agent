import re

def calculate_ats_score(resume_text, job_description):
    # Clean and tokenize
    def tokenize(text):
        return set(re.findall(r'\b\w+\b', text.lower()))

    res_tokens = tokenize(resume_text)
    jd_tokens = tokenize(job_description)
    
    # 1. Keyword Match (Base Score)
    matches = res_tokens.intersection(jd_tokens)
    keyword_score = (len(matches) / len(jd_tokens)) * 100 if jd_tokens else 0
    
    # 2. Length & Density Check
    word_count = len(resume_text.split())
    length_penalty = 0
    if word_count < 200: length_penalty = 15 # Too short
    if word_count > 1000: length_penalty = 10 # Too long
    
    # 3. Final Calculation
    final_score = (keyword_score * 0.9) - length_penalty
    return max(0, min(100, round(final_score, 2)))