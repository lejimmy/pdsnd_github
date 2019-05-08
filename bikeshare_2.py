import time
import pandas as pd
import numpy as np

# global variables for data files
CITY_DATA = {
    "chicago": "chicago.csv",
    "new york city": "new_york_city.csv",
    "washington": "washington.csv",
}

# global variables for available months and days
months = ["january", "february", "march", "april", "may", "june", "all"]
days = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
    "all",
]


def get_filters():
    """
    Asks user to specify a city and filters by month, day, both, or none.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    while True:
        # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        city = input("Enter a city (Chicago, New York City, or Washington): ").lower()

        # if city is not valid, restart the while loop
        if city not in CITY_DATA:
            print("Invalid city input, try again!")
            continue

        # get user to input filter(s)
        filter = input("Would you like to filter by month, day, both or none? ").lower()

        if filter not in ["month", "day", "both", "none"]:
            print("Invalid filter, try again!")
            continue

        # if filter is none, select all months and all days
        if filter == "none":
            month = "all"
            day = "all"

        # if filtering by month, get user to input month and select all days
        if filter == "month":
            month = input(
                "Enter a month (All, January, February, ... , June): "
            ).lower()

            # if month is not valid, restart the loop
            if month not in months:
                print("Invalid month input, try again!")
                continue

            day = "all"

        # if filtering by day, get user to input day and select all months
        if filter == "day":

            day = input(
                "Enter a day of week (All, Monday, Tuesday, ... Sunday): "
            ).lower()

            # if day is not valid, restart the loop
            if day not in days:
                print("Invalid day of week input, try again!")
                continue

            month = "all"

        # if filtering by both months and days, get user to input both
        if filter == "both":

            month = input(
                "Enter a month (All, January, February, ... , June): "
            ).lower()

            # if month is not valid, restart the loop
            if month not in months:
                print("Invalid month input, try again!")
                continue

            day = input(
                "Enter a day of week (All, Monday, Tuesday, ... Sunday): "
            ).lower()

            # if day is not valid, restart the loop
            if day not in days:
                print("Invalid day of week input, try again!")
                continue

        print()
        print("Inputs accepted!")
        print()

        break

    print("-" * 40)

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
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    # extract month and day of week from Start Time to create new columns
    df["month"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.weekday_name

    # filter by month if applicable
    if month != "all":
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df.loc[df["month"] == month]

    # filter by day of week if applicable
    if day != "all":
        # filter by day of week to create the new dataframe

        df = df.loc[df["day_of_week"] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    # display the most common month
    common_month = df["month"].mode()[0]

    print(
        "The most popular month was {}.".format(months[common_month - 1].capitalize())
    )

    # display the most common day of week
    common_day = df["day_of_week"].mode()[0]

    print("The most popular day of the week was {}.".format(common_day.capitalize()))

    # display the most common start hour
    common_hour = df["Start Time"].dt.hour.mode()[0]

    print(
        "The most popular period was {}:00-{}:00.".format(common_hour, common_hour + 1)
    )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # display most commonly used start station
    common_start = df["Start Station"].mode()[0]

    print("The most popular start station was at: {}.".format(common_start))

    # display most commonly used end station
    common_end = df["End Station"].mode()[0]

    print("The most popular end station was at: {}.".format(common_end))

    # display most frequent combination of start station and end station trip
    common_comb = (
        df.groupby(["Start Station", "End Station"])
        .size()
        .reset_index()
        .rename(columns={0: "count"})
    )

    max_comb = common_comb.max()

    # displays different output if the start and end stations are the same
    if max_comb[0] == max_comb[1]:
        print(
            "The most popular route taken by {} people, started and ended at the {} Station.".format(
                max_comb[2], max_comb[0]
            )
        )
    else:
        print(
            "The most popular route taken by {} people, started at the {} Station and ended at the {} Station.".format(
                max_comb[2], max_comb[0], max_comb[1]
            )
        )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # display total travel time in days
    total_days = round(df["Trip Duration"].sum() / 60 / 60 / 24, 2)

    print("The total of all trip durations was {} days.".format(total_days))

    # display mean travel time in minutes
    average_trip = round(df["Trip Duration"].mean() / 60, 2)

    print("The average trip durations was {} minutes.".format(average_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # Display counts of user types
    user_types = df["User Type"].value_counts()

    for i in range(user_types.size):
        print(
            "{} user(s) are {}(s).".format(user_types[i], user_types.index[i].lower())
        )

    # Try to caculate gender and birth year data
    try:
        # Display counts of gender
        gender_types = df["Gender"].value_counts()

        print()
        print(
            "{} users are {} and {} users are {}.".format(
                gender_types[0],
                gender_types.index[0].lower(),
                gender_types[1],
                gender_types.index[1].lower(),
            )
        )

        # Display earliest, most recent, and most common year of birth
        earliest_year = int(df["Birth Year"].min())
        recent_year = int(df["Birth Year"].max())
        common_year = int(df["Birth Year"].mode()[0])

        print()
        print(
            "The user with the earliest year of birth was in {}.".format(earliest_year)
        )
        print(
            "The user with the most recent year of birth was in {}.".format(recent_year)
        )
        print("The most common year of birth was in {}.".format(common_year))

    except KeyError:
        print("No gender or birth years available for city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def main():

    print()
    print("Hello! Let's explore some US bikeshare data!")
    print()
    print(" o__         __o        ,__o        __o           __o")
    print(" ,>/_       -\<,      _-\_<,       _`\<,_       _ \<_")
    print("(*)`(*).....O/ O.....(*)/'(*).....(*)/ (*).....(_)/(_)\n")

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        while True:
            sample = input("Would you like to see sample data?  Yes or No: ")

            if sample.lower() == "yes":
                print(df.sample(n=5))
                continue

            if sample.lower() == "no":
                break

            print("Invalid Input, please enter Yes or No")
            print()

        restart = input("\nPlease enter yes to restart, otherwise program will end: ")
        if restart.lower() != "yes":
            break

    print()
    print("Bye! See you next time.")
    print()
    print(" o__         __o        ,__o        __o           __o")
    print(" ,>/_       -\<,      _-\_<,       _`\<,_       _ \<_")
    print("(*)`(*).....O/ O.....(*)/'(*).....(*)/ (*).....(_)/(_)\n")


if __name__ == "__main__":
    main()
