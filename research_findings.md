# Research findings (SIMULATED DATA)

> **These findings come from a synthetic dataset of 1,000 simulated students created to test the pipeline.
> They are not findings about real students. The dataset contains no genuine questionnaire responses and its
> timestamps are not real submission times.** Every number below is traceable to
> `student_academic_performance_synthetic_1000.csv` through `analysis_notebook.ipynb` (outputs in `results/`).

## Dataset
- 1000 rows, 17 columns, `data_source = SYNTHETIC`; 60 missing cells in 59 rows; 0 duplicate IDs; 0 out-of-range values.
- Target rule (fixed before modelling, applied only to `current_performance`): High >= 60, Medium 50-59.9, Low < 50. Rows disagreeing with the rule: 0.
- Classes: Low 264 (26.4%), Medium 381 (38.1%), High 355 (35.5%).

## Observations (simulated data only)
- Class balance: Low 264 (26.4%), Medium 381 (38.1%), High 355 (35.5%). The largest class is 38.1% of rows, so the simulated data is only mildly imbalanced.
- Study hours: median 9.0 (Low), 12.0 (Medium), 15.0 (High) hours per week; Kruskal-Wallis H = 109.42, p <0.001. The ranges overlap heavily (see box plots), so no category is separable on study hours alone.
- Attendance, assignment completion and sleep show the same ordering (Low < Medium < High in the medians); social media use runs the other way (median 4.05 for Low vs 3.3 for High hours per day).
- Correlations with current performance: assignment completion 0.367, study hours 0.355, attendance 0.303, sleep 0.201, social media -0.164, number of courses 0.021, previous performance 0.643.
- Year of study, study location and internet access showed no clear association with category in this file (chi-square p = 0.932, 0.959 and 0.367 respectively).
- Previous performance is the strongest single correlate of current performance (r = 0.643, n = 984); see the redundancy check in the cleaning report.
- On a single stratified 80:20 split (test n = 200), test macro-F1 was 0.184 for the majority baseline, 0.556 for Logistic Regression and 0.549 for Random Forest. Cross-validated macro-F1 on the training part was 0.570 (SD 0.021) and 0.580 (SD 0.017). The gap between the two models is smaller than the fold-to-fold spread, so neither is shown to be better. These runs only prove the pipeline works.

## Pipeline test results (single 80:20 split, not evidence of real-world performance)
| Model | CV macro-F1 (train, mean ± SD) | Test accuracy | Test macro-F1 |
|---|---|---|---|
| Majority baseline | 0.184 ± 0.000 | 0.380 | 0.184 |
| Logistic Regression | 0.570 ± 0.021 | 0.560 | 0.556 |
| Random Forest | 0.580 ± 0.017 | 0.555 | 0.549 |

## Previous performance redundancy check
Previous vs current performance: Pearson r = 0.643. Test macro-F1 (LR / RF): all predictors 0.556 / 0.549; without previous performance 0.454 / 0.462; previous performance only 0.570 / 0.561.

## Limitations
- Synthetic data: relationships reflect the simulator's design, not reality.
- Real data will be small (50-150), self-reported and voluntary; estimates will be wide and selection bias is likely.
- Universities use different grading scales; mapping must be documented or flagged.
- Classification is not causation; predictions should support, never label, students.
