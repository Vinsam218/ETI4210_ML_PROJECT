import json, sys
from pathlib import Path
import matplotlib
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, PageBreak, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
sys.path.insert(0, str(Path(__file__).parent))
import form_spec as FS

ROOT = Path(__file__).resolve().parent.parent
S = json.load(open(ROOT / "results/summary.json"))
fdir = Path(matplotlib.get_data_path()) / "fonts/ttf"
pdfmetrics.registerFont(TTFont("DV", str(fdir / "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DVB", str(fdir / "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFontFamily("DV", normal="DV", bold="DVB", italic="DV", boldItalic="DVB")

BLUE = colors.HexColor("#2a78d6"); INK = colors.HexColor("#0b0b0b"); GREY = colors.HexColor("#52514e"); LIGHT = colors.HexColor("#f0efec")
base = ParagraphStyle("b", fontName="DV", fontSize=9, leading=13, textColor=INK)
small = ParagraphStyle("s", parent=base, fontSize=7.5, leading=10, textColor=GREY)
cell = ParagraphStyle("c", parent=base, fontSize=7.5, leading=9.5)
cellb = ParagraphStyle("cb", parent=cell, fontName="DVB")
h1 = ParagraphStyle("h1", parent=base, fontName="DVB", fontSize=15, leading=19, spaceBefore=6, spaceAfter=6)
h2 = ParagraphStyle("h2", parent=base, fontName="DVB", fontSize=11.5, leading=15, spaceBefore=10, spaceAfter=4, textColor=BLUE)
title = ParagraphStyle("t", parent=base, fontName="DVB", fontSize=21, leading=26, spaceAfter=8)
banner_st = ParagraphStyle("bn", parent=base, fontName="DVB", fontSize=8.5, leading=12, textColor=colors.HexColor("#8a2b0e"))
P = lambda t, st=base: Paragraph(t, st)

def banner(text):
    t = Table([[P(text, banner_st)]], colWidths=[17 * cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fdeee8")), ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#eb6834")),
                           ("LEFTPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    return t
def table(rows, widths=None, header=True, fs=7.5):
    data = [[P(str(c), cellb if (header and i == 0) else cell) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    st = [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#c3c2b7")), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4), ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]
    if header: st += [("BACKGROUND", (0, 0), (-1, 0), LIGHT)]
    t.setStyle(TableStyle(st)); return t
def img(name, width=15.5 * cm, cap=None):
    w, h = Image.open(ROOT / "charts" / name).size
    items = [RLImage(str(ROOT / "charts" / name), width=width, height=width * h / w)]
    if cap: items.append(P(cap, small))
    return KeepTogether(items + [Spacer(1, 8)])
def footer(c, d):
    c.saveState(); c.setFont("DV", 7); c.setFillColor(GREY)
    c.drawString(2 * cm, 1.2 * cm, d.footer_txt); c.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"Page {d.page}"); c.restoreState()
def build(path, story, ftxt):
    d = SimpleDocTemplate(str(path), pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.8 * cm, bottomMargin=2 * cm)
    d.footer_txt = ftxt; d.build(story, onFirstPage=footer, onLaterPages=footer)
pv = lambda p: "<0.001" if p < 0.001 else f"{p:.3f}"
SIMTXT = ("SIMULATED DATA NOTICE: all results in this document are calculated from a synthetic dataset created to test the research pipeline. "
          "They are not findings about real students, and the dataset contains no genuine questionnaire responses.")

# =============== questionnaire.pdf ===============
st = [P(FS.TITLE, title), P("Research questionnaire (final design). Anonymous, voluntary, about 10-12 minutes.", base), Spacer(1, 6),
      P(FS.DESCRIPTION, base), Spacer(1, 6),
      banner("Status: this PDF is the questionnaire design. The Google Form must be created by running google_form_apps_script.gs (see README). "
             "No form has been created and no responses have been collected."), Spacer(1, 8),
      P("Please do not enter your name, registration number, telephone number or email address anywhere in this form.", base)]
cur = None
for q in FS.Q:
    if q["sec"] != cur:
        cur = q["sec"]; st.append(P(f"Section {cur}: {q.get('secname', '')}", h2))
    blk = [P(("<b>" + q["text"] + "</b>") + ("" if q["req"] else " <i>(optional)</i>"), base)]
    if q.get("help"): blk.append(P(q["help"], small))
    t = q["type"]
    if t in ("mc", "dropdown"):
        blk.append(P(("Choose one (dropdown): " if t == "dropdown" else "Choose one: ") + "  |  ".join(("○ " if t == "mc" else "") + o for o in q["opts"]), cell))
    elif t == "checkbox":
        blk.append(P("Select all that apply: " + "  |  ".join("☐ " + o for o in q["opts"]) + ("  |  ☐ Other: ______" if q.get("other") else ""), cell))
    elif t == "scale":
        blk.append(P(f"Scale {q['lo']} ({q['lolabel']}) to {q['hi']} ({q['hilabel']}):  " + "   ".join(f"○ {i}" for i in range(q["lo"], q["hi"] + 1)), cell))
    elif t == "number":
        blk.append(P(f"Number between {q['lo']} and {q['hi']}: ________", cell))
    else:
        blk.append(P("Short answer: ______________________", cell))
    blk.append(Spacer(1, 5)); st.append(KeepTogether(blk))
st += [PageBreak(), P("Researcher notes (not shown to respondents)", h1),
       P("Target variable and grading scheme", h2),
       P("The performance category is derived from question 30 (current semester average) <b>only</b>, using thresholds fixed before any model is trained. "
         "It is never calculated from study hours, attendance, assignment completion or any other predictor.", base), Spacer(1, 4),
       table([["Category", "Mean score (%)", "Kenyan degree-classification analogue", "Matching band in Q30b"],
              ["High", "60 and above", "Upper Second Class and above", "70%+ and 60-69%"],
              ["Medium", "50 to 59.9", "Lower Second Class", "50-59%"],
              ["Low", "Below 50", "Pass band / marginal / failing", "40-49% and Below 40%"]], [2.5 * cm, 3 * cm, 6.5 * cm, 5 * cm]),
       Spacer(1, 6),
       P("Grading-scale harmonisation (limitation, not an assumption)", h2),
       P("Kenyan universities do not all use the same scale. Respondents state the format they used (Q27a, Q30a) and the band their university maps it to (Q30b). "
         "Percentage means map directly to the thresholds above. GPA responses should be converted only through the institution's published conversion table, "
         "and responses whose scale cannot be defensibly mapped must be excluded or analysed separately, and this must be reported as a limitation. "
         "Do not assume that a 3.0/4.0 GPA at one university equals a 3.0/5.0 GPA at another.", base),
       P("Previous vs current performance (leakage control)", h2),
       P("Question 27 asks about the semester <b>before</b> the most recently completed semester, and question 30 about the most recent one, so previous performance refers to an "
         "earlier period. Previous performance is nevertheless expected to correlate with the target and must be tested for redundancy (refit without it).", base),
       P("Questionnaire to dataset variable mapping", h2),
       table([["Item", "Dataset variable", "Role"]] + [[q["id"], q["var"], ("target source" if q["id"] in ("I30", "I30b") else "predictor" if q["var"] in
              ("study_hours_weekly","attendance_percentage","assignment_completion_percentage","sleep_hours","internet_access","study_location","social_media_hours_daily","previous_performance") else "background / supplementary")] for q in FS.Q],
             [2.2 * cm, 8 * cm, 6.8 * cm]),
       Spacer(1, 4), P("Number of courses (a planned predictor) is not asked in the question list supplied; add one numeric item (e.g. 'How many courses/units are you taking this semester?') if it is to be used.", small)]
build(ROOT / "questionnaire.pdf", st, "Student Learning Habits and Academic Performance Survey: questionnaire design")

# =============== data_dictionary.xlsx ===============
cols = [
 ("student_id", "Anonymous synthetic identifier (SYN0001-SYN1000)", "Text", "Unique", "n/a (synthetic)", "Identifier: never a feature"),
 ("university", "Simulated university affiliation", "Categorical", "19 categories (18 named Kenyan universities + Other)", "A1", "Administrative: excluded from features"),
 ("programme", "Academic programme", "Categorical", "17 programmes", "A2", "Administrative: excluded from features"),
 ("year_of_study", "Current year of study", "Integer", "1-5", "A3", "Descriptive: not a planned predictor"),
 ("study_hours_weekly", "Weekly independent study hours", "Numeric", "0-80 hours", "B6", "Predictor"),
 ("attendance_percentage", "Share of scheduled lectures attended", "Numeric", "0-100 %", "C11", "Predictor"),
 ("assignment_completion_percentage", "Share of assignments submitted before deadline", "Numeric", "0-100 %", "D14", "Predictor"),
 ("sleep_hours", "Average nightly sleep", "Numeric", "2-14 hours", "E17", "Predictor"),
 ("internet_access", "Reliable internet access for academic work", "Categorical", "Yes / No", "F20", "Predictor"),
 ("study_location", "Preferred study location", "Categorical", "Home / Library / Hostel / Classroom / Other", "B8", "Predictor"),
 ("number_of_courses", "Courses taken this semester", "Integer", "1-12", "(item to be added)", "Predictor"),
 ("social_media_hours_daily", "Daily social media hours", "Numeric", "0-16 hours", "G24", "Predictor"),
 ("previous_performance", "Mean score (%) in the earlier semester", "Numeric", "0-100 %", "H27", "Predictor (test for redundancy with target)"),
 ("current_performance", "Mean score (%) in the most recent completed semester", "Numeric", "0-100 %", "I30", "Source of the target: NEVER a feature (leakage)"),
 ("performance_category", "Low / Medium / High derived from current_performance", "Categorical (target)", "Low <50; Medium 50-59.9; High >=60", "I30 / I30b", "Target (y)"),
 ("timestamp", "SIMULATED response timestamp (not a real submission time)", "Datetime", "2026-09-14 to 2026-10-25", "n/a (synthetic)", "Administrative: excluded from features"),
 ("data_source", "Provenance flag", "Text", "SYNTHETIC", "n/a", "Provenance: excluded from features"),
]
miss = {r["variable"]: r["missing"] for r in S["validation"]}
wb = Workbook(); ws = wb.active; ws.title = "Data dictionary"
hdr = ["Variable", "Description", "Type", "Allowed values / range", "Questionnaire item", "Role in analysis", "Missing values (synthetic file)"]
ws.append(hdr)
for c in cols: ws.append(list(c) + [miss.get(c[0], 0)])
hf = PatternFill("solid", fgColor="2A78D6"); thin = Side(style="thin", color="C3C2B7")
def style(ws, widths):
    for c in ws[1]: c.font = Font(bold=True, color="FFFFFF"); c.fill = hf; c.alignment = Alignment(wrap_text=True, vertical="center")
    for row in ws.iter_rows():
        for c in row: c.alignment = Alignment(wrap_text=True, vertical="top"); c.border = Border(top=thin, bottom=thin, left=thin, right=thin)
    for i, w in enumerate(widths, 1): ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "A2"
style(ws, [30, 48, 18, 40, 18, 40, 16])
w2 = wb.create_sheet("Grading scheme")
for r in [["Category", "Mean score (%)", "Kenyan classification analogue"], ["High", ">= 60", "Upper Second Class and above"],
          ["Medium", "50 - 59.9", "Lower Second Class"], ["Low", "< 50", "Pass band / marginal / failing"]]: w2.append(r)
w2.append([]); w2.append(["Applied only to current_performance. Thresholds fixed before modelling. Universities' scales differ: map with institutional tables or flag as a limitation."])
style(w2, [18, 20, 50])
w3 = wb.create_sheet("Questionnaire items")
w3.append(["Item", "Dataset variable", "Question text", "Type", "Options / range", "Required"])
for q in FS.Q:
    opt = "; ".join(q["opts"]) if q.get("opts") else (f"{q['lo']}-{q['hi']}" if "lo" in q else "")
    w3.append([q["id"], q["var"], q["text"], q["type"], opt, "Yes" if q["req"] else "No"])
style(w3, [8, 34, 70, 12, 70, 10])
w4 = wb.create_sheet("README")
for line in ["SYNTHETIC dataset for pipeline testing. Not real questionnaire responses.", "Timestamps are simulated and are not real submission times.",
             "Random seed 20261112 (scripts/generate_synthetic_data.py)."]: w4.append([line])
w4.column_dimensions["A"].width = 100
wb.save(ROOT / "data_dictionary.xlsx")

# =============== data_cleaning_report.pdf ===============
vrows = [["Variable", "Allowed range", "Observed min", "Observed max", "Missing (n)", "Missing (%)", "Out of range (n)"]]
for r in S["validation"]: vrows.append([r["variable"], r["allowed"], r["min"], r["max"], r["missing"], r["missing_%"], r["out_of_range"]])
drows = [["Variable", "Mean", "SD", "Min", "Median", "Max", "Missing", "IQR outliers"]]
for r in S["descriptives"]: drows.append([r["variable"], r["mean"], r["std"], r["min"], r["50%"], r["max"], r["missing"], r["iqr_outliers"]])
ab = {r["feature_set"]: r for r in S["ablation"]}
c1 = [P("Data Cleaning and Quality Report", title), banner(SIMTXT), Spacer(1, 6),
      P("1. Dataset", h2),
      P(f"File: student_academic_performance_synthetic_1000.csv. Rows: {S['n_rows']}. Columns: {S['n_cols']}. "
        f"Data source flag: {', '.join(S['data_source_values'])}. Simulated timestamps span {S['ts_min']} to {S['ts_max']} and are <b>not</b> actual submission times.", base),
      P("2. Validation results", h2),
      P(f"Duplicate student identifiers: {S['duplicate_ids']}. Fully duplicated response rows (ignoring identifier): {S['duplicate_rows']}. "
        f"Rows whose category disagrees with the documented grading thresholds: {S['target_mismatches']}. "
        f"Total missing cells: {S['total_missing_cells']} across {S['rows_with_any_missing']} rows.", base), Spacer(1, 4),
      table(vrows, [4.3 * cm, 2.2 * cm, 2 * cm, 2 * cm, 2 * cm, 2 * cm, 2.5 * cm]),
      P("3. Descriptive statistics and outliers", h2),
      P("Outliers were identified with the 1.5 x IQR rule and <b>inspected, not removed</b>: values stay inside plausible ranges, and extreme but possible answers (for example long study hours) are legitimate variation.", base), Spacer(1, 4),
      table(drows, [4.3 * cm, 1.7 * cm, 1.5 * cm, 1.5 * cm, 1.7 * cm, 1.5 * cm, 1.6 * cm, 2.2 * cm]),
      P("4. Cleaning decisions", h2),
      table([["Issue", "Decision", "Reason"],
             ["Missing values (about 1% per affected column)", "Keep rows. Impute inside the modelling pipeline: median for numeric columns, most frequent for categorical columns, fitted on training data only.", "Avoids discarding rows (small samples) and avoids test-set information shaping the model."],
             ["Out-of-range values", f"None found; range rules retained for real data (percentages 0-100, sleep 2-14 h, courses 1-12, etc.).", "Validation must be re-run on genuine responses."],
             ["Duplicates", "None found. With real data check repeated submissions (identical rows within minutes).", "Anonymous forms cannot rule out repeats; flag, do not auto-delete."],
             ["Outliers", "Kept; model scaling uses standardisation (LR), none needed for Random Forest.", "Removal would shift the sample toward unrealistically tidy students."],
             ["Target definition", "Derived only from current_performance with fixed thresholds (High >=60, Medium 50-59.9, Low <50).", "Prevents the target from being reconstructed from predictors."]],
            [4 * cm, 7.5 * cm, 5.5 * cm]),
      P("5. Machine-learning readiness", h2),
      table([["Topic", "Recommendation"],
             ["Features", "Study hours, attendance, assignment completion, sleep, internet access, study location, number of courses, social media hours, previous performance (9 predictors)."],
             ["Excluded", "student_id, university, programme, year_of_study, timestamp, data_source (identifiers/administrative, no scientific justification as predictors) and current_performance (the target is derived from it: leakage)."],
             ["Missing values", "SimpleImputer (median / most frequent) inside a Pipeline, fitted on the training partition only."],
             ["Encoding", "One-hot encoding for internet_access and study_location; unseen categories ignored."],
             ["Scaling", "StandardScaler for numeric predictors (needed for regularised Logistic Regression, harmless for Random Forest)."],
             ["Split", f"Stratified 80:20 split (train {S['split']['train']}, test {S['split']['test']}), seed 42; 5-fold stratified CV on the training part for model selection; test set used once. With the planned 50-150 real students the test set will hold only about 10-30 people, so use fewer folds and report uncertainty."],
             ["Leakage prevention", "Fit every transformer inside the pipeline; never fit on the full dataset; keep current_performance and its derivatives out of X."],
             ["Class imbalance", f"Counts: Low {S['imbalance']['counts']['Low']}, Medium {S['imbalance']['counts']['Medium']}, High {S['imbalance']['counts']['High']}. Majority share {S['imbalance']['majority_share']*100:.1f}%, largest-to-smallest ratio {S['imbalance']['ratio_max_to_min']}. Mild imbalance: use stratification and macro-F1; consider class_weight only if a class becomes small in real data."]],
            [3.2 * cm, 13.8 * cm]),
      P("6. Is previous performance redundant with the target?", h2),
      P(f"Pearson correlation between previous and current performance is {S['prev_cur_pearson']} (Spearman {S['prev_cur_spearman']}, n={S['prev_cur_n']}). "
        f"Test macro-F1 for Logistic Regression / Random Forest: all nine predictors {ab['All nine predictors']['Logistic Regression test macro-F1']:.3f} / {ab['All nine predictors']['Random Forest test macro-F1']:.3f}; "
        f"without previous performance {ab['Without previous_performance']['Logistic Regression test macro-F1']:.3f} / {ab['Without previous_performance']['Random Forest test macro-F1']:.3f}; "
        f"previous performance alone {ab['previous_performance only']['Logistic Regression test macro-F1']:.3f} / {ab['previous_performance only']['Random Forest test macro-F1']:.3f}. "
        "Previous performance carries a large share of the usable signal here. It refers to an earlier period, so it is legitimate history rather than direct leakage, but it should be reported both with and without it. "
        "These are single-split results on 200 test rows, so differences of about 0.01 are within noise. The pattern comes from the simulator's design and says nothing about real students.", base)]
build(ROOT / "data_cleaning_report.pdf", c1, "SIMULATED DATA: data cleaning report (synthetic pipeline-test dataset)")

# =============== exploratory_data_analysis.pdf ===============
fc = {r["performance_category"]: r for r in S["freq_performance_category"]}
tests = {r["variable"]: r for r in S["predictor_tests"]}
nice = {"attendance_percentage": "Attendance (%)", "study_hours_weekly": "Study hours per week", "sleep_hours": "Sleep (hours/night)",
        "assignment_completion_percentage": "Assignment completion (%)", "social_media_hours_daily": "Social media (hours/day)"}
trows = [["Predictor", "Median Low", "Median Medium", "Median High", "Mean Low", "Mean Medium", "Mean High", "Kruskal-Wallis H", "p-value"]]
for k, r in tests.items(): trows.append([nice[k], r["median_Low"], r["median_Medium"], r["median_High"], r["mean_Low"], r["mean_Medium"], r["mean_High"], r["kruskal_H"], pv(r["p_value"])])
def top(key, n=6): return [[r[key.split("|")[0]], r["count"], r["percent"]] for r in S[f"freq_{key.split('|')[0]}"][:n]]
frow = lambda k: [[k.replace("_", " ").capitalize(), "Count", "%"]] + [[r[k], r["count"], r["percent"]] for r in S[f"freq_{k}"]]
ct = lambda k: [[k.replace("_", " ").capitalize(), "Low", "Medium", "High"]] + [[r[k], r["Low"], r["Medium"], r["High"]] for r in S[f"crosstab_{k}"]]
cwc = S["corr_with_current"]
obs = [
 f"Class balance: Low {fc['Low']['count']} ({fc['Low']['percent']}%), Medium {fc['Medium']['count']} ({fc['Medium']['percent']}%), High {fc['High']['count']} ({fc['High']['percent']}%). The largest class is {S['imbalance']['majority_share']*100:.1f}% of rows, so the simulated data is only mildly imbalanced.",
 f"Study hours: median {tests['study_hours_weekly']['median_Low']} (Low), {tests['study_hours_weekly']['median_Medium']} (Medium), {tests['study_hours_weekly']['median_High']} (High) hours per week; Kruskal-Wallis H = {tests['study_hours_weekly']['kruskal_H']}, p {pv(tests['study_hours_weekly']['p_value'])}. The ranges overlap heavily (see box plots), so no category is separable on study hours alone.",
 f"Attendance, assignment completion and sleep show the same ordering (Low < Medium < High in the medians); social media use runs the other way (median {tests['social_media_hours_daily']['median_Low']} for Low vs {tests['social_media_hours_daily']['median_High']} for High hours per day).",
 f"Correlations with current performance: assignment completion {cwc['assignment_completion_percentage']}, study hours {cwc['study_hours_weekly']}, attendance {cwc['attendance_percentage']}, sleep {cwc['sleep_hours']}, social media {cwc['social_media_hours_daily']}, number of courses {cwc['number_of_courses']}, previous performance {cwc['previous_performance']}.",
 f"Year of study, study location and internet access showed no clear association with category in this file (chi-square p = {pv(S['chi2_year_of_study']['p'])}, {pv(S['chi2_study_location']['p'])} and {pv(S['chi2_internet_access']['p'])} respectively).",
 f"Previous performance is the strongest single correlate of current performance (r = {S['prev_cur_pearson']}, n = {S['prev_cur_n']}); see the redundancy check in the cleaning report.",
 f"On a single stratified 80:20 split (test n = {S['split']['test']}), test macro-F1 was {S['model_results'][0]['test_macro_f1']:.3f} for the majority baseline, {S['model_results'][1]['test_macro_f1']:.3f} for Logistic Regression and {S['model_results'][2]['test_macro_f1']:.3f} for Random Forest. Cross-validated macro-F1 on the training part was {S['model_results'][1]['cv_macro_f1_mean']:.3f} (SD {S['model_results'][1]['cv_macro_f1_sd']:.3f}) and {S['model_results'][2]['cv_macro_f1_mean']:.3f} (SD {S['model_results'][2]['cv_macro_f1_sd']:.3f}). The gap between the two models is smaller than the fold-to-fold spread, so neither is shown to be better. These runs only prove the pipeline works.",
]
e = [P("Exploratory Data Analysis", title), banner(SIMTXT), Spacer(1, 6),
     P("1. Dataset overview and sample composition", h2),
     P(f"{S['n_rows']} simulated students, {S['n_cols']} columns, {S['total_missing_cells']} missing cells ({S['rows_with_any_missing']} rows affected). Category rule: High &ge; 60, Medium 50-59.9, Low &lt; 50 (mean score %, current semester).", base), Spacer(1, 4),
     table(frow("year_of_study"), [4 * cm, 3 * cm, 3 * cm]), Spacer(1, 4),
     table(frow("performance_category"), [4 * cm, 3 * cm, 3 * cm]), Spacer(1, 4),
     table(frow("internet_access"), [4 * cm, 3 * cm, 3 * cm]), Spacer(1, 4),
     table(frow("study_location"), [4 * cm, 3 * cm, 3 * cm]),
     P("2. Descriptive statistics", h2),
     table(drows, [4.3 * cm, 1.7 * cm, 1.5 * cm, 1.5 * cm, 1.7 * cm, 1.5 * cm, 1.6 * cm, 2.2 * cm]),
     P("3. Predictors by performance category", h2),
     table(trows, [3.4 * cm, 1.6 * cm, 1.9 * cm, 1.6 * cm, 1.6 * cm, 1.9 * cm, 1.6 * cm, 2 * cm, 1.4 * cm]),
     P("Kruskal-Wallis tests are descriptive here: the dataset is simulated, so a small p-value only confirms that the pipeline detects the structure built into the simulator.", small),
     Spacer(1, 4), P("Cross-tabulations (counts)", h2),
     table(ct("year_of_study"), [4 * cm, 2.5 * cm, 2.5 * cm, 2.5 * cm]), Spacer(1, 4),
     table(ct("study_location"), [4 * cm, 2.5 * cm, 2.5 * cm, 2.5 * cm]), Spacer(1, 4),
     table(ct("internet_access"), [4 * cm, 2.5 * cm, 2.5 * cm, 2.5 * cm]),
     P("4. Preliminary observations (all calculated from the simulated file)", h2)] + [P("• " + o, base) for o in obs] + [Spacer(1, 4),
     P("5. Limitations", h2),
     P("• The data is synthetic; relationships were put there by the simulation design, so none of these patterns is evidence about real students.<br/>"
       "• Real data will be smaller (planned 50-150 students), self-reported and voluntary, so expect more noise, selection bias and measurement error.<br/>"
       "• Different university grading scales cannot be assumed equivalent; real data needs a documented mapping.<br/>"
       "• Association and prediction do not establish causation.", base), PageBreak(), P("6. Charts", h1)]
caps = [("01_students_by_university.png", "Figure 1. Students by university."), ("02_students_by_programme.png", "Figure 2. Students by programme."),
 ("03_students_by_year.png", "Figure 3. Students by year of study."), ("04_performance_category_distribution.png", "Figure 4. Performance category distribution."),
 ("05_study_hours_distribution.png", "Figure 5. Study hours."), ("06_attendance_distribution.png", "Figure 6. Attendance."),
 ("07_assignment_completion_distribution.png", "Figure 7. Assignment completion."), ("08_sleep_distribution.png", "Figure 8. Sleep duration."),
 ("09_social_media_distribution.png", "Figure 9. Social media use."), ("10_internet_access_distribution.png", "Figure 10. Internet access."),
 ("11_study_location_distribution.png", "Figure 11. Study location."), ("12_previous_vs_current_performance.png", "Figure 12. Previous vs current performance."),
 ("13_attendance_by_category.png", "Figure 13. Attendance by category."), ("14_study_hours_by_category.png", "Figure 14. Study hours by category."),
 ("15_sleep_by_category.png", "Figure 15. Sleep by category."), ("16_assignment_completion_by_category.png", "Figure 16. Assignment completion by category."),
 ("17_social_media_by_category.png", "Figure 17. Social media by category."), ("18_correlation_heatmap.png", "Figure 18. Correlation heatmap."),
 ("19_category_composition_stacked.png", "Figure 19. Category composition by year, location and internet access."),
 ("20_rf_feature_importance.png", "Figure 20. Random Forest feature importance (pipeline test)."), ("21_confusion_matrices.png", "Figure 21. Test confusion matrices (pipeline test).")]
for n, c in caps:
    w = 12.5 * cm if n.split("_")[0] in {"13","14","15","16","17","03","04","05","06","07","08","09","10","11"} else 15.5 * cm
    e.append(img(n, w, c + " SIMULATED DATA."))
build(ROOT / "exploratory_data_analysis.pdf", e, "SIMULATED DATA: exploratory data analysis (synthetic pipeline-test dataset)")

# =============== markdown files ===============
mr = S["model_results"]
md = f"""# Research findings (SIMULATED DATA)

> **These findings come from a synthetic dataset of 1,000 simulated students created to test the pipeline.
> They are not findings about real students. The dataset contains no genuine questionnaire responses and its
> timestamps are not real submission times.** Every number below is traceable to
> `student_academic_performance_synthetic_1000.csv` through `analysis_notebook.ipynb` (outputs in `results/`).

## Dataset
- {S['n_rows']} rows, {S['n_cols']} columns, `data_source = SYNTHETIC`; {S['total_missing_cells']} missing cells in {S['rows_with_any_missing']} rows; {S['duplicate_ids']} duplicate IDs; 0 out-of-range values.
- Target rule (fixed before modelling, applied only to `current_performance`): High >= 60, Medium 50-59.9, Low < 50. Rows disagreeing with the rule: {S['target_mismatches']}.
- Classes: Low {fc['Low']['count']} ({fc['Low']['percent']}%), Medium {fc['Medium']['count']} ({fc['Medium']['percent']}%), High {fc['High']['count']} ({fc['High']['percent']}%).

## Observations (simulated data only)
""" + "\n".join("- " + o for o in obs) + f"""

## Pipeline test results (single 80:20 split, not evidence of real-world performance)
| Model | CV macro-F1 (train, mean ± SD) | Test accuracy | Test macro-F1 |
|---|---|---|---|
""" + "\n".join(f"| {r['model']} | {r['cv_macro_f1_mean']:.3f} ± {r['cv_macro_f1_sd']:.3f} | {r['test_accuracy']:.3f} | {r['test_macro_f1']:.3f} |" for r in mr) + f"""

## Previous performance redundancy check
Previous vs current performance: Pearson r = {S['prev_cur_pearson']}. Test macro-F1 (LR / RF): all predictors {ab['All nine predictors']['Logistic Regression test macro-F1']:.3f} / {ab['All nine predictors']['Random Forest test macro-F1']:.3f}; without previous performance {ab['Without previous_performance']['Logistic Regression test macro-F1']:.3f} / {ab['Without previous_performance']['Random Forest test macro-F1']:.3f}; previous performance only {ab['previous_performance only']['Logistic Regression test macro-F1']:.3f} / {ab['previous_performance only']['Random Forest test macro-F1']:.3f}.

## Limitations
- Synthetic data: relationships reflect the simulator's design, not reality.
- Real data will be small (50-150), self-reported and voluntary; estimates will be wide and selection bias is likely.
- Universities use different grading scales; mapping must be documented or flagged.
- Classification is not causation; predictions should support, never label, students.
"""
open(ROOT / "research_findings.md", "w").write(md)

open(ROOT / "google_form_links.txt", "w").write("""GOOGLE FORM LINKS
=================
STATUS: NOT CREATED YET. No Google Form exists, so there is no editor link and no respondent link.

Why: this session has no connected Google Forms or Google Drive access, and browser control is not available on the current plan.
Rather than provide a mock form or invented links, the complete implementation is included:

  google_form_apps_script.gs   - run it once at https://script.google.com to create the REAL Google Form
                                 (anonymous, no email collection, linked response Google Sheet).

After you run it, the Execution log prints the three real URLs. Paste them below:

EDITOR URL    : (paste here)
RESPONDENT URL: (paste here)
RESPONSE SHEET: (paste here)

Verification still to do by you: open the respondent URL in a private window, submit one test answer,
confirm it reaches the Sheet, then delete that test row.

No responses have been collected. Nothing in this folder describes real respondents.
""")

open(ROOT / "distribution_guide.md", "w").write("""# Distributing the survey across Kenyan universities

Do this only after the form exists (see `google_form_links.txt`) and after approvals.

1. **Approvals first.** Obtain your institution's research-ethics / supervisor approval, and check each target university's requirements for surveying its students (some require permission from the Dean of Students or a registrar). Consider a research permit if the study will be published beyond coursework (NACOSTI applies to formal research in Kenya).
2. **Pilot.** Send the link to 5-10 friendly students, check timing and wording, and fix confusing items (especially grading-scale questions).
3. **Channels.** Class WhatsApp/Telegram groups via class representatives, student association and club mailing lists, departmental notice boards with a QR code, lecturers who agree to share it in e-learning platforms, and social media posts in university communities.
4. **Message template.** "We are students doing an academic research project on learning habits and academic performance. The survey takes about 10 minutes, is anonymous and voluntary. Please do not enter your name, registration number, phone or email. Link: <respondent URL>."
5. **Reach and balance.** Aim for several universities, both public and private, different programmes and years, to reduce a single-campus sample. Track counts per university in the response Sheet and push targeted reminders where a group is thin.
6. **Quality control.** Watch for duplicate submissions (identical rows close in time), implausible values and incomplete scale information; flag rather than silently delete.
7. **Be honest about limits.** A voluntary online sample is self-selected. Report this and the grading-scale issue as limitations.
8. **Privacy.** Keep the response Sheet restricted to the research team, never ask for identifiers, and delete the test row.
""")

open(ROOT / "README.md", "w").write("""# Student Academic Performance: data collection and analysis workflow

Project: *Machine Learning-Based Classification of Student Academic Performance Using Learning and Behavioural Factors*.

## Honest status
| Item | Status |
|---|---|
| Questionnaire design | Done (`questionnaire.pdf`, `form_spec.json`) |
| Real Google Form | **Not created.** No Google Forms/Drive access in this session. Run `google_form_apps_script.gs` to create it (steps inside the file and in `google_form_links.txt`) |
| Real responses | **None collected.** Nothing here describes real students |
| Synthetic dataset | Done: 1,000 simulated rows, flagged `SYNTHETIC`, for testing the pipeline only |
| Analysis and ML readiness | Done on the synthetic data (all results labelled SIMULATED) |

## Contents
| File / folder | What it is |
|---|---|
| `google_form_links.txt` | Honest status plus placeholders for the real links once you create the form |
| `google_form_apps_script.gs` | Script that creates the real, anonymous Google Form and linked response Sheet |
| `questionnaire.pdf` | Final questionnaire plus researcher notes (grading bands, variable mapping) |
| `student_academic_performance_synthetic_1000.csv` | SYNTHETIC dataset (UTF-8 with BOM, opens in Excel and pandas) |
| `data_dictionary.xlsx` | Variables, types, allowed values, roles; grading scheme; questionnaire mapping |
| `data_cleaning_report.pdf` | Validation, missing values, outliers, ML-readiness recommendations, redundancy check |
| `exploratory_data_analysis.pdf` | Tables, observations, limitations and all 21 charts (simulated) |
| `charts/` | 21 PNGs at 300 dpi |
| `analysis_notebook.ipynb` | Executed notebook (reproduces everything) |
| `results/` | CSV/JSON outputs behind every reported number (`summary.json`) |
| `research_findings.md` | Written findings, explicitly simulated |
| `distribution_guide.md` | How to distribute the real form across Kenyan universities |
| `scripts/` | Data generator, notebook builder, report builder, form spec |

## Reproduce
```bash
pip install pandas numpy matplotlib seaborn scikit-learn scipy openpyxl reportlab nbformat nbclient ipykernel
python scripts/generate_synthetic_data.py          # seed 20261112 -> the CSV
python scripts/build_notebook.py                    # writes analysis_notebook.ipynb
jupyter nbconvert --to notebook --execute --inplace analysis_notebook.ipynb   # charts/ and results/
python scripts/build_reports.py                     # PDFs, xlsx, findings, README helpers
```
Run commands from this folder.

## Using real data later
Export the response Sheet to CSV, rename columns to match `data_dictionary.xlsx`, convert grades with a documented mapping, and point the notebook's `df` at the file. Re-validate ranges, then discard every number from the synthetic run.

## Simulation design (transparency)
Behaviours are generated from latent traits plus large random noise; `current_performance` is simulated from prior ability, behaviours and noise; `performance_category` is then derived from `current_performance` only (High >= 60, Medium 50-59.9, Low < 50). Predictors are informative but not deterministic. Timestamps (2026-09-14 to 2026-10-25) are simulated.
""")
print("built")
