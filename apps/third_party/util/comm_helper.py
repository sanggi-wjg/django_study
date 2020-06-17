from django.http import HttpResponse


def popup_close():
    return HttpResponse('<script type="text/javascript">window.close()</script>')
