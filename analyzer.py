import preprocessing as ps
import streamlit as st
import work
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title('WHATSAPP ANALYZER')

upload_file = st.sidebar.file_uploader("Choose File")
if upload_file is not None:
    byte_data = upload_file.getvalue()
    byte_data = byte_data.decode('utf-8')

    df = ps.preprocess(byte_data)
    df = df[df['user'] != 'groud_notification']
    user_list = df['user'].unique().tolist()
    user_list.insert(0, 'Overall')

    selected_user = st.sidebar.selectbox("Select user", user_list)

    if st.sidebar.button('Show'):
        new_message, word, media, link = work.stats(selected_user, df)
        st.title('CHAT ANALYSIS')

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages Sent")
            st.title(new_message)

        with col2:
            st.header("Total No. of Words")
            st.title(word)

        with col3:
            st.header("Total Links Shared")
            st.title(link)

        with col4:
            st.header("Total Media Shared")
            st.title(media)

        # timeline
        st.title('Timeline')
        col1, col2 = st.columns(2)

        timeline, daily_timeline = work.monthly_timeline(selected_user, df)
        with col1:
            st.header('Monthly')
            fig, ax = plt.subplots()
            ax.plot(timeline['time'], timeline['message'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header('Daily ')
            fig, ax = plt.subplots()
            ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # busiest user
        if selected_user == 'Overall':
            st.title("MOST BUSY USER")
            x, new_df = work.most_busy(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                fig, ax = plt.subplots(figsize=(6, 6))
                ax.pie(new_df['percent'], labels=new_df['name'], autopct='%1.1f%%', startangle=90)
                ax.axis('equal')  # Equal aspect ratio makes the pie circular
                ax.set_title('Top Users')
                st.pyplot(fig)

        # WordCloud
        st.title('Word Analysis')
        col1, col2 = st.columns(2)
        with col1:
            st.header("WordCloud")
            df_wc = work.word_cloud(selected_user, df)
            fig, ax = plt.subplots()
            ax.imshow(df_wc)
            st.pyplot(fig)

        # common word
        with col2:
            st.header('Most Common Word')
            most_word_df = work.common_word(selected_user, df)

            fig, ax = plt.subplots()
            ax.bar(most_word_df['Word'], most_word_df['Count'])
            plt.xticks(rotation='vertical')

            st.pyplot(fig)

        # emoji
        emoji_df = work.emoji_get(selected_user, df)
        st.title('Emoji')

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df['count'].head(), labels=emoji_df['emoji'].head(), autopct='%1.1f%%')
            st.pyplot(fig)

        # activity
        st.title('Activity Map')
        col1, col2 = st.columns(2)
        busy_day, busy_month = work.activity(selected_user, df)

        with col1:
            st.header('Most Busy day')
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='red')
            plt.xticks(rotation=45)
            st.pyplot(fig)

        with col2:
            st.header('Most Busy Month')
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='red')
            plt.xticks(rotation=45)
            st.pyplot(fig)

        # heatmap
        st.title('Weakly activity map')
        user_heatmap = work.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)
