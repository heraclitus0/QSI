<p align="center">
  <img src="docs/brand/QSI_logo.png" alt="QSI logo" width="96" />
</p>

---

> **QSI** is an agnostic decision-intelligence layer.  
> It governs the gap between **what was expected** and **what actually happened**,  
> detecting ruptures, quantifying preventable losses, and translating volatility into board-level insight.  

---

## Why QSI?  

Forecasts fail. Plans drift. Models misalign.  
QSI does not replace your models — it **sits above them**, continuously monitoring outcomes and exposing where volatility silently erodes value.  

- **Not just anomaly detection** → QSI estimates *time to persistent breach* and *scope of alignment*.  
- **Not a dashboard** → QSI generates intelligence streams that can be consumed by analysts, boards, or autonomous systems.  
- **Not domain-locked** → supply chains, finance, pharma, cybersecurity — anywhere drift exists, QSI applies.  

---

## Features  

- **Rupture Analytics**: Detect when deviations exceed adaptive thresholds.  
- **Economic Impact**: Quantify preventable losses in real currency, not abstract metrics.  
- **Board Diagnostics**: Scope score, PSI, Pareto loss share, weekend vs weekday multipliers.  
- **Policy Effectiveness**: Split outcomes by regulatory, operational, or business controls.  
- **Cognize Integration**: Plug into self-adapting epistemic kernels for intelligent thresholds.  
- **Custom Models**: Register bespoke enterprise rules for thresholds or diagnostics.  

---

## Use Cases  

QSI is **agnostic** — designed for *any* context where expected vs actual must be reconciled.  

- **Forecast vs Actual Governance**  
  Ensure your predictive models or planning systems remain aligned with reality.  

- **Volatility & Breach Management**  
  Anticipate when drifts will breach thresholds and act before losses lock in.  

- **Scenario Translation for Boards**  
  Convert technical volatility into strategic language — *“X% of days drove Y% of losses.”*  

- **Policy & Control Effectiveness**  
  Test whether interventions (pricing, staffing, cybersecurity controls) actually reduce volatility.  

- **Adaptive Experimentation**  
  Let thresholds self-learn with Cognize to handle non-stationary environments.  

- **Cross-Domain Examples**  
  - **Pharma**: drug forecast vs prescriptions  
  - **Finance**: budget vs spend  
  - **Cybersecurity**: expected vs observed traffic  
  - **Retail**: sales vs forecast  
  - **Energy**: demand vs supply balance  

---

## Quick Start  

```bash
pip install qsi
```

```python
import pandas as pd
from qsi import QSIEngine, QSIConfig, EpistemicAnalytics, EpistemicConfig

# Load your data
df = pd.read_csv("your_timeseries.csv")

# Run core QSI engine
cfg = QSIConfig()
out, report = QSIEngine(cfg).analyze(df)

# Add board-level diagnostics
epicfg = EpistemicConfig()
diagnostics = EpistemicAnalytics.enrich(out, epicfg)

print(report["summary"])
print(diagnostics["epistemic"])
```

---

## Design Philosophy  

- **Apple Simplicity** → one-click install, clean API, clear defaults.  
- **McKinsey Rigor** → quantified insights, economic framing, board-ready diagnostics.  
- **Agnostic Intelligence** → no sector lock-in; QSI applies wherever forecasts meet outcomes.  

---

## License  

MIT License.  
Use freely, adapt responsibly, contribute if you extend.  

---
*QSI: Governing volatility, everywhere.*  


