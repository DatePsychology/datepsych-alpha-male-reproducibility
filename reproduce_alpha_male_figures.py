#!/usr/bin/env python3
"""Reproduce the published-mean figures and auditable arithmetic for
'What Makes a Man Seem Alpha?' (critique of Date Psychology, July 2024).

Usage
    python -m pip install -r requirements.txt
    python reproduce_alpha_male_figures.py
    python reproduce_alpha_male_figures.py --output-dir /path/to/test-output

This is a reconstruction from ROUNDED PUBLIC SUMMARY TABLES, not an
independent reanalysis of unshared participant-level responses.

Reproduces:
* Four original outcome charts and the attractiveness manipulation check.
* An accurately labeled redraw of Courtright et al.'s PUBLISHED
  meta-analytic estimates (no individual study synthesis is performed).
* ANOVA df-pattern arithmetic, approximate partial eta^2, independent
  reconstruction of sex-specific F tests from Tukey CI widths, a weighted
  mean check, and the flawed Welch CI endpoint.

Requires only the five small CSV files in the same directory.
"""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import studentized_range, t as tdist

HERE = Path(__file__).resolve().parent
BLUE = '#172C3D'
TEAL = '#68949A'
INK = '#283849'
MUTED = '#627586'
GRID = '#DDE5E9'

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'axes.spines.right': False,
    'axes.spines.top': False,
    'axes.spines.left': False,
    'axes.edgecolor': '#BBC6CD',
    'axes.labelcolor': INK,
    'xtick.color': MUTED,
    'ytick.color': MUTED,
    'savefig.facecolor': 'white',
    'figure.facecolor': 'white',
})


def read_csv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def fmt_num(x: float) -> str:
    return f'{x:.2f}'.rstrip('0').rstrip('.')


def outcomes() -> dict[str, dict[str, tuple[float, float]]]:
    data = {}
    for rec in read_csv('published_vignette_means.csv'):
        data.setdefault(rec['outcome'], {})[rec['vignette']] = (
            float(rec['attractive_framing_mean']),
            float(rec['unattractive_framing_mean']),
        )
    return data


def make_bar_chart(out: Path, entries: dict, *, number: int, filename: str,
                   question: str, caption: str, axis_label: str,
                   extra_note: str = '') -> None:
    profiles = ['Prosocial', 'Wealthy playboy', 'Antisocial']
    values = np.array([entries[p] for p in profiles])
    fig = plt.figure(figsize=(11.81, 10.22), dpi=100)
    fig.text(.024, .971, question, fontsize=20, fontweight='bold', color=BLUE, va='top')
    fig.text(.024, .914, f'Figure {number}  ·  {caption}', fontsize=12.7, color=MUTED, va='top')
    ax = fig.add_axes([.090, .25, .885, .56])
    xs = np.arange(3)
    bw = .35
    ax.bar(xs-bw/2, values[:,0], width=bw, color=BLUE, label='Attractive framing')
    ax.bar(xs+bw/2, values[:,1], width=bw, color=TEAL, label='Unattractive framing')
    for col, shift in [(0,-bw/2),(1,bw/2)]:
        for i, value in enumerate(values[:,col]):
            ax.text(xs[i]+shift, value + .11, fmt_num(value), ha='center', va='bottom',
                    color=INK, weight='semibold', fontsize=12.2)
    ax.set_ylim(0,7)
    ax.set_yticks(np.arange(0,8))
    ax.set_xticks(xs,profiles,fontsize=11.5)
    ax.tick_params(axis='both',length=0,labelsize=11.5,pad=8)
    ax.yaxis.grid(True,color=GRID,lw=.85)
    ax.set_axisbelow(True)
    ax.set_ylabel(axis_label,fontsize=11.5)
    ax.legend(loc='upper center',bbox_to_anchor=(.5,-.16),ncol=2,frameon=False,
              labelcolor=INK,fontsize=11.6,handlelength=1.3)
    fig.add_artist(plt.Line2D([.025,.975],[.097,.097],transform=fig.transFigure,lw=.8,color=GRID))
    fig.text(.025,.077,'Descriptive means only  |  N = 238 (arms: 121 and 117)  |  No cell confidence intervals reported',
             fontsize=9.6,color=MUTED,va='top')
    fig.text(.025,.046,extra_note or 'Display range: 0–7. Original response anchors not documented.',
             fontsize=9.4,color=MUTED,va='top')
    fig.savefig(out/filename,dpi=100)
    plt.close(fig)


def make_leadership_forest(out:Path, rows:list[dict[str,str]])->None:
    expected = ['Overall leader emergence','Informal leader emergence',
                'Formal leader emergence','Subjective formal emergence',
                'Objective formal emergence','Leadership effectiveness']
    d={r['outcome']:r for r in rows}
    assert set(expected)==set(d), 'Unexpected or missing meta-analysis rows'
    fig=plt.figure(figsize=(11.81,11.50),dpi=100)
    fig.text(.024,.971,'Attractiveness and leadership outcomes',fontsize=20,
             color=BLUE,fontweight='bold',va='top')
    fig.text(.024,.919,'Figure 6  ·  Dots: corrected correlations (ρ); lines: 95% confidence intervals',
             fontsize=12.5,color=MUTED,va='top')
    fig.text(.024,.887,'Courtright et al.  ·  k = correlations; N = rated targets (not raters)',
             fontsize=10.6,color=MUTED,va='top')
    ax=fig.add_axes([.45,.145,.26,.69])
    ax.set_xlim(-.06,.71)
    ax.set_ylim(-.90,6.50)
    ax.set_yticks([])
    ax.set_xticks([0,.15,.30,.45,.60])
    ax.set_xticklabels(['0','0.15','0.30','0.45','0.60'],fontsize=10)
    ax.axvline(0,color='#A4B6BD',lw=1.5,zorder=0)
    ax.xaxis.grid(True,color=GRID,lw=.8)
    ax.set_axisbelow(True)
    ax.spines['bottom'].set_color('#BBC6CD')
    ax.tick_params(axis='x',length=0,pad=9)
    ylevels=[5.7,4.65,3.6,2.55,1.5,-.2]
    for name,y in zip(expected,ylevels):
        r=d[name]
        val=float(r['rho_corrected']);lo=float(r['ci_lower']);hi=float(r['ci_upper'])
        is_sub=name in expected[3:5]
        is_effect=name=='Leadership effectiveness'
        color=MUTED if is_effect else (TEAL if is_sub else BLUE)
        ax.plot([lo,hi],[y,y],c=color,lw=3.0,solid_capstyle='round',zorder=2)
        ax.scatter([val],[y],c=color,s=65,zorder=3)
        y_fig=fig.transFigure.inverted().transform(ax.transData.transform((0,y)))[1]
        label={'Overall leader emergence':'Overall leader emergence',
               'Informal leader emergence':'Informal leadership',
               'Formal leader emergence':'Formal leadership',
               'Subjective formal emergence':'Subjective judgments (formal)',
               'Objective formal emergence':'Actual role attainment (formal)',
               'Leadership effectiveness':'Leadership effectiveness'}[name]
        xpos=.045 if is_sub else .025
        fig.text(xpos,y_fig+.016,label,color=INK,fontsize=11.7 if not is_sub else 10.6,va='center')
        fig.text(xpos,y_fig-.014,f"k = {int(r['k_correlations'])}; N = {int(r['N_rated_targets']):,}",
                 color=MUTED,fontsize=9.5,va='center')
        lo_text='−0.004' if lo == -.004 else f'{lo:.2f}'
        fig.text(.742,y_fig,f"{val:.2f}  [{lo_text}, {hi:.2f}]",fontsize=10.7,color=INK,va='center')
    # Separation in the chart deliberately marks effectiveness as a different outcome.
    ax.axhline(.75,c='#A6B7C0',lw=1.1)
    fig.text(.025,.272,'DIFFERENT OUTCOME  ·  ONLY THREE STUDIES',color=MUTED,
             fontsize=9.1,fontweight='bold')
    fig.text(.505,.096,'Corrected correlation (ρ)',fontsize=10.4,color=INK)
    fig.text(.025,.062,'Corrected for measurement unreliability; these are published pooled estimates, not a new meta-analysis.',
             fontsize=9.2,color=MUTED)
    fig.text(.025,.041,'Overall emergence I² ≈ 61%; subgroups can overlap. Leadership effectiveness is a separate outcome.',
             fontsize=9.2,color=MUTED)
    fig.savefig(out/'figure_06_leadership_meta.png',dpi=100)
    plt.close(fig)


def reconstruct(data:dict, outfile:Path)->str:
    reported=read_csv('published_anova_tests.csv')
    qmeans=read_csv('questionnaire_group_means.csv')
    tukey=read_csv('questionnaire_tukey_intervals.csv')
    assert len(data['Alpha'])==3
    N=238
    lines=[
        'What Makes a Man Seem "Alpha"? — Reconstructed calculations',
        '============================================================',
        'Published inputs are rounded. This is a summary-statistic audit, not raw-data reanalysis.',
        '',
        '1. Degrees-of-freedom pattern (compatibility check, not proof of analysis code)',
        f'   Total: {N} respondents × 3 repeated vignettes = {N*3} scores.',
        f'   Independent-cell 2×3 ANOVA: residual df = {N*3} − 6 = {N*3-6}.',
        f'   Independent-category one-way ANOVA: residual df = {N*3} − 3 = {N*3-3}.',
        f'   Hypothesized subgroup n=54: df = 3×54 − 3 = {3*54-3}.',
        f'   Hypothesized subgroup n=184: df = 3×184 − 3 = {3*184-3}.',
        '   These exactly match the published error dfs 708, 711, 159, and 549.',
        '   Alternative analysis choices could share these dfs; original code unavailable.',
        '',
        '2. Partial eta-squared calculated from published F and dfs',
        '   eta_p^2 = F * df_effect / (F * df_effect + df_error)',
    ]
    for row in reported[:3]:
        f=float(row['F_reported']);d1=int(row['numerator_df']);d2=int(row['denominator_df'])
        val=f*d1/(f*d1+d2)
        lines.append(f"   {row['factor']}: F({d1},{d2})={f:.2f} -> eta_p^2={val:.6f} (≈ {val:.3f})")
    lines += [
        '   These are likely partial eta-squared, not an additive variance partition.',
        '   Their inferential validity depends on whether the repeated measures were modeled correctly.',
        '',
        '3. Published alpha-rating framing gaps (attractive minus unattractive)',
    ]
    for profile in ('Prosocial','Wealthy playboy','Antisocial'):
        va,vb=data['Alpha'][profile]
        lines.append(f'   {profile}: {va:.2f} - {vb:.2f} = {va-vb:.2f} points')
    lines += ['','4. Questionnaire sex-label consistency check',
             '   Hypothesis being audited: Table 4 group names are correct, text ANOVA group names swapped.',
             '   Tukey 95% half-width h = q_0.95(k=3, df) * sqrt(MSE / n) (equal-n independent one-way model).',
             '   Therefore MSE ≈ n*(h/q)^2 and F = n*sum((mean-grand_mean)^2)/(2*MSE).',
             '   This reconstructs the author-reported independent-observation model, NOT a corrected mixed model.']
    for group,n in [('Men',184),('Women',54)]:
        means=np.array([float(r['mean']) for r in qmeans if r['group_label_in_table']==group])
        qrows=[r for r in tukey if r['group_label_in_table']==group]
        good=[]
        for r in qrows:
            d=float(r['difference']);lo=float(r['ci_lower']);hi=float(r['ci_upper'])
            if abs((lo+hi)/2-d)<.08:
                good.append((hi-lo)/2)
        df=n*3-3
        qcrit=float(studentized_range.ppf(.95,3,df))
        median_half_width=float(np.median(good))
        mse=n*(median_half_width/qcrit)**2
        grand=float(np.mean(means));F=n*float(np.sum((means-grand)**2))/(2*mse)
        lines += [f'   Table-labeled {group}: hypothetical n={n}, df={df}, Tukey q={qcrit:.5f};',
                  f'      consistent CI half-width ≈ {median_half_width:.3f}; implied MSE≈{mse:.4f}; F≈{F:.3f}.']
        if group=='Men':
            assert abs(F-65.18)<.15,(group,F)
        else:
            assert abs(F-8.98)<.10,(group,F)
    lines += ['   Text labels F(2,159)=8.98 "men" and F(2,549)=65.18 "women" therefore appear swapped.',
              '   This does NOT independently determine respondents’ sex coding in the original dataset.',
              '   IMPORTANT additional table issue: Women, Status − Money = 4.54 has CI [1.20, 7.08],',
              '      whose midpoint is 4.14. This interval is not centered on its reported difference.',
              '      It is excluded from the equal-width reconstruction (the other two CIs agree).',
              '',
              '5. Pooled questionnaire attractiveness mean',]
    groups={r['group_label_in_table']:float(r['mean']) for r in qmeans if r['category']=='Attractiveness'}
    weighted=(184*groups['Men']+54*groups['Women'])/238
    reversed_weight=(54*groups['Men']+184*groups['Women'])/238
    lines += [f'   If Table 4 labels are correct (184 Men, 54 Women): {weighted:.4f}.',
              f'   Reversing weights (54 Men, 184 Women): {reversed_weight:.4f}.',
              '   Published plotted pooled mean ≈27.2, consistent with the first assignment.',
              '   This is circumstantial support for a text-label typo, not independent sex verification.',
              '',
              '6. Reported Welch test: money-category sex difference',]
    diff=groups.get('Men',0) # replace below
    money={r['group_label_in_table']:float(r['mean']) for r in qmeans if r['category']=='Money'}
    diff=money['Men']-money['Women']
    t_reported=1.13;df_w=73.59
    se=abs(diff/t_reported)
    margin=float(tdist.ppf(.975,df_w)*se)
    lines += [f'   Table means difference = {money["Men"]:.2f} − {money["Women"]:.2f} = {diff:.2f}.',
              f'   t = {t_reported:.2f}; Welch df = {df_w:.2f}; reconstructed 95% CI ≈ [{diff-margin:.2f}, {diff+margin:.2f}].',
              '   Published CI is [-0.81, 5.54]; upper endpoint is inconsistent with estimate/test statistic.',
              '   Rounded inputs prevent exact recovery of the author’s unrounded interval.',
              '',
              '7. Courtright et al. estimates (COPIED from published tables; NOT recomputed meta-analysis)',]
    for r in read_csv('courtright_meta_summary.csv'):
        lo=float(r['ci_lower']);hi=float(r['ci_upper']);val=float(r['rho_corrected'])
        lines.append(f"   {r['outcome']}: rho={val:.3f} [{lo:.3f},{hi:.3f}], k={r['k_correlations']}, N={r['N_rated_targets']}")
    lines += [
        '   N refers to rated targets and k to correlations, as tabulated in the paper.',
        '   Corrected rho is not interchangeable with an uncorrected correlation r.',
        '   The subjective-vs-objective contrast is reported as Z=2.98 (one-sided p≈.001);',
        '      a normal two-sided p is ≈.0029, still significant (study-set comparison, not causal).',
        '',
        '8. What this package cannot calculate',
        '   * Repeated-measures/mixed-effects tests, adjusted condition effect, or participant-level CIs.',
        '   * Within-condition correlations underlying the published pooled r=.90.',
        '   * Randomization balance, sample exclusions, or sex×condition×vignette tests.',
        '   * Independent reanalysis of Courtright et al.’s individual study effect sizes.',
        '   These require raw data or fuller published inputs not available for this audit.',
        '',
    ]
    report='\n'.join(lines)
    outfile.write_text(report,encoding='utf-8')
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',type=Path,default=HERE,
                        help='Directory for figures and reconstruction_results.txt (default: script folder)')
    args=parser.parse_args()
    out=args.output_dir.resolve();out.mkdir(parents=True,exist_ok=True)
    data=outcomes()
    assert len(read_csv('published_vignette_means.csv'))==18
    tasks=[
       ('Attractiveness',1,'figure_01_attractiveness.png','How attractive did the profiles seem?',
        'Published attractiveness-rating means','Mean survey rating',
        'Ratings combine photograph and vignette text; not independent facial ratings.'),
       ('Alpha',2,'figure_02_alpha.png','Who was rated more “alpha”?',
        'Published alpha-rating means','Mean survey rating','Display range: 0–7. Original response anchors not documented.'),
       ('Status',3,'figure_03_status.png','Who was seen as higher status?',
        'Published perceived-status means','Mean survey rating','Display range: 0–7. Original response anchors not documented.'),
       ('Long-term desirability prediction',4,'figure_04_long_term.png',
        'Who was expected to appeal long-term?',
        'Respondents’ predictions about women’s preferences','Mean predicted desirability',
        'Third-person prediction only; no actual women’s mate choices were observed.'),
       ('Short-term desirability prediction',5,'figure_05_short_term.png',
        'Who was expected to appeal short-term?',
        'Respondents’ predictions about women’s preferences','Mean predicted desirability',
        'Third-person prediction only; no actual women’s mate choices were observed.'),
    ]
    for name,num,fn,title,subtitle,ylabel,note in tasks:
        make_bar_chart(out,data[name],number=num,filename=fn,question=title,
                       caption=subtitle,axis_label=ylabel,extra_note=note)
    make_leadership_forest(out,read_csv('courtright_meta_summary.csv'))
    print(reconstruct(data,out/'reconstruction_results.txt'))
    print('\nFigures written:')
    for file in sorted(out.glob('figure_*.png')):
        print(' ', file.name, f'({file.stat().st_size:,} bytes)')

if __name__=='__main__':
    main()
