# Student Academic Performance: data collection and analysis workflow

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
