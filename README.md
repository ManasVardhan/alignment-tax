# Alignment Tax Calculator: Quantifying Capability Tradeoffs in RLHF

A measurement framework for the performance gap between base language models and their RLHF-tuned variants.

## Motivation

The standard narrative in model releases presents RLHF as an unqualified improvement: the "instruct" or "chat" version is simply "better aligned." However, the alignment process involves explicit and implicit tradeoffs. Certain capabilities, particularly creative generation, mathematical reasoning, and stylistic flexibility, may degrade during the RLHF pipeline.

This project attempts to make those tradeoffs measurable and comparable across model families.

## Research Question

What is the quantitative cost of alignment? Which capabilities improve, which degrade, and by how much?

## Tax Formula

```
Alignment Tax = (Base_Score - RLHF_Score) / Base_Score * 100
```

Negative values indicate improvement from RLHF. The overall tax is a weighted average across dimensions.

## Evaluation Dimensions

| Dimension | Measurement | Weight |
|-----------|-------------|--------|
| Creativity | Story generation diversity (distinct-n, self-BLEU) | 1.0 |
| Mathematics | GSM8K, MATH benchmark accuracy | 1.2 |
| Coding | HumanEval, MBPP solve rate | 1.2 |
| Knowledge | TriviaQA, Natural Questions accuracy | 1.0 |
| Calibration | Expected Calibration Error, abstention rate | 0.8 |
| Humor | Human-rated joke quality | 0.6 |

## Architecture

```
alignment-tax/
├── evals/               # Evaluation suites per dimension
│   ├── creativity.py
│   ├── math.py
│   ├── coding.py
│   ├── knowledge.py
│   ├── calibration.py
│   └── humor.py
├── models/              # Base and RLHF model pairs
├── dashboard/           # Live comparison interface
├── data/                # Historical scores
└── reports/             # Auto-generated comparison outputs
```

## Example Output

```
Model: Llama-3-8B-Instruct
Base:  Llama-3-8B

ALIGNMENT TAX REPORT
--------------------
Overall Tax: 23.2%

By Capability:
  creativity     +30.8%
  math           +26.2%
  coding         +13.2%
  knowledge      + 8.5%
  calibration    -44.1%  (improved by RLHF)
  humor          +21.5%

Most taxed:    creativity (30.8% decrease)
Least taxed:   knowledge (8.5% decrease)

Improved by RLHF: calibration

Verdict: Moderate tax. Acceptable for general use.
```

## Models Tracked

- Llama 3 family (base vs instruct)
- Qwen 2.5 family (base vs chat)
- Mistral family (base vs instruct)
- Gemma family (base vs IT)
- DeepSeek family (base vs chat)

Community submissions of additional model pairs are welcome.

## Dependencies

```
streamlit
pandas
plotly
```

## Current Status

Calculator operational with synthetic demo data. Real evaluations require API access or local inference.

## Citation

```
@software{alignment_tax_2026,
  author = {Vardhan, Manas},
  title = {Alignment Tax Calculator: Quantifying Capability Tradeoffs in RLHF},
  year = {2026},
  url = {https://github.com/ManasVardhan/alignment-tax}
}
```

## License

MIT
