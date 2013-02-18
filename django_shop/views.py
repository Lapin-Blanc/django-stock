from django.views.generic.simple import direct_to_template

def index(request):
    return direct_to_template(request, template="index.html", user=request.user)
