# Day 17 - Resume and Job Description Analyzer
print("+---------------------------------------------+")
print("| Resume and Job Description Analyzer        |")
print("+---------------------------------------------+")
skills = [
    "python",
    "javascript",
    "sql",
    "machine learning",
    "data analysis",
    "git",
    "docker",
    "aws",
    "rest api"
]
print("\n Enter your resume text")
resume_text = input(">>")
print("\n Enter the job description text")
job_text = input(">>")
resume_text=resume_text.lower()
job_text=job_text.lower()
resume_skills = []

for skill in skills:
    if skill in resume_text:
        resume_skills.append(skill)

job_skills = []
for skill in skills:
    if skill in job_text:
        job_skills.append(skill)

matched_skills = []
for skill in resume_skills:
    if skill in job_skills:
        matched_skills.append(skill)

missed_skills = []
for skill in job_skills:
    if skill not in resume_skills:
        missed_skills.append(skill)

if len(job_skills) > 0:
    match_score = (len(matched_skills) / len(job_skills)) * 100
else:
    match_score = 0

print("\n" + "=" * 45)
print("             ANALYSIS REPORT")
print("=" * 45)

print("\nMatched Skills:")
for skill in matched_skills:
    print("✓", skill.title())

print("\nMissing Skills:")
for skill in missed_skills:
    print("✗", skill.title())

print("\nMatch Score:", round(match_score, 2), "%")
print("Skills Matched:", len(matched_skills), "/", len(job_skills))

print("=" * 45)