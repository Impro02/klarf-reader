# MODELS
from ..models.klarf_content import KlarfContent, SingleKlarfContent


def convert_to_single_klarf_content(
    klarf_content: KlarfContent, wafer_index: int
) -> SingleKlarfContent:
    """Convert KlarfContent to SingleKlarfContent focus on one specific wafer

    Args:
        klarf_content (KlarfContent): _description_
        wafer_index (int): _description_

    Returns:
        SingleKlarfContent: _description_
    """

    if wafer_index > klarf_content.number_of_wafers - 1:
        raise ValueError(f"{wafer_index=} does not exist in {KlarfContent.__name__}")

    return SingleKlarfContent(
        file_version=klarf_content.file_version,
        file_timestamp=klarf_content.file_timestamp,
        inspection_station_id=klarf_content.inspection_station_id,
        sample_type=klarf_content.sample_type,
        result_timestamp=klarf_content.result_timestamp,
        lot_id=klarf_content.lot_id,
        device_id=klarf_content.device_id,
        sample_size=klarf_content.sample_size,
        setup_id=klarf_content.setup_id,
        step_id=klarf_content.step_id,
        sample_orientation_mark_type=klarf_content.sample_orientation_mark_type,
        orientation_mark_location=klarf_content.orientation_mark_location,
        die_pitch=klarf_content.die_pitch,
        has_sample_test_plan=klarf_content.has_sample_test_plan,
        sample_plan_test=klarf_content.sample_plan_test,
        wafer=klarf_content.wafers[wafer_index],
    )
