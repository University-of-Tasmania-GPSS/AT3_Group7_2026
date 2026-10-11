
# Import required packages
from pathlib import Path
from heapq import heappush, heappop
from math import exp, hypot, isfinite

import numpy as np
import rasterio


# Calculate walking speed using Tobler's function
def tobler_speed(gradient):
    """
    Calculate walking speed from directional terrain gradient.

    Parameters
    ----------
    gradient : float
        Signed rise/run gradient between two raster cells.
        Positive = uphill, negative = downhill.

    Returns
    -------
    float
        Estimated walking speed in kilometres per hour.
    """
    return 6 * exp(-3.5 * abs(gradient + 0.05))


# Define anisotropic least-cost path function
def calculate_walking_path(
    dem_file,
    suitability_file,
    start_xy,
    end_xy,
    output_route,
    penalty_strength=2.0
):
    """
    Calculate an anisotropic least-cost walking path using
    Tobler's Hiking Function and an MCDA suitability penalty.

    Parameters
    ----------
    dem_file : str or Path
        Path to the projected elevation raster.

    suitability_file : str or Path
        Path to the WLC or TOPSIS suitability raster,
        standardised between 0 and 1.

    start_xy : tuple
        Starting coordinates (Easting, Northing) in the
        raster CRS.

    end_xy : tuple
        Destination coordinates (Easting, Northing) in
        the raster CRS.

    output_route : str or Path
        Path for the resulting least-cost route GeoTIFF.

    penalty_strength : float, optional
        Controls the influence of suitability on walking
        cost. Default is 2.0.

    Returns
    -------
    float
        Total accumulated penalised walking cost.
    """

    if penalty_strength < 0:
        raise ValueError("Penalty strength must be >= 0")

    # Load DEM
    with rasterio.open(dem_file) as src:
        dem = src.read(1, masked=True)
        dem_profile = src.profile.copy()
        transform = src.transform
        dem_crs = src.crs
        dem_nodata_mask = np.ma.getmaskarray(dem)

    # Load suitability raster
    with rasterio.open(suitability_file) as src:
        suitability = src.read(1, masked=True)
        suitability_mask = np.ma.getmaskarray(suitability)

        if (
            src.crs != dem_crs
            or src.transform != transform
            or src.shape != dem.shape
        ):
            raise ValueError(
                "DEM and suitability raster grids do not match"
            )

    # Convert input rasters to numerical arrays
    elevation = np.asarray(dem.filled(np.nan), dtype=np.float64)
    scores = np.asarray(
        suitability.filled(np.nan), dtype=np.float64
    )

    # Identify cells with valid elevation and suitability
    valid = (
        ~dem_nodata_mask
        & ~suitability_mask
        & np.isfinite(elevation)
        & np.isfinite(scores)
        & (scores >= 0)
        & (scores <= 1)
    )

    height, width = elevation.shape

    # Convert coordinates to raster indices
    start_row, start_col = rasterio.transform.rowcol(
        transform, *start_xy
    )

    end_row, end_col = rasterio.transform.rowcol(
        transform, *end_xy
    )

    start = (start_row, start_col)
    end = (end_row, end_col)

    for row, col in (start, end):
        if not (0 <= row < height and 0 <= col < width):
            raise ValueError("Start or end lies outside raster")

        if not valid[row, col]:
            raise ValueError("Start or end lies on an invalid cell")

    # Define eight neighbouring movement directions
    directions = [
        (-1, 0), (1, 0),
        (0, -1), (0, 1),
        (-1, -1), (-1, 1),
        (1, -1), (1, 1)
    ]

    # Pixel dimensions in metres
    dx = abs(transform.a)
    dy = abs(transform.e)

    # Require a north-up raster
    if (
        transform.b != 0
        or transform.d != 0
        or not dem_crs.is_projected
    ):
        raise ValueError(
            "DEM must be a north-up projected raster"
        )

    # Convert projected units to metres (EPSG:7855 expected)
    if dem_crs.to_epsg() != 7855:
        raise ValueError("Input rasters must use EPSG:7855")

    # Initialize accumulated cost
    cost = np.full((height, width), np.inf)

    # Store previous cell for reconstructing the route
    previous = np.full(
        (height, width), -1, dtype=np.int64
    )

    cost[start] = 0.0

    # Priority queue for Dijkstra's algorithm
    queue = [(0.0, start_row, start_col)]

    while queue:

        current_cost, row, col = heappop(queue)

        if current_cost > cost[row, col]:
            continue

        if (row, col) == end:
            break

        # Evaluate each possible movement direction
        for dr, dc in directions:

            nr = row + dr
            nc = col + dc

            if not (0 <= nr < height and 0 <= nc < width):
                continue

            if not valid[nr, nc]:
                continue

            # Prevent diagonal corner cutting across NoData
            if dr != 0 and dc != 0:
                if not (
                    valid[row + dr, col]
                    and valid[row, col + dc]
                ):
                    continue

            # Horizontal travel distance (metres)
            distance = hypot(dc * dx, dr * dy)

            # Directional rise/run gradient
            elevation_change = (
                elevation[nr, nc] - elevation[row, col]
            )

            gradient = elevation_change / distance

            # Walking speed in km/h
            speed = tobler_speed(gradient)

            # Base walking time in minutes
            walking_time = distance / (speed * 1000 / 60)

            # Average suitability between neighbouring cells
            average_suitability = (
                scores[row, col] + scores[nr, nc]
            ) / 2

            # Additional suitability penalty
            penalty = (
                1 + penalty_strength
                * (1 - average_suitability)
            )

            # Combined anisotropic movement cost
            movement_cost = walking_time * penalty

            new_cost = current_cost + movement_cost

            # Update least accumulated cost
            if new_cost < cost[nr, nc]:

                cost[nr, nc] = new_cost

                previous[nr, nc] = row * width + col

                heappush(
                    queue, (new_cost, nr, nc)
                )

    # Check that a path was found
    if not isfinite(cost[end]):
        raise ValueError("No valid path found between points")

    # Reconstruct least-cost route
    route = np.zeros((height, width), dtype=np.uint8)

    row, col = end

    while (row, col) != start:

        route[row, col] = 1

        parent = previous[row, col]

        if parent < 0:
            raise RuntimeError("Route reconstruction failed")

        row, col = divmod(int(parent), width)

    route[start] = 1

    # Preserve study area mask
    route[~valid] = 255

    # Update raster metadata
    dem_profile.update(
        driver="GTiff",
        dtype="uint8",
        count=1,
        nodata=255,
        compress="deflate"
    )

    # Save route raster
    output_route = Path(output_route)
    output_route.parent.mkdir(parents=True, exist_ok=True)

    with rasterio.open(
        output_route, "w", **dem_profile
    ) as dst:
        dst.write(route, 1)

    print("Least-cost route created:", output_route)
    print(
        "Accumulated penalised cost:",
        round(float(cost[end]), 3)
    )

    return float(cost[end])


# Import required packages
from pathlib import Path
from heapq import heappush, heappop
from math import exp, hypot, isfinite

import numpy as np
import rasterio
from rasterio.transform import rowcol


# Calculate walking speed using Tobler's Hiking Function
def tobler_speed(gradient):
    """
    Calculate walking speed from signed terrain gradient.

    Parameters
    ----------
    gradient : float
        Directional rise/run gradient.
        Positive = uphill; negative = downhill.

    Returns
    -------
    float
        Predicted walking speed in km/h.
    """
    return 6 * exp(-3.5 * abs(gradient + 0.05))


# Define anisotropic A* least-cost path function
def calculate_astar_path(
    dem_file,
    suitability_file,
    start_xy,
    end_xy,
    output_route,
    penalty_strength=2.0
):
    """
    Calculate an anisotropic least-cost walking path using
    A* search, Tobler's Hiking Function and MCDA suitability.

    Parameters
    ----------
    dem_file : str or Path
        Path to the DEM in EPSG:7855.

    suitability_file : str or Path
        Path to the standardised WLC or TOPSIS raster (0–1).

    start_xy : tuple
        Starting coordinates (Easting, Northing).

    end_xy : tuple
        Destination coordinates (Easting, Northing).

    output_route : str or Path
        Path for the resulting A* route GeoTIFF.

    penalty_strength : float, optional
        Strength of MCDA suitability penalty.
        Default is 2.0.

    Returns
    -------
    float
        Total accumulated penalised movement cost.
    """

    if penalty_strength < 0:
        raise ValueError("Penalty strength must be non-negative")

    # Load reference DEM
    with rasterio.open(dem_file) as src:
        dem = src.read(1, masked=True)
        profile = src.profile.copy()
        transform = src.transform
        dem_crs = src.crs
        dem_mask = np.ma.getmaskarray(dem)

    # Load MCDA suitability raster
    with rasterio.open(suitability_file) as src:
        suitability = src.read(1, masked=True)
        suitability_mask = np.ma.getmaskarray(suitability)

        # Check raster grids match
        if (
            src.crs != dem_crs
            or src.transform != transform
            or src.shape != dem.shape
        ):
            raise ValueError("DEM and suitability grids do not match")

    if dem_crs is None or dem_crs.to_epsg() != 7855:
        raise ValueError("DEM must use EPSG:7855")

    if transform.b != 0 or transform.d != 0:
        raise ValueError("DEM must be north-up and unrotated")

    if transform.a <= 0 or transform.e >= 0:
        raise ValueError("Unexpected DEM pixel orientation")

    # Convert raster data to arrays
    elevation = np.asarray(
        dem.filled(np.nan), dtype=np.float64
    )

    scores = np.asarray(
        suitability.filled(np.nan), dtype=np.float64
    )

    # Identify valid cells
    valid = (
        ~dem_mask
        & ~suitability_mask
        & np.isfinite(elevation)
        & np.isfinite(scores)
        & (scores >= 0)
        & (scores <= 1)
    )

    height, width = elevation.shape

    # Convert map coordinates to row/column
    start = rowcol(transform, *start_xy)
    end = rowcol(transform, *end_xy)

    for row, col in (start, end):
        if not (0 <= row < height and 0 <= col < width):
            raise ValueError("Start or end outside raster")

        if not valid[row, col]:
            raise ValueError("Start or end is on an invalid cell")

    # Raster cell dimensions in metres
    dx = abs(transform.a)
    dy = abs(transform.e)

    # Define 8 neighbouring movement directions
    directions = [
        (-1, 0), (1, 0),
        (0, -1), (0, 1),
        (-1, -1), (-1, 1),
        (1, -1), (1, 1)
    ]

    # Define A* heuristic: minimum possible travel time
    # Tobler maximum = 6 km/h = 100 m/min
    def heuristic(row, col):
        straight_distance = hypot(
            (end[1] - col) * dx,
            (end[0] - row) * dy
        )
        return straight_distance / 100.0

    # Initialise accumulated costs and parent pointers
    g_cost = np.full((height, width), np.inf)

    previous = np.full(
        (height, width), -1, dtype=np.int64
    )

    g_cost[start] = 0.0

    # A* priority queue: (f-score, g-score, row, col)
    queue = [
        (heuristic(*start), 0.0, start[0], start[1])
    ]

    cells_explored = 0

    # A* search
    while queue:

        f_score, current_cost, row, col = heappop(queue)

        # Ignore outdated queue entries
        if current_cost > g_cost[row, col]:
            continue

        cells_explored += 1

        # Stop when the destination is reached
        if (row, col) == end:
            break

        # Explore neighbouring cells
        for dr, dc in directions:

            nr = row + dr
            nc = col + dc

            if not (0 <= nr < height and 0 <= nc < width):
                continue

            if not valid[nr, nc]:
                continue

            # Prevent diagonal movement through NoData corners
            if dr != 0 and dc != 0:
                if not (
                    valid[row + dr, col]
                    and valid[row, col + dc]
                ):
                    continue

            # Horizontal movement distance
            distance = hypot(dc * dx, dr * dy)

            # Directional elevation change
            elevation_change = (
                elevation[nr, nc] - elevation[row, col]
            )

            gradient = elevation_change / distance

            # Tobler walking speed
            speed = tobler_speed(gradient)

            # Walking time in minutes
            walking_time = distance / (speed * 1000 / 60)

            # Average MCDA suitability of the two cells
            average_suitability = (
                scores[row, col] + scores[nr, nc]
            ) / 2

            # Suitability penalty
            penalty = (
                1 + penalty_strength
                * (1 - average_suitability)
            )

            # Combined directional movement cost
            movement_cost = walking_time * penalty

            # New accumulated cost
            new_cost = current_cost + movement_cost

            # Update neighbour if cheaper path found
            if new_cost < g_cost[nr, nc]:

                g_cost[nr, nc] = new_cost

                previous[nr, nc] = row * width + col

                # A* priority = accumulated cost + heuristic
                priority = new_cost + heuristic(nr, nc)

                heappush(
                    queue,
                    (priority, new_cost, nr, nc)
                )

    # Check whether destination was reached
    if not isfinite(g_cost[end]):
        raise ValueError("No valid path found")

    # Reconstruct optimal route
    route = np.zeros((height, width), dtype=np.uint8)

    row, col = end

    while (row, col) != start:

        route[row, col] = 1

        parent = previous[row, col]

        if parent < 0:
            raise RuntimeError("Route reconstruction failed")

        row, col = divmod(int(parent), width)

    route[start] = 1

    # Set invalid cells to NoData
    route[~valid] = 255

    # Save output raster
    profile.update(
        driver="GTiff",
        dtype="uint8",
        count=1,
        nodata=255,
        compress="deflate"
    )

    output_route = Path(output_route)
    output_route.parent.mkdir(parents=True, exist_ok=True)

    with rasterio.open(output_route, "w", **profile) as dst:
        dst.write(route, 1)

    print("A* route created:", output_route)
    print("Cells explored:", cells_explored)
    print("Accumulated cost:", round(float(g_cost[end]), 3))

    return float(g_cost[end])
