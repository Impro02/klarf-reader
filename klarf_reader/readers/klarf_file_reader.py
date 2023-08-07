# MODULES
import re
import os
from pathlib import Path
from typing import Dict, Generator, List, Tuple

# MODELS
from ..models.klarf_content import (
    Defect,
    DieOrigin,
    DiePitch,
    InspectionStationId,
    KlarfContent,
    SampleCenterLocation,
    SamplePlanTest,
    SetupId,
    Summary,
    Test,
    Wafer,
)

ACCEPTED_KLARF_VERSIONS = [1.1, 1.2]


def _get_raw_content(klarf: Path):
    with open(klarf, "r") as f:
        for line in f.readlines():
            yield line


def readKlarf(
    klarf: Path,
    custom_columns_wafer: List[str] = None,
    custom_columns_defect: List[str] = None,
    parse_summary: bool = True,
    defects_as_generator: bool = False,
) -> Tuple[KlarfContent, Generator[str, None, None],]:
    """this function open, read and parse a klarf file

    Args:
        klarf (Path): the path of the klarf file

    Returns:
        KlarfContent: the content of the klarf as a dataclass
    """

    if not os.path.exists(klarf):
        raise Exception(f"{klarf=} does not exists")

    raw_content = _get_raw_content(klarf)

    klarf_content = convert_raw_to_klarf_content(
        raw_content=_get_raw_content(klarf),
        custom_columns_wafer=custom_columns_wafer,
        custom_columns_defect=custom_columns_defect,
        parse_summary=parse_summary,
        defects_as_generator=defects_as_generator,
    )

    klarf_content.wafers = list(
        {item.id: item for item in klarf_content.wafers}.values()
    )

    return klarf_content, raw_content


def convert_raw_to_klarf_content(
    raw_content: Generator[str, None, None],
    custom_columns_wafer: List[str] = None,
    custom_columns_defect: List[str] = None,
    parse_summary: bool = True,
    defects_as_generator: bool = False,
) -> KlarfContent:

    RAW_DEFECT_COLUMNS = [
        "DEFECTID",
        "XREL",
        "YREL",
        "XINDEX",
        "YINDEX",
        "XSIZE",
        "YSIZE",
        "DEFECTAREA",
        "DSIZE",
        "CLASSNUMBER",
        "TEST",
        "CLUSTERNUMBER",
        "ROUGHBINNUMBER",
        "FINEBINNUMBER",
        "IMAGECOUNT",
    ]

    device_id = None
    setup_id = "no_setup"
    sample_type = None
    next_line_has_coords, next_line_has_numb = (False, False)
    has_sample_test_plan, next_line_has_sample_test_plan, skip_next_sample_test_plan = (
        False,
        False,
        False,
    )
    sample_plan_test_x, sample_plan_test_y = [], []
    wafers: List[Wafer] = []
    tests: List[Test] = []

    if custom_columns_wafer is None:
        custom_columns_wafer = []

    if custom_columns_defect is None:
        custom_columns_defect = []

    index = 0
    custom_columns_found = False
    custom_columns_wafer_dict = {}
    for line in raw_content:
        index += 1
        line = line.rstrip("\n")

        if index == 1 and not line.lstrip().lower().startswith("fileversion"):
            raise Exception(f"Unable to read this format from klarf")

        for item in custom_columns_wafer:
            if line.lstrip().lower().startswith(item.lower()):
                attribute_values = line.rstrip(";").split()
                custom_columns_wafer_dict[item] = attribute_values[1]
                custom_columns_found = True

                break

        if custom_columns_found:
            custom_columns_found = False
            continue

        if line.lstrip().lower().startswith("fileversion"):
            file_version_values = line.rstrip(";").split(" ")
            file_version = float(f"{file_version_values[1]}.{file_version_values[2]}")
            if file_version not in ACCEPTED_KLARF_VERSIONS:
                raise ValueError(
                    f"Klarf file version not valid (current={file_version} | accepted={ACCEPTED_KLARF_VERSIONS})"
                )
            continue

        if line.lstrip().lower().startswith("filetimestamp"):
            file_timestamp = line[14:33].rstrip(";")
            continue

        if line.lstrip().lower().startswith("inspectionstationid"):
            inspection_station_id = line.split(";")[0].split(" ")
            inspection_station_id = [id.strip('"') for id in inspection_station_id]
            inspection_station_id = inspection_station_id[1:4]

            inspection_station_id = InspectionStationId(*inspection_station_id)
            continue

        if line.lstrip().lower().startswith("sampletype"):
            sample_type = line.rstrip(";").split()[1]
            continue

        if line.lstrip().lower().startswith("resulttimestamp"):
            result_timestamp = line[16:35].rstrip(";")
            continue

        if line.lstrip().lower().startswith("lotid"):
            lot_id = line.split('"')[1]
            continue

        if line.lstrip().lower().startswith("samplesize"):
            sample_size = line.rstrip(";").split(" ")[2]
            sample_size = int(sample_size)
            continue

        if line.lstrip().lower().startswith("deviceid"):
            device_id = line.split('"')[1]
            continue

        if line.lstrip().lower().startswith("setupid"):
            setup_id_value = line.rstrip(";").split('"')
            setup_id = SetupId(
                name=setup_id_value[1].strip(), date=setup_id_value[2].strip()
            )
            continue

        if line.lstrip().lower().startswith("stepid"):
            step_id = line.split('"')[1]
            continue

        if line.lstrip().lower().startswith("sampleorientationmarktype"):
            sample_orientation_mark_type = line.rstrip(";").split()[1]
            continue

        if line.lstrip().lower().startswith("orientationmarklocation"):
            orientation_mark_location = line.rstrip(";").split()[1]
            continue

        if line.lstrip().lower().startswith("diepitch"):
            die_pitch_value = line.rstrip(";").split()
            die_pitch = DiePitch(
                x=float(die_pitch_value[1]), y=float(die_pitch_value[2])
            )
            continue

        if line.lstrip().lower().startswith("dieorigin"):
            die_origin_value = line.rstrip(";").split()
            die_origin = DieOrigin(
                x=float(die_origin_value[1]), y=float(die_origin_value[2])
            )
            continue

        if line.lstrip().lower().startswith("samplecenterlocation"):
            sample_center_location_value = line.rstrip(";").split()
            sample_center_location = SampleCenterLocation(
                x=float(sample_center_location_value[1]),
                y=float(sample_center_location_value[2]),
            )
            continue

        if line.lstrip().lower().startswith("waferid"):
            wafer_id = line.split('"')[1]
            continue

        if line.lstrip().lower().startswith("slot"):
            slot_values = line.rstrip(";").split()
            slot = int(slot_values[1])
            continue

        if line.lstrip().lower().startswith("inspectiontest"):
            inspection_test = line.rstrip(";").split()
            inspection_test = int(inspection_test[1])
            continue

        if line.lstrip().lower().startswith("areapertest"):
            area_per_test = line.rstrip(";").split()
            area_per_test = float(area_per_test[1])

            tests.append(
                Test(id=inspection_test, area=area_per_test),
            )
            continue

        if line.lstrip().lower().startswith("defectrecordspec"):
            defects = []

            line_without_space = re.sub("\s+", " ", line).strip()
            parameters = line_without_space.strip().split(" ")

            defect_columns = {
                column: parameters.index(column) - 1
                for column in RAW_DEFECT_COLUMNS
                if column in parameters
            }
            defect_columns_custom = {
                column: parameters.index(column) - 1
                for column in custom_columns_defect
                if column in parameters
            }

            continue

        if line.lstrip().lower().startswith("defectlist"):
            next_line_has_coords = True

            if not line.rstrip().endswith(";"):
                continue

        if next_line_has_coords:
            if line.startswith(" "):

                defect_parameters = line.strip().split(";")[0].split()

                defect_paramters_values = {
                    k.lower(): defect_parameters[v - 1]
                    for k, v in defect_columns.items()
                }

                defect_paramters_custom_values = {
                    k.lower(): defect_parameters[v - 1]
                    for k, v in defect_columns_custom.items()
                }

                x, y = convert_coordinates(
                    die_pitch=die_pitch,
                    sample_center_location=sample_center_location,
                    xrel=float(defect_paramters_values.get("xrel")),
                    yrel=float(defect_paramters_values.get("yrel")),
                    xindex=int(defect_paramters_values.get("xindex")),
                    yindex=int(defect_paramters_values.get("yindex")),
                )

                roughbin = defect_paramters_values.get("roughbinnumber")
                roughbin = int(roughbin) if roughbin is not None else 0

                finebin = defect_paramters_values.get("finebinnumber")
                finebin = int(finebin) if finebin is not None else 0

                image_count = defect_paramters_values.get("imagecount")
                image_count = int(image_count) if image_count is not None else 0

                cluster_number = defect_paramters_values.get("clusternumber")
                cluster_number = (
                    int(cluster_number) if cluster_number is not None else 0
                )

                defects.append(
                    Defect(
                        id=int(defect_paramters_values.get("defectid")),
                        x_rel=float(defect_paramters_values.get("xrel")),
                        y_rel=float(defect_paramters_values.get("yrel")),
                        x_index=int(defect_paramters_values.get("xindex")),
                        y_index=int(defect_paramters_values.get("yindex")),
                        x_size=float(defect_paramters_values.get("xsize")),
                        y_size=float(defect_paramters_values.get("ysize")),
                        area=float(defect_paramters_values.get("defectarea")),
                        d_size=float(defect_paramters_values.get("dsize")),
                        class_number=int(defect_paramters_values.get("classnumber")),
                        test_id=int(defect_paramters_values.get("test")),
                        cluster_number=cluster_number,
                        image_count=image_count,
                        roughbin=roughbin,
                        finebin=finebin,
                        point=(x, y),
                        custom_attribute=defect_paramters_custom_values,
                    )
                )

            if line.rstrip().endswith(";"):
                next_line_has_coords = False

                wafers.append(
                    Wafer(
                        id=wafer_id,
                        slot=slot,
                        die_origin=die_origin,
                        sample_center_location=sample_center_location,
                        defects=(defect for defect in defects)
                        if defects_as_generator
                        else defects,
                        tests=tests.copy(),
                        custom_attribute=custom_columns_wafer_dict,
                    )
                )

                tests.clear()

        if (
            parse_summary
            and line.lstrip().lower().startswith("summarylist")
            and not (line.rstrip().endswith(";"))
        ):
            next_line_has_numb = True
            continue

        if next_line_has_numb and line.startswith(" "):
            next_line_has_numb = False
            linewithoutSpace = re.sub("[\s;]+", " ", line).strip()

            split = linewithoutSpace.split()

            wafers[-1].summary = Summary(
                number_of_defects=int(split[1]),
                defect_density=float(split[2]),
                number_of_dies=int(split[3]),
                number_of_def_dies=int(split[4]),
            )
            continue

        if not skip_next_sample_test_plan and line.lstrip().lower().startswith(
            "sampletestplan"
        ):
            next_line_has_sample_test_plan = True
            has_sample_test_plan = True
        if next_line_has_sample_test_plan:
            if line.startswith(" "):
                sample_test_plan_value = line.strip().rstrip(";").split()

                x = int(sample_test_plan_value[0])
                sample_plan_test_x.append(x)

                y = int(sample_test_plan_value[1])
                sample_plan_test_y.append(y)
            if line.rstrip().endswith(";"):
                next_line_has_sample_test_plan = False
                skip_next_sample_test_plan = True
            continue

    return KlarfContent(
        file_version=file_version,
        file_timestamp=file_timestamp,
        inspection_station_id=inspection_station_id,
        sample_type=sample_type,
        result_timestamp=result_timestamp,
        lot_id=lot_id,
        device_id=device_id,
        sample_size=sample_size,
        step_id=step_id,
        sample_orientation_mark_type=sample_orientation_mark_type,
        orientation_mark_location=orientation_mark_location,
        die_pitch=die_pitch,
        setup_id=setup_id,
        has_sample_test_plan=has_sample_test_plan,
        sample_plan_test=SamplePlanTest(x=sample_plan_test_x, y=sample_plan_test_y),
        wafers=wafers,
    )


def convert_coordinates(
    die_pitch: DiePitch,
    sample_center_location: SampleCenterLocation,
    xrel: float,
    yrel: float,
    xindex: int,
    yindex: int,
) -> Tuple[float, float]:
    """convert defect attributes to real x,y coordianates

    Args:
        die_pitch (DiePitch): _description_
        sample_center_location_x (float): _description_
        sample_center_location_y (float): _description_
        xrel (float): _description_
        yrel (float): _description_
        xindex (int): _description_
        yindex (int): _description_

    Returns:
        Tuple[float, float]: the x and y coordinates
    """

    x = xindex * die_pitch.x + xrel - sample_center_location.x
    y = yindex * die_pitch.y + yrel - sample_center_location.y

    return x, y
