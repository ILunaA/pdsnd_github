#modules
import os
import time
import pandas as pd
import numpy as np

# variables to be used in all the functions
city_data = { 1: {'file': 'chicago.csv', 'city':'chicago'},
              2: {'file': 'new_york_city.csv', 'city': 'new york' },
              3: {'file': 'washington.csv','city': 'washington'  } }

months_name = ['all','january','february','march','april','may','june','july','august','september','october','november','december']
months_id = list(range(13))
months_data = dict(zip(months_id,months_name))

days_name = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']
days_id = list(range(8))
days_data = dict(zip(days_id,days_name))
#########

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city_file - name of the city csv file to analyze
        (int) month - number of the month to filter by, or 0 for all (no month filter)
        (str) day - name of the day of week to filter by, or "All" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).

    while True:

        try:
            city_input = int(input("Select city for analysis, please type: 1 for Chigaco, 2 for New York, 3 for Washington: ",))
            # city_options = [i for i in range(1,4)]
            if city_input in range(1,4):

                city = city_data[city_input]['city']
                city_file = city_data[city_input]['file']
                print('You have chosen city {}'.format(city))
            else:
                print('input is not part of options')
                continue

        except ValueError:
            print('Please check you type an integer of the possible options(1,2,3)')
            continue

        else:
            break

    print('-'*40)

    # get user input for month to be used as filter.
    while True:

        try:
            month_input = int(input("type integer for month to be used in filter, please type: 0 for all (no filter), 1 for January up to 12 for december: ",))

            if month_input in range(13):

                month_filter = months_data[month_input]
                print('You have chosen {} as month filter'.format(month_input))
            else:
                print('input is not part of options, try again')
                continue

        except ValueError:
            print('Please check you type an integer of the possible options(0 to 12)')
            continue

        else:
            break


           # get user input for day (all, monday...sunday)

    print('-'*40)

    while True:

        try:
            day_input = int(input("type integer for day to be used in filter, please type: 0 for all (no filter), 1 for Monday up to 7 for Sunday: ",))

            if day_input in range(8):

                day_filter = days_data[day_input]
                print('You have chosen {} as day filter'.format(day_input))
            else:
                print('input is not part of options, try again')
                continue

        except ValueError:
            print('Please check you type an integer of the possible options(0 to 7)')
            continue

        else:
            break

    print('-'*40)

    print(" Your input translate into city: {}, month: {}, day: {} . Thank you!!".format(city.title(),month_filter.title(),day_filter.title()))

    return city_file,month_input,day_filter.title()

####

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city file to analyze
        (int) month - number of the month to filter by, or 0 to apply no month filter
        (str) day - name of the day of week to filter by, or "All" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    ### open file
    print('we open file for chosen city: ', city)
    data_pkg_path = ''
    filename = city
    path = os.path.join(data_pkg_path, filename)
    df = pd.read_csv(path)

    ### transform to datetime and extract month,day,hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    #month
    df['month'] = df['Start Time'].dt.month
    #day
    df['dayofweek'] = df['Start Time'].dt.day_of_week
    df['dayname'] = df['Start Time'].dt.day_name()
    #hour
    df['hour'] = df['Start Time'].dt.hour


    ### filter by month
    if month == 0 :
        print('no filter by month')
    else :
        print ('filter by month: ', month )
        df = df[df['month'] == month]
        print('dimensions after filter by month: ',df.shape)

    ### filter by day
    if day == 'All' :
        print('no filter by day')
    else :
        print ('filter by day: ', day )
        df = df[df['dayname'] == day]
        print('dimensions after filter by day: ',df.shape)

        print('-'*40)

    if df.shape[0] == 0:
        print('There is no data for your filter selection, please try another one')

    print('-'*40)

    return df


####
def time_stats(df, month_value, day_value):

    """
    Displays statistics on the most frequent times of travel.

    Args:
        (df) df - DataFrame to analyze
        (int) month_value - number of the month to filter by (1-12), or 0 to apply no month filter
        (str) day_value - name of the day of week to filter by, or "All" to apply no day filter
    Returns:
        Print of calculated stats regarding time of travel
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month_value == 0:
        mc_month = df['month'].mode()[0]
        month_name = months_data[mc_month]
        print('Most popular month:',month_name)
    else :
        print('Filtered by month')
    # display the most common day of week
    if day_value == 'All':
        mc_dayown = df['dayname'].mode()[0]
        print('Most popular day of week:', mc_dayown)
    else :
        print('Filtered by day')

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('Most popular start hour:', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

####
def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.

    Args:
        (df) df - DataFrame to analyze

    Returns:
        Print of calculated stats regarding stations and trips
    """


    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    mc_start_station = df['Start Station'].mode(0)[0]
    print('Most common start station was: ', mc_start_station)
    # display most commonly used end station
    mc_end_estation = df['End Station'].mode(0)[0]
    print('Most common end station was: ', mc_end_estation)

    # display most frequent combination of start station and end station trip
    mc_trip = df.groupby(['Start Station','End Station']).size().idxmax()
    print('Most common trip was from {} to {}.'.format(mc_trip[0],mc_trip[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

####
def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration

    Args:
        (df) df - DataFrame to analyze

    Returns:
        Print of calculated stats regarding trip duration
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time_hr = df['Trip Duration'].sum()/3600
    print('Total travel time was: {} hours '.format(round(total_travel_time_hr,2)))

    # display mean travel time
    ave_travel_time_min = df['Trip Duration'].mean()/60
    # ave_travel_time_hour = ave_travel_time_min/60
    print('Average travel time was: {} minutes '.format(round(ave_travel_time_min,2)))
    # print(ave_travel_time_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
####
def user_stats(df, city_value):
    """
    Displays statistics on bikeshare users

    Args:
        (df) df - DataFrame to analyze

    Returns:
        Print of calculated stats regarding users
    Note: Chicago and New york have gender and birth year data, but not Washington.

    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    for idx,name in enumerate(df['User Type'].value_counts().index.tolist()):
        print('Name :', name)
        print('Counts :', df['User Type'].value_counts()[idx])



    ## chicago and new york have gender and birth year data

    # Display counts of gender
    if city_value == 'washington.csv':
        print('Washington dataset does not have gender and birth data')
    else :
        print('-'*20)
        # print('gender stats')
        for idx,name in enumerate(df['Gender'].value_counts().index.tolist()):
            print('Name :', name)
            print('Counts :', df['Gender'].value_counts()[idx])

    # Display earliest, most recent, and most common year of birth
        print('-'*20)
        yb_earliest = df['Birth Year'].min()
        print('Earliest year of birth is: ',int(yb_earliest))
        yb_mrecent = df['Birth Year'].max()
        print('Most recent year of birth is: ',int(yb_mrecent))
        mc_yb = df['Birth Year'].mode()[0]
        print('Most common year of birth: ', int(mc_yb))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
####
def show_data(df):
    """
    Shows raw data records (5 rows each time)

    Args:
        (df) df - DataFrame to show

    Returns:
        Records of dataframe (5 each time)


    """

    while True :

        try:
            show_datai = input("\nWould you like to see data about trips? Enter 'y' or 'n' (for no or yes).\n")
            if show_datai == 'y':

                nrows = df.shape[0]
                irows = 0

                while irows < nrows:

                    # print('input value was: ',show_datai)
                    print('first row to show is: ',irows)
                    print(df.iloc[range(irows,irows + 5),1:9])

                    #check if user want to see more rows
                    show_more = input("\nWould you like to see more data about trips? Enter 'y' or any other value to terminate.\n")
                    if show_more.lower() == 'y':
                        irows += 5
                        continue

                    else :
                        print("Done exploring data. I will terminate now.")
                        break
            elif  show_datai == 'n':
                print('You have chosen not to explore raw data. I will terminate now.')
                break

            else :
                print('input value is not valid, please try again')
                continue
        except ValueError:
            print('Please check you input of the possible options(y or n)')
            continue

        else:
            break
####

def main():
    while True:
        city, month, day = get_filters()
        print(city, month, day)
        df = load_data(city, month, day)

        time_stats(df, month_value = month, day_value = day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city_value = city)
        show_data(df)



        restart = input('\nWould you like to restart? Enter yes or any other input to stop.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
