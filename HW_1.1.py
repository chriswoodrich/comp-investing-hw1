## homework #1 for Computational investing part 1

#QTSK and other imports

import pandas as pd
import numpy as np
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import datetime as dt
import matplotlib.pyplot as plt
from itertools import product

trading_days = 252

def simulate(dt_start, dt_end, ls_symbols, ls_allocation):

        #date timestamps
        dt_timeofday = dt.timedelta(hours=16)
        ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)

        # read closing values
        ls_keys = ['close']
        c_dataobj = da.DataAccess('Yahoo')
        ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
        d_data = dict(zip(ls_keys, ldf_data))
        
        #agg portfolio value
        temp = d_data['close'].values.copy()
        d_normal = temp / temp[0,:]
        alloc = np.array(ls_allocation).reshape(4,1)
        portfolio = np.dot(d_normal, alloc)

        #daily returns
        dailyVal = portfolio.copy()
        tsu.returnize0(dailyVal) # who named this function?

        # calc. daily return, trading vol., sharpe ratio, and total returns
        daily_return = np.mean(dailyVal)
        vol = np.std(dailyVal)
        sharpe = np.sqrt(trading_days) * daily_return / vol
        cum_return = portfolio[portfolio.shape[0] -1][0]
        
        return vol, daily_return, sharpe, cum_return



def print_stuff(dt_start, dt_end, ls_symbols, ls_allocation):
        vol, daily_return, sharpe, cum_return  = simulate( dt_start, dt_end, ls_symbols, ls_allocation )
        print "start", dt_start
        print "end: ", dt_end
        print "ticker symbols: ", ls_symbols
        print "optimal: ", ls_allocation
        print "Sharpe ratio: ", sharpe
        print "standard devaition: ", vol
        print "average daily return: ", daily_return
        print "total return: ", cum_return #heh


#special thanks to Tristan Chong for this bit of itertools code.
#While it is cleaner than the 4 nested for loops I had before, the return 'count' is still 10000, so it's running 10^4 times, even tough there are only
#288 'legal' portfolio allocations.

def best_allocation(dt_start, dt_end, ls_symbols):

    #populate possibles
    possibles = []
    count = 0
    for digits in product('0123456789', repeat=4):
        count += 1
        if sum(map(int, digits)) == 10:
            possibles.append(tuple([float(digit)/10 for digit in digits]))
                
                
    max_sharpe = -1
    best_alloc = [0.0, 0.0, 0.0, 0.0]
    alloc = [0.0, 0.0, 0.0, 0.0]
    
    #print possibles[1], possibles[2], possibles[3]
    #test possibles    
    for x in range(0, len(possibles)):    
        alloc = possibles[x]
        vol, daily_return, sharpe, cum_return = simulate( dt_start, dt_end, ls_symbols, alloc )
        if sharpe > max_sharpe:
            max_sharpe = sharpe
            best_alloc = alloc

    return best_alloc, count




# question 1 and 2?  # allocation not defined in question 1...
dt_start = dt.datetime(2011,1,1)
dt_end = dt.datetime(2011,12,31)
ls_symbols = ['C', 'GS', 'IBM', 'HNZ'] 
ls_allocation = [0.6, 0.1, 0.1, 0.1]

max_alloc, count = best_allocation(dt_start, dt_end, ls_symbols)
print_stuff(dt_start, dt_end, ls_symbols, max_alloc)
print "this many times:" , count



