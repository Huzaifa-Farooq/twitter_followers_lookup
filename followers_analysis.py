import pandas as pd
import os
from datetime import datetime


def get_datetime_object(datetime_str):
    """ gets a string and returns a datetime object """
    datetime_str = datetime_str.split('T')
    #datetime_str = f"{datetime_str[0]} {datetime_str[1].split('.')[0]}"

    # ignoring time
    # only date is required
    datetime_str = f"{datetime_str[0]}"
    dt_obj = datetime.strptime(datetime_str, '%Y-%m-%d')

    return dt_obj


def check_req_directories(path):
    if not os.path.exists(f"{path}\\modified"):
        os.mkdir(f"{path}\\modified")
        print("Created Required Directory")

def convert_to_dt_object(path):
    """ takes string row of a dataframe and convert it into datetime_object
     so that reading(parser_dates=[]) it will be easy """

    # checking directories
    check_req_directories(path)

    for file in os.listdir(path):
        print(file)
        # first condition to ignore folders and 2nd to check if files are csv
        if '.' in file and file.split('.')[1] == 'csv':
            df = pd.read_csv(f"{path}\\{file}")

            print(f"converting {file}")
            modified_df = df.copy()
            date_column = modified_df['created_at']

            for index, row in date_column.iteritems():
                # getting datetime object
                dt_obj = get_datetime_object(row)
                date_column.loc[index] = dt_obj
                print(index)

            modified_df.to_csv(f"{path}\\modified\\{file}")


def filter_df(df):
    """ function to make the dataframe in suitable form """

    required_df = df.copy()

    required_fields = ['id', 'name', 'username', 'location', 'created_at',
                       'followers_count', 'following_count', 'tweet_count', 'is_verified']

    # getting df_columns
    df_columns = list(required_df.columns)
    # getting extra fields
    fields_to_remove = list(set(df_columns).difference(set(required_fields)))

    # dropping unnecessary columns
    for field in fields_to_remove:
        del required_df[field]

    return required_df


def store_combine_df(path):
    """ gets a pth reads all csv files from that path and store a combined file of that csv files """
    df_list = []
    for file in os.listdir(f"{path}\\modified"):
        print(file)
        # first condition to ignore folders and 2nd to check if files are csv
        if '.' in file and file.split('.')[1] == 'csv':
            df = pd.read_csv(f"{path}\\modified\\{file}", parse_dates=['created_at'])
            print(df['created_at'].loc[0])
            # filtering dataframe for any non-required fields
            df = filter_df(df)
            df_list.append(df)

    combined = pd.concat(df_list)
    combined.to_csv(f"{path}\\modified\\combined.csv")
    print(f"Stored combined csv file to {path}\\modified\\combined.csv")


def load_data(path):
    """ loads data in dataframes"""

    # checking if all csv files have been combined
    # if not then combine and store them in a csv file
    if not os.path.exists(f"{path}\\modified\\combined.csv"):
        store_combine_df(path)

    df = pd.read_csv(f"{path}\\modified\\combined.csv", parse_dates=['created_at'])
    df = filter_df(df)
    return df


def get_creation_date_plot(df):
    """ gets a df and creates a  plot """
    import matplotlib.pyplot as plt

    print("creating plot")

    dates = list(date.to_pydatetime() for date in df['created_at'])
    dates_dict = dict(Counter(dates))

    df.groupby('created_at').count().plot()
    # plotting accounts created after date 2020-9-1 the day account was created
    df[df.created_at > datetime(2020, 9, 1, 0, 0, 0)].groupby('created_at').count().plot()


    import time
    x_values = []  # dates
    y_values = []  # no. of accounts created on that date

    for date, count in dates_dict.items():
        if date >= datetime(2020, 9, 1):
            x_values.append(date)
            y_values.append(count)

    # increasing y scale
    y_limits = [0, max(y_values)+500]

    plt.style.use('seaborn')
    fig, ax = plt.subplots()

    plt.scatter(x_values, y_values, s=15, edgecolors=None)
    plt.title('Followers of NS', fontsize=20)
    plt.xlabel('', fontsize=14)
    fig.autofmt_xdate()
    plt.ylabel('No of followers Created', fontsize=14)
    plt.ylim(y_limits)
    plt.tick_params(axis='both', which='major', labelsize=14)


    plt.show()
    plt.savefig(f"{path}\\plot.png")



from collections import Counter
path = "D:\\Huzaifa\\automation\\twitter\\NawazSharifMNS\\followers"
data = load_data(path)

print(data.head())
print(data[data.duplicated('id')])

print(data.shape[0])

dates = list(date.to_pydatetime() for date in data['created_at'])
dates_dict = dict(Counter(dates))

temp = data.loc[data['created_at'] >= datetime(2020, 9, 1)]
print(f"{temp.shape[0]} Accounts were created between {datetime(2020, 9, 1)} upto {datetime.now()}")
print(temp)


get_creation_date_plot(data)



