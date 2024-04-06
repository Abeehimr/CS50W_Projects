from django.urls import path # give ability to reroute urls
from . import views # import any functions we created in veiws

urlpatterns = [ # call path function ( A string representing the URL path, a function from views.py that we wish to call when that URL is visited, and (optionally) a name for that path, in the format name="something")
    path("",views.index, name="index"),
    path("<str:name>",views.greet,name="greet"),
]