# Discussion 

## WLC and TOPSIS and their Outcomes

Despite using identical criteria and weights, WLC and TOPSIS produced noticeably different suitability surfaces and walking-track alignments. WLC displayed greater spatial variation, whereas TOPSIS classified much of the study area within a narrower, moderately high suitability range. This demonstrates how different aggregation methods can influence spatial decision-making, even when the underlying environmental information remains unchanged (Malczewski, 2006).

WLC permits favourable conditions in one criterion to compensate for less suitable conditions in another, while TOPSIS evaluates alternatives according to their relative distances from ideal and least-ideal solutions (Hwang & Yoon, 1981). Neither method inherently produces a more environmentally sustainable route; their reliability depends on how the criteria, weights and constraints represent the planning problem.

The greatest route divergence occurred between Fools Tarn and Hutchinsons Falls, where TOPSIS followed a more westerly alignment and WLC a more easterly corridor. This finding demonstrates that selecting an MCDA decision rule can influence the geographical location of proposed recreational infrastructure.

## Environmental Sustainability Versus Walking Efficiency

A key limitation was that both modelled routes traversed sensitive vegetation despite environmental sensitivity receiving the highest weighting (45%). This was particularly concerning near Fools Tarn, where highland grassy sedgeland contains recorded dainty leek-orchid occurrences.

Research demonstrates that recreational trail construction and trampling can contribute to vegetation damage, soil compaction and erosion (Ballantyne & Pickering, 2015; Pickering et al., 2010). The modelled alignments therefore highlight a conflict between minimising walking effort and conserving sensitive habitats.

Both routes also established substantial new corridors towards Hutchinsons Falls rather than following more of the existing Moss-Bed Link. Although the resulting alignments minimise the defined movement costs, constructing additional infrastructure could introduce avoidable ecological disturbance and maintenance requirements.

This suggests that the existing-track criterion, weighted at 10%, may have provided insufficient incentive for infrastructure reuse. However, this cannot be confirmed without testing alternative weights.

Importantly, the findings expose a limitation of compensatory MCDA: high suitability for slope or other criteria may offset poor environmental suitability (Malczewski, 2006). Where habitat protection is essential, exclusion zones or non-compensatory constraints may be more appropriate than low suitability scores alone.

## A* Versus Dijkstra: Does the Algorithm Matter?

Dijkstra's algorithm identifies minimum-cost paths through systematic network exploration, whereas A* uses a heuristic to guide the search towards the destination (Dijkstra, 1959; Hart et al., 1968).

When applied to identical non-negative movement costs with an admissible heuristic, both can identify optimal paths of equal total cost. The algorithms therefore differ primarily in search efficiency rather than the quality of their environmental decisions.

The broadly similar outcomes observed in this project suggest that **the definition of the cost surface matters more to route selection than the choice of optimal pathfinding algorithm**. Consequently, separate A* and Dijkstra route figures were not prioritised, allowing greater emphasis on the differences between WLC and TOPSIS.

## Sensitivity Analysis and Future Improvements

The results demonstrate the importance of testing how modelling assumptions influence route selection. Sensitivity analysis is widely recognised as an important component of spatial MCDA because criterion weights and standardisation decisions can substantially affect rankings and resulting decisions (Malczewski, 2006).

Future analysis could examine increased penalties for conservation-significant vegetation, stronger incentives to reuse existing tracks and alternative criterion weights. For example, comparing routes that prioritise the Moss-Bed Link against the current modelled alignments could reveal trade-offs in walking distance, elevation change, vegetation disturbance and new construction requirements.

The analysis should also consider field-scale constraints, including cliffs, unstable ground and water crossings, which may not be adequately represented by raster datasets. As recognised in Wellington Park's management framework, recreational development must be consistent with protecting natural and cultural values (Wellington Park Management Trust, 2013).

Ultimately, the results demonstrate that **a mathematically optimal route is only optimal according to the costs included in the model**. WLC, TOPSIS and least-cost path algorithms provide valuable decision-support tools, but identifying a feasible and environmentally responsible walking track requires sensitivity testing, ecological assessment and practical evaluation beyond the initial GIS outputs.

### Beyond Least-Cost Paths: Multi-Objective Optimisation

Although A* and Dijkstra's algorithm use different search strategies, both seek minimum-cost paths through a defined network. When applied to the same non-negative movement costs with an appropriate heuristic, they can produce equally optimal solutions. Comparing these algorithms therefore offers limited insight into the competing environmental and recreational objectives of walking-track planning (Dijkstra, 1959; Hart et al., 1968).

A more informative alternative would be the **Non-dominated Sorting Genetic Algorithm II (NSGA-II)**, which explores trade-offs between multiple objectives without requiring them to be combined into a single cost value (Deb et al., 2002). For Wellington Park, these objectives could include minimising walking effort, disturbance to conservation-significant vegetation, watercourse crossings and the length of newly constructed track.

Rather than producing one minimum-cost route, NSGA-II could generate a set of approximately Pareto-optimal alternatives, where improving one objective requires compromising another. Such approaches are particularly relevant to spatial route planning, where weighted cost functions may conceal important trade-offs between competing priorities (Xiao et al., 2008).

This distinction is significant given that both modelled routes traversed sensitive vegetation and made limited use of the existing Moss-Bed Link. A multi-objective approach could reveal whether slightly greater walking effort would substantially reduce new track construction or ecological disturbance.

**Consequently, the most appropriate route may not be the one with the lowest combined cost, but the one offering the most defensible balance between environmental protection, walking convenience and practical feasibility.**