# encoding: utf-8
def Bostonfit(crim_value,zn_value,indus_value,chas_value,
                nox_value,rm_value,age_value,dis_value,
                rad_value,tax_value,ptratio_value,b_value,
                lstat_value):
    import os
    from sklearn.externals import joblib
    import  numpy as np
    from django.conf import settings

    machine_file = os.path.join(settings.PROJECT_ROOT,"app", "machine.pkl")
    lr = joblib.load(machine_file)

    if crim_value and zn_value and indus_value and chas_value and nox_value and rm_value and age_value and dis_value and rad_value and tax_value and ptratio_value and b_value and lstat_value:
        input_value = np.array([crim_value,zn_value,indus_value,chas_value,nox_value,rm_value,age_value,dis_value,rad_value,tax_value,ptratio_value,b_value,lstat_value],dtype='float')
        y_value = lr.predict(input_value)
        demo_data = 0
    else: #default value for testing
        input_value = [0.00632, 18, 2.31 ,0 ,0.538 ,6.575, 65.2, 4.09, 1, 296, 15.3, 396.9, 4.98]
        y_value = lr.predict(input_value)
        demo_data = 1

    #========================================================================

    HTML_text1 =''
    if demo_data:
        HTML_text1 += "<p><p><div class='alert alert-warning' role='alert'>No input data, using demo data set!</div>"

    HTML_text1 +=' <h4>Fitting Model for Boston Experiment</h4>'
    HTML_text1 +="<p>data = %s" % input_value
    HTML_text1 +="<H4>Calculated Target = %f</H4><p>" % y_value
    #========================================================================

    # prepare High Chart , Second block of the result page
    #========================================================================
    HTML_text2 ="<p>feature_names = [CRIM, ZN, INDUS, CHAS, NOX, RM, AGE, DIS, RAD, TAX, PTRATIO, B, LSTAT]"
    HTML_text2 +="<p>Target = MEDV : Median value of owner-occupied homes in $1000's"
    HTML_text2 += "<H4>Provided by Yun-Wen Wang & Teng-Yi Huang</H4>"

    #print HTML
    import Plotting_lib
    chart_title = 'Fitting model for Boston experiment'
    xAxis_label = 'Measured'
    yAxis_label = 'Predicted'
    result_dict = {
            'HTML_text1': HTML_text1,
            'HTML_text2': HTML_text2,
            'plot1':Plotting_lib.highchart1(input_value,y_value,xAxis_label,yAxis_label,chart_title),
            'plot2':Plotting_lib.dynamic_svg1(input_value,y_value,xAxis_label,yAxis_label,chart_title),
               }
    return result_dict
