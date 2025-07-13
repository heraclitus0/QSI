RUPTURE DETECTOR
================

Forecast Drift Monitoring & Preventable Loss Detection for Supply Chains

[Live Demo](https://rupture-detector-vxcv8twev4y3vcuqzjprnw.streamlit.app/)

This tool detects misalignments between forecasted and actual demand. It identifies rupture points where deviation becomes costly and suggests corrective resets. The system quantifies preventable monetary loss using real-time thresholds and memory-aware state tracking.

---------------------------------------------------------
SECTION 1 — FEATURES
---------------------------------------------------------

- Upload real-world data via Excel or CSV
- Auto-calculate drift: Delta(t), E(t), Theta(t)
- Detect rupture events where ∆(t) > Θ(t)
- Quantify preventable loss in monetary terms
- Visual diagnostics and downloadable output

---------------------------------------------------------
SECTION 2 — INSTALLATION
---------------------------------------------------------

Create and activate a virtual environment:

    python -m venv venv
    source venv/bin/activate     # On Windows: .\venv\Scripts\activate

Install the required packages:

    pip install -r requirements.txt

---------------------------------------------------------
SECTION 3 — FILE STRUCTURE
---------------------------------------------------------

    rupture_detector/
    ├── app.py            # Streamlit interface
    ├── rupture.py        # Core logic
    ├── requirements.txt  # Dependency list

---------------------------------------------------------
SECTION 4 — DATA FORMAT
---------------------------------------------------------

Your input file must be an Excel or CSV with the following columns:

    Date        (YYYY-MM-DD format)
    Forecast    (numeric)
    Actual      (numeric)
    Unit_Cost   (monetary per unit)

---------------------------------------------------------
SECTION 5 — RUNNING LOCALLY
---------------------------------------------------------

To start the app locally:

    streamlit run app.py

Streamlit UI will load in your browser.

---------------------------------------------------------
SECTION 6 — PARAMETERS
---------------------------------------------------------

The following parameters are adjustable in-app:

    c        - Drift amplification factor
    a        - Sensitivity of threshold to drift
    Theta0   - Base rupture threshold
    sigma    - Noise level for volatility
    alpha    - EWMA smoothing factor
    k        - EWMA standard deviation multiplier

These can be exposed to UI sliders or presets.

---------------------------------------------------------
SECTION 7 — OUTPUTS
---------------------------------------------------------

- Delta(t): instantaneous drift
- E(t): cumulative epistemic misalignment
- Theta(t): rupture threshold over time
- Rupture Table: dates and loss amounts
- Plot: Drift vs Threshold (with rupture flags)
- Total preventable monetary loss

---------------------------------------------------------
SECTION 8 — DEPLOYMENT OPTIONS
---------------------------------------------------------

You can deploy on:

- Streamlit Cloud
- Self-hosted server (Docker or VM)
- Embedded inside ERP dashboards
- Local desktop usage (single-user Excel monitor)

---------------------------------------------------------
SECTION 9 — EXTENSION IDEAS
---------------------------------------------------------

- REST API integration (e.g., with NetSuite)
- Email/Slack alerts for new ruptures
- Authentication for multi-team use
- Multi-sheet ingestion
- Real-time data ingestion hook

---------------------------------------------------------
SECTION 10 — LICENSE
---------------------------------------------------------

MIT License. Free for personal and commercial use with attribution.

---------------------------------------------------------
SECTION 11 — AUTHOR
---------------------------------------------------------

Built by Pulikanti Sashi Bharadwaj

Contact: bharadwajpulikanti11@gmail.com
---------------------------------------------------------
SECTION 12 — THEORETICAL FOUNDATION
---------------------------------------------------------

This tool is grounded in the principles of the **Recursion Control Calculus (RCC)** — a formal framework for regulating epistemic misalignment in volatile environments.

RCC introduces symbolic memory (`V(t)`), distortion (`∆(t)`), and adaptive rupture thresholds (`Θ(t)`) to track misalignment between internal projections and emergent reality — enabling early detection of systemic drift.

For the complete mathematical formulation, see:

Pulikanti, S.B. (2025). *Recursion Control Calculus: A Formal Epistemic Control System for Drift Regulation under Stochastic Volatility*. Zenodo.  
[https://doi.org/10.5281/zenodo.15730197](https://doi.org/10.5281/zenodo.15730197)

