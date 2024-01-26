from django.apps import AppConfig


class NetworkConfig(AppConfig):
    name = 'network'

    def ready(self) -> None:
            import network.signals.handlers