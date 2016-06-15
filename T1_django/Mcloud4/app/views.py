"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse
from django.template import RequestContext
from datetime import datetime

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        context_instance = RequestContext(request,
        {
            'title':'Home Page',
            'year':datetime.now().year,
        })
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        context_instance = RequestContext(request,
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        })
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        context_instance = RequestContext(request,
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        })
    )


from app.forms import BootstrapCurveFittingForm
def T1LL_input(request):

    return render(
        request,
        'app/fitting_input.html',
        context_instance = RequestContext(request,
        {
            'title':'Fitting Input',
            'form': BootstrapCurveFittingForm,
               })
    )


def T1LL_result(request):
    import pyFitMR.Fitting_lib as FB

    t_value = request.POST.get('t_value')
    y_value = request.POST.get('y_value')
    fitted_result_dict = FB.T1fitting(t_value, y_value)
    return render(
        request,
        'app/fitting_result.html',
        context_instance = RequestContext(request, fitted_result_dict)
       )


from app.forms import BootstrapCurveFittingForm
def Boston_fit(request):

    return render(
        request,
        'app/fitting_input1.html',
        context_instance = RequestContext(request,
        {
            'title':'Boston Fitting Input',
            'form': BootstrapCurveFittingForm,
               })
    )

def Boston_result(request):
    #import pyFitMR.Fitting_lib as FB
    import pyFitMR.boston_lib as boston_lib

    crim_value = request.POST.get('crim_value')
    zn_value = request.POST.get('zn_value')
    indus_value = request.POST.get('indus_value')
    chas_value = request.POST.get('chas_value')
    nox_value = request.POST.get('nox_value')
    rm_value = request.POST.get('rm_value')
    age_value = request.POST.get('age_value')
    dis_value = request.POST.get('dis_value')
    rad_value = request.POST.get('rad_value')
    tax_value = request.POST.get('tax_value')
    ptratio_value = request.POST.get('ptratio_value')
    b_value = request.POST.get('b_value')
    lstat_value = request.POST.get('lstat_value')

    #fitted_result_dict = FB.T1fitting(t_value, y_value)
    result_dict = boston_lib.Bostonfit(crim_value,zn_value,indus_value,chas_value,
                                        nox_value,rm_value,age_value,dis_value,
                                        rad_value,tax_value,ptratio_value,b_value,
                                        lstat_value)


    return render(
        request,
        'app/boston_result.html',
        context_instance = RequestContext(request, result_dict)
       )
