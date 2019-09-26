from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass()
class ReadGroup:
    id: str
    R1: Path
    R2: Optional[Path] = None
    R1_md5: Optional[str] = None
    R2_md5: Optional[str] = None

    def __post_init__(self):
        if not self.R1.exists():
            raise FileNotFoundError(str(self.R1))
        if self.R2 is not None:
            if not self.R2.exists():
                raise FileNotFoundError(str(self.R2))


@dataclass()
class Library:
    id: str
    readgroups: List[ReadGroup]


@dataclass()
class Sample:
    id: str
    libraries: List[Library]


@dataclass()
class SampleGroup:
    samples: List[Sample]
