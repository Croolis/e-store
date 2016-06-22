from __future__ import unicode_literals

from django.apps import AppConfig


class StoreConfig(AppConfig):
    name = 'store'
    verbose_name = 'Store'
    app_label='store'

    #def ready(self):
    #	print('&&&&&&&&&&&&&&&&')
    #	import estore.signals