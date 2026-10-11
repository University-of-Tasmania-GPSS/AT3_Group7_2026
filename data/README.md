# Welly on the Way

### Mapping Sustainable Walking Routes through kunanyi / Wellington Park

KGG375 – Geospatial Data Analytics. University of Tasmania. 2026

Group members: Ellie Pippos & Luke Smith

## Project Overview

Welly on the Way explores how Python-based geospatial analysis can support sustainable walking-track development in kunanyi / Wellington Park, Tasmania.

The project investigates potential routes connecting Slump Pond, Fools Tarn and Hutchinsons Falls, balancing environmental conservation, walking accessibility and route efficiency.

## Objectives

- Assess walking-track suitability using four weighted criteria: environmental sensitivity (35%), slope (20%), existing-track proximity (25%) and hydrological sensitivity (20%).
- Compare Weighted Linear Combination (WLC) and TOPSIS suitability models.
- Apply anisotropic movement-cost modelling and least-cost path analysis to generate alternative walking routes.
- Evaluate proposed routes based on distance, walking effort, track connectivity and environmental impacts.

## Project Website

[Explore our Jupyter Book](INSERT-WEBSITE-URL)

The website presents our methodology, interactive maps, visualisations, findings and discussion.

## Repository Structure

```text
├── README.md          # Project overview
├── environment.yml    # Python dependencies
├── Input_data/        # Original spatial datasets
├── Output_data/       # Processed data and model outputs
├── notebooks/         # Python analysis and modelling
└── book/              # Jupyter Book website
```

Folder names and contents will be updated to reflect the final repository.

## Reproducing the Analysis

1. Clone this repository.

2. Create and activate the Conda environment:

   ```bash
   conda env create -f environment.yml
   conda activate kgg375_AT3
   ```

3. Obtain the datasets listed in the Jupyter Book and place them in their designated input folders.

4. Run the Python notebooks in their documented order.

5. Build the website using Jupyter Book 1.x:

   ```bash
   jupyter-book build book/
   ```

Detailed data sources, scientific references and processing methods are documented in the Jupyter Book.

## AI Usage

Generative AI (ChatGPT, OpenAI) was used throughout this project as a supporting tool for literature discovery, methodological clarification, Python coding assistance, troubleshooting, and the development and refinement of written content. This included assistance with understanding MCDA techniques, suitability classifications, geospatial workflows, and Jupyter Book development.

AI-assisted material was reviewed and adapted by the group, with responsibility for analytical decisions, code implementation, source verification, interpretation of results, and final project content remaining with the authors.

---

Welly on the Way. Finding a sustainable path through Wellington Park.