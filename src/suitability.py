# Import required packages
from qgis.core import QgsRasterLayer
import processing


# Define function for Weighted Linear Combination
def calculate_wlc(
    slope_raster,
    vegetation_raster,
    watercourse_raster,
    tracks_raster,
    slope_weight,
    vegetation_weight,
    watercourse_weight,
    tracks_weight,
    output_raster
):
    """
    Calculate walking-track suitability using Weighted
    Linear Combination (WLC) of four reclassified rasters.

    Parameters
    ----------
    slope_raster : str or Path
        Filepath to the reclassified slope raster.

    vegetation_raster : str or Path
        Filepath to the reclassified vegetation raster.

    watercourse_raster : str or Path
        Filepath to the standardised watercourse distance raster.

    tracks_raster : str or Path
        Filepath to the standardised existing-track distance raster.

    slope_weight : float
        Weight applied to the slope criterion.

    vegetation_weight : float
        Weight applied to the vegetation criterion.

    watercourse_weight : float
        Weight applied to the hydrological criterion.

    tracks_weight : float
        Weight applied to the existing-track proximity criterion.

    output_raster : str or Path
        Filepath for the final walking-track suitability raster.

    Returns
    -------
    str
        Filepath to the WLC walking-track suitability raster.
    """

    # Load reclassified raster datasets
    slope_layer = QgsRasterLayer(
        str(slope_raster),
        "Slope"
    )

    vegetation_layer = QgsRasterLayer(
        str(vegetation_raster),
        "Vegetation"
    )

    watercourse_layer = QgsRasterLayer(
        str(watercourse_raster),
        "Watercourse"
    )

    tracks_layer = QgsRasterLayer(
        str(tracks_raster),
        "Tracks"
    )

    # Check that all rasters loaded correctly
    layers = [
        slope_layer,
        vegetation_layer,
        watercourse_layer,
        tracks_layer
    ]

    for layer in layers:
        if not layer.isValid():
            raise ValueError(
                f"{layer.name()} raster could not be loaded"
            )

    # Check weights sum to 1
    total_weight = (
        slope_weight
        + vegetation_weight
        + watercourse_weight
        + tracks_weight
    )

    if abs(total_weight - 1.0) > 1e-6:
        raise ValueError("WLC weights must sum to 1.0")

    # Check rasters have matching grids
    reference = slope_layer

    for layer in layers[1:]:
        if (
            layer.crs() != reference.crs()
            or layer.width() != reference.width()
            or layer.height() != reference.height()
            or layer.extent() != reference.extent()
        ):
            raise ValueError(
                f"{layer.name()} does not match the slope raster grid"
            )

    # Weighted Linear Combination expression
    expression = (
        f'("Slope@1" * {slope_weight}) + '
        f'("Vegetation@1" * {vegetation_weight}) + '
        f'("Watercourse@1" * {watercourse_weight}) + '
        f'("Tracks@1" * {tracks_weight})'
    )

    # Calculate WLC suitability raster
    processing.run(
        "native:rastercalc",
        {
            "LAYERS": layers,
            "EXPRESSION": expression,
            "EXTENT": reference.extent(),
            "CELL_SIZE": reference.rasterUnitsPerPixelX(),
            "CRS": reference.crs(),
            "OUTPUT": str(output_raster)
        }
    )

    print(f"WLC suitability raster created: {output_raster}")

    return str(output_raster)
