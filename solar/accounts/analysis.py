import pandas as pd
from sklearn.externals import joblib
from sklearn.preprocessing import MinMaxScaler
from datetime import date, datetime,timedelta

csv_url = '/home/mayuresh/solar/accounts/Dataset/'


def prediction(date, city):
    date = str(date)
    print(date)

    y = date.split('-')

    url = csv_url + city + '/2017.csv'

    data = pd.read_csv(url)

    data['Hour'] = data['Hour'] + data['Minute'] / 60
    data = data.drop('Minute', 1)
    x = data.loc[(data['Month'] == int(y[1])) & (data['Day'] == int(y[2])), 'Month':'Pressure'].values

    time = ["00.00", "00.30", "1.00", "1.30", "2.00", "2.30", "3.00", "3.30", "4.00", "4.30", "5.00", "5.30", "6.00",
            "6.30",
            "7.00", "7.30", "8.00", "8.30", "9.00", "9.30", "10.00", "10.30", "11.00", "11.30", "12.00", "12.30",
            "13.00", "13.30", "14.00", "14.30", "15.00", "15.30", "16.00", "16.30", "17.00", "17.30", "18.00", "18.30",
            "19.00", "19.30",
            "20.00", "20.30", "21.00", "21.30", "22.00", "22.30", "23.00", "23.30"]

    print(len(time))

    scaler = MinMaxScaler()
    X_test = scaler.fit_transform(x)
    knn2 = joblib.load('/home/mayuresh/solar/accounts/Model/knn_model.pkl')
    y = knn2.predict(X_test)
    print(len(y))

    ans = []
    for i in range(0, 48, 2):
        y[i] = round(y[i], 2)
        temp = [time[i], y[i]]
        ans.append(temp)
    return ans


def total_energy_generation(ans):
    total = 0
    for i, j in ans:
        total = total + j
    total = round(total, 2)
    return total


def current_time_generation(ans):
    curr = 0
    now = datetime.now()
    print("Now",now)
    now = str(now)
    date_time = now.split(" ")
    hours = date_time[1].split(":")
    print("Hours",hours[0])
    for i, j in ans:
        print(i,"i")
        if float(i) <= int(hours[0]):
            curr = curr + j
        else:
            break
    return round(curr, 2)


def peak5hours(ans):
    temp_list1 = []
    temp_list2 = []

    for i, j in ans:
        temp_list1.append(i)
        temp_list2.append(j)

    count = 0

    peak_answer = []
    while count != 5:
        max1 = max(temp_list2)
        index = temp_list2.index(max1)
        temp = [temp_list1[index], max1]
        peak_answer.append(temp)
        temp_list1.remove(temp_list1[index])
        temp_list2.remove(max1)
        count = count + 1

    return peak_answer


def current_analysis(city):
    today = date.today()
    ans = prediction(today, city)
    total = total_energy_generation(ans)
    curr = current_time_generation(ans)
    print(curr, "\t", total)
    return ans, curr, total


def future_prediction(date1,city):
    ans = prediction(date1,city)
    total = total_energy_generation(ans)
    peak_hours = peak5hours(ans)
    return ans, total, peak_hours


def weekly():
    days1 = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekly_day_production = [5000, 5103, 5400, 3500, 4900, 6000, 4400]
    weekly_day_usage = [3000, 3103, 4400, 3000, 2000, 4000, 3400]
    weekly_day_energy_left = []

    for i in range(0, len(weekly_day_production)):
        temp = weekly_day_production[i] - weekly_day_usage[0]
        weekly_day_energy_left.append(temp)

    energy_left = sum(weekly_day_energy_left)
    total = sum(weekly_day_production)
    today = date.today()
    prev_monday = today + timedelta(days=-today.weekday())

    ans = []
    for i in range(0, 7):
        temp = [days1[i], weekly_day_usage[i], weekly_day_energy_left[i]]
        ans.append(temp)

    return ans, energy_left, total, prev_monday
