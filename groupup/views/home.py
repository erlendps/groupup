from django.http import HttpResponse

def hello(request):
   text = """<h1>Welcome to GroupUp !</h1>"""
   return HttpResponse(text)