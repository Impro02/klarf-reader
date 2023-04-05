from typing import Dict, List, Tuple
from dataclasses import dataclass, field


@dataclass
class SetupId:
    name: str
    date: str


@dataclass
class DiePitch:
    x: float
    y: float


@dataclass
class DieOrigin:
    x: float
    y: float


@dataclass
class SampleCenterLocation:
    x: float
    y: float


@dataclass
class SamplePlanTest:
    x: List[int] = field(default_factory=lambda: [])
    y: List[int] = field(default_factory=lambda: [])


@dataclass
class Defect:
    id: int
    x_rel: float
    y_rel: float
    x_index: int
    y_index: int
    x_size: float
    y_size: float
    area: float
    roughbin: int
    finebin: int
    point: Tuple[float, float] = field(default_factory=lambda: [])
    custom_attribute:  Dict[str, any] = None


@dataclass
class Summary:
    defect_density: float = None
    number_of_defects: int = None
    number_of_dies: int = None
    number_of_def_dies: int = None

    percent_of_def_die: float = None

    def __post_init__(self):
        self.percent_of_def_die = float(self.number_of_def_dies / self.number_of_dies)


@dataclass
class Wafer:
    id: str
    slot: int
    die_origin: DieOrigin
    sample_center_location: SampleCenterLocation
    defects: List[Defect] = field(default_factory=lambda: [])
    summary: Summary = None


@dataclass
class BasicKlarfContent:
    file_version: float
    file_timestamp: str
    inspection_station_id: str
    result_timestamp: str
    lot_id: str
    device_id: str
    sample_size: int
    setup_id: SetupId
    step_id: str
    orientation_mark_location: str
    die_pitch: DiePitch
    has_sample_test_plan: bool
    sample_plan_test: SamplePlanTest
    custom_attribute: Dict[str, any] = None


@dataclass
class KlarfContent(BasicKlarfContent):
    wafers: List[Wafer] = field(default_factory=lambda: [])

    @property
    def number_of_wafers(self) -> int:
        return len(self.wafers)


@dataclass
class SingleKlarfContent(BasicKlarfContent):
    wafer: Wafer = None
