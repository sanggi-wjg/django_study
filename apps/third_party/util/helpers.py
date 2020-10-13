from django.http import HttpResponse


def popup_close():
    return HttpResponse('<script type="text/javascript">window.close()</script>')


def alert(msg: str):
    return HttpResponse('<script type="text/javascript">alert("{}"); history.back(); </script>'.format(msg))
