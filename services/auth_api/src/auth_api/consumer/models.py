from dataclasses import dataclass

import orjson


@dataclass(frozen=True)
class BillMessageBody:
    user_uuid: str
    type: str
    item_uuid: str

    @staticmethod
    def from_message_value(message_value: bytes):
        message_value_str = message_value.decode('utf-8')
        message_value_params = orjson.loads(message_value_str)
        return BillMessageBody(
            user_uuid=message_value_params['user_uuid'],
            type=message_value_params['type'],
            item_uuid=message_value_params['item_uuid'],
        )


@dataclass(frozen=True)
class BillMessage:
    title: str
    body: BillMessageBody

    @staticmethod
    def from_message(message):
        title = message.key.decode('utf-8')
        body = BillMessageBody.from_message_value(message.value)
        return BillMessage(title, body)
