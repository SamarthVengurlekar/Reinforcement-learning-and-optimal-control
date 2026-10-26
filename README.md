# ENN582 Exam Prep: Reinforcement Learning and Optimal Control

A single-page study site for ENN582 (QUT). It covers MPC, deterministic and stochastic dynamic programming, infinite-horizon DP (value and policy iteration), approximate DP, and reinforcement learning (TD, SARSA, Q-learning). It includes:

- ELI5 explanations with diagrams and YouTube videos
- a lesson for each practical (P1–P6)
- a mock exam
- a worked 2024 paper
- practice questions
- a two-page cheatsheet you can print

**Live site:** https://samarthvengurlekar.github.io/Reinforcement-learning-and-optimal-control/

## Files

| Path | What it is |
| --- | --- |
| `index.html` | The site (served by GitHub Pages) |
| `cheatsheet.pdf` | Two-page A4 exam cheatsheet (downloaded by the Cheatsheet tab) |
| `src/v1/` | v1 sources: base page (`main_base.html`), practical lessons (`prac.html`), mock exam (`mock.html`), cheatsheet HTML (`cs.html`, `cs9.html`), `build.py`, `mkpdf_v1.py` |
| `src/v2/` | v2 additions: ELI5 blocks (`eli5.html`) and `build_v2.py` |
| `src/make_index.py` | Wraps the built page into a standalone `index.html` |
| `src/checks/` | Python scripts that verify the worked numbers (DP tables, VI/PI, Sarsa/Q-learning updates, etc.) |

## Rebuilding

Requires Python 3 with `pymupdf` and `numpy`. The cheatsheet PDF uses macOS system fonts.

```sh
cd src/v1 && python build.py . && python mkpdf_v1.py .   # -> enn582-v1.html, cheatsheet.pdf
cd ../v2 && python build_v2.py .                         # -> enn582-v2.html (reads ../v1/enn582-v1.html)
cd .. && python make_index.py v2/enn582-v2.html ../index.html
```

Course lecture notes, past exam papers and practical submissions are not included in this repository.
