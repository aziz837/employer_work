from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

def staff_required(f):
    return staff_member_required(f, login_url='dashboard:login')

@staff_required
def index(request):

    ctx = {}
    return TemplateResponse(request, 'dashboard/index.html', ctx)


def login(request):

    ctx = {}
    return TemplateResponse(request, 'dashboard/login.html', ctx)