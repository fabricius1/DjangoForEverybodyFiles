from django.shortcuts import render


def myview(request):
    view_count = request.session.get('view_count', 0) + 1
    request.session['view_count'] = view_count

    request.session.save()
    response = render(request, 'hello/main.html',
                     {"view_count": view_count})
    response.set_cookie('dj4e_cookie', 'dcef2760', max_age=1000)
    return response
