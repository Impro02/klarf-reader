from pathlib import Path
import re
from typing import List, Tuple

from ..models.klarf_content import (
    Defect,
    DieOrigin,
    DiePitch,
    KlarfContent,
    SampleCenterLocation,
    SamplePlanTest,
    SetupId,
    Summary,
    Wafer,
)

ACCEPTED_KLARF_VERSIONS = [1.2]


def readKlarf(klarf: Path) -> Tuple[KlarfContent, List[str]]:
    """this function open, read and parse a klarf file

    Args:
        klarf (Path): the path of the klarf file

    Returns:
        KlarfContent: the content of the klarf as a dataclass
    """

    setup_id = "no_setup"
    next_line_has_coords, next_line_has_numb = False, False
    has_sample_test_plan, next_line_has_sample_test_plan = False, False
    sample_plan_test_x, sample_plan_test_y = [], []
    wafers: List[Wafer] = []

    with open(klarf, "r") as f:
        contents = f.readlines()

        index = 0
        for line in contents:
            index += 1
            line: str = line.rstrip("\n")

            if index == 1 and not line.lstrip().lower().startswith("fileversion"):
                raise Exception(f"Unable to read this format from klarf")

            if line.lstrip().lower().startswith("fileversion"):
                file_version_values = line.rstrip(";").split(" ")
                file_version = float(
                    f"{file_version_values[1]}.{file_version_values[2]}"
                )
                if file_version not in ACCEPTED_KLARF_VERSIONS:
                    raise ValueError(
                        f"Klarf file version not valid (current={file_version} | accepted={ACCEPTED_KLARF_VERSIONS})"
                    )
                continue

            if line.lstrip().lower().startswith("filetimestamp"):
                file_timestamp = line[14:33].rstrip(";")
                continue

            if line.lstrip().lower().startswith("inspectionstationid"):
                inspection_station_id = line.split('"')[-2]
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

            if line.lstrip().lower().startswith("defectrecordspec"):
                line_without_space = re.sub("\s+", " ", line).strip()
                parameters = line_without_space.strip().split(" ")

                column_defect_id = parameters.index("DEFECTID") - 1
                column_x_rel = parameters.index("XREL") - 1
                column_y_rel = parameters.index("YREL") - 1
                column_x_index = parameters.index("XINDEX") - 1
                column_y_index = parameters.index("YINDEX") - 1
                column_x_size = parameters.index("XSIZE") - 1
                column_y_size = parameters.index("YSIZE") - 1
                column_defect_area = parameters.index("DEFECTAREA") - 1

                column_roughbin = (
                    parameters.index("ROUGHBINNUMBER") - 1
                    if "ROUGHBINNUMBER" in parameters
                    else -1
                )

                column_finebin = (
                    parameters.index("FINEBINNUMBER") - 1
                    if "FINEBINNUMBER" in parameters
                    else -1
                )
                continue

            if line.lstrip().lower().startswith("defectlist") and not (
                line.rstrip().endswith(";")
            ):
                next_line_has_coords = True
                defects = []
                continue

            if next_line_has_coords:
                if line.startswith(" "):
                    defect_parameters = line.strip().split()

                    defect_id = int(defect_parameters[column_defect_id - 1])
                    x_rel = float(defect_parameters[column_x_rel - 1])
                    y_rel = float(defect_parameters[column_y_rel - 1])
                    x_index = int(defect_parameters[column_x_index - 1])
                    y_index = int(defect_parameters[column_y_index - 1])
                    x_size = float(defect_parameters[column_x_size - 1])
                    y_size = float(defect_parameters[column_y_size - 1])
                    area = float(defect_parameters[column_defect_area - 1])

                    val_roughbin, val_finebin = None, None

                    if column_roughbin > 0:
                        val_roughbin = int(defect_parameters[column_roughbin - 1])

                    if column_finebin > 0:
                        val_finebin = int(defect_parameters[column_finebin - 1])

                    x, y = convert_coordinates(
                        die_pitch=die_pitch,
                        sample_center_location=sample_center_location,
                        xrel=x_rel,
                        yrel=y_rel,
                        xindex=x_index,
                        yindex=y_index,
                    )

                    defects.append(
                        Defect(
                            id=defect_id,
                            x_rel=x_rel,
                            y_rel=y_rel,
                            x_index=x_index,
                            y_index=y_index,
                            x_size=x_size,
                            y_size=y_size,
                            area=area,
                            roughbin=val_roughbin,
                            finebin=val_finebin,
                            point=(x, y),
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
                            defects=defects,
                        )
                    )

            if line.lstrip().lower().startswith("summarylist") and not (
                line.rstrip().endswith(";")
            ):
                next_line_has_numb = True
                continue

            if next_line_has_numb and line.startswith(" "):
                next_line_has_numb = False
                linewithoutSpace = re.sub("\s+", " ", line).strip()

                split = linewithoutSpace.split()

                wafers[-1].summary = Summary(
                    number_of_defects=int(split[1]),
                    defect_density=float(split[2]),
                    number_of_dies=int(split[3]),
                    number_of_def_dies=int(split[4]),
                )
                continue

            if line.lstrip().lower().startswith("sampletestplan"):
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
                continue

    return (
        KlarfContent(
            file_version=file_version,
            file_timestamp=file_timestamp,
            inspection_station_id=inspection_station_id,
            result_timestamp=result_timestamp,
            lot_id=lot_id,
            device_id=device_id,
            sample_size=sample_size,
            step_id=step_id,
            orientation_mark_location=orientation_mark_location,
            die_pitch=die_pitch,
            setup_id=setup_id,
            has_sample_test_plan=has_sample_test_plan,
            sample_plan_test=SamplePlanTest(x=sample_plan_test_x, y=sample_plan_test_y),
            wafers=wafers,
        ),
        contents,
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
