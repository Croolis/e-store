from __future__ import unicode_literals

from django.apps import AppConfig


class StoreConfig(AppConfig):
    name = 'estore'
    verbose_name = 'eStore'
    app_label='estore'

    def ready(self):
    	import estore.signals