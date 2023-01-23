from typing import List, Tuple
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
    defects: List[Defect] = field(default_factory=lambda: [])
    summary: Summary = None


@dataclass
class KlarfContent:
    inspection_station_id: str
    result_timestamp: str
    lot_id: str
    device_id: str
    sample_size: int
    setup_id: SetupId
    step_id: str
    layer: int
    oml: str
    die_pitch: DiePitch
    has_sample_test_plan: str
    sample_plan_test: SamplePlanTest
    wafers: List[Wafer] = field(default_factory=lambda: [])

    number_of_wafers: int = None

    def __post_init__(self):
        self.number_of_wafers = len(self.wafers)
