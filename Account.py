import dataclasses


@dataclasses.dataclass
class Account:

    uid: [int, int, int, int]
    name: str
    surname: str
    phoneNumber: str
    parkingSpace: int