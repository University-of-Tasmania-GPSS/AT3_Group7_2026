
# Import required packages
from pathlib import Path
from qgis.core import QgsRasterLayer, QgsVectorLayer
import processing


# Define function to polygonise and merge optimised tracks
def polygonise_and_merge_tracks(
    route_files,
    output_file
):
    """
    Extracts optimised walking-track cells from raster datasets,
    converts them into vector polygons using GDAL, and merges
    the polygons into one shapefile.

    Parameters
    ----------
    route_files : list
        List of paths to optimised route rasters.
        Track cells must have a value of 1.

    output_file : str or Path
        Path and filename for the merged vector shapefile.

    Returns
    -------
    str
        Filepath to the merged polygon track dataset.
    """

    if not route_files:
        raise ValueError("No route raster files provided")

    polygon_layers = []

    for route_file in route_files:

        # Load route raster
        route_layer = QgsRasterLayer(
            str(route_file),
            Path(route_file).stem
        )

        if not route_layer.isValid():
            raise ValueError(f"Invalid raster: {route_file}")

        # Extract only track cells with value = 1
        # Background becomes 0, which is assigned NoData
        extracted = processing.run(
            "gdal:rastercalculator",
            {
                "INPUT_A": str(route_file),
                "BAND_A": 1,
                "FORMULA": "(A==1)*1",
                "NO_DATA": 0,
                "RTYPE": 0,
                "OUTPUT": "TEMPORARY_OUTPUT"
            }
        )

        # Convert valid track cells into vector polygons
        polygon_result = processing.run(
            "gdal:polygonize",
            {
                "INPUT": extracted["OUTPUT"],
                "BAND": 1,
                "FIELD": "VALUE",
                "EIGHT_CONNECTEDNESS": True,
                "EXTRA": "",
                "OUTPUT": "TEMPORARY_OUTPUT"
            }
        )

        # Load polygon layer and check output
        polygon_layer = QgsVectorLayer(
            str(polygon_result["OUTPUT"]),
            Path(route_file).stem,
            "ogr"
        )

        if not polygon_layer.isValid():
            raise ValueError(
                f"Polygonisation failed: {route_file}"
            )

        # Confirm that only route polygons were created
        if polygon_layer.featureCount() == 0:
            raise ValueError(
                f"No route polygons created: {route_file}"
            )

        values = {
            feature["VALUE"]
            for feature in polygon_layer.getFeatures()
        }

        if values != {1}:
            raise ValueError(
                f"Unexpected polygon values in {route_file}: {values}"
            )

        # Store polygon layer for merging
        polygon_layers.append(polygon_layer)

        print(f"Polygonised: {Path(route_file).name}")

    # Define output directory
    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Merge all polygon layers into one shapefile
    processing.run(
        "native:mergevectorlayers",
        {
            "LAYERS": polygon_layers,
            "OUTPUT": str(output_file)
        }
    )

    print(f"Merged tracks saved: {output_file}")

    return str(output_file)

