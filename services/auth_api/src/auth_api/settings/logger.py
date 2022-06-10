from pathlib import Path

log_dir = Path.home() / 'logs'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {'json': {'()': 'ecs_logging.StdlibFormatter',},},
    'handlers': {
        'auth_handler': {
            'level': 'INFO',
            'formatter': 'json',
            'class': 'logging.FileHandler',
            'filename': log_dir / 'auth_consumer.json',
        },
        'auth_api': {
            'level': 'INFO',
            'formatter': 'json',
            'class': 'logging.FileHandler',
            'filename': log_dir / 'auth_api.json',
        },
        'console': {'level': 'DEBUG', 'class': 'logging.StreamHandler',},
    },
    'loggers': {
        '': {'handlers': ['console'], 'level': 'INFO',},
        'auth_consumer': {'handlers': ['auth_handler'], 'level': 'INFO', 'propagate': False,},
        'auth_api': {'handlers': ['auth_api'], 'level': 'INFO', 'propagate': False,},
    },
    'root': {'level': 'INFO', 'handlers': ['console',],},
}
