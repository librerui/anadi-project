# Frontend User Manual

## Overview

The frontend is the user interface for the PTD Capacity Dashboard. It provides a guided workflow for selecting real PTD records, running predictions, and simulating charger installation loads.

## Main Screens

- **Predict**: configure a profile, choose a model, select a PTD, and run a prediction.
- **Simulate**: run Monte Carlo overload simulations with noise and target overload class.
- **Health**: verify API and model readiness, and inspect feature importance.

## Prediction Workflow

1. Open the **Predict** view.
2. Select a **Profile**: `leve`, `regular`, or `pesado`.
3. Choose a **Task**: `classification` or `regression`.
4. Select a **Model** for the chosen task.
5. Use the **PTD Selection** panel to filter by district and municipality.
6. Choose a PTD from the dropdown.
7. The UI auto-populates the model features from the selected PTD.
8. Adjust individual feature values if needed.
9. Click **Run Prediction**.

## Using PTDs

- **District** filters PTDs by region.
- **Municipality** narrows the PTDs list further.
- **PTD** loads actual transformer station data for the selected location.

Selecting a PTD helps avoid manual feature entry and keeps predictions grounded in real-world data.

## Charger Simulation

The charger simulation panel allows you to estimate whether a PTD can support a planned charger installation.

- **Charger Power**: choose a rated charger power (e.g. 3.7 kW, 7.4 kW, 22 kW, 50 kW).
- **Number of Chargers**: how many chargers you want to install.
- **Utilization Factor**: expected average operating share of the chargers.

The UI computes the total charger load and a supported charger count based on the current prediction.

## Result Interpretation

After prediction, the UI shows:

- predicted value or class,
- model and version used,
- profile and PTD metadata,
- class probabilities for classification,
- a confidence gauge for the top prediction.