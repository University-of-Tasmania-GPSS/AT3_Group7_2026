# Welly on the Way

# Balancing Recreational Access and Environmental Conservation Through GIS-Based Walking-Track Optimisation

What makes a great walking track? Is it the shortest route between two destinations, the easiest path across challenging terrain, or the opportunity to experience landscapes that would otherwise remain inaccessible?

In protected natural areas, the answer is rarely straightforward. Walking tracks provide opportunities to experience natural landscapes, yet their construction and continued use can contribute to vegetation disturbance, soil compaction and erosion (Ballantyne & Pickering, 2015). Planning recreational infrastructure therefore requires balancing visitor access with environmental conservation.

This challenge is particularly relevant in Wellington Park, Tasmania, where rugged terrain, diverse vegetation communities and distinctive geological features create opportunities for recreation alongside significant environmental constraints. The Wellington Park Management Plan 2013 recognises the importance of providing recreational opportunities while conserving the Park's natural, cultural and water catchment values (Wellington Park Management Trust, 2013).

The challenge is not simply finding a path through the landscape, but determining where that path should go.

## Our challenge

This project investigates the potential development of a walking track for experienced bushwalkers connecting three natural features within Wellington Park: Slump Pond, Fools Tarn and Hutchinsons Falls.

Beginning at a designated trailhead on the Mountain River Trail, the proposed route will visit Slump Pond, continue to Fools Tarn and finish at the base of Hutchinsons Falls.

Connecting these destinations presents competing planning considerations, including environmentally sensitive vegetation, steep terrain, watercourses and existing recreational infrastructure. The project investigates whether a continuous route can accommodate these factors while maintaining recreational accessibility and limiting potential environmental disturbance.

Walking-track planning also forms part of Tasmania's broader protected-area management framework, which recognises the importance of maintaining recreational access while managing walking-track infrastructure and associated environmental impacts (Parks and Wildlife Service, 2011).

## Why use GIS?

Geographic Information Systems (GIS) provide a systematic framework for evaluating landscapes through multiple spatial datasets. GIS-based multi-criteria decision analysis (MCDA) enables competing environmental and recreational priorities to be considered together rather than selecting routes based on distance or visual interpretation alone (Malczewski, 2006).

This project compares two MCDA methods: Weighted Linear Combination (WLC) and the Technique for Order Preference by Similarity to Ideal Solution (TOPSIS). WLC combines standardised criteria through weighted summation, while TOPSIS evaluates alternatives according to their relative proximity to ideal and least-ideal conditions (Hwang & Yoon, 1981). Comparing these methods allows the influence of different decision rules on spatial suitability predictions to be investigated.

Four criteria are considered: environmental sensitivity, slope-based walking convenience, proximity to existing tracks and hydrological sensitivity.

However, suitable areas do not necessarily form practical walking routes. Pedestrian movement varies with terrain gradient and direction of travel, as demonstrated by Tobler's (1993) slope-dependent walking-speed model. Integrating suitability assessment with anisotropic movement-cost modelling and least-cost path optimisation therefore provides a framework for evaluating alternative routes across complex terrain.

## Project aim

To identify and compare potential walking routes connecting Slump Pond, Fools Tarn and the base of Hutchinsons Falls using GIS-based multi-criteria suitability analysis, terrain-dependent walking costs and least-cost path optimisation.

## Project objectives

1. Assess landscape suitability: Identify and standardise environmental, topographic and accessibility factors influencing potential walking-track development.
2. Compare MCDA approaches: Develop WLC and TOPSIS suitability models using consistent criteria and weights, and evaluate differences in their spatial predictions.
3. Model walking effort: Incorporate directional terrain effects into an anisotropic movement-cost model.
4. Optimise potential routes: Generate continuous least-cost routes connecting the three destinations in a predetermined sequence.
5. Evaluate route alternatives: Compare modelled routes according to distance, terrain difficulty, cumulative movement cost and environmental suitability.

## Our approach

Combining Python, GIS and spatial decision modelling, this project explores how geospatial technologies can inform recreational infrastructure planning in environmentally complex landscapes.

The resulting routes are not intended as final construction proposals, but as evidence-based alternatives that can inform further environmental assessment and field investigation.

Ultimately, the project asks a broader question: Can the best path through a landscape also be one that respects the landscape it passes through?
