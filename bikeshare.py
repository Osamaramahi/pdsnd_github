import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inpupts
    city = input('Please insert city name (Chicago ,New York city ,Washington):\n').lower()
    while city not in CITY_DATA.keys() :
          city= input( 'Please insert valid city:\n').lower() 

    # TO DO: get user input for month (all, january, february, ... , june)
    months = ['All','January', 'February', 'March', 'April', 'May', 'June']
    month = input('Please insert a month name (All or a month between January and June): \n').lower().title()
    while month not in months:
        month = input ('Please insert valid month:\n').lower().title()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day_of_week = ['Sunday', 'Monday', 'Tuesday','Wednesday','Thursday','All']
    day = input('Please insert day name (All or a specific day): \n').lower().title()
    while day not in day_of_week:
        day = input( 'Please insert a valid day: \n').lower().title()

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
# load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month.lower() != 'all':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day.lower() != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print('the most common month: ')
    print(df['Start Time'].dt.month_name().mode()[0])
    
    # TO DO: display the most common day of week
    print('the most common day of week: ')
    print(df['Start Time'].dt.day_name().mode()[0])

    # TO DO: display the most common start hour
    print('the most common start hour: ')
    print(df['Start Time'].dt.hour.mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('most commonly used start station: ')
    print(df['Start Station'].mode()[0])

    # TO DO: display most commonly used end station
    print('most commonly used end station: ')
    print(df['End Station'].mode()[0])

    # TO DO: display most frequent combination of start station and end station trip
    print('most commonly used Combination of start and end station: ')
    df['combination'] = df['Start Station'].astype(str) +' < Start - End > '+ df['End Station']
    print(df['combination'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    # TO DO: display total travel time
    print('total travel time: ')
    print(df['Trip Duration'].sum())
    
    
    # TO DO: display mean travel time
    print('mean travel time: ')
    print(df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('counts per user types: ')
    print(df['User Type'].value_counts())
    
    # TO DO: Display counts of gender
    if 'Male' or 'Female' not in df['Gender']: 
        print('no Data related to gender!')
    else:
        print('counts per gender: ')
        print(df['Gender'].value_counts())

    # TO DO: Display earliest, most recent, and most common year of birth
    if city in ('washington'):
        print('birth year is not available')
    else:
        print('Most common birth year:')
        print(df['Birth Year'].mode()[0])
        print('Earliest birth year:')
        print(df['Birth Year'].loc[df['Start Time']==df['Start Time'].min()].to_string(index=False))  
        print('Most recent birth year:')
        print(df['Birth Year'].loc[df['Start Time']==df['Start Time'].max()].to_string(index=False))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

def display_data(df):
    """Displays 5 row of data if user ask."""
    display = input('do you want to see first 5 row of the data? (yes,no) n/').lower()

    df2 = df.reset_index()
    index=0
    while display == 'yes':
        print(df2.iloc[index:index+5])
        index +=5
        display = input('do you want to see the next 5 row of the data? (yes,no) n/').lower()
    
    
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
