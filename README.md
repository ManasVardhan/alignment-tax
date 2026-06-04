# Alignment Tax Calculator -- Measuring What RLHF Takes Away

A live dashboard that quantifies the performance gap between base models and their RLHF-tuned variants. Because alignment is not free.

## The Hook

"RLHF makes models more helpful and less capable. I measured exactly how much."

## Concept

Every major model release ships with an "RLHF'd" version. The assumption: alignment improves everything. The reality: alignment trades off capabilities.

This project measures the "alignment tax" across dimensions:

1. **Creative writing** -- originality, surprise, stylistic range
2. **Mathematical reasoning** -- accuracy on olympiad problems, proof generation
3. **Coding performance** -- LeetCode solve rate, bug detection, refactoring
4. **Factual recall** -- knowledge-intensive QA, rare facts
5. **Metacognition** -- willingness to say "I don't know"
6. **Humor** -- joke quality, wit, comedic timing (yes, really)
7. **Translation** -- accuracy vs fluency tradeoff

## Stack

- HuggingFace for model loading
- EleutherAI LM Evaluation Harness for standardized testing
- Streamlit for live dashboard
- SQLite for tracking model versions

## Architecture

```
alignment-tax/
├── evals/               # Custom evaluation suites
│   ├── creativity.py      # Story generation diversity metrics
│   ├── math.py            # GSM8K, MATH, proof completion
│   ├── coding.py          # HumanEval, MBPP, bug detection
│   ├── knowledge.py       # TriviaQA, Natural Questions
│   ├── calibration.py     # ECE, willingness to abstain
│   └── humor.py           # Human-rated joke quality
├── models/                # Base vs RLHF model pairs
├── dashboard/             # Streamlit live dashboard
├── data/                  # Historical scores per model
└── reports/               # Auto-generated comparison posts
```

## The Tax Formula

```
Alignment Tax = (Base_Score - RLHF_Score) / Base_Score * 100

Example:
  Base model MATH score: 42%
  RLHF model MATH score: 31%
  Tax: (42-31)/42 = 26%
```

## Dashboard Views

1. **Model Comparison** -- Select any two models, see tax per dimension
2. **Tax Over Time** -- Track how tax evolves with each RLHF iteration
3. **Family Tree** -- Visualize base -> SFT -> DPO -> RLHF progression
4. **Prediction** -- Given a base model score, predict RLHF tax
5. **Leaderboard** -- Models ranked by "least tax" for each capability

## Models Tracked

- Llama 3 base vs instruct
- Qwen 2.5 base vs chat
- Mistral base vs instruct
- Gemma base vs it
- DeepSeek base vs chat
- (Community submissions welcome)

## Viral Mechanics

- Auto-generated "tax report cards" for new model releases
- "Most Taxed Capability" award each month
- Community predictions: "Guess the tax before release"
- X threads comparing specific model pairs with receipts

## Output Example

```
Model: Llama-3-8B-Instruct
Base:  Llama-3-8B

ALIGNMENT TAX REPORT
--------------------
Overall Tax: 18.3%

By Capability:
- Creativity:     -31% (base writes more original stories)
- Math:           -26% (base solves more olympiad problems)
- Coding:         -12% (base finds more bugs)
- Knowledge:      -8%  (base recalls more rare facts)
- Calibration:    +15% (RLHF better calibrated)
- Humor:          -22% (base is funnier, sorry)

Conclusion: Alignment trades creativity for safety.
           Worth it? Depends on your use case.
```

## License

MIT -- quantify the tradeoffs honestly.
