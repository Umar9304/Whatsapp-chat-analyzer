import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import emoji


def stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    new_messages = df.shape[0]
    words = []
    for i in df['message']:
        words.extend(i.split())

    media = df[df['message'] == '<Media omitted>\n'].shape[0]

    links = []
    for message in df['message']:
        ext = URLExtract()
        url = ext.find_urls(message)
        links.extend(url)

    return new_messages, len(words), media, len(links)


def most_busy(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts().head() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'user': 'name', 'count': 'percent'})

    return x, df


def word_cloud(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'groud_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_word(message):
        y = []
        for i in message.lower().split():
            if not emoji.is_emoji(i):
                if i not in stop_words:
                    y.append(i)
        return " ".join(y)

    wc = WordCloud(height=300, width=300, min_font_size=10, background_color='white')
    temp['message'].apply(remove_stop_word)
    df_wc = wc.generate(df['message'].str.cat(sep=' '))
    return df_wc


def common_word(selected_user, df):
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = f.read().splitlines()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'groud_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if not emoji.is_emoji(word):
                if word not in stop_words:
                    words.append(word)

    # Get top 20 common words
    common_words = Counter(words).most_common(20)

    # Convert to DataFrame
    most_word_df = pd.DataFrame(common_words, columns=['Word', 'Count'])

    return most_word_df


def emoji_get(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for i in df['message']:
        emojis.extend([x for x in i if emoji.is_emoji(x)])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(emojis)))
    emoji_df.columns = ['emoji', 'count']
    return emoji_df


def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))

    timeline['time'] = time
    return timeline, daily_timeline


def activity(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts(), df['month'].value_counts()


def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return user_heatmap
