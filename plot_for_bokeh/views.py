


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

