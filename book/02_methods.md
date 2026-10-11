# Methodology

How can a proposed walking track be both practical to walk and sensitive to the environment it crosses? This project addressed that question through two linked analyses. First, we evaluated landscape suitability using multi-criteria decision analysis (MCDA). Second, we used terrain-dependent movement costs to investigate routes connecting the selected destinations. Treating suitability and route-finding as related but separate problems makes it possible to examine not only where a track might be appropriate, but also whether those places can be connected efficiently.

The workflow was designed around a consistent set of spatial criteria, two contrasting suitability models, Weighted Linear Combination (WLC) and the Technique for Order Preference by Similarity to Ideal Solution (TOPSIS), and a directional least-cost path analysis. This approach draws on established GIS-MCDA principles (Malczewski, 2006) and recent Tasmanian geotrail research combining landscape criteria with route optimisation (Williams et al., 2025).

[Insert workflow figure: input data → preprocessing → four standardised criteria → WLC and TOPSIS → directional walking costs → least-cost routes → comparison.]

## Defining the route-planning problem

The analysis considered potential walking-track alignments for experienced bushwalkers within the approximately 9 km² study area described in Section 2. Routes were required to connect four locations in a fixed sequence:

1. A designated starting point on the Mountain River Trail.
2. Slump Pond.
3. Fools Tarn.
4. The base of Hutchinsons Falls.

These locations were treated as mandatory waypoints rather than additional suitability criteria. The purpose was therefore not to find the shortest possible line between arbitrary points, but to compare feasible connections between destinations already selected for their geological interest.

A continuous route was modelled as three consecutive segments. The same study-area extent, destination sequence, input criteria and relative weights were maintained when comparing WLC and TOPSIS, allowing differences to be attributed more clearly to the decision models rather than changes in the planning problem.

## Spatial datasets and preparation

Four principal spatial datasets informed the analysis: a Digital Elevation Model (DEM), vegetation mapping, existing walking tracks and watercourses. The DEM supported slope calculation and elevation-dependent walking costs; TASVEG classified vegetation communities; and track and watercourse features were used to calculate proximity surfaces.

| Input | Role in the analysis | Source |
|---|---|---|
| 25 m Digital Elevation Model | Slope, elevation and directional walking gradient | LIST Tasmania 25 Metre Digital Elevation Model |
| TASVEG 5.0 vegetation mapping | Vegetation communities and environmental-sensitivity scores | Department of Natural Resources and Environment Tasmania (2025) |
| Existing walking-track network | Distance to established tracks | [Confirm dataset title and custodian] |
| Watercourse polylines | Distance to waterways and potential crossings | [Confirm dataset title and custodian] |
| Study-area boundary and destination points | Analysis extent and required route waypoints | Project GIS layers; destination locations to be checked against source mapping |

The input layers required different forms of preparation before they could be compared. Multiple DEM tiles were mosaicked to obtain continuous elevation coverage, while the two local-government watercourse datasets were combined into a single layer. Vector and raster datasets were then projected to GDA2020 / MGA Zone 55 (EPSG:7855), a metre-based coordinate system suitable for measuring distances in southern Tasmania.

All inputs were clipped to the same study-area boundary and aligned to a common raster grid, using the 25 m DEM as the reference resolution. Continuous data, such as elevation, were resampled using an appropriate continuous-data method, while categorical vegetation values were retained using nearest-neighbour resampling. Raster alignment was checked so corresponding cells represented the same ground locations. Cells outside the study boundary or without valid input data were excluded from the suitability calculations.

Because each 25 m raster cell represents a generalised area, the analysis is intended for preliminary corridor planning rather than the identification of construction-ready track alignments.

## Selecting and standardising the criteria

The model used four criteria representing environmental protection and recreational practicality. Their selection was informed by track-impact literature, Tasmanian walking-track management guidance and the practical requirements of linking the three destinations (Parks and Wildlife Service, 2011; Whinam & Chilcott, 2003; Williams et al., 2025).

Each criterion was converted to a common ordinal suitability scale:

$$
S_j(x) \in \{1,2,3,4,5\}
$$

where $S_j(x)$ is the suitability score assigned to raster cell $x$ for criterion $j$. A score of 1 indicates relatively low suitability and 5 indicates relatively high suitability. This common direction is important: every input must represent a benefit, with larger values consistently indicating more favourable conditions.

### Environmental sensitivity

TASVEG vegetation communities were assigned project-defined suitability scores according to their anticipated vulnerability to ground disturbance, including trampling, understorey clearance and soil degradation. Ecologically sensitive or wet vegetation communities were given lower scores, while comparatively more resilient forest communities were assigned higher scores. These were screening judgements informed by vegetation descriptions and evidence of trampling impacts in Tasmanian alpine and subalpine environments (Whinam & Chilcott, 2003), not official sensitivity ratings published by TASVEG.

The mapping distinguishes vegetation communities, but it does not establish the precise location of every threatened species. Species records informed interpretation and discussion; they were not assumed to indicate confirmed occupancy in every cell of a mapped community. The complete community-to-score lookup table should be included in the repository to make this classification reproducible.

### Slope and walking convenience

Slope was derived from the DEM and expressed in degrees. Lower gradients generally offer more practical opportunities for track construction and walking, whereas steep slopes may require major earthworks, steps or erosion-control structures. The proposed slope reclassification was:

| Slope (degrees) | Suitability score |
|---|---:|
| 0 to less than 10 | 5 |
| 10 to less than 20 | 4 |
| 20 to less than 30 | 3 |
| 30 to less than 42 | 2 |
| 42 or greater | 1 |

These breakpoints are project-defined modelling assumptions rather than universally accepted walking-track standards. Slopes at or above 42° were also proposed as a routing constraint; this exclusion must be checked against the final pathfinding code and terrain feasibility.

Slope appears twice in the overall analysis but serves different purposes. Here it represents general suitability for track development; later, *directional gradient* influences estimated effort when moving between adjacent cells. Because these effects are related, the possibility of double-counting slope is considered in the model evaluation.

### Proximity to existing walking tracks

Distance to the existing track network was calculated for each raster cell. Locations nearer established tracks were generally favoured because they may offer opportunities to connect with existing infrastructure and limit the length of entirely new construction. Tasmanian track-management guidance highlights the need to plan additions to the track network carefully rather than encourage unnecessary track proliferation (Parks and Wildlife Service, 2011).

Proximity is nevertheless only a screening indicator. Being near an existing track does not prove that a new alignment can physically or environmentally connect to it. The final analysis should distinguish proximity to an existing track from the actual distance a proposed route follows that track.

### Hydrological sensitivity

Distance to mapped watercourses was calculated to identify areas where new track construction could interfere with drainage, increase erosion or create the need for crossings. Cells closer to waterways were generally scored less favourably, while those farther away received higher scores.

Distance classes were defined for this project rather than interpreted as statutory walking-track setbacks. They require confirmation against the final reclassification code. Drainage conditions cannot be inferred completely from mapped watercourse lines: seepage, saturated soils and small unmapped channels may also affect route feasibility, especially near Fools Tarn.

[Insert four-panel figure: standardised environmental sensitivity, slope, track proximity and watercourse proximity rasters. Use a shared legend where 1 = least suitable and 5 = most suitable.]

## Assigning criterion weights

The four criteria were assigned a common set of weights for both suitability models. Vegetation sensitivity received the greatest emphasis (45%), followed by slope (25%), hydrological sensitivity (20%) and proximity to existing tracks (10%). This weighting prioritises the avoidance of ecologically sensitive environments while still recognising walking feasibility, drainage impacts and infrastructure connectivity.

| Criterion | Weight | Relative importance |
|---|---:|---:|
| Environmental sensitivity | 0.45 | 45% |
| Existing-track proximity | 0.10 | 10% |
| Slope and walking convenience | 0.25 | 25% |
| Hydrological sensitivity | 0.20 | 20% |
| Total | 1.00 | 100% |

The weights satisfy:

$$
\sum_{j=1}^{4} w_j = 1
$$

where $w_j$ denotes the weight of criterion $j$.

These weights represent the group's planning priorities and should not be presented as objectively measured environmental impacts or as the output of an Analytic Hierarchy Process unless pairwise AHP calculations were actually performed. Applying identical weights to WLC and TOPSIS provides a controlled comparison of the two decision rules.

## Weighted Linear Combination (WLC)

WLC combines the four standardised criteria into a single suitability surface. For each raster cell, every criterion score is multiplied by its weight and the results are summed (Malczewski, 2006).

$$
\mathrm{WLC}(x) = \sum_{j=1}^{4} w_j S_j(x)
$$

For this project, the weighted model can be written explicitly as:

$$
\boxed{\mathrm{WLC}(x)=0.45V(x)+0.25G(x)+0.20H(x)+0.10T(x)}
$$

Here, $V$ is the vegetation-sensitivity score, $T$ is the existing-track proximity score, $G$ is the slope score and $H$ is the hydrological score. Higher WLC values indicate more favourable combinations of the four conditions.

For example, a cell with scores of 4 for vegetation, 3 for track proximity, 5 for slope and 2 for hydrology would receive:

$$
\mathrm{WLC}=0.45(4)+0.25(5)+0.20(2)+0.10(3)=3.75
$$

The example demonstrates how the weighted sum works; it is not a measured result from the study area. A strength of WLC is its transparency: readers can see exactly how each criterion contributes. Its limitation is compensability, meaning a poor result for one criterion can be offset by high scores in others. This is particularly important where ecologically sensitive sites might warrant exclusion rather than a merely lower score.

## Technique for Order Preference by Similarity to Ideal Solution (TOPSIS)

TOPSIS evaluates each raster cell relative to a hypothetical best and worst combination of criterion values. Whereas WLC directly adds weighted scores, TOPSIS identifies cells that are simultaneously close to the positive ideal and far from the negative ideal (Hwang & Yoon, 1981).

First, the standardised criterion scores are vector-normalised across all valid study-area cells:

$$
r_{ij}=\frac{S_{ij}}{\sqrt{\sum_{k=1}^{m}S_{kj}^{2}}}
$$

Here, $S_{ij}$ is the score of cell $i$ for criterion $j$, and $m$ is the number of valid raster cells. The normalised values are then multiplied by the same weights used in WLC:

$$
v_{ij}=w_j r_{ij}
$$

For each criterion, the positive ideal is the highest weighted normalised value and the negative ideal is the lowest, because all inputs have been coded so that higher values mean greater suitability:

$$
A_j^{+}=\max_i(v_{ij}), \qquad A_j^{-}=\min_i(v_{ij})
$$

Each cell's Euclidean distance to the two ideals is calculated:

$$
D_i^{+}=\sqrt{\sum_{j=1}^{4}(v_{ij}-A_j^{+})^2}
$$

$$
D_i^{-}=\sqrt{\sum_{j=1}^{4}(v_{ij}-A_j^{-})^2}
$$

Finally, relative closeness to the ideal solution is calculated:

$$
\boxed{C_i=\frac{D_i^{-}}{D_i^{+}+D_i^{-}}}
$$

Values of $C_i$ range from 0 to 1, with higher values indicating cells closer to the preferred combination of criteria. The TOPSIS surface was retained as a continuous relative-suitability measure so that differences would not be concealed by premature classification into broad map categories.

Unlike WLC, TOPSIS is sensitive to the distribution of scores across the study area because vector normalisation and ideal values are calculated from the cells being compared. This provides a useful basis for investigating whether the two methods identify similar or contrasting areas as suitable for walking-track development.

[Insert side-by-side figure: WLC suitability and TOPSIS relative closeness, each with an accurately labelled colour scale.]

## Anisotropic walking costs

High landscape suitability does not guarantee that a location forms part of an efficient walking route. A walker moving uphill may experience a different travel cost from someone moving downhill across the same terrain. This direction-dependent behaviour is described as *anisotropic* movement.

A widely used starting point is Tobler's (1993) hiking function, which estimates walking speed from the signed gradient of travel:

$$
\boxed{v(s)=6e^{-3.5\lvert s+0.05\rvert}}
$$

where $v(s)$ is walking speed in kilometres per hour, $e$ is the base of the natural logarithm, and $s$ is signed gradient, calculated as elevation change divided by horizontal distance. Positive gradients indicate uphill movement, negative gradients indicate downhill movement. Gradient is a ratio, not a slope angle in degrees.

For movement from cell $i$ to a neighbouring cell $j$, directional gradient is:

$$
s_{ij}=\frac{z_j-z_i}{d_{ij}}
$$

where $z_i$ and $z_j$ are elevations in metres and $d_{ij}$ is horizontal movement distance in metres. For a square raster grid, diagonal moves have a greater horizontal distance than orthogonal moves.

If Tobler's function is used to convert directional gradient into edge travel time, the estimated time in minutes is:

$$
t_{ij}=\frac{60\,d_{ij}}{1000\,v(s_{ij})}
$$

Tobler's equation provides a general approximation of pedestrian speed, not a precise prediction for experienced walkers negotiating boulders, wet vegetation or unformed tracks. Accordingly, it should be interpreted as a comparative movement-cost model rather than an itinerary time estimate. The exact walking-speed function and any off-track adjustment must be checked against the implemented `04_walking_cost.ipynb` notebook.

## Integrating suitability and least-cost route optimisation

To integrate walking effort and environmental suitability, the suitability surfaces must be translated into penalties: relatively suitable cells should be cheaper to cross, while less suitable cells should be more costly.

One transparent way to express this relationship is to define a dimensionless suitability penalty $p$:

$$
p_i^{\mathrm{WLC}}=\frac{5-\mathrm{WLC}_i}{4}
$$

$$
p_i^{\mathrm{TOPSIS}}=1-C_i
$$

Using the mean penalty of the cells at either end of a movement, a combined directed edge-cost formulation is:

$$
\boxed{c_{ij}=t_{ij}\left[1+\lambda\left(\frac{p_i+p_j}{2}\right)\right]}
$$

where $t_{ij}$ is the directional walking time, $p_i$ and $p_j$ are suitability penalties, and $\lambda\geq0$ controls how strongly environmental suitability influences route choice relative to movement effort. A value of $\lambda=0$ would remove the suitability penalty, producing a movement-effort-only comparison. The final form and value of $\lambda$ must match the implemented cost function; this equation is a proposed representation, not a verified transcription of the current code.

A pathfinding algorithm then seeks the route with the lowest cumulative edge cost:

$$
\boxed{P^*=\operatorname*{arg\,min}_{P}\sum_{(i,j)\in P}c_{ij}}
$$

Here, $P$ is any permissible route between the specified endpoints, and $P^*$ is the route with the lowest cumulative cost. Raster cells form the graph nodes, while permissible movements between neighbouring cells form weighted, directed edges. A graph-based shortest-path solver such as Dijkstra's algorithm or A* can be used, provided the implementation handles direction-dependent edge costs correctly.

The analysis first connects the trailhead to Slump Pond, then Slump Pond to Fools Tarn, and finally Fools Tarn to Hutchinsons Falls. The three segments are joined in that order. Where applied, steep-slope exclusions and any other valid barriers are enforced consistently for both the WLC-based and TOPSIS-based routes.

The resulting paths are modelled corridor alternatives, not surveyed or approved track alignments. In particular, a 25 m grid cannot resolve individual boulders, narrow gullies, informal drainage lines or microsites that may prevent practical construction.

## Comparing the alternatives

The performance of the routes is evaluated across the planning objectives rather than declaring the minimum-cost path automatically preferable. For a route consisting of $n$ consecutive movements, total horizontal distance is:

$$
L(P)=\sum_{k=1}^{n}d_k
$$

Total accumulated ascent is calculated from positive elevation changes only:

$$
A(P)=\sum_{k=1}^{n}\max(0,z_{k+1}-z_k)
$$

Where directional time costs are used, overall modelled walking time is:

$$
T(P)=\sum_{k=1}^{n}t_k
$$

Route comparison should additionally report mean landscape suitability, the number of mapped watercourse crossings, the proportion of the alignment coinciding with or close to existing tracks, and the length traversing low-suitability vegetation. These outcomes measure different aspects of route quality; no single measure should be used as a substitute for the others.

To assess the influence of methodological choices, the WLC- and TOPSIS-derived routes can be compared with a shortest-feasible-distance or movement-effort-only baseline under the same barriers. A sensitivity assessment should also test whether moderate changes to criterion weights or the suitability-penalty parameter materially alter route geometry. If these additional comparisons are not ultimately implemented, they should be removed from the final Methods description rather than presented as completed analyses.

[Insert route-comparison figure: modelled alternatives over hillshade, followed by a chart of route length, accumulated ascent, environmental suitability and crossings.]

## Interpretation, limitations and reproducibility

This workflow provides a transparent, repeatable screening method for evaluating possible track corridors. Its conclusions are conditional on the accuracy of source maps, the choice of raster resolution, the classification of vegetation communities, the four weights and the walking-cost assumptions. In particular, higher modelled suitability should not be interpreted as proof of low ecological impact. A route that performs well numerically may still intersect unmapped habitat, culturally sensitive locations, unstable terrain or drainage features that require field assessment.

The analysis was developed using Python notebooks and reusable geospatial functions stored in the project repository. The workflow is organised into data preparation, WLC, TOPSIS, walking costs, least-cost paths and model comparison, allowing the outputs to be regenerated and each methodological decision to be inspected. All final parameter values and dataset versions should be documented alongside the code. As Williams et al. (2025) demonstrate for Tasmanian geotrail planning, field validation remains an essential step between GIS-modelled routes and practical trail proposals.
