"""
Generate a SYNTHETIC dataset (1,000 simulated students) for testing the research pipeline.
NOT genuine questionnaire data. Every row carries data_source = SYNTHETIC.

Simulation design (documented for transparency):
  * Each simulated student has latent traits (conscientiousness, prior ability, resources).
  * Behavioural predictors are drawn from those traits plus substantial independent noise.
  * current_performance (mean % score, most recent semester) is simulated from prior ability,
    behaviours and a large random term, so predictors are informative but NOT deterministic.
  * performance_category is then derived ONLY from current_performance using fixed thresholds
    (Kenyan university percentage scheme). It is never computed from the predictors.
"""
import numpy as np, pandas as pd
from pathlib import Path

SEED = 20261112
rng = np.random.default_rng(SEED)
N = 1000
OUT = Path(__file__).resolve().parent.parent

universities = {  # name: (weight, type)
    "University of Nairobi": (11, "Public"), "Kenyatta University": (10, "Public"),
    "Moi University": (7, "Public"), "Jomo Kenyatta University of Agriculture and Technology": (9, "Public"),
    "Egerton University": (6, "Public"), "Maseno University": (5, "Public"),
    "Technical University of Kenya": (5, "Public"), "Dedan Kimathi University of Technology": (4, "Public"),
    "Masinde Muliro University of Science and Technology": (4, "Public"), "Multimedia University of Kenya": (4, "Public"),
    "Strathmore University": (6, "Private"), "United States International University-Africa": (4, "Private"),
    "Mount Kenya University": (8, "Private"), "Daystar University": (3, "Private"),
    "Catholic University of Eastern Africa": (3, "Private"), "KCA University": (4, "Private"),
    "Africa Nazarene University": (2, "Private"), "Kabarak University": (3, "Private"),
    "Other (not listed)": (2, "Other"),
}
programmes = {
    "BSc Computer Science": 10, "BSc Information Technology": 8, "Bachelor of Commerce": 12,
    "BSc Nursing": 7, "Bachelor of Education (Arts)": 9, "Bachelor of Education (Science)": 6,
    "BSc Civil Engineering": 6, "BSc Electrical and Electronic Engineering": 6, "Bachelor of Laws (LLB)": 5,
    "BSc Agriculture": 5, "Bachelor of Medicine and Surgery (MBChB)": 3, "BA Economics": 5,
    "BSc Statistics and Data Science": 4, "BSc Mathematics": 3, "BA Journalism and Mass Communication": 4,
    "BSc Biochemistry": 3, "Bachelor of Business Information Technology": 4,
}
unis = list(universities); uw = np.array([universities[u][0] for u in unis], float); uw /= uw.sum()
progs = list(programmes); pw = np.array(list(programmes.values()), float); pw /= pw.sum()

def clip(x, lo, hi): return np.clip(x, lo, hi)

university = rng.choice(unis, N, p=uw)
programme = rng.choice(progs, N, p=pw)
year = rng.choice([1, 2, 3, 4, 5], N, p=[0.22, 0.26, 0.26, 0.20, 0.06])
# MBChB/Engineering are longer programmes: allow year 5 more often only there
long_prog = np.isin(programme, ["Bachelor of Medicine and Surgery (MBChB)", "BSc Civil Engineering", "BSc Electrical and Electronic Engineering"])
year = np.where((year == 5) & ~long_prog, 4, year)

# latent traits
conscient = rng.normal(0, 1, N)
ability = rng.normal(0, 1, N)
resources = rng.normal(0, 1, N)

internet = rng.random(N) < clip(0.80 + 0.07 * resources, 0.5, 0.97)
study_hours = clip(np.round(12 + 4.5 * conscient + 1.5 * ability + rng.normal(0, 6, N)), 0, 60)
attendance = clip(np.round(76 + 8 * conscient + 2 * ability + rng.normal(0, 11, N)), 20, 100)
assign = clip(np.round(78 + 9 * conscient + 3 * ability + rng.normal(0, 13, N)), 10, 100)
sleep = clip(np.round(6.6 + 0.3 * conscient + rng.normal(0, 1.1, N), 1), 3.5, 10)
courses = clip(np.round(rng.normal(6.2, 1.3, N) + 0.2 * (year >= 3)), 3, 10).astype(int)
social = clip(np.round(3.6 - 0.5 * conscient + rng.normal(0, 1.6, N), 1), 0, 12)
locs = np.array(["Home", "Library", "Hostel", "Classroom", "Other"])
base = np.array([0.34, 0.24, 0.20, 0.10, 0.12])
study_location = []
for i in range(N):
    adj = np.array([-0.03, 0.06 * (conscient[i] > 0.5), 0, -0.01, -0.02 * (conscient[i] > 0.5)])
    pr = (base + adj).clip(0.02)
    study_location.append(rng.choice(locs, p=pr / pr.sum()))
study_location = np.array(study_location)

# previous semester mean % (earlier period), driven mainly by ability + conscientiousness
prev = clip(np.round(57 + 7.5 * ability + 3 * conscient + rng.normal(0, 6, N), 1), 25, 95)
# current semester mean % : persistence of ability, behaviours, plus large noise
cur = (0.55 * (prev - 57) + 57
       + 0.12 * (study_hours - 12) + 0.07 * (attendance - 76) + 0.05 * (assign - 78)
       + 0.9 * (sleep - 6.6) - 0.55 * (social - 3.6) - 1.2 * (~internet)
       + rng.normal(0, 7.5, N))
cur = clip(np.round(cur, 1), 20, 98)

# --- documented grading scheme, applied ONLY to current_performance ---
# High   : >= 60  (Upper Second Class Honours and above)
# Medium : 50-59.9 (Lower Second Class)
# Low    : < 50   (Pass / marginal / fail band)
perf_cat = np.where(cur >= 60, "High", np.where(cur >= 50, "Medium", "Low"))

start, end = pd.Timestamp("2026-09-14 06:00"), pd.Timestamp("2026-10-25 23:00")
secs = rng.integers(0, int((end - start).total_seconds()), N)
ts = start + pd.to_timedelta(np.sort(secs), unit="s")

df = pd.DataFrame({
    "student_id": [f"SYN{str(i+1).zfill(4)}" for i in range(N)],
    "university": university, "programme": programme, "year_of_study": year,
    "study_hours_weekly": study_hours.astype(float), "attendance_percentage": attendance.astype(float),
    "assignment_completion_percentage": assign.astype(float), "sleep_hours": sleep,
    "internet_access": np.where(internet, "Yes", "No"), "study_location": study_location,
    "number_of_courses": courses, "social_media_hours_daily": social,
    "previous_performance": prev, "current_performance": cur,
    "performance_category": perf_cat, "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
    "data_source": "SYNTHETIC",
})

# realistic imperfections: a small amount of missingness (skipped optional answers)
for col, p in [("sleep_hours", 0.012), ("social_media_hours_daily", 0.015), ("previous_performance", 0.020),
               ("study_hours_weekly", 0.008), ("attendance_percentage", 0.008)]:
    df.loc[rng.random(N) < p, col] = np.nan

df.to_csv(OUT / "student_academic_performance_synthetic_1000.csv", index=False, encoding="utf-8-sig")
print(df.shape); print(df.performance_category.value_counts()); print(df.isna().sum()[df.isna().sum() > 0])
