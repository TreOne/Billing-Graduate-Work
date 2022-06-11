[![AuthAPI - Style check](https://github.com/TreOne/billing/actions/workflows/auth-api.yml/badge.svg)](https://github.com/TreOne/billing/actions/workflows/auth-api.yml)  
[![Billing - Style check](https://github.com/TreOne/billing/actions/workflows/billing.yml/badge.svg)](https://github.com/TreOne/billing/actions/workflows/billing.yml)  
[![Event To Notification - Style check](https://github.com/TreOne/billing/actions/workflows/event-to-notification.yml/badge.svg)](https://github.com/TreOne/billing/actions/workflows/event-to-notification.yml)  
[![NotificationAPI - Style check](https://github.com/TreOne/billing/actions/workflows/notification-api.yml/badge.svg)](https://github.com/TreOne/billing/actions/workflows/notification-api.yml)  
[![NotificationAPISender - Style check](https://github.com/TreOne/billing/actions/workflows/notification-sender.yml/badge.svg)](https://github.com/TreOne/billing/actions/workflows/notification-sender.yml)  

# Биллинг
Реализовать два метода работы с картами:
1. Оплатить подписку
2. Отменить подписку и вернуть за нее деньги

Система должна быть устойчива к перебоям (строго однократная доставка).  
Интеграция с админкой Django (контроль оплаты подписок клиентами).  

## Архитектура проекта
![Архитектура проекта](docs/architecture/diagram_to_be.png)

## Экраны в клиентском приложении
![Экран клиентского приложения](docs/images/user_screen.jpg)
