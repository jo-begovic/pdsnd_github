import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}

# list of months
months = ['january', 'february', 'march', 'april', 'may', 'june']
#list of days
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
# list of cities
cities = ['chicago', 'new york', 'washington']
# list of filters
filters = ['month', 'day', 'both', 'none']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # declare month and day variables with the value None
    month = None
    day = None
    # Save error text in variable
    error_msg = 'You made a typo! Please try again!'

    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Which city would you like to see data from? Chicago, New York or Washington?\n').lower()
        if city in cities:
            break
        print('Please try again! Select one of these three cities: Chicago, New York, Washington!')

    # get user input for filter and store it in filter variable
    while True:
        filter = input('Would you like to filter the data by month, day, both or not at all? Type \'none\' for no time filter.\n').lower()
        if filter in filters:
            break
        print(error_msg)

    # get user input for filters
    while filter != 'none':
        if filter == 'both':
            while True:
                month = input('Which month would you like to filter the data? January, February, March, April, May or June?\n').lower()
                day = input('Which day would you like to filter the data?\n').lower()
                if (month in months) and (day in days):
                    break
                print(error_msg)
        elif filter == 'month':
            while True:
                month = input('Which month would you like to filter the data? January, February, March, April, May or June?\n').lower()
                if month in months:
                    break
                print(error_msg)
        else:
            while True:
                day = input('Which day would you like to filter the data?\n').lower()
                if day in days:
                    break
                print(error_msg)
        break

    print('-' * 40)
    print('Loading the results for:\n CITY: {}\n MONTH: {}\n DAY: {}'.format(city, month, day).title())
    print('-' * 40)
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

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != None:
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != None:
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0] - 1
    print('Most Frequent Month:', months[popular_month].title())

    # display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    popular_week = df['day_of_week'].mode()[0]
    print('Most Frequent Day:', popular_week)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Frequent Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station:\n', popular_start_station)

    # display the count of most commonly used start station
    start_station_count = df.loc[df['Start Station'] == popular_start_station].count()[0]
    print('Count:', start_station_count)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station:\n', popular_end_station)

    # display the count of most commonly used end station
    end_station_count = df.loc[df['Start Station'] == popular_end_station].count()[0]
    print('Count:', end_station_count)

    # display most frequent combination of start station and end station trip
    popular_combination = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('Most Popular Combination:\n', popular_combination.to_string())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total = df['Trip Duration'].sum()
    print('Total duration:', total)

    # display mean travel time

    avg = df['Trip Duration'].mean()
    print('Average:', avg)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Counts of user types:\n', user_types.to_string())

    # display infos for Gender if column exists
    if 'Gender' in df.columns:
        # Display counts of gender
        gender = df['Gender'].value_counts()
        print('Counts of gender:\n', gender.to_string())

    # display infos for Birth Year if column exists
    if 'Birth Year' in df.columns:
        # Display earliest, most recent, and most common year of birth
        earliest_yob = df['Birth Year'].min()
        print('Earliest year of birth:', earliest_yob)

        most_recent_yob = df['Birth Year'].max()
        print('Most recent year of birth:', most_recent_yob)

        most_common_yob = df['Birth Year'].mode()[0]
        print('Most common year of birth:', most_common_yob)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def raw_data(df):
    x = 5
    while True:
        display = input('\nWould you like to see the raw data? Enter yes or no.\n')
        while display.lower() == 'yes':
            print(df.head(x))
            x += 5
            display = input('\nAdditional five rows? Enter yes or no.\n')
        break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
