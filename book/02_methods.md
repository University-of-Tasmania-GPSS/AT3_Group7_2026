
# Methodology

This project combined multi-criteria decision analysis (MCDA), terrain-dependent walking costs and least-cost path optimisation to identify potential walking tracks connecting Slump Pond, Fools Tarn and Hutchinsons Falls.

The workflow followed three main stages: preparing spatial suitability criteria, comparing Weighted Linear Combination (WLC) and TOPSIS, and generating routes using Dijkstra's algorithm and A* search.

## Spatial Data and Preparation

Four spatial datasets were used: a 1 m Digital Elevation Model (DEM), TASVEG vegetation mapping, watercourses and existing walking tracks. These represented terrain difficulty, ecological sensitivity, hydrology and recreational connectivity.

Datasets were projected to MGA2020 Zone 55 (EPSG:7855), clipped to the approximately 9 km² study area and aligned to a common 1 m raster grid.

The DEM was used to derive slope and directional walking gradients, while distances to watercourses and existing tracks were calculated to assess proximity.

## Criteria Standardisation and Weighting

Each criterion was reclassified onto a common suitability scale from **1 (very low suitability) to 5 (very high suitability)**, allowing different landscape characteristics to be compared.

| Criterion | Weight | Suitability principle |
|:---|---:|:---|
| Vegetation sensitivity | 45% | Favour less environmentally sensitive communities |
| Slope | 25% | Favour gentler terrain |
| Watercourse proximity | 20% | Discourage routes near waterways |
| Existing-track proximity | 10% | Encourage connections to established infrastructure |

Vegetation scores were informed by TASVEG classifications and research on trampling impacts in Tasmanian alpine environments (Whinam & Chilcott, 2003).

Slope was reclassified using five project-defined categories, ranging from a suitability score of 5 for gradients below 10° to 1 for gradients of 42° or greater.

The weights reflect the project's conservation priorities and were held constant across both suitability models.

## WLC and TOPSIS Suitability Modelling

Two MCDA approaches were used to investigate how different decision rules influence the distribution of suitable track corridors.

### Weighted Linear Combination (WLC)

Weighted Linear Combination calculated suitability through the weighted sum of standardised criteria (Malczewski, 2006):

$$
\displaystyle
\mathrm{WLC}
=
0.45V
+
0.25G
+
0.20H
+
0.10T
$$

where:

- $V$ = vegetation suitability
- $G$ = slope suitability
- $H$ = hydrological suitability
- $T$ = existing-track proximity suitability

The resulting WLC scores represent the combined influence of the four weighted criteria, with higher values indicating more suitable areas for walking-track development.

### Technique for Order Preference by Similarity to Ideal Solution (TOPSIS)

TOPSIS evaluated each raster cell according to its relative distance from ideal and least-ideal criterion combinations (Hwang & Yoon, 1981).

The relative closeness coefficient was calculated as:

$$
\displaystyle
C_i
=
\frac{D_i^{-}}
{D_i^{+}+D_i^{-}}
$$

where:

- $C_i$ = relative closeness to the ideal solution
- $D_i^{+}$ = distance from the positive ideal solution
- $D_i^{-}$ = distance from the negative ideal solution

Higher closeness values indicate greater relative suitability.

The resulting WLC and TOPSIS surfaces were compared to determine how each model represented the same landscape.

## Anisotropic Walking Costs

Suitability alone does not account for the physical effort of travelling through mountainous terrain.

Therefore, directional walking costs were incorporated using the principles of Tobler's (1993) hiking function:

$$
\displaystyle
v(s)
=
6\exp\left(-3.5\left|s+0.05\right|\right)
$$

where:

- $v(s)$ = predicted walking speed in kilometres per hour
- $s$ = signed terrain gradient, expressed as rise divided by horizontal distance

The function accounts for different movement costs when travelling uphill and downhill.

The resulting walking costs were combined with WLC- and TOPSIS-derived suitability penalties to represent both pedestrian effort and landscape conditions.

## Route Optimisation: Dijkstra and A*

Two graph-based pathfinding algorithms were used to generate least-cost routes through the study area.

**Dijkstra's algorithm** systematically explores the network to identify the path with the lowest accumulated movement cost (Dijkstra, 1959).

**A* search** incorporates a heuristic estimate of the remaining cost to the destination, potentially reducing the area searched (Hart et al., 1968).

Both algorithms seek minimum-cost paths but differ in their search strategies. Using both allowed the project to explore whether the pathfinding method influenced the resulting alignments.

Routes were generated in three consecutive segments:

1. Mountain River Trail to Slump Pond
2. Slump Pond to Fools Tarn
3. Fools Tarn to Hutchinsons Falls

These segments were combined into continuous routes for comparison.

## Route Evaluation and Limitations

The resulting WLC- and TOPSIS-derived alignments were examined in relation to walking distance, terrain conditions, vegetation sensitivity and existing-track connectivity.

The analysis was intended for preliminary route planning rather than identifying construction-ready tracks.

Although the 1 m DEM provides detailed topographic information, it cannot represent every small cliff, unstable surface or drainage feature. Additionally, the relative criterion weights influence the resulting suitability and route costs.

Consequently, the modelled routes provide alternatives for further evaluation rather than definitive construction recommendations. Field validation and sensitivity testing would be necessary before considering their practical implementation (Williams et al., 2025).
