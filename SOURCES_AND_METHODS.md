# Data provenance, calculations, and interpretation

## 1. Provenance

**Alexander (2024):** https://datepsychology.com/what-is-an-alpha-male/

- `published_vignette_means.csv`: Table 1, which reports six outcomes for three vignette descriptions in each of the two conditions. One record per outcome and vignette, with two condition columns. Original article labels `ST Desire` and `LT Desire` are expanded here to `Short-term desirability prediction` and `Long-term desirability prediction`, to prevent confusing respondents' beliefs with observed mating behavior.
- `published_anova_tests.csv`: F and df printed under **Statistical Tests**, **Questionnaire Traits of Alphaness**, and **Sex Differences in Questionnaire Scores**.
- `questionnaire_group_means.csv`: Table 4, sex-labelled category means.
- `questionnaire_tukey_intervals.csv`: Table 5, reported Tukey differences, intervals, and p-values, *including possible transcription/author errors preserved as printed*.

**Courtright et al., *The Beauty Bias and Leader Emergence* (2025 online / 2026 issue):** https://doi.org/10.1177/01492063251330199

- `courtright_meta_summary.csv`: Table 3 (overall leader emergence, N, k, corrected ρ, CI and I²), Table 5 (informal and formal leadership emergence), Table 6 (formal emergence broken into subjective judgments and actual role attainment), and the discussion for leadership effectiveness (only three studies, N=138, ρ≈.10 and CI approximately [-.004,.21]). `k` denotes the number of correlations, not necessarily nonoverlapping samples; `N` refers to the numbers of rated leader *targets* used in the published aggregation, not the number of raters. Values are printed to the precision the article provides. The aggregate rows and their subgroups are **not independent datasets**, and should not be summed.
- Uncorrected `r` and attenuation-corrected `ρ` are different quantities. We plot the latter and make no attempt to recompute reliability corrections or pooled estimates without study-level data.

## 2. Why the reported df pattern is notable but not conclusive

The article reports `N = 238` participants, each evaluating three profiles. If the 714 resulting alpha ratings are modeled as six independent groups (2 randomized framing conditions × 3 within-subject profiles), a two-way ordinary ANOVA has `714-6 = 708` error degrees of freedom. That matches all three published tests of condition, vignette, and their interaction: `F(1,708) = 126.02`, `F(2,708) = 2.41`, and `F(2,708) = 9.60`.

The repeated questionnaire category totals give `238×3−3 = 711` under an ordinary independent one-way ANOVA, matching `F(2,711) = 62.86`. The sex-specific denominators of 159 and 549 match `3×54−3` and `3×184−3`.

The matches are difficult to explain casually, but they do not prove exactly which software call or data structure generated the output. Participant-level repeated measurements typically require a model accounting for within-person covariance. We **do not** assert that all p-values must be inflated; the direction of the error depends on the tested contrast and the covariance structure. A corrected p-value is **not reconstructible** here.

## 3. Partial η² from reported tests

For a conventional ANOVA, `partial_eta_squared = (F × df_effect)/(F × df_effect + df_error)`.

Using the printed statistics gives approximately `.151099`, `.006762`, and `.026403`. These match `.151`, `.007`, and `.026`, suggesting the reported η² labels are actually **partial** η². Such estimates are not independent shares summing to 100%, and the inference remains conditional on the model.

## 4. Reconstructing the questionnaire F tests

For three categories with the **same hypothetical number n of independent ratings in each category**, the 95% Tukey contrast interval has half-width:

`h = q(.95; k=3, df_error) × sqrt(MSE/n)`.

Solving for the pooled within-category variance gives:

`MSE = n × (h/q)²`.

Given three printed category means `m1, m2, m3`, the inferred ordinary one-way ANOVA statistic is:

`F = [n × Σ(mi − mean(m))² / (3−1)] / MSE`.

The Table 4 group *labeled men* has means `[28.13, 23.30, 27.74]`; setting `n=184` and using the consistent Table 5 CI half-width of 1.105 reconstructs `F≈65.13` with `df=(2,549)`. The group *labeled women* has means `[24.22, 22.24, 26.78]`; with `n=54` and consistent half-width 2.54, the reconstructed `F≈8.99` with `df=(2,159)`. The prose's ANOVA assignment names these groups in the opposite order, probably due to a label swap in the prose.

**Caveats:** This reconstruction tests an explicitly stated *independent-cell* model, not a corrected repeated-measures model. Input means and CI endpoints are rounded. It is possible for other models to have similar output. Most importantly, matching group labels in printed tables does **not** establish original participant sex classifications.

### Independent Table 5 data-quality issue

The row for women, `Status − Money = 4.54`, reports the interval `[1.20, 7.08]`. Its midpoint is `(1.20+7.08)/2=4.14`, **not 4.54**, and its half-width differs from the two other female contrasts. To avoid silently repairing the source, we preserve the original interval in the CSV and exclude it from the equal-width MSE calculation. The other two female intervals are each centered on their reported differences and have half-width 2.54.

### Weighted-mean consistency check

If the sex labels in Table 4 are as printed, assigning `184` to the group labeled Men and `54` to Women yields attractiveness-category mean `(184×28.13+54×24.22)/238 ≈27.24`, consistent with the article's pooled Figure 6 (~27.2). Reversing weights gives ≈25.11. This reinforces, **but does not prove**, the inference that the *ANOVA sentence*, not the Table 4 labels, was swapped.

## 5. Welch confidence interval sanity check

The text reports the sex difference in money questionnaire scores at `t(73.59)=1.13`, a mean difference of `23.30−22.24=1.06`, and a 95% CI `[-0.81,5.54]`. Assuming the conventional two-sided Welch interval, reconstruct `SE≈abs(1.06/1.13)` and `margin=t(.975,73.59)×SE`, giving approximately `[-0.81,2.93]`. Because both the mean difference and t statistic are rounded, this is an **approximation**, but the published upper endpoint of 5.54 is not compatible with the center of the interval and test statistic.

## 6. Figures and limits

- **Figures 1–5:** Descriptive bar charts of the published Table 1 means only. We use the common displayed y-range `0–7`, with an explicitly stated caveat that the exact source response anchors are not adequately documented. We cannot attach correct participant-level confidence intervals or formal cross-cell comparison p-values.
- **Figure 1:** Attractiveness ratings reflect *photo-plus-description* stimuli, not attractiveness rated independently of the text. Thus it does not isolate whether face identity, narrative context, or both produced differences.
- **Figures 4–5:** Third-person predictions about preferences of women, not sampled women making consequential actual choices.
- **Figure 6:** The Courtright et al. published corrected meta-analytic associations and 95% CIs. The subjective and objective rows are subgroups of formal emergence, and their study sets may overlap with other rows. Effectiveness is a **separate outcome** based on very little evidence. Large cross-study heterogeneity (overall I² ~61%) must be kept in view. Do not compare corrected ρ values as if they were uncorrected r values.

## 7. Missing information

The present data cannot identify the isolated causal effect of *physical attractiveness itself* (versus social-proof assertions and attractiveness of partners); correct the repeated-measures analyses; estimate a within-condition correlation for the published `r=.90`; test alpha/beta latent-factor structure; reproduce original qualitative coding; or establish real-world mate choice or social leadership. All would require richer stimulus documentation, participant-level responses, and/or new experimental or behavioral data.

## 8. Copyright and scope

The repository redistributes **only transcribed summary data from publicly reported tables, independently written calculation code, and newly rendered charts**. It does not archive the original post's embedded images, full original text, study PDFs, or human-subject records. The literature discussion in the companion article is targeted and non-systematic.
