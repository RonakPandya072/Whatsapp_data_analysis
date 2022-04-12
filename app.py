import matplotlib.pyplot as plt
import streamlit as st
import preprocessor,helper
import seaborn as sns
st.sidebar.title("Whatsapp Chat Analyzer")

#file upload
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
     # To read file as bytes:
     bytes_data = uploaded_file.getvalue()
     data = bytes_data.decode("utf-8")

     data = preprocessor.preprocess(data)
     #st.write("Overall data")
     #st.dataframe(data)

     #fetch unique users:
     user_list = data['user'].unique().tolist()
     user_list.remove('Group Notification')
     user_list.sort()
     user_list.insert(0,'Overall')
     selected_user=st.sidebar.selectbox("Show analysis with respect to",user_list)



     if st.sidebar.button("Show analysis"):
          if selected_user != 'Overall':
               st.write("Updated list")
               new_df= data[data['user']==selected_user]
               #st.write(new_df)

          st.title("Top statistics")
          num_messages, words, media_msg ,links= helper.fetch_stats(selected_user,data)
          col1,col2,col3,col4 = st.columns(4)

          with col1:
               st.header("Total messages:")
               st.title(num_messages)

          with col2:
               st.header("Total words:")
               st.title(words)

          with col3:
               st.header("Media shared")
               st.title(media_msg)

          with col4:
               st.header("Links shares")
               st.title(links)

          #timeline
          st.title("Monthly timeline")
          timeline = helper.monthly_user(selected_user,data)
          fig,ax = plt.subplots()
          ax.plot(timeline['time'],timeline['message'], color='green')
          plt.xticks(rotation='vertical')
          plt.xlabel('Timeline', fontweight='bold')
          plt.ylabel('No. of messages', fontweight='bold')
          st.pyplot(fig)

          #daily timeline
          st.title("Daily Timeline")
          daily_timeline = helper.daily_timeline(selected_user,data)

          fig, ax = plt.subplots()
          ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='red')
          plt.xticks(rotation='vertical')
          plt.xlabel('Daily Timeline', fontweight='bold')
          plt.ylabel('No. of messages', fontweight='bold')
          st.pyplot(fig)

          #activity map
          st.title("Activity Map")
          col1, col2 = st.columns(2)
          with col1:
               st.header("Most busy day")
               busy_day = helper.week_activity_map(selected_user,data)
               fig, ax = plt.subplots()
               ax.bar(busy_day.index,busy_day.values)
               st.pyplot(fig)

          with col2:
               st.header("Most busy month")
               busy_month = helper.month_activity_map(selected_user, data)
               fig, ax = plt.subplots()
               ax.bar(busy_month.index, busy_month.values, color='orange')
               st.pyplot(fig)

          st.title("Weekly activity map")
          user_heatmap = helper.activity_heatmap(selected_user, data)
          fig, ax = plt.subplots()
          ax = sns.heatmap(user_heatmap)
          st.pyplot(fig)
          #finding active member in the group
          if selected_user == 'Overall':
               st.title("Most Active User")
               col1,col2 = st.columns(2)
               x, active_User = helper.busy_user(data)
               fig,ax = plt.subplots()

               with col1:
                    ax.bar(x.index,x.values, color=['maroon','olive','teal','gold','peru'])
                    plt.xticks(rotation='vertical')
                    plt.xlabel('User',fontweight='bold')
                    plt.ylabel('No. of messages',fontweight='bold')
                    plt.title("Top 5 active Users")
                    st.pyplot(fig)

               with col2:
                    st.write(active_User)

          #create word cloud
          st.title("Word cloud")
          df_wc = helper.create_word_cloud(selected_user,data)
          fig,ax=plt.subplots()
          ax.imshow(df_wc)
          plt.axis('off')
          st.pyplot(fig)

          #most common words
          st.title("Most common words")
          most_common = helper.most_common_words(selected_user,data)
          word = most_common['word'].values
          freq = most_common['frequency'].values
          fig = plt.figure(figsize=(10, 8))
          plt.xticks(rotation='vertical')
          plt.xlabel("Most common words", fontweight='bold')
          plt.ylabel("frequency", fontweight='bold')
          sns.barplot(y = word,x = freq)
          st.pyplot(fig)



