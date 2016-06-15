
def T1fitting(t_value, y_value):
    """T1 曲線擬合，t_value 為 TI 時間，y_value為信號強度"""
    import numpy as np
    from scipy.optimize.minpack import curve_fit

    import pyT1


    if t_value and y_value:
        demo_data = 0
    else: #default value for testing
        t_value = "120 220 370 1130 1168 1233 2115 2125 2145 3078 4035"
        y_value = "114 87 56 75 80 89 137 132 128 151 168"
        demo_data = 1


    dict_T1fit_result =pyT1.T1fitting(t_value,y_value)

    # prepare HTML_text1 , first block of the result page
    #========================================================================
    if dict_T1fit_result ['error_status']:
        result_dict = {    'HTML_text1': "<div class='alert alert-danger' role='alert'> %s </div> " %    dict_T1fit_result ['error_str']  }
        return result_dict

    HTML_text1 =''
    if demo_data:
        HTML_text1 += "<p><p><div class='alert alert-warning' role='alert'>No input data, using demo data set!</div>"

    HTML_text1 +=' <h4>T1 Fitting Model for Look-Locker Experiment</h4>'
    HTML_text1 +="<p> $$ SI =  {A - B e^{- \\frac{TI}{T_{1}^*}}}$$ "  #在兩個$$中間包住LATEX表示法的算式
    HTML_text1 += "The obtained T1 model are: A = %.2f, B = %.2f, T1* = %.2f ms<p>" % (dict_T1fit_result ['A'] , dict_T1fit_result ['B'] , dict_T1fit_result ['T1_star'] )
    HTML_text1 += "<p> $$ SI =  {%.2f - %.2f e^{- \\frac{TI}{%.2f}}}$$" %  (dict_T1fit_result ['A'] , dict_T1fit_result ['B'] , dict_T1fit_result ['T1_star'] )
    HTML_text1 += "<H4>LL corrected T1: %.2f ms</H4><p>" % dict_T1fit_result ['T1']
    #========================================================================

# prepare High Chart , Second block of the result page
#========================================================================
    HTML_text2 = "<p>t values = %s" % t_value
    HTML_text2 += "<p>y values = %s" % y_value
    HTML_text2 +="<p> fitting residue = %.2f<p>" % dict_T1fit_result ['residue']
        #print HTML
    import Plotting_lib
    chart_title = 'T1 fitting for Look-Locker Experiment'
    xAxis_label = 'Inversion Time (ms)'
    yAxis_label = 'Signal Intensity (A.U.)'
    result_dict = {
            'HTML_text1': HTML_text1,
            'HTML_text2': HTML_text2,
            'SVG':Plotting_lib.dynamic_svg(dict_T1fit_result ['t_val_org'],dict_T1fit_result ['y_val_org'],dict_T1fit_result ['t_val_fit'], dict_T1fit_result ['y_val_fit'],xAxis_label,yAxis_label,chart_title),
            'highchart':Plotting_lib.highchart(dict_T1fit_result ['t_val_org'],dict_T1fit_result ['y_val_org'],dict_T1fit_result ['t_val_fit'], dict_T1fit_result ['y_val_fit'],xAxis_label,yAxis_label,chart_title),
               }
    return result_dict
