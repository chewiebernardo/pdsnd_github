import datetime
import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'new york': 'new_york_city.csv', # Added in case of typo
              'washington': 'washington.csv' }

# usefull variables
months = ['january', 'february', 'march', 'april', 'may', 'june']
days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

# REFERENCE: https://pypi.org/project/colorama/
def colored_text(text, foreground=None, background=None):

    foreground_dict = { 'black': '\033[30m',
                        'red': '\033[31m',
                        'green': '\033[32m',
                        'yellow': '\033[33m',
                        'blue': '\033[34m',
                        'magenta': '\033[35m',
                        'cyan': '\033[36m',
                        'white': '\033[37m' }
    background_dict = { 'black': '\033[40m',
                        'red': '\033[41m',
                        'green': '\033[42m',
                        'yellow': '\033[43m',
                        'blue': '\033[44m',
                        'magenta': '\033[45m',
                        'cyan': '\033[46m',
                        'white': '\033[47m' }

    formated_text = ''
    # apply background color if selected
    if background != None:
        formated_text += background_dict[background]
    # apply foreground color if selected
    if foreground != None:
        formated_text += foreground_dict[foreground]

    # reset styles
    formated_text += text + '\033[39m\033[49m'

    return formated_text

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (int) month - name of the month to filter by, or "all" to apply no month filter
        (int) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city = ''
    month = None
    day = None

    print('Hello! Let\'s explore some US bikeshare data!')
    print('Please choose a city before we start')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city_inputed = input('You can choose between Chicago, New York City or Washington:\r\n')
        if city_inputed.lower() in CITY_DATA:
            city = city_inputed.lower()
            print('Great, let\'s work with {} for now.\r\nYou can reestart and change it later.'.format(city_inputed))
            break
        print('Sorry, I couldn\'t find the city you typed, can you check again please?')

    # get user input for month (all, january, february, ... , june)
    print('\r\nAlright, now tell me which month you want to analyze')
    while True:
        month_inputed = input('You can choose between January and June, or ALL for all months\r\n')
        if month_inputed.lower() in months or month_inputed.lower() == 'all':
            if month_inputed.lower() == 'all':
                print('OK, everything it is.')
            else:
                print('OK, let me show you how {} went.'.format(month_inputed))
                month = months.index(month_inputed.lower())+1
            break
        print('Sorry, I couldn\'t understand you.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    print('\r\nLast but not least, do you want to know about a specific day of the week?')
    while True:
        #Dictionay used only to switch from abbreviation to full name and get it's index
        week_days_abbreviation = {'mon':('monday',1), 'tue':('tuesday',2), 'wed':('wednesday',3), 'thu':('thursday',4), 'fri':('friday',5), 'sat':('saturday',6), 'sun':('sunday',7)}

        day = input('Choose the week day you want to know more information: Mon, Tue, Wed, Thu, Fri, Sat, Sun or All for everything\r\n').lower()
        if day in week_days_abbreviation:
            print('OK, let me show you how {} went.'.format(week_days_abbreviation[day][0].title()))
            day = week_days_abbreviation[day][1]
            break
        elif day == 'all':
            print('OK, everything it is.')
            day = None
        else:
            print('You need to choose one of the days.')


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (int) month - name of the month to filter by, or None to apply no month filter
        (int) day - name of the day of week to filter by, or None to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['start_hour'] = df['Start Time'].dt.hour


    # filter by month if applicable
    if month != None:
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != None:
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('The most popular month is: ', colored_text(months[popular_month-1].title(), 'green'))

    # display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]
    print('The most popular day of the week is: ', colored_text(days_of_week[popular_day_of_week-1].title(), 'green'))

    # display the most common start hour
    popular_start_hour = str(df['start_hour'].mode()[0])
    print('The majority of the trips starts at ', colored_text(popular_start_hour, 'green'))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0].title()
    print('The station most used to begin the trip is: ', colored_text(popular_start_station, 'green'))

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0].title()
    print('The station most used to finish the trips is: ', colored_text(popular_end_station, 'green'))

    # display most frequent combination of start station and end station trip
    popular_route = df.groupby(['Start Station', 'End Station'])['Start Station'].count().sort_values(ascending=False).keys()[0]
    print('And this is the most popular route is from {} to {}.'.format(colored_text(popular_route[0], 'green'), colored_text(popular_route[1], 'green')))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = str(df['Trip Duration'].sum())
    print('In this period, the sum of trips durations is: ', colored_text(total_travel_time, 'green'))

    # display mean travel time
    mean_travel_time = str(df['Trip Duration'].mean())
    print('But, in average, the trips took: ', colored_text(mean_travel_time, 'green'))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df.groupby('User Type')['User Type'].count()
    print(user_types)
    print('\r\n')

    # Display counts of gender
    try:
        user_gender = df.groupby('Gender')['Gender'].count()
        print(user_gender)
    except:
        print('We don\'t have data related to Gender in this base')

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_birth_year = str(int(df['Birth Year'].min()))
        oldest_age = str(int(datetime.datetime.now().year - df['Birth Year'].min()))
        print('The earliest Birth Year is {}, so that person would have {} years today.'.format(colored_text(earliest_birth_year, 'yellow'), colored_text(oldest_age, 'yellow')))

        most_recent_birth_year = str(int(df['Birth Year'].max()))
        youngest_age = str(int(datetime.datetime.now().year - df['Birth Year'].max()))
        print('In other hand, the most recent Birth Year is {}, that person has {} years.'.format(colored_text(most_recent_birth_year, 'yellow'), colored_text(youngest_age, 'yellow')))

        most_common_birth_year = str(int(df['Birth Year'].mode()[0]))
        print('And the most common Birth Year is {}.'.format(colored_text(most_common_birth_year, 'yellow')))
    except:
        print('We don\'t have data related to Birth Year in this base')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_raw_data(df, step):
    """Displays raw data on bikeshare users."""

    print('\nShowing some raw data...\n')
    start_time = time.time()


    window_size = 15
    start_index = step*window_size
    end_index = (step+1)*window_size
    if end_index > df.size:
        end_index = df.size

    if df[start_index:end_index].empty:
        print(colored_text('No more data to show', 'red'))
    else:
        print(df[start_index:end_index])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        raw_data = input('\nWould you like to see some raw data? Enter yes or no.\n')
        step = 0
        while raw_data.lower() == 'yes':
            show_raw_data(df, step)
            step += 1
            raw_data = input('\nWould you like to see more raw data? Enter yes or no.\n')

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
