from django.conf import settings

def debug(request):
    # print("Is Live =", settings.LIVE)
    return {
        'debug' : settings.DEBUG,
        'live'  : settings.LIVE
    }