def plot(FC):
    from bokeh.plotting import figure,vplot
    from bokeh.resources import CDN
    from bokeh.embed import components
    import numpy as np
   
    from collections import OrderedDict
    from bokeh.models import HoverTool, ColumnDataSource
    
    import csv
    import os

    FILE_ROOT = os.path.abspath(os.path.dirname(__file__))

    with open(os.path.join(FILE_ROOT,'aal.txt'), 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        allnames=[xx[1] for xx in spamreader]
        
    names=allnames[0:90]    
    #%matplotlib inline

    
    def  rgb_code(i,cmap):
        '''cmap, 0: jet, 1:cool'''
        import matplotlib.pyplot as plt
        if cmap:
            rgba=plt.cm.cool(int(i))
        else:
            rgba=plt.cm.jet(int(i))
        red = int(rgba[0]*255)
        green = int(rgba[1]*255)
        blue = int(rgba[2]*255)
        return '#{r:02x}{g:02x}{b:02x}'.format(r=red,g=green,b=blue)
    
    N = len(names)
    counts = np.abs(FC.copy())
    
    xname = []
    yname = []
    color = []
    alpha = []
    for ii in range(90):
        for jj in range(90):
            xname.append(names[ii])
            yname.append(names[jj])
            a = min(counts[ii,jj]*1.2, 1)
            alpha.append(1)
            #color.append('lightgrey')
            color.append(rgb_code(a*256,1))
    
    
    source = ColumnDataSource(
        data=dict(
            xname=xname,
            yname=yname,
            colors=color,
            alphas=alpha,
            count=counts.flatten(),
        )
    )
    
    #output_file("les_mis.html")
    
    p = figure(title="Functional Connectivity AAL-90",
        x_axis_location="above", tools="hover,save", toolbar_location="below",
        x_range=names, y_range=list(reversed(names)))
    p.plot_width = 1440
    p.plot_height = 1440
    
    p.rect('xname', 'yname', 0.95, 0.95, source=source,
         color='colors', alpha='alphas', line_color=None)
    
    p.grid.grid_line_color = None
    p.axis.axis_line_color = None
    p.axis.major_tick_line_color = None
    p.axis.major_label_text_font_size = "3pt"
    p.axis.major_label_standoff = 0
    p.xaxis.major_label_orientation = np.pi/2
    
    hover = p.select(dict(type=HoverTool))
    hover.tooltips = OrderedDict([
        ('AAL', '@yname, @xname'),
        ('FC', '@count'),
    ])

    # show the plot

    script, div = components(p, CDN)
    return script, div