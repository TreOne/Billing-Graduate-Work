import logging
from datetime import datetime
from typing import List

from celery import shared_task

from billing.repositories.user_autopay import UserAutoPayRepository
from config.payment_service import payment_system
from utils.schemas import PaymentParams

log = logging.getLogger(__name__)


@shared_task
def autopay_periodic_task():
    """Задача для автопродление подписки."""
    # TODO: брать данные с сервиса Auth
    users_for_pay: List[str] = []

    auto_pays = UserAutoPayRepository.get_actual_auto_pays(users=users_for_pay)

    for auto_pay in auto_pays:
        # Проводим автоплатеж по ранее сохраненному платежу
        auto_payment_params = PaymentParams(
            bill_uuid=str(uuid.uuid4()),
            amount=300.0,
            description=f'Оплата подписки "Practix.Premium".',
            autopay_id=auto_pay.id,
        )
        is_successful = payment_system.make_autopay(auto_payment_params)
        if is_successful:
            print(f"Автоплатеж проведен успешно.")
        else:
            print(f"ОШИБКА: Не удалось выполнить автоплатеж!")
