from django.apps import AppConfig



class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'

    def ready(self):
        return super().ready()
        # import account.signals
        # signals.signals_ready(self.get_model('User'))
        # signals.signals_ready(self.get_model('Profile'))
        # signals.signals_ready(self.get_model('User'))
