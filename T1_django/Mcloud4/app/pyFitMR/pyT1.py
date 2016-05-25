

def T1fitting(t_value, y_value):
    """T1 曲線擬合，t_value 為 TI 時間，y_value為信號強度
        輸入值為兩個 numpy.ndarray
        t_value: 時間變數
        y_value:信號強度
        以下為參數回傳
        result_dict = {
            'A': A,
            'B': B,
            'T1_star':t,
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

    # setup initial value for test.
    if  not (t_value and y_value):
        dict_T1fit_result = {
            'error_status':1,
            'error_str':'No input data',}
        return dict_T1fit_result

    x =np.array( [float(xx) for xx in t_value.split()])
    y = np.array([float(xx) for xx in y_value.split()])
    if len(x) != len(y):
        dict_T1fit_result = {
        'error_status':2,
        'error_str':'TI series & SI series is not mach',}
        return dict_T1fit_result

    #將 x做排序

    guessnum = np.array([100, 200, 500, 800, 1000, 1500, 2000, 2500])  #設定T1 起始值之猜測
    errornum = guessnum * 0
    t_order= x.argsort()
    x=x[t_order]
    y=y[t_order]

   #   使用不同的起始 T1 值去計算，再找出誤差最小的來使用
    result_list=['',]
    for index in range(len(guessnum)):

        guess = [y.max(), 2 * y.max(), guessnum[index]]
        fit_result=T1fit_run(x,y,guess,abs_fit=1)
        errornum[index]  = fit_result['residue']
        if index == 0:
            result_list[0]=[fit_result,]
        else:
            result_list.append(fit_result)

    prerun_result=  result_list[np.argmin(errornum)]

    #接下來去找出曲線翻轉  ，以前一次的結果當成初始值
    index_ylow=np.argmin(y)
    count=-1
    result_list=[0,0,0] # 準備一個大小為3的list
    index_temp=[0,0,0]
    errornum=[0,0,0]
    for index in [index_ylow-1,index_ylow,index_ylow+1]:
        count +=1
        print index
        if index < 0 or index >=len(y):
            errornum[count]=1e8
            fit_result=prerun_result
        else:
            flipped_y=y.copy()
            flipped_y[:index+1]=-1*y[:index+1]
            guess = [prerun_result['A'], prerun_result['B'], prerun_result['T1_star']]
            fit_result=T1fit_run(x,flipped_y,guess,abs_fit=0)
            errornum[count]  = fit_result['residue']
        print errornum[count]
        index_temp[count]=index
        result_list[count]=fit_result
        obtained_result_list=result_list[np.argmin(errornum)]






   # return  guessnum[np.argmin(errornum)]
    return obtained_result_list

def T1fit_run(x,y,guess,abs_fit):
    import numpy as np
    from scipy.optimize.minpack import curve_fit
    #t_order= x.argsort()
    #x=x[t_order]
    #y=y[t_order]
    smoothx = np.linspace(x[0], x[-1], 1000)
    #guess_a, guess_b, guess_c = y.max(), 2 * y.max(), T1_guess
    #guess = [guess_a, guess_b, guess_c]
    if abs_fit:
        exp_f = lambda x, A, B, t:abs((A - (B * np.exp(-x / t))))
    else:
        exp_f = lambda x, A, B, t:((A - (B * np.exp(-x / t))))
    params, cov = curve_fit(exp_f, x, y, p0=guess)
    A, B, t = params
    #best_fit = lambda x: abs((A - (B * np.exp(-x / t))))
    smoothy = exp_f(smoothx, A, B, t)
    T1 = t * (B / A - 1)
    yfitting = exp_f(x, A, B, t)
    #yfitting = abs(A - (B * np.exp(-x / t)))
    residue=np.sum(abs(yfitting - y));
    result_dict = {
            'A': A,
            'B': B,
            'T1_star':t,
            'T1':T1,
            't_val_org':x,
            'y_val_org':y,
            't_val_fit':smoothx,
            'y_val_fit':smoothy,
            'residue':residue,
            'error_status':0,
            'error_str':'OK!',
          }
    return result_dict
