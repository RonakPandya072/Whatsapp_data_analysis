import pandas as pd
import re

def preprocess(data):
    pattern = '\d{1,2}\/\d{1,2}\/\d{2,4},\s\d{1,2}:\d{1,2}\s\D{2}\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'User_messages': messages, "message_dates": dates})
    df['message_dates'] = pd.to_datetime(df['message_dates'], format='%d/%m/%Y, %H:%M %p - ', exact=False)
    df.rename(columns={'message_dates': 'dates'}, inplace=True)

    # separate user and messages
    user = []
    messages = []
    pattern = '([^:]*)'
    for message in df['User_messages']:
        entry = re.split(pattern, message)
        if len(entry) > 5:
            user.append(entry[1])
            messages.append(entry[5])
        else:
            messages.append(entry[0])
            user.append('Group Notification')

    df['user'] = user
    df['message'] = messages
    df.drop(columns=['User_messages'], inplace=True)

    df['year'] = df['dates'].dt.year
    df['only_date'] = df['dates'].dt.date
    df['month'] = df['dates'].dt.month_name()
    df['day'] = df['dates'].dt.day
    df['hour'] = df['dates'].dt.hour
    df['minute'] = df['dates'].dt.minute
    df['month_no'] = df['dates'].dt.month
    df['day_name'] = df['dates'].dt.day_name()

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df['period'] = period


    return df