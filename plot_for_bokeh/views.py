# encoding: utf-8
"""
Definition of views.
"""

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpRequest
from django.http import HttpResponse
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth.decorators import login_required

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



def AHA17(request):
    if not request.POST:
        from app.forms import AHAForm
        return render(
            request,
            'app/inp_AHA17.html',
            context_instance = RequestContext(request,
            {'title':'AHA 17 Input',
                    'form': AHAForm}))
    else:
        import pyFitMR.AHA17_lib as AHA17_lib

        t_value = request.POST.get('t_value')
        t_min = request.POST.get('t_min')
        t_max = request.POST.get('t_max')
        result_dict=AHA17_lib.Plot17(t_value,t_min,t_max)

        return render(request,'app/resultpage.html',
            context_instance = RequestContext(request, result_dict)
           )



def fcmat(request):
    if not request.POST:

        from app.models import Document
        from app.forms import DocumentForm
        form = DocumentForm() # A empty, unbound form

        # Render list page with the documents and the form
        return render_to_response(
            'app/inp_fcmat.html',
            {'title':'Displaying Functional Connectivity Matrix','form': form},
            context_instance=RequestContext(request)
        )
    else:
        from app.models import Document
        from app.forms import DocumentForm
        from django.http import HttpResponseRedirect
        from django.core.urlresolvers import reverse
        from django.conf import settings #or from my_project import settings
        import os
        import pyFitMR.fcmat_lib as fcmat_lib
        from django.conf import settings #or from my_project import settings
        uploadedfile = False

        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()
            matfile = os.path.join(settings.MEDIA_ROOT,newdoc.docfile.name)
            uploadedfile = True
        else:
            FILE_ROOT = os.path.abspath(os.path.dirname(__file__))
            matfile = os.path.join(FILE_ROOT,'CC_testfile.mat')


        import scipy.io
        #import matplotlib.pyplot as plt
        mat = scipy.io.loadmat(matfile)
        FC=mat['connectome']
        #FC=mat.items()[0][1]
        #plt.imshow(FC)
        #print FC
        script, div = fcmat_lib.plot(FC)
        if uploadedfile:
            newdoc.docfile.delete()
        return render(request, 'app/fcmat_result.html', {"the_script":script, "the_div":div})


def NetworkNodes(request):
    if not request.POST:

        from app.models import Document
        from app.forms import DocumentForm
        form = DocumentForm() # A empty, unbound form

        # Render list page with the documents and the form
        return render_to_response(
            'app/inp_nn.html',
            {'title':'Displaying Functional Networks','form': form},
            context_instance=RequestContext(request)
        )
    else:
        from app.models import Document
        from app.forms import DocumentForm
        from django.http import HttpResponseRedirect
        from django.core.urlresolvers import reverse
        from django.conf import settings #or from my_project import settings
        import os
        import pyFitMR.CCNode_lib as CCNode_lib
        from django.conf import settings #or from my_project import settings
        uploadedfile = False

        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()
            matfile = os.path.join(settings.MEDIA_ROOT,newdoc.docfile.name)
            uploadedfile = True
        else:
            FILE_ROOT = os.path.abspath(os.path.dirname(__file__))
            matfile = os.path.join(FILE_ROOT,'CNTOE_DMN13_sample.mat')


        import scipy.io
        #import matplotlib.pyplot as plt
        mat = scipy.io.loadmat(matfile)
        FC=mat['connectome']
        result_dict = CCNode_lib.plot(FC)

        if uploadedfile:
            newdoc.docfile.delete()

        return render(request,'app/resultpage.html',
            context_instance = RequestContext(request, result_dict)
           )



def fit(request,fit_func):
    ''' fit_func = "T1", "T1LL", "T1sr", "T2","gamma" '''
    from app.forms import BootstrapCurveFittingForm
    #不是post 意思就是說沒有輸入資料，因此進入資料輸入頁面
    if not request.POST:
        alldict = { "T1":T1dict(),
                    "T1LL":T1LLdict(),
                    "T1sr":T1srdict(),
                    "T2":T2dict(),
                    "gamma":gammadict(),}

        return render(
            request,
            'app/inp_fit.html',
            context_instance = RequestContext(request, alldict[fit_func])
        )
    else:
        t_value = request.POST.get('t_value')
        y_value = request.POST.get('y_value')

        if fit_func == "T1":
            import pyFitMR.T1_lib as T1_lib
            result_dict = T1_lib.T1fit(t_value, y_value)

        elif fit_func == "T1LL":
            import pyFitMR.T1LL_lib as T1LL_lib
            result_dict = T1LL_lib.T1LLfit(t_value, y_value)

        elif fit_func == "T1sr":
            import pyFitMR.T1sr_lib as T1sr_lib
            result_dict = T1sr_lib.T1srfit(t_value, y_value)

        elif fit_func == "T2":
            import pyFitMR.T2_lib as T2_lib
            result_dict = T2_lib.T2fit(t_value, y_value)

        elif fit_func == "gamma":
            import pyFitMR.perfusion_lib as perfusion_lib
            result_dict = perfusion_lib.perfusionfit(t_value, y_value)


        return render(
            request,
            'app/resultpage.html',
            context_instance = RequestContext(request, result_dict)
           )

def T1dict():
    from app.forms import BootstrapCurveFittingForm

    return {'title':'T1 Fitting for Inversion-Recovery Experiments',
            'form': BootstrapCurveFittingForm,
            'instruction':'Fill in TI and SI to calculate T1',
            't_label':'Inversion Time (TI) (msec)',
            'y_label':'Signal Intensity (A.U.)',
            'note':'''<p>Try it!
                       <p>
                       Simply copy the following test data into the input boxes and click submit.
                       <p>Test data:
                       <p>
                       TI= 120 220 370 1130 1168 1233 2115 2125 2145 3078 4035
                       <p>
                       SI= 114 87 56 75 80 89 137 132 128 151 168
                       <p><p>Provided by Yi-Fu Tsai & Teng-Yi Huang'''}

def T1LLdict():
    from app.forms import BootstrapCurveFittingForm

    return {'title':'T1 Fitting for Look-Locker Experiments',
            'form': BootstrapCurveFittingForm,
            'instruction':'Fill in TI and SI to calculate T1',
            't_label':'Inversion Time (TI) (msec)',
            'y_label':'Signal Intensity (A.U.)',
            'note':'''<p>Try it!
                      <p>
                      Simply copy the following test data into the input boxes and click submit.
                      <p>Test data:
                      <p>
                      TI= 120 220 370 1130 1168 1233 2115 2125 2145 3078 4035
                      <p>
                      SI= 114 87 56 75 80 89 137 132 128 151 168
                      <p>
                      Provided by Yi-Fu Tsai & Teng-Yi Huang'''}

def T1srdict():
    from app.forms import BootstrapCurveFittingForm

    return {'title':'T1 Fitting for Saturation-Recovery Experiments',
            'form': BootstrapCurveFittingForm,
            'instruction':'Fill in TR and SI to calculate T1',
            't_label':'Repetition Time (TR) (msec)',
            'y_label':'Signal Intensity (A.U.)',
            'note':'''<p>Try it!
                      <p>
                      Simply copy the following test data into the input boxes and click submit.
                      <p>Test data:
                      <p>
                      TR= 100 200 300 400 500 600 800 1000 1500
                      <p>
                      SI= 46 68 111 150 172 192 251 301 387
                      <p>
                      Provided by Yun-Wen Wang & Teng-Yi Huang'''}


def T2dict():
    from app.forms import BootstrapCurveFittingForm

    return {'title':'T2 Fitting for Multi-TE Spin-Echo Experiments',
            'form': BootstrapCurveFittingForm,
            'instruction':'T2 Fitting Input',
            't_label':'Echo Time (TE) (msec)',
            'y_label':'Signal Intensity (A.U.)',
            'note':'''<p>Try it!
                      <p>
                      Simply copy the following test data into the input boxes and click submit.
                      <p>Test data:
                      <p>
                      TE=0 10 20 30 40 50 60 70 80 90 100 110 120 130 140 150 160 170 180 190
                      <p>
                      S0= 1.0 0.72 0.51 0.37 0.26 0.19 0.13 0.09 0.07 0.05 0.03 0.03 0.01 0.01 0.01 0.006 0.004 0.003 0.002 0.001
                      <p>Provided by Chun-Yu Huang & Teng-Yi Huang'''}

def gammadict():
    from app.forms import BootstrapCurveFittingForm

    return {'title':'Gamma Fitting for First-Pass Perfusion Experiments',
            'form': BootstrapCurveFittingForm,
            'instruction':'Gamma Fitting Input',
            't_label':'Time (sec)',
            'y_label':'Signal Intensity (A.U.)',
            'note':'''<p>Try it!
                      <p>
                      Simply copy the following test data into the input boxes and click submit.
                      <p>Test data:
                      <p>
                      T=0.   1.   2.   3.   4.   5.   6.   7.   8.   9.  10.  11.  12.  13.  14.
                        15.  16.  17.  18.  19.  20.  21.  22.  23.  24.  25.  26.  27.  28.  29.
                        30.  31.  32.  33.  34.  35.  36.  37.  38.  39.  40.  41.  42.  43.  44.
                        45.  46.  47.
                      <p>
                      S0= 5.   4.   7.   0.   3.   1.   5.   3.   7.   4.   2.
                               4.   8.   8.  10.  16.  22.  30.  37.  46.  56.  55.
                              54.  54.  57.  50.  42.  44.  44.  37.  31.  25.  23.
                              22.  29.  29.  25.  35.  39.  42.  34.  32.  37.  24.
                              15.  17.  16.  19.
                      <p>Provided by Yi-Fu Tsai & Teng-Yi Huang'''}
