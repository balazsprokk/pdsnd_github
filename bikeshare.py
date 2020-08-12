"""
Some random comments for practice
"""

import time
import pandas as pd
import numpy as np
import calendar

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

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = input("First of all, let's choose a city! We have bike data for Chicago, New York City and Washington. \n Please, enter the name of your preferred city, here: ").lower()

    while city not in CITY_DATA.keys():
        city = input("Please, enter a valid city: ").lower()


    # TO DO: get user input for month (all, january, february, ... , june)

    month = input("Please, enter your preferred month from January to June or all for all months: ").lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    day = input("Please, enter your preferred day - i.e. from Sunday to Monday- or all for all days: ").lower()

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
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    df['month'] = df['Start Time'].dt.month
    most_common_month = df['month'].mode()[0]

    # TO DO: display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    most_common_day = df['day_of_week'].mode()[0]

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print(most_common_start_station)

    # TO DO: display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print(most_common_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    trip_counts = df.groupby(['Start Station', 'End Station'])['Start Time'].count()
    frequent_trip_stations = trip_counts.sort_values(ascending=False)
    print(frequent_trip_stations)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_duration = df['Trip Duration'].sum()
    print(total_travel_duration)

    # TO DO: display mean travel time
    rows = len(df)
    mean = total_travel_duration/ rows
    print(mean)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    # Use the .count() function

    user_type_counts = df.groupby('User Type')['User Type'].count()
    print(user_type_counts)

    # TO DO: Display counts of gender
    if 'Gender' in df:
        gender_counts = df.groupby('Gender')['Gender'].count()
        print(gender_counts)


    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth year' in df:
        earliest_birth_year = "Earliest birth year: " + str(int(df['Birth Year'].min()))
        most_recent_birth_year = "Most recent birth year: " + str(int(df['Birth Year'].max()))
        birth_year_counts = df.groupby('Birth Year')['Birth Year'].count()
        sorted_birth_years = birth_year_counts.sort_values(ascending=False)
        total_trips = df['Birth Year'].count()
        most_common_birth_year = "Most common birth year: " + str(int(sorted_birth_years.index[0])) + " (" + str(sorted_birth_years.iloc[0]) + " trips, " +                   '{0:.2f}%'.format(((sorted_birth_years.iloc[0]/total_trips) * 100)) + " of trips)"

        print(earliest_birth_year)
        print(most_recent_birth_year)
        print(most_common_birth_year)


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

        print("Would you like see a tabular presentation of this data with five rows? \n Please, enter yes or no: ")
        display_data = input()
        display_data = display_data.lower()

        i = 5
        while display_data == 'yes':
            """ To display few rows of data for user view """
            print(df[:i])
            print("Would you like to see how this tabular presentation continues with another five rows? \n Please, enter yes or no: ")
            i += 5
            display_data = input()
            display_data = display_data.lower()

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
