from dataclasses import dataclass


@dataclass
class RFIDReadResponse:
    tag: int
