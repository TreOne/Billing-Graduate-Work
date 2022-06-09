__all__ = 'LOGGING'

from pathlib import Path

log_dir = Path.home() / 'logs'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {'json': {'()': 'ecs_logging.StdlibFormatter', }, },
    'handlers': {
        'app_handler': {
            'level': 'INFO',
            'formatter': 'json',
            'class': 'logging.FileHandler',
            'filename': log_dir / 'email_sender.json',
        },
        'console': {'level': 'DEBUG', 'class': 'logging.StreamHandler', },
    },
    'loggers': {
        '': {'handlers': ['console'], 'level': 'INFO', },
        'email_sender': {'handlers': ['app_handler'], 'level': 'INFO', 'propagate': False, },
    },
    'root': {'level': 'INFO', 'handlers': ['console', ], },
}
