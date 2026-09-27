# Day 13 - Resume Skill Matcher

print("\n╔════════════════════════════════════╗")
print("║       📄 RESUME SKILL MATCHER      ║")
print("╚════════════════════════════════════╝")
print("       Match Skills. Find Gaps. 🎯")

# Get resume and job skills
resume_input = input("\nEnter your resume skills:\n>> ")
job_input = input("\nEnter job requirements:\n>> ")

# Clean and convert skills into lists
resume_skills = [
    skill.strip().lower()
    for skill in resume_input.split(",")
]

job_skills = [
    skill.strip().lower()
    for skill in job_input.split(",")
]

# Find matched and missing skills
matched_skills = []
missing_skills = []

for skill in job_skills:
    if skill in resume_skills:
        matched_skills.append(skill)
    else:
        missing_skills.append(skill)

# Calculate match percentage
match_score = (len(matched_skills) / len(job_skills)) * 100

# Display report
print("\n╔════════════════════════════════════╗")
print("║          📊 MATCH REPORT           ║")
print("╚════════════════════════════════════╝")

print("\n✅ Matched Skills:")
for skill in matched_skills:
    print("   •", skill.title())

print("\n❌ Missing Skills:")
for skill in missing_skills:
    print("   •", skill.title())

print("\n🎯 Match Score    :", round(match_score, 2), "%")
print("📌 Skills Matched :", len(matched_skills), "/", len(job_skills))

print("\n──────────────────────────────────────")
print("       Resume analysis complete! 🚀")
print("──────────────────────────────────────")
