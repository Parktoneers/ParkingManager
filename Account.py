import dataclasses

@dataclasses.dataclass
class Account:
    uid: [int, int, int, int]
    name: str
    surname: str
    phoneNumber: str
    parkingSpace: int


    # 6:  54 29 127 34
    # 4:  251 190 167 34
    # 2:  187 12 152 34
    # 1:  38 12 230 34