from dataclasses import dataclass

@dataclass
class BodyMessage:
    bill_uuid: str
    status: str
    user_uuid: str
    type: str
    item_uuid: str
    amount: float


@dataclass
class Message:
    title: str
    body: BodyMessage

