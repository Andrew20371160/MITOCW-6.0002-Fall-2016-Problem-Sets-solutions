# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: 
# Collaborators (discussion):
# Time:


import pylab
import re
import datetime
# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\\d\\d\\d\\d)(\\d\\d)(\\d\\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    # TODO
    ret_list = []
    for deg in degs:
        ret_list.append(pylab.array(pylab.polyfit(x,y,deg)))
    return ret_list




def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """

    # TODO

    mse =sum((y-estimated)**2)
    
    y_mean = sum(y)/len(y)
    
    y_var = sum((y-y_mean)**2)
    
    return 1 -(mse/y_var)




def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    # TODO
    
    for model in models:
        pylab.figure()
        
        estimates = pylab.polyval(model,x)

        se_over_slope_val = None
        
        if len(model)==2:
            se_over_slope_val = se_over_slope(x,y,estimates,model)

        pylab.plot(x,y,'bo',label = 'Observations')
        
        pylab.plot(x,estimates,'-r',label = 'Estimates')
        
        title = 'Regression degree = '+str((len(model)-1))+'\n'+'R-squared = '+str(r_squared(y,estimates))
        if se_over_slope_val !=None:
            title +='\nSE/slope= '+str(se_over_slope_val)
        
        pylab.title(title)
        pylab.legend()
        pylab.xlabel('Years')
        pylab.ylabel('degrees Celsius')

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")

        filename =f"figure_{timestamp}.png"
        pylab.savefig(filename)    





def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    ret_degrees = pylab.zeros(len(years))
    
    for i in range(len(years)):
        for city in multi_cities:
            annual_city_degrees = climate.get_yearly_temp(city,years[i])
            ret_degrees[i] +=sum(annual_city_degrees)/len(annual_city_degrees)
        ret_degrees[i]/=len(multi_cities)
    
    return ret_degrees

def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    # TODO
    arr = pylab.zeros(len(y))
    index = 0
    temp_window = 1
    for start in range(len(y)-window_length+1):
        while  temp_window<window_length:
            arr[index] = sum(y[start:start+temp_window])/temp_window
            temp_window+=1
            index+=1
        arr[index] =sum(y[start:start+window_length])/window_length
        index+=1
    return arr 





def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    return (sum((y-estimated)**2)/len(y))**0.5


def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    ret_res = pylab.zeros(len(years))
    #def get_yearly_temp(self, city, year):
    for year_c in range(len(years)):
        avg_daily_temps =climate.get_yearly_temp(multi_cities[0],years[year_c])
        for city_c in range(1,len(multi_cities)):
            avg_daily_temps +=climate.get_yearly_temp(multi_cities[city_c],years[year_c])
        avg_daily_temps/=len(multi_cities)
        
        ret_res[year_c] = (sum((avg_daily_temps-sum(avg_daily_temps)/len(avg_daily_temps))**2)/len(avg_daily_temps))**0.5

    return ret_res 

def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    for model in models:
        pylab.figure()
        
        estimates = pylab.polyval(model,x)


        pylab.plot(x,y,'bo',label = 'Observations')
        
        pylab.plot(x,estimates,'-r',label = 'Estimates')
        
        title = 'Regression degree = '+str((len(model)-1))+'\n'+'RMSE = '+str(rmse(y,estimates))
        
        pylab.title(title)
        pylab.legend()
        pylab.xlabel('Years')
        pylab.ylabel('degrees Celsius')

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")

        filename =f"figure_{timestamp}.png"
        pylab.savefig(filename)    



if __name__ == '__main__':

    c = Climate('data.csv')

    # Part A.4
    #def get_daily_temp(self, city, month, day, year):
    training_years = pylab.array(TRAINING_INTERVAL)
    
    degrees = pylab.zeros(len(training_years))
    for i in range(len(training_years)):
        degrees[i] = c.get_daily_temp('NEW YORK',1,10,training_years[i])
    models = generate_models(training_years,degrees,[1])
    evaluate_models_on_training(training_years,degrees,models)

    #def get_yearly_temp(self, city, year):

    for i in range(len(training_years)):

        yearly_temp =c.get_yearly_temp('NEW YORK',training_years[i]) 
        
        degrees[i] =sum(yearly_temp)/len(yearly_temp)
    
    models = generate_models(training_years,degrees,[1])
    
    evaluate_models_on_training(training_years,degrees,models)
    

    # Part B
    # TODO: replace this line with your code
    degrees = gen_cities_avg(c,CITIES,training_years)
    models = generate_models(training_years,degrees,[1])
    evaluate_models_on_training(training_years,degrees,models)
    
    # Part C
    # TODO: replace this line with your code
    degrees = moving_average(degrees,5)
    models = generate_models(training_years,degrees,[1])
    evaluate_models_on_training(training_years,degrees,models)

    # Part D
    
    #part D.1
    models = generate_models(training_years,degrees,[1,2,20])
    evaluate_models_on_training(training_years,degrees,models)
    
    #part D.2
    testing_years = pylab.array(TESTING_INTERVAL)

    testing_degreees_avgs  = gen_cities_avg(c,CITIES,testing_years)
    
    testing_degreees_avgs =moving_average(testing_degreees_avgs,5)

    evaluate_models_on_testing(testing_years,testing_degreees_avgs,models)


    
    # Part E
    # TODO: replace this line with your code

    yearly_stds = gen_std_devs(c,CITIES,training_years)
    yearly_stds = moving_average(yearly_stds,5)
    models = generate_models(training_years,yearly_stds,[1])
    evaluate_models_on_training(training_years,yearly_stds,models)
    
