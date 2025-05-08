import re
import pandas as pd


def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2},\s*\d{1,2}:\d{2}\s*(?:AM|PM)'

    message = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    dates = [re.sub(r'[\u00A0\u2000-\u200B\u202F\u205F\u3000]', ' ', d) for d in dates]

    df = pd.DataFrame({'username': message, 'date': dates})
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%y, %I:%M %p')

    users = []
    messages = []
    for i in df['username']:
        entry = re.split(r'^\s*-?\s*([^:]+):\s', i)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('groud_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns='username', inplace=True)

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['only_date'] = df['date'].dt.date
    df['month_num'] = df['date'].dt.month
    df['day_name'] = df['date'].dt.day_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + '-' + str(hour + 1))
    df['period'] = period

    return df.sort_values('user')
