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
        demo_data = 0
        input_value = np.array([crim_value,zn_value,indus_value,chas_value,nox_value,rm_value,age_value,dis_value,rad_value,tax_value,ptratio_value,b_value,lstat_value],dtype='float')
        y_value = lr.predict(input_value)
    else: #default value for testing
        input_value = [0.00632, 18, 2.31 ,0 ,0.538 ,6.575, 65.2, 4.09, 1, 296, 15.3, 396.9, 4.98]
        y_value = lr.predict(input_value)
        demo_data = 1

    #dict_Bofit_result =fit(crim_value,zn_value,indus_value,chas_value,nox_value,rm_value,age_value,dis_value,rad_value,tax_value,ptratio_value,b_value,lstat_value)

#========================================================================

    HTML_text1 =''

    HTML_text1 +=' <h4>Fitting Model for Boston Experiment</h4>'
    HTML_text1 +="<p>feature_names = ['CRIM' 'ZN' 'INDUS' 'CHAS' 'NOX' 'RM' 'AGE' 'DIS' 'RAD' 'TAX' 'PTRATIO' 'B' 'LSTAT']"
    HTML_text1 +="<p>data = %s" % input_value
    HTML_text1 +="<p>target = %s" % y_value
#========================================================================
    HTML_text2 = "<H4>Provided by Yun-Wen Wang & Teng-Yi Huang</H4>"

    import Plotting_lib
    chart_title = 'Fitting Model for Boston Experiment'
    xAxis_label = 'Measured'
    yAxis_label = 'Predicted'
    result_dict = {
            'HTML_text1': HTML_text1,
            'HTML_text2': HTML_text2,
            'plot2':Plotting_lib.dynamic_svg1(input_value,xAxis_label,yAxis_label,chart_title),
               }
    return result_dict



'''
def T1srfit(t_value, y_value):
    """T1 曲線擬合，t_value 為 TR 時間，y_value為信號強度"""
    import  numpy as np
    from scipy.optimize.minpack import curve_fit

    if t_value and y_value:
        demo_data = 0
    else: #default value for testing
        t_value = "100 200 300 400 500 600 800 1000 1500"
        y_value = "46 68 111 150 172 192 251 301 387"
        demo_data = 1

    t_value = np.array( [float(xx) for xx in t_value.split()])
    y_value = np.array([float(xx) for xx in y_value.split()])

    dict_T1fit_result =T1fit(t_value,y_value)

# prepare HTML_text1 , first block of the result page
#========================================================================
    if dict_T1fit_result ['error_status']:
        result_dict = {    'HTML_text1': "<div class='alert alert-danger' role='alert'> %s </div> " %    dict_T1fit_result ['error_str']  }
        return result_dict

    HTML_text1 =''
    if demo_data:
        HTML_text1 += "<p><p><div class='alert alert-warning' role='alert'>No input data, using demo data set!</div>"

    HTML_text1 +=' <h4>T1 Fitting Model for Saturation-Recovery Experiment</h4>'
    HTML_text1 +="<p> $$ S(TR) =  S_0({1 - e^{- \\frac{TR}{T_{1}}}})$$ "  #在兩個$$中間包住LATEX表示法的算式
    HTML_text1 += "The obtained T1 model are: S0 = %.2f,  T1 = %.2f ms<p>" % (dict_T1fit_result ['S0'] , dict_T1fit_result ['T1'] )
    HTML_text1 += "<p> $$ S(TR) =  %.2f({1 - e^{- \\frac{TR}{%.2f}}})$$" %  (dict_T1fit_result ['S0'] , dict_T1fit_result ['T1'] )
    HTML_text1 += "<H4>Calculated T1: %.2f ms</H4><p>" % dict_T1fit_result ['T1']
#========================================================================

# prepare High Chart , Second block of the result page
#========================================================================
    HTML_text2 =  "<p>t values = %s" % t_value
    HTML_text2 += "<p>y values = %s" % y_value
    #HTML_text2 += "<p> fitting residue = %.2f<p>" % dict_T1fit_result ['residue']
    HTML_text2 += "<H4>Provided by Yun-Wen Wang & Teng-Yi Huang</H4>"

        #print HTML
    import Plotting_lib
    chart_title = 'T1 fitting for Saturation-Recovery Experiment'
    xAxis_label = 'Repetition Time (ms)'
    yAxis_label = 'Signal Intensity (A.U.)'
    result_dict = {
            'HTML_text1': HTML_text1,
            'HTML_text2': HTML_text2,
            'plot1_title':'Interactive Plot',
            'plot2_title':'SVG type',
            'plot1':Plotting_lib.highchart(dict_T1fit_result ['t_val_org'],dict_T1fit_result ['y_val_org'],dict_T1fit_result ['t_val_fit'], dict_T1fit_result ['y_val_fit'],xAxis_label,yAxis_label,chart_title),
            'plot2':Plotting_lib.dynamic_svg(dict_T1fit_result ['t_val_org'],dict_T1fit_result ['y_val_org'],dict_T1fit_result ['t_val_fit'], dict_T1fit_result ['y_val_fit'],xAxis_label,yAxis_label,chart_title),
               }
    return result_dict

def T1fit(t_value, y_value):
    """T1 曲線擬合，t_value 為 TR 時間，y_value為信號強度
        輸入值為兩個 numpy.ndarray
        t_value: 時間變數
        y_value:信號強度
        以下為參數回傳
        result_dict = {
            'S0': S0,
            'T1':T1,
            't_val_org':x,
            'y_val_org':y,
            't_val_fit':smoothx,
            'y_val_fit':smoothy,
            'residue':residue,
            'error_status':0,
            'error_str':'OK!',
          }

    """
    import numpy as np
    from scipy.optimize import curve_fit

    x=t_value
    y=y_value

    # setup initial value for test.
    if  not (len(x) and len(y)):
        dict_T1fit_result = {
            'error_status':1,
            'error_str':'No input data',}
        return dict_T1fit_result

    if len(x) != len(y):
        dict_T1fit_result = {
        'error_status':2,
        'error_str':'TR series & SI series is not mach',}
        return dict_T1fit_result

    def func(x, S0, T1):
        return S0*(1 - (np.exp(-x/T1)))

    popt, pcov = curve_fit(func, x, y, [2000,50])
    S0, T1 = popt

    smoothx = np.linspace(np.min(x), np.max(x), 1000)
    smoothy = func(smoothx, S0, T1)

    result_dict = {
            'S0': S0,
            'T1':T1,
            't_val_org':x,
            'y_val_org':y,
            't_val_fit':smoothx,
            'y_val_fit':smoothy,
            'error_status':0,
            'error_str':'OK!',
          }
    return result_dict
'''
