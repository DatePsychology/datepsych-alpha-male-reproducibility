# What Makes a Man Seem “Alpha”? — Reproducibility Materials

This repository contains **code, transcribed published summary statistics, statistical reconstructions, and six figures** accompanying a methodological review of Date Psychology's July 2024 essay [“What Is an ‘Alpha Male?’”](https://datepsychology.com/what-is-an-alpha-male/).

**Scope.** These are **audits and redrawn figures from published, rounded summary statistics**. They are **not an independent replication, a corrected reanalysis of participant-level responses, or a new meta-analysis**. The survey microdata, original analysis code, full stimulus assignment details, and cell-level sampling variances were not available for this work. The package therefore deliberately does **not** manufacture raw observations, confidence intervals, within-condition correlations, or corrected mixed-model p-values.

The repository follows the organization of the companion [Date Psychology status-signals reproducibility project](https://github.com/DatePsychology/datepsych-status-signals-reproducibility): plainly documented inputs, a standalone script, reference output, and the accompanying figure files.

## Files

| File | Purpose |
| --- | --- |
| `reproduce_alpha_male_figures.py` | Reads the CSVs; checks the published summary-statistic arithmetic; regenerates Figures 1–6 and `reconstruction_results.txt`. |
| `published_vignette_means.csv` | All 36 published cell means (six ratings × three profiles × two framing conditions), transcribed from Alexander's Table 1. |
| `published_anova_tests.csv` | ANOVA F statistics and degrees of freedom as printed in Alexander's post; the problematic sex labels are preserved as published. |
| `questionnaire_group_means.csv` | Sex-labeled means for attractiveness, money, and status from Table 4. |
| `questionnaire_tukey_intervals.csv` | Tukey differences and confidence limits as printed in Table 5, including a suspicious interval explicitly flagged in its note. |
| `courtright_meta_summary.csv` | Selected published meta-analytic estimates, 95% confidence limits, numbers of correlations, and rated targets; these are *copied pooled statistics*, not newly meta-analyzed effects. |
| `reconstruction_results.txt` | Reference output detailing the degrees-of-freedom checks, partial η² calculations, sex-label reconstruction, pooled-mean check, and confidence-interval issue. |
| `figure_01_attractiveness.png` | Attractiveness ratings of the three photograph-and-description profiles. |
| `figure_02_alpha.png` | Published alpha-rating means. |
| `figure_03_status.png` | Published perceived-status means. |
| `figure_04_long_term.png` | Respondents' predictions about women's long-term preferences. |
| `figure_05_short_term.png` | Respondents' predictions about women's short-term preferences. |
| `figure_06_leadership_meta.png` | Published corrected correlations from Courtright et al., with leadership-emergence subgroups and a separately labeled effectiveness outcome. |
| `requirements.txt` | Python dependencies. |
| `SOURCES_AND_METHODS.md` | Input provenance, calculations, limitations, and reporting caveats. |
| `.gitignore` | Excludes common local Python and editor artifacts. |

## Reproduce the figures and results

Use **Python 3.10 or later**:

```bash
python -m pip install -r requirements.txt
python reproduce_alpha_male_figures.py
```

The script reads the CSVs in this directory, prints the numerical audit, and regenerates the six PNGs plus `reconstruction_results.txt`. It will **overwrite** files with those names when run in the repository directory. To keep the checked-in outputs untouched:

```bash
python reproduce_alpha_male_figures.py --output-dir regenerated
```

The figures use the article's dark-navy/teal visual system and reproduce its **data, figure concepts, and six-panel sequence**. Minor differences in font rendering can occur across operating systems; figure pixels are not intended to be a platform-independent checksum. All figures are **descriptive** unless their caption explicitly identifies externally published confidence intervals.

## Key reproducible numerical checks

- **Repeated observations and reported ANOVA dfs:** 238 people × 3 vignettes = 714 ratings. An ordinary independent-cell 2 × 3 ANOVA would yield `714 − 6 = 708` residual degrees of freedom; a one-way analysis of three repeated questionnaire categories treated as independent would yield `714 − 3 = 711`. Both match the paper. This is **strong circumstantial evidence**, **not proof** of the software procedure used.
- **Effect-size labels:** From the published F statistics, the values `0.151`, `0.007`, and `0.026` reconstruct as **partial η²** under the stated ANOVA dfs; these are not an additive decomposition of variance.
- **Alpha-rating differences:** Attractive minus unattractive framing gives `2.12` (prosocial), `1.25` (wealthy playboy), and `0.82` (antisocial). These are differences in **descriptive published means**, not tested within-person contrasts.
- **Sex-label discrepancy:** Table 4 means and two or more internally consistent Tukey limits reproduce approximately `F(2,549)=65.13` for the group *labeled men* and `F(2,159)=8.99` for the group *labeled women*. The narrative prints the sex labels against the opposite statistics. Swapped labels in the narrative are the most plausible explanation; **the original respondents' sex coding is not independently verifiable**.
- **Additional Table 5 issue:** The published female-group `Status − Money = 4.54` interval `[1.20, 7.08]` has midpoint `4.14`, inconsistent with the reported difference. This interval is **not used** to infer the residual variance.
- **Money t-test interval:** The published sex difference, `t=1.13` with Welch `df=73.59`, and rounded means give a 95% interval approximately `[-0.81, 2.93]`, not the published `[-0.81, 5.54]`.
- **Leadership context:** The forest plot redraws **published corrected true-score correlations ρ**, not simple observed correlations `r`; it does **not** estimate meta-analytic effects anew.

For the formulas, individual input sources, and further caveats, see [`SOURCES_AND_METHODS.md`](SOURCES_AND_METHODS.md) and [`reconstruction_results.txt`](reconstruction_results.txt).

## What cannot be independently reproduced

The published material does not permit the corrected mixed-effects/repeated-measures ANOVAs, independent tests of `sex × condition × vignette`, within-condition analysis of the pooled `r = .90` correlation, assessment of the original randomization, or uncertainty intervals around individual vignette cells. The Courtright plot likewise redraws published meta-analytic estimates rather than re-running an effect-level meta-analysis.

This limitation is substantive, not a software shortcoming. We prefer transparent uncertainty to invented data.

## Principal sources

1. Alexander (July 16, 2024), [“What Is an ‘Alpha Male?’”](https://datepsychology.com/what-is-an-alpha-male/) — Tables 1, 4, 5 and statistical results in the article.
2. Courtright, S. H., et al., *The Beauty Bias and Leader Emergence: A Theoretical Integration, Extension, and Meta-Analysis*, *Journal of Management* (2026), [DOI: 10.1177/01492063251330199](https://doi.org/10.1177/01492063251330199) — Tables 3, 5, 6 and the discussion of effectiveness.

The critique contains broader references on dominance, prestige, mate selection, and Dark Triad traits. **No third-party study PDFs, webpage copies, participants' data, or original stimulus photographs are redistributed here.**
