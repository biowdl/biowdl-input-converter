from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass()
class Node:
    id: str
    additional_properties: Dict[str, Any]


@dataclass()
class ReadGroup(Node):
    R1: Path
    R2: Optional[Path] = None
    R1_md5: Optional[str] = None
    R2_md5: Optional[str] = None
    additional_properties: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.R1.exists():
            raise FileNotFoundError(str(self.R1))
        if self.R2 is not None:
            if not self.R2.exists():
                raise FileNotFoundError(str(self.R2))


@dataclass()
class Library(Node):
    readgroups: List[ReadGroup]
    additional_properties: Dict[str, Any] = field(default_factory=dict)


@dataclass()
class Sample(Node):
    libraries: List[Library]
    additional_properties: Dict[str, Any] = field(default_factory=dict)


@dataclass()
class SampleGroup:
    samples: List[Sample]
