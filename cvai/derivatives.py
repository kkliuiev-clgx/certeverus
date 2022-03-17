"""
This method creates the path to the target

"""
# import math
import numpy as np
import pandas as pd
import sympy as sp
from sympy.solvers import solve
# import matplotlib.pyplot as plt
# import simplejson as json
# import plotly

# from IPython.display import display

try:
    from cvai import plot_table as pt
except ImportError:
    import plot_table as pt


def distance(x, y, x2, y2):
    return (((x2-x)**2)+((y2-y)**2))**.5


def distcheck(xdel, theta):
    return xdel/np.cos(theta)


def f(x, T, y, start):
    return ((((start - x)**2)+((y - T/(x))**2))**(.5))
    # creates the distance function ((start - x)**2)+((y -T/(x))**2)


# def plot_baseline(xs, ys, start, y, Label_x, Label_y, yscale, xiso1):
#     fig1 = plt.figure(figsize=(5, 5))
#     # p1 = plt.plot(xs, ys, "b--",)  # plot target line

#     # p2 = plt.plot(start, y, "ro")  # plot each data point
#     # p3=plt.vlines(np.mean(start),0,6,colors ="g",linestyles='dashed',linewidth =.5)
#     # p4=plt.hlines(np.mean(start),0,6,colors ="g",linestyles='dashed',linewidth =.5)
#     plt.ylim(0, yscale)  # limit the y-axis
#     plt.xlim(0, xiso1)  # limit the y-axis
#     plt.xlabel(Label_x)
#     plt.ylabel(Label_y)
#     # fig1.show()
#     return fig1


# def plot_prescriptive_vectors(xs, ys, start, y, Label_x, Label_y, cv, ya, yscale, xiso1):
#     fig2 = plt.figure(figsize=(5, 5))
#     p1 = plt.plot(xs, ys, "b--",)
#     p2 = plt.plot(start, y, "ro", ms=7, mec="r")
#     plt.ylim(0, yscale)
#     plt.xlim(0, xiso1)
#     plt.xlabel(Label_x)
#     plt.ylabel(Label_y)
#     # p3 = plt.plot(cv,ya,'ko', ms = 7, mec = 'k')
#     xvalues = ([start, cv])
#     yvalues = ([y, ya])
#     # p4= plt.plot(xvalues,yvalues, lw ='1', ls=':',c='g')
#     p5 = plt.hlines(y, start, cv)
#     p6 = plt.vlines(cv, y, ya)
#     # p7 = plt.plot([0,6],[0,6])
#     # fig2.show()
#     return fig2


def get_angle(cv, start, ya, y, T):
    deltax = cv - start  # finds change in x (capacity)
    deltay = ya - y      # finds change in y (productivity)
    deltas = deltay/deltax  # Calculates the Tan(theta) for the prescription
    # print( "the change in y is:",deltay)
    # print( "the change in x is:",deltax)
    deltas = deltas.reshape(T.size,)
    # print("the deltas are:",deltas)
    deltas = deltas.astype(np.float64)
    thetar = np.arctan(deltas)
    theta = np.degrees(thetar)
    return theta, deltax, deltay, thetar


def create_prescriptions(fx, theta, deltax, Label_x, deltay, Label_y):
    """
    This method will build the prescriptions table based
    Created on Sun Jan 02 2022 - 18:34:37
    @author: michaelprinci

    @Parameters
        ----------
    fx, theta, deltax, Label_x, deltay, Label_y

    @Returns
        -------
    prescription: object
    """
    prescription = np.empty_like(fx)
    theta = theta.astype(np.float64)

    for count, items in enumerate(theta):
        if items <= (60):  # TODO Revise the angular assignments to connect to tactics
            prescription[count] = f"Add {deltax[count]:.2f} " + Label_x
        else:
            prescription[count] = f"Change {Label_y} by {deltay[count]:.2f} "
    return prescription


def get_critical_values(fx, x, T):  # TODO #274 Review how CV is getting calculated
    """
    This method will differentiate (first derivative) to find critical points for f(x)=> f'(x)
    Created on Sun Jan 02 2022 - 18:35:57
    @author: michaelprinci

    @Parameters
        ----------
    fx, x, T

    @Returns
        -------
    cv: object
    """
    d = sp.diff(fx, x)
    print("D = \n\n", d)
    d = np.asarray(d)  # load array - might be able to streamline
    cv = np.empty_like(fx)  # create empty array for critical values

    for count, items in enumerate(d):  # loop to load critical numbers
        # find critical numbers cv for each f'(x)
        cv[count] = np.asarray(solve(items, x, set=False))

    # temp = map(lambda elem: filter(lambda a: a>0, elem), cv)  #creates a temp array with only positive values for critical numbers
    # loads positive (quadrant 1 CVs) -- PROBLEM THIS BECOMES A LIST
    cv = [[a for a in elem if a > 0] for elem in cv]
    # cv1 = np.array(cv, dtype=object) # converts to array
    cv = np.array([l[0] if l else np.nan for l in cv])
    cv = cv.reshape(T.size,)

    return cv  # FIXME: [CAM-42] refactor code and make labels more meaningful


def build_prescription_list(start, y, T, cv, ya, theta, dist, prescription):
    colsname = ['x1', 'y1', 'Result', 'Target', 'x2', 'y2', 'Reset Target',
                'Angle', 'Distance', 'Prescription', 'Additional value']
    # df = pd.DataFrame(np.stack((start, y, start*y, T, cv, ya, cv*ya,
    # theta, dist, prescription, (cv*ya)-(start*y)), axis=1))
    df = pd.DataFrame(np.stack((start, y, start*y, T, cv, ya, cv*ya,
                                theta, dist, prescription, (cv*ya)-(start*y)), axis=1), columns=colsname)

    # df.rename(columns={0: 'x1', 1: 'y1', 2: 'Result', 3: 'Target', 4: 'x2', 5: 'y2', 6: 'Reset Target',
    #    7: 'Angle', 8: 'Distance', 9: 'Prescription', 10: 'Additional value'}, inplace=True)
    # df['Prescription'] = prescription
    df = df.sort_values('Additional value', ascending=False)
    # df['Additional value'] = df['Additional value'].round(2)
    q = df['Additional value'].sum()
    qq = df['Reset Target'].sum()
    qqq = df['Result'].sum()
    # df['Additional value'] = df['Additional value'].map('${:,.2f}'.format)
    dfc = df.style.format({
        'x1': '{:,3d}'.format,
        'y1': '{:,3d}'.format,
        'y2': '{:,3d}'.format,
        'Angle': '{:,3d}'.format,
        'x2': '{:,3d}'.format,
        'Reset Target': '{:,3d}'.format,
        'Distance': '{:,3d}'.format,
        'Additional value': '{:,3d}'.format
    })
    return q, qq, qqq, df, dfc


def course_change(start, y, Label_x, Label_y, x, T):

    # fig1 = plot_baseline(xs, ys, start, y, Label_x, Label_y,yscale,xiso1) # Plot Baseline
    # Get Critical Values
    # get the function values for differentiation of f(x)
    fx = f(x, T, y, start)
    # print('fx:',fx)
    cv = get_critical_values(fx, x, T)  # get critical values
    # print('critical values:',cv)

    # Plot Prescriptive Vectors
    ya = np.asarray(
        T)/np.asarray(cv)  # Defines prescription y value for incrementing driver
    # print('ya:',ya, np.asarray(T), np.asarray(cv)) # checks values
    # fig2 = plot_prescriptive_vectors(xs, ys, start, y, Label_x, Label_y, cv, ya,yscale,xiso1)# Plots example with prescriptions plotted against the target

    # Find the angle using trig to define the prescription
    theta, deltax, deltay, thetar = get_angle(cv, start, ya, y, T)
    prescription = create_prescriptions(
        fx, theta, deltax, Label_x, deltay, Label_y)  # Create the prescriptions
    # Calculate distance and hypotheses for comparison
    dist = distance(start, y, cv, ya)
    # Create a dataframe to present the results
    hypot = distcheck(deltax, thetar)
    print(hypot, dist)
    q, qq, qqq, df, dfc = build_prescription_list(
        start, y, T, cv, ya, theta, dist, prescription)
    print('Additional value of ${0:3.2f}M  bringing portfolio to ${1:3.2f}M from current performance at ${2:3.2f}M  '.format(
        q, qq, qqq), '\n\n')
    return df, dfc


# def normalzed(C, T, L):
#     sqrtx = np.roots([(-5*C)/(2*T), 6, -3*L, 0, C*T])
#     # print(answer2)
#     return sqrtx

def get_data_for_local_test(source='local'):
    # from sympy.abc import x
    x = sp.symbols('x',real=True)
    print(x)
    # T =sp.symbols ('T')
    # y = sp.symbols("y")
    # start = sp.symbols('s')

    # ADD STARTING VALUES
    if source == 'local':
        Label_x = 'Ordered Quantity'
        Label_y = 'Net Sales/Ordered Quantity'
        xscale = 10
        yscale = 10
        xiso0 = 0
        xiso1 = 20
        obs = 5
        target = 6
        start = xscale*np.random.random_sample((obs, ))
        y = yscale*np.random.random_sample((obs, ))
        # Load Target Array
        T = 1.075 * max(start*y)*np.asarray(np.ones(y.size,))
    else:
        Label_x = 'Ordered Quantity'
        Label_y = 'Net Sales/Ordered Quantity'
        xscale = 10
        yscale = 10
        xiso0 = 0
        xiso1 = 20
        start = np.array([2188, 1233, 5959, 6291, 8624])
        y = np.array([1464.71, 924, 415.61, 244, 240])
        obs = len(start)
        target = (17472763/obs)
        T = np.asarray(np.ones(y.size,))*target

    return start, y, Label_x, Label_y, x, T

# Run the function locally for testing


def main(source=None):
    start, y, Label_x, Label_y, x, T = get_data_for_local_test(source)
    df, dfc = course_change(start, y, Label_x,
                            Label_y, x, T)
    print(df)
    fig = pt.plot_table(df)
    return fig

# fig.show()
# print(fig)
# aaa = plotly.io.to_json(fig)
# print(aaa)

# C= .40
# L= 19000
# T = 200
# norm = normalzed(C,T,L)
# print(norm)
# for x in norm:
#     z = distance(L,C,x,T/x)
#     print(x,"paired with",z)

    #     print(z)


# main()


# Now we can use both *args ,**kwargs
# to pass arguments to this function :
