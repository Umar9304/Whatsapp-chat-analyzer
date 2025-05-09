# Whatsapp-chat-analyzer
Running the Project:
- To run the project, follow these steps:
    - Install the required dependencies:
        pip install: pandas, streamlit, wordcloud, matplotlib, seaborn, emoji, urlextract
    - Launch the Streamlit app:
        streamlit run analyzer.py
    - Upload a WhatsApp chat file:  
       Once the app is running, open your browser and upload your WhatsApp chat export file. Select a user from the sidebar to view their analysis.
    - Explore the analysis:  
       Interact with various visualizations to explore message statistics, word clouds, emoji usage, and activity trends.

Tools & Technologies Used:
  - Python: The primary programming language used to build the project.
  - Streamlit: For creating the interactive web interface where users can upload chat data and view analysis results.
  - Pandas: For data manipulation and processing.
  - Matplotlib & Seaborn: For data visualization (e.g., bar charts, pie charts, heatmaps).
  - WordCloud: To generate word clouds from the messages.
  - URLExtract: To extract URLs from the chat messages.
  - Emoji: For detecting and analyzing emojis in the messages.

NOTE: the regular expresion used in my code is for txt formate:
 - day/month/year(last 2 digit), hour(12):minute (AM/PM) - User name: message
 - change the regular expresions based on your txt data
 - here is one for 24 hr formate :
   - pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d(2)\s-\s' #Change in preprocessing.py line 6
   - entry = re.split('([\w\W]+?):\s',message) #Change in preprocessing.py line 18
