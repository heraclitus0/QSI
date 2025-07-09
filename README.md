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
    ├── rupture.py        # Core logic (RCC silently embedded)
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
SECTION 12 — THEORETICAL INFLUENCES
---------------------------------------------------------

The rupture detection framework implemented in this tool is influenced by a broad spectrum of concepts drawn from control theory, signal processing, and system feedback analysis. Its logic draws inspiration from:

Recursive filtering methods for state estimation under uncertainty (e.g., Kalman, 1960)

Feedback control systems and dynamic threshold adaptation (Åström & Murray, 2008)

Second-order cybernetics, particularly self-regulating and autopoietic feedback structures (von Foerster, 2003; Maturana & Varela, 1980)

Symbolic logic and recursion theory, useful for interpretive modeling and deviation analysis (Soare, 1996; Odifreddi, 1992)

The approach adopted emphasizes the detection of significant divergence between system expectations and live observations, using adaptive thresholding mechanisms and accumulated drift analysis. While grounded in practical system design, the logic accommodates both numerical volatility and symbolic disruption, aiming to flag high-risk discontinuities before systemic failure.

Key references include:

Kalman, R. E. (1960). A new approach to linear filtering and prediction problems. IEEE Transactions on Automatic Control. https://doi.org/10.1109/TAC.1960.1107752

Åström, K. J., & Murray, R. M. (2008). Feedback Systems: An Introduction for Scientists and Engineers. https://fbswiki.org

von Foerster, H. (2003). Understanding Understanding: Essays on Cybernetics and Cognition. https://doi.org/10.1007/978-1-4615-5889-1

Maturana, H. R., & Varela, F. J. (1980). Autopoiesis and Cognition: The Realization of the Living. https://doi.org/10.1007/978-94-009-8947-4

Soare, R. I. (1996). Computability and Recursion. Theoretical Computer Science. https://doi.org/10.1016/0890-5401(96)90015-7

Odifreddi, P. (1992). Classical Recursion Theory. https://doi.org/10.1007/978-3-642-58127-0
