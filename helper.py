from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter




extract = URLExtract()
links = []
def fetch_stats(selected_user,df):
    #fetch no. of messages
    if selected_user == 'Overall':
        num_messages = df.shape[0]
        #no. of media files count
        num_media_message = df[df['message'] == ' <Media omitted>\n' ].shape[0]
        #no. of links shared
        for message in df['message']:
            links.extend(extract.find_urls(message))
        #no. of words count
        length = 0
        for messages in df['message']:
            length = length+len(messages.split())
        return num_messages, length,num_media_message, len(links)

    else:
        new_df= df[df['user']==selected_user]
        num_messages = new_df.shape[0]
        num_media_message = new_df[new_df['message'] == ' <Media omitted>\n' ].shape[0]
        for message in new_df['message']:
            links.extend(extract.find_urls(message))
        length = 0
        for messages in new_df['message']:
            length = length + len(messages.split())
        return num_messages, length, num_media_message, len(links)


def busy_user(df):
    #finding most active person
    active = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'user','user':"%age"})
    return active, df

def create_word_cloud(selected_user,df):
    f = open('stop_hinglish.txt')
    stop_words = f.read()
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'Group Notification	']
    temp = temp[temp['message'] != ' <Media omitted>\n']

    def remove_stop_words(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)
    wc = WordCloud(height=500,width=500,min_font_size=10,background_color='white')
    temp['message']=temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):
    f = open('stop_hinglish.txt')
    stop_words = f.read()
    if selected_user !='Overall':
        df=df[df['user']==selected_user]
    temp = df[df['user'] != 'Group Notification	']
    temp = temp[temp['message'] != ' <Media omitted>\n']
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20)).reset_index().rename(columns={0:"word",1:"frequency"})
    return most_common_df

def monthly_user(selected_user,df):
    if selected_user !='Overall':
        df=df[df['user']==selected_user]
    timeline = df.groupby(['year', 'month', 'month_no']).count()['message'].reset_index()
    timeline = timeline.sort_values(['year', 'month_no'])
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user, df):
    if selected_user !='Overall':
        df=df[df['user']==selected_user]
    daily_timeline = df.groupby(['only_date']).count()['message'].reset_index()
    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user !='Overall':
        df=df[df['user']==selected_user]
    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user !='Overall':
        df=df[df['user']==selected_user]
    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user !='Overall':
        df=df[df['user']==selected_user]
    activity_heat = df.pivot_table(index='day_name',columns='period', values='message',aggfunc='count').fillna(0)
    return activity_heat
