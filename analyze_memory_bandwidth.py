
#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
from sklearn.metrics import r2_score
from scipy.optimize import curve_fit
import enum

def log_func(x, a, c):
    return (a * x.apply(np.log) + c)

def power_series_func(x, a, b):
    return (a * x.pow(b))

def sqrt_func(x, a, c):
    return (a * x.apply(math.sqrt) + c)



# xs      : pandas.Series
# true_ys : pandas.Series
# pred_ys : pandas.series
def find_distances_to_trendline(xs, true_ys, pred_ys):
    pred_ys_array = pred_ys.array

    dist = []

    for index, value in true_ys.items():
        dist.append(abs(value - pred_ys_array[index]))
            
    distance = pd.Series(dist)

    return distance



def process_unrolled_accumulator_loop_test(csv_filepath, fig_title, fig_file_name):
    data = pd.read_csv(csv_filepath, header=None, names=['num_bytes', 'num_cycles', 'bytes_per_cycle', 'bytes_per_ns'])

    num_bytes = data['num_bytes']
    xmin = num_bytes.min()
    xmax = num_bytes.max()
    x_range = xmax - xmin

    bytes_per_ns = data['bytes_per_ns']
    y_min = bytes_per_ns.min()
    y_max = bytes_per_ns.max()
    y_range = y_max - y_min

    fig, ax = plt.subplots()
    fig.set_size_inches(15, 8)
    plt.grid()
    ax.axis([(xmin - (x_range * 0.1)), (xmax + (x_range * 0.1)), (y_min - (y_range * 0.1)), (y_max + (y_range * 0.1))])

    plt.title(fig_title)
    plt.xlabel('Number of Bytes')
    plt.ylabel('Bytes per Nanosecond')

    #z = np.polyfit(num_bytes, bytes_per_ns, 1)
    #y_hat = np.poly1d(z)(num_bytes)

    popt, pcov = curve_fit(log_func, num_bytes, bytes_per_ns)
    y_hat = log_func(num_bytes, *popt)
 
    distance = find_distances_to_trendline(num_bytes, bytes_per_ns, y_hat)
    dist_std = distance.std()

    outliers_x_a = []
    outliers_y_a = []

    outliers_x_b = []
    outliers_y_b = []

    outliers_x_c = []
    outliers_y_c = []

    for i, value in distance.items():
        if (value > (2.8 * dist_std)) and (bytes_per_ns[i] < y_hat[i]):

            if value < 1.7:
                outliers_x_a.append(num_bytes[i])
                outliers_y_a.append(bytes_per_ns[i])

            else:
                outliers_x_c.append(num_bytes[i])
                outliers_y_c.append(bytes_per_ns[i])

            num_bytes = num_bytes.drop(i)
            bytes_per_ns = bytes_per_ns.drop(i) 



    popt1, pcov1 = curve_fit(log_func, num_bytes, bytes_per_ns)
    y_hat1 = log_func(num_bytes, *popt1)
    y_hat_r2 = r2_score(y_true=bytes_per_ns, y_pred=y_hat1)

    plt.plot(num_bytes, y_hat1, "r--")
    text = 'y=%5.3f * log(x) + %5.3f' % tuple(popt1)
    text = text + '\nR^2 = %5.3f\n' % y_hat_r2
    

    ax.scatter(num_bytes, bytes_per_ns, c='#00cecb', alpha=0.5)


    set_a_xs = pd.Series(outliers_x_a)
    set_a_ys = pd.Series(outliers_y_a)
    
    popta,pcova = curve_fit(sqrt_func, set_a_xs, set_a_ys)
    y_hat_a = sqrt_func(set_a_xs, *popta)
    a_b_distances = find_distances_to_trendline(set_a_xs, set_a_ys, y_hat_a)
    a_b_dist_std = a_b_distances.std()
   
    for i, value in a_b_distances.items():
        if (value > a_b_dist_std) and (set_a_ys[i] < y_hat_a[i]):
            outliers_x_b.append(set_a_xs[i])
            outliers_y_b.append(set_a_ys[i])

            set_a_xs = set_a_xs.drop(i)
            set_a_ys = set_a_ys.drop(i)



    ax.scatter(set_a_xs, set_a_ys, c='#ff5b5e', alpha=0.5)

    popta1,pcova1 = curve_fit(sqrt_func, set_a_xs, set_a_ys)
    y_hat_a1 = sqrt_func(set_a_xs, *popta1)
    plt.plot(set_a_xs, y_hat_a1, "r--")
    y_hata1_r2 = r2_score(y_true=set_a_ys, y_pred=y_hat_a1)
    text = text + '\ny=%5.3f * sqrt(x) + %5.3f' % tuple(popta1)
    text = text + '\nR^2 = %5.3f\n' % y_hata1_r2



    set_b_xs = pd.Series(outliers_x_b)
    set_b_ys = pd.Series(outliers_y_b)

    ax.scatter(set_b_xs, set_b_ys, c='#ddb967', alpha=0.5)

    poptb,pcovb = curve_fit(sqrt_func, set_b_xs, set_b_ys)
    y_hat_b = sqrt_func(set_b_xs, *poptb)
    plt.plot(set_b_xs, y_hat_b, "r--")
    y_hat_b_r2 = r2_score(y_true=set_b_ys, y_pred=y_hat_b)
    text = text + '\ny=%5.3f * sqrt(x) + %5.3f' % tuple(poptb)
    text = text + '\nR^2 = %5.3f\n' % y_hat_b_r2



    set_c_xs = pd.Series(outliers_x_c)
    set_c_ys = pd.Series(outliers_y_c)

    ax.scatter(set_c_xs, set_c_ys, c='#003d5b', alpha=0.5)

    poptc, pcovc = curve_fit(sqrt_func, set_c_xs, set_c_ys)
    y_hat2 = sqrt_func(set_c_xs, *poptc)
    y_hat2_r2 = r2_score(y_true=set_c_ys, y_pred=y_hat2)
    plt.plot(set_c_xs, y_hat2, "r--")

    text = text + '\ny=%5.3f * sqrt(x) + %5.3f' % tuple(poptc)
    text = text + '\nR^2 = %5.3f\n' % y_hat2_r2



    plt.gca().text(0.05, 0.95, text,transform=plt.gca().transAxes, fontsize=10, verticalalignment='top')

    plt.savefig(fig_file_name, dpi=100)

    plt.cla()
    plt.clf()


def process_bcopy_test(csv_filepath, fig_title, fig_file_name, guess_parent_fn=Parent_Func.none):
    data = pd.read_csv(csv_filepath, header=None, names=['num_bytes', 'num_cycles', 'bytes_per_cycle', 'bytes_per_ns'])

    num_bytes = data['num_bytes']
    xmin = num_bytes.min()
    xmax = num_bytes.max()
    x_range = xmax - xmin

    bytes_per_ns = data['bytes_per_ns']
    y_min = bytes_per_ns.min()
    y_max = bytes_per_ns.max()
    y_range = y_max - y_min

    fig, ax = plt.subplots()
    fig.set_size_inches(15, 8)
    plt.grid()

    popt, pcov = curve_fit(power_series_func, num_bytes, bytes_per_ns)
    y_hat = power_series_func(num_bytes, *popt)
    y_hat_r2 = r2_score(y_true=bytes_per_ns, y_pred=y_hat)
    plt.plot(num_bytes, y_hat, "r--")

    text = 'y=%5.3f * x^%5.3f' % tuple(popt)
    text = text + '\nR^2 = %5.3f' % y_hat_r2
    plt.gca().text(0.05, 0.95, text,transform=plt.gca().transAxes, fontsize=14, verticalalignment='top')

    steps = np.linspace(start=math.floor(y_min - (y_range * 0.1)), stop=math.ceil(y_max + (y_range * 0.1)), num=bytes_per_ns.count())

    ax.scatter(num_bytes, bytes_per_ns, c=steps, cmap='viridis', alpha=0.5)
    ax.axis([(xmin - (x_range * 0.1)), (xmax + (x_range * 0.1)), (y_min - (y_range * 0.1)), (y_max + (y_range * 0.1))])

    plt.title(fig_title)
    plt.xlabel('Number of Bytes')
    plt.ylabel('Bytes per Nanosecond')

    plt.savefig(fig_file_name, dpi=100)

    plt.cla()
    plt.clf()



def main():
    #process_bcopy_test('../memory/data/bcopy_memory_bandwidth_results.csv', 'bcopy Memory Bandwidth Test', 'bcopy_memory_bandwidth_test.png')

    process_unrolled_accumulator_loop_test('../memory/data/unrolled_accumulator_loop_memory_bandwidth_results.csv', 'Unrolled Accumulator Loop Memory Bandwidth Test', 'unrolled_accumulator_loop_memory_bandwidth_test.png')



if __name__=="__main__":
    main()
