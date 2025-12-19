# Emergency Hospital Accessibility in Baku (10-Minute Analysis)

This repository contains a reproducible geospatial analysis that evaluates emergency hospital accessibility across **Baku** using a **10-minute travel-time threshold** under two mobility scenarios: **driving** and **walking**. The workflow generates travel-time service areas for emergency hospitals, aggregates citywide coverage, and identifies **blind spots**—areas inside the study boundary that are not reachable within the threshold.

**Study area definition:** Baku is defined strictly by the polygon contained in `data/baku_boundary.geojson`. All metrics and visual outputs are constrained to this boundary.

---

## Overview

Timely access to emergency medical care depends on both distance and network connectivity. Rather than using straight-line distance, this project models reachability through the road and pedestrian network to estimate practical access under a fixed time constraint. The analysis converts travel-time reach into spatial coverage surfaces and highlights areas where access is structurally limited. Results are presented both quantitatively and through interactive maps.

---

## Key Outputs

- `data/blind_spots_driving.geojson`  
  Areas within the study boundary not reachable within 10 minutes by driving.

- `data/blind_spots_walking.geojson`  
  Areas within the study boundary not reachable within 10 minutes by walking.

- `outputs/coverage_driving.html`  
  Interactive map displaying hospitals, the study boundary, driving coverage, and driving blind spots.

- `outputs/coverage_walking.html`  
  Interactive map displaying hospitals, the study boundary, walking coverage, and walking blind spots.

---

## Method Summary

Hospital locations were obtained from OpenStreetMap and curated to focus on facilities that plausibly provide emergency medical care, excluding clearly non-emergency specialty institutions. For each retained hospital location, a travel-time service area was generated under a fixed 10-minute threshold for both driving and walking using a routing engine operating on the street network. All generated service areas were spatially constrained to the defined Baku study boundary to avoid attributing coverage outside the area of interest. Mode-specific service areas were then aggregated into a single citywide coverage surface to represent effective accessibility without double counting overlapping regions. Accessibility blind spots were derived as the remaining portions of the study boundary not covered by the aggregated surface. Final results were exported as standard geospatial layers and interactive maps to support inspection, interpretation, and reporting.

---

## Running the Analysis Locally

### Environment setup

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
```
### Install dependencies
```
pip install -r requirements.txt
```
### Execute the pipeline
```
python scripts/build_hospitals_csv.py
python scripts/generate_isochrones.py
python scripts/analyze_coverage.py
```
---
## Limitations 

Travel-time estimates represent network-based free-flow conditions and do not account for real-world traffic congestion, signal delays, parking or search time, or time required for facility intake. Hospital data is sourced from OpenStreetMap and may contain omissions or inconsistencies; the emergency-capable filtering approach is heuristic rather than based on an official registry. All reported metrics are contingent on the study boundary defined in data/baku_boundary.geojson, and alternative boundary definitions would yield different absolute values. The analysis considers only driving and walking as isolated mobility modes and does not model multimodal travel or emergency-specific routing behavior.

---

## Data and Code Availability

All scripts and final output layers required to reproduce the analysis are included in this repository. Large intermediate artifacts, such as raw per-hospital isochrone files generated during processing, are excluded to maintain repository clarity and manageable size.


