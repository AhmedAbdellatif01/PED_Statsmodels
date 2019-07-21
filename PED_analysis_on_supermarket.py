# -*- coding: utf-8 -*-
"""
Created on Tue Feb 24 15:26:19 2015

@author: Andrew
"""

#import statsmodels.graphics.api as smg
import numpy as np
import pandas as pd

#price and sales unit data
filename = "supermarket.csv"

#point_est for iterations of point estimation
point_est = 10000

df = pd.read_csv(filename)

def reg_fit(df):
    import statsmodels.formula.api as smf
    import statsmodels.graphics.api as smg
    global b0, b1, ped_fit
    df["Price_Eggs"] = df["Price.Eggs"]
    ped_fit = smf.ols(formula='Sales ~ Price_Eggs',data=df).fit()
    ped_fit.summary()
    #Linear format of the model: y = b0 + b1*x
    b0 = ped_fit.params["Intercept"]
    b1 = ped_fit.params["Price_Eggs"]
    smg.plot_fit(ped_fit,1)
    
    return b0, b1, ped_fit

def value_loop(b0,b1,point_est):
    global a_matrix
    y = []
    x = []
    a_m = []
    x_int = -b0/b1 #negative b0 intercept as a part of negative slope of line
    it = x_int/point_est
    n = 0
    while n < x_int:
        y_calc = b0+(b1*n)
        y.append(y_calc)
        x.append(n)
        a_m.append(y_calc*n)
        n = n + it
    y = pd.Series(y)
    x = pd.Series(x)
    a_m = pd.Series(a_m)
    a_matrix = pd.DataFrame({"y":y,"x":x,"area":a_m})
    a_matrix.plot(kind='scatter', x='x', y='area')
    text = "The Unit Price Elasticity of Demand for this model is estimated to be: $"
    text2 = "This has a total revenue of: $"
    text3 = "With expected sales quantity of :"
    max_area = a_matrix["area"].max()
    s_m = a_matrix.sort('area',ascending=False)
    unit_elastic_price = s_m.iloc[0]['x']
    expected_sales_quntity = s_m.iloc[0]['y']
    print text + str(round(unit_elastic_price,2))
    print text2 + str(round(max_area,2))
    print text2 + str(round(expected_sales_quntity,2))
    plt.plot(unit_elastic_price, max_area,'ro')
    plt.plot([unit_elastic_price,unit_elastic_price],[max_area,0],'k')
    plt.plot([0,unit_elastic_price],[max_area,max_area],'k')
    return

reg_fit(df)
value_loop(b0,b1,point_est)
