
# User Manual: EV Grid Load Analysis Platform

## What This Tool Does

This platform helps you analyze whether electrical grid transformers (called **PTDs**) can handle the addition of electric vehicle chargers. Think of it as a "stress test" for the electrical grid — it tells you **how risky** it would be to install EV chargers in a specific area, and **how many chargers** the grid can safely support.

The platform has **three main tools**, each with its own page:

| Tool | What It Does |
|------|-------------|
| **Prediction** | Make a single prediction for one specific transformer |
| **Simulation** | Test "what-if" scenarios by adding random noise to see how the model behaves |
| **Regional Analysis** | Analyze **all transformers** in a district or municipality at once |

---

## Key Concepts

Before using the tool, here are a few terms you'll see:

| Term | What It Means |
|------|--------------|
| **PTD** | A specific electrical transformer in the grid. Each has a code (like `PTD-12345`) and a location. |
| **Profile** | A preset setting: `leve` (light), `regular` (medium), or `pesado` (heavy). This tells the system how aggressively to analyze. |
| **Model** | The "brain" that makes predictions. Options include NeuralNet, Decision Tree, SVM, etc. The ones marked **Recommended** usually work best. |
| **Classification** | The risk level: **Low** (safe), **Medium** (caution), or **High** (dangerous overload). |
| **Regression** | A number prediction — specifically, how much power (in kW) the grid will need to handle. |
| **Installed Power** | The maximum power the transformer was built to handle (in kVA). |
| **Charger Power** | How much power one EV charger uses (in kW). |
| **Utilization Factor** | How much of the time chargers are actually being used (0 to 1). For example, 0.7 means chargers are in use 70% of the time. |
| **Total Charger Load** | The actual power demand from all chargers combined = `Number of Chargers × Power per Charger × Utilization Factor`. |

---

## Page 1: Prediction

Use this when you want to analyze **one specific transformer** and see if it can handle EV chargers.

### Step-by-Step Guide

#### 1. Configuration (Top Section)
- **Profile**: Choose `leve`, `regular`, or `pesado`. This affects how strict the analysis is.
- **Version** (optional): Leave blank unless you have a specific model version to test.
- **Model**: Pick a prediction model. The ones with a green **Recommended** tag usually give the best results.

#### 2. Select a Location (PTD Selection)
- Use the **map and selector** to find your transformer.
- When you select a PTD, the system automatically fills in all the technical details about that transformer (installed power, number of lights, etc.).
- The **Distrito_enc** and **Concelho_enc** values update automatically based on your selection.

#### 3. Choose Your Task (Tabs)

**Tab A: Classification** — "Will this transformer overload?"
- The system predicts whether the risk is **Low**, **Medium**, or **High**.
- After clicking **Submit**, you'll see:
  - A **color-coded risk tag** (green = safe, orange = caution, red = danger)
  - A **confidence gauge** showing how sure the model is
  - **Raw scores** showing the probability for each risk level

**Tab B: Regression** — "How much power will be needed?"
- The system predicts the **exact power demand** in kW.
- You can also configure **charger simulation**:
  - Pick a **charger model** from the dropdown (this auto-fills the power)
  - Set **how many chargers** you want to install
  - Set the **utilization factor** (how busy the chargers will be)
- You'll see:
  - The **predicted power value** in kW
  - **Total charger load** and **supported chargers count**
  - A **Grid Security Chart** showing whether your plan is safe

#### 4. Review Results
Results appear below the form. The system automatically scrolls to them. Each prediction is saved to your history.

---

## Page 2: Simulation

Use this to run **"what-if" experiments**. Instead of one prediction, the system runs **hundreds or thousands** of predictions with slightly randomized data to see how stable the results are.

### Step-by-Step Guide

#### 1. Configuration
- Set **Profile**, **Version**, and **Model** just like in Prediction.

#### 2. Select a PTD
- Choose a transformer. The encoded values (Distrito_enc, Concelho_enc, N_Clientes) display automatically.

#### 3. Choose a Scenario
- Click one of three cards to set the **target risk level** you want to test:
  - 🟢 **Low Risk** — Test if the system consistently says "safe"
  - 🟠 **Medium Risk** — Test borderline cases
  - 🔴 **High Risk** — Test if the system catches dangerous situations

#### 4. Set Parameters
- **Iterations**: How many random tests to run (100 to 100,000). More = more accurate but slower.
- **Noise Scale**: How much randomness to add (0.01 to higher values). Higher = more variation in test data.
- **Seed**: A number that makes the randomness repeatable. Use the same seed to get the same "random" results.

#### 5. Review Results
After clicking **Run Scenario**, you'll see:

| Result | What It Means |
|--------|--------------|
| **Detection Rate Gauge** | How often the model correctly identified your chosen scenario |
| **Distribution Pie Chart** | The breakdown of Low/Medium/High results across all iterations |
| **Overload Probability** | The chance that the grid would actually overload |
| **Summary Statistics** | Mean, standard deviation, min/max probabilities |
| **Detection Breakdown** | A bar chart showing how often each risk level was detected |

**Reading the Detection Banner:**
- 🟢 **Green** (≥70%): The model reliably detects this scenario
- 🟠 **Orange** (30-70%): The model is uncertain
- 🔴 **Red** (<30%): The model struggles to detect this scenario

---

## Page 3: Regional Analysis

Use this to analyze **every transformer in an entire district or municipality** at once. This is great for planning large-scale EV charger deployments.

### Step-by-Step Guide

#### 1. Configuration
- Set **Profile**, **Version**, and **Model** (for this page, you use **regression models**).

#### 2. Select a Region
- **District**: Pick a district (e.g., "Lisboa", "Porto").
- **Municipality**: Pick a specific municipality within that district, or leave it blank to analyze the whole district.
- The system shows how many **PTDs** (transformers) were found in your selection.

#### 3. Configure Chargers
- Pick a **charger model** (auto-fills power)
- Set **number of chargers** per transformer
- Set **utilization factor**
- The system shows:
  - **Total Charger Load** — power demand from all chargers
  - **Load per PTD** — how much each transformer must handle

#### 4. Run Analysis
- Click **"Run Analysis (X PTDs)"** to start.
- A **progress bar** shows how many transformers have been analyzed.
- The system processes in batches of 10 to avoid overloading.

#### 5. Review Results

**Summary Card:**
- Total PTDs analyzed
- Count of **Low**, **Medium**, and **High** risk transformers
- **Average predicted load** across all transformers
- A **pie chart** showing the risk distribution

**Map:**
- Each transformer appears as a colored dot on the map:
  - 🟢 Green = Low risk
  - 🟠 Orange = Medium risk
  - 🔴 Red = High risk
- **Click any dot** to see detailed info about that transformer
- The map automatically zooms to fit all results

**Detailed Results Table:**
- Sortable, filterable table with all transformers
- Columns include:
  - PTD Code
  - District / Municipality
  - Predicted Load (kW)
  - Installed Power (kVA)
  - **Total Load** (red if it exceeds capacity!)
  - **Margin** (safety buffer, red if negative)
  - **Risk Classification** (color-coded tag)
  - **Supported Chargers** (how many chargers this transformer can actually handle)
- Use **Clear Filters** to reset, or **Export CSV** to download the data

---

## Tips for Best Results

| Tip | Why It Helps |
|-----|-------------|
| Start with **Recommended models** | They've been pre-tested for accuracy |
| Use **low iterations** (100-500) for quick tests, **high iterations** (5000+) for final reports | Balances speed vs. accuracy |
| Always check the **margin** in Regional Analysis | Negative margin = overload = danger |
| Compare **classification** and **regression** results | Classification gives risk level; regression gives exact numbers |
| Use the **same seed** in Simulation to compare different settings | Keeps randomness consistent |
| If a PTD shows **High Risk**, reduce chargers or pick a more powerful transformer | Safety first! |

---

## Understanding Risk Levels

| Level | Color | Meaning | Action |
|-------|-------|---------|--------|
| **Low** | 🟢 Green | Safe to install chargers | Proceed with confidence |
| **Medium** | 🟠 Orange | Borderline — may overload under heavy use | Monitor closely; consider fewer chargers |
| **High** | 🔴 Red | Dangerous — likely to overload | Do not install; upgrade transformer first |

---

## Exporting Your Data

From the **Regional Analysis** page, click **Export CSV** to download a spreadsheet with all results. The filename includes the district and date (e.g., `regional_analysis_Lisboa_2026-07-07.csv`). Open it in Excel or Google Sheets for further analysis.

