import dash
from dash import dcc, html, Input, Output, callback
import requests
from pages.user_analysis_graph_layouts import wordcloud_layout, plot_topic_likes_views, visualize_trending_hashtags, visualize_sentiment_distribution
import dash_bootstrap_components as dbc
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize Dash app
dash.register_page(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define layout of the app
layout = html.Div([
    html.H3("User Analysis", style={"margin-top": "10px", "margin-bottom": "10px"}),
    html.Div([
        html.Div([
            html.Label("Enter Username:", className="form-label"),
            dcc.Input(id='username-input', type='text', value='', className="form-control", style={'width': '225px'}),
        ], className="col-8", style={'width': '250px'}),
        html.Div([
            html.Button('Submit', id='submit-button', n_clicks=0, className="btn btn-primary"),
        ], className="col-4 d-flex align-items-end"),
    ], className="row mb-3"),
    html.Div(id='tabs-content')
])

# Callback to generate tabs content
@callback(
    Output('tabs-content', 'children'),
    [Input('submit-button', 'n_clicks')],
    [dash.dependencies.State('username-input', 'value')]
)
def generate_tabs_content(n_clicks, username):
    if n_clicks > 0:
        tweet_data = get_user_tweets(username)
        # Analyze topics of tweets and count their occurrence
        topic_counts = {}
        topic_likes = {}
        topic_views = {}
        for tweet_text, likes, views in tweet_data:
            analysis = analyze_tweet_topics(tweet_text)
            if "topics" in analysis:
                for topic in analysis["topics"]:
                    if topic["confidence"] < 0.5:
                        break
                    if topic["label"] in topic_counts:
                        topic_counts[topic["label"]] += 1
                        topic_likes[topic["label"]].append(likes)
                        topic_views[topic["label"]].append(views)
                    else:
                        topic_counts[topic["label"]] = 1
                        topic_likes[topic["label"]] = [likes]
                        topic_views[topic["label"]] = [views]
        
        for topic, _ in topic_counts.items():
            topic_likes[topic] = sum(topic_likes[topic])/len(topic_likes[topic])
            topic_views[topic] = sum(topic_views[topic])/len(topic_views[topic])
        
        
        print("Topics usually tweeted about by", username, ":")
        for topic, count in topic_counts.items():
            print(topic, ":", count)
        # Count hashtags used in tweets
        tweet_texts = [tweet_text for tweet_text, _, _ in tweet_data]
        hashtag_counts = count_hashtags(tweet_texts)
        # Analyze sentiment of tweets
        compound_scores = []
        for text in tweet_texts:
            score = analyze_tweet_sentiment(text)
            compound_scores.append(score)        
        # Create content for each tab
        tabs_content = [
            dbc.Tab(label='Word Cloud of Tweeted Topics', tab_id='wordcloud', children=[wordcloud_layout(topic_counts)]),
            dbc.Tab(label='Topic-wise Likes and Views', tab_id='likes_views', children=[dcc.Graph(figure=plot_topic_likes_views(topic_likes, topic_views))]),
            dbc.Tab(label='Top Hashtags Used', tab_id='trending_hashtags', children=[dcc.Graph(figure=visualize_trending_hashtags(hashtag_counts))]),
            dbc.Tab(label='Tweet Sentiments', tab_id='sentiment', children=[dcc.Graph(figure=visualize_sentiment_distribution(compound_scores))])
        ]

        # Return the tabs content
        return dbc.Tabs(tabs_content, id="tabs", active_tab="wordcloud")
    else:
        return None

# Function to fetch user tweets
def get_user_tweets(username):
    url = "https://twitter154.p.rapidapi.com/user/tweets"
    querystring = {
        "username": username,
        "limit": "40",
        "include_replies": "false"
    }
    headers = {
        "X-RapidAPI-Key": "a4be85bfcfmsh7bb496430bd6f61p1012d5jsn93766042a3be",
        "X-RapidAPI-Host": "twitter154.p.rapidapi.com"
    }
    responses = requests.get(url, headers=headers, params=querystring).json()

    tweet_data = []
    for response in responses['results']:
        tweet_text = response['text']
        likes = response.get('favorite_count', 0)
        views = response.get('views', 0)
        tweet_data.append((tweet_text, likes, views))

    url = "https://twitter154.p.rapidapi.com/user/tweets/continuation"
    querystring = {
        "continuation_token": responses["continuation_token"],
        "username": username, "limit": "40",
        "include_replies": "false"
    }
    responses = requests.get(url, headers=headers, params=querystring).json()
    for response in responses['results']:
        tweet_text = response['text']
        likes = response.get('favorite_count', 0)
        views = response.get('views', 0)
        tweet_data.append((tweet_text, likes, views))
    print(f"Fetched {len(tweet_data)} tweets for user {username}")
    return tweet_data

# Function to analyze tweet topics
def analyze_tweet_topics(tweet_text):
    url = "https://twitter154.p.rapidapi.com/ai/topic-classification"
    querystring = {"text": tweet_text} 
    headers = {
        "X-RapidAPI-Key": "a4be85bfcfmsh7bb496430bd6f61p1012d5jsn93766042a3be",
        "X-RapidAPI-Host": "twitter154.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

def extract_hashtags(tweet_text):
    # Regular expression to match hashtags
    hashtags = re.findall(r'#(\w+)', tweet_text)
    return hashtags

def count_hashtags(tweet_texts):
    hashtag_counts = {}
    for text in tweet_texts:
        hashtags = extract_hashtags(text)
        for hashtag in hashtags:
            if hashtag in hashtag_counts:
                hashtag_counts[hashtag] += 1
            else:
                hashtag_counts[hashtag] = 1
    return hashtag_counts

def analyze_tweet_sentiment(tweet_text):
    # Function to analyze sentiment of a tweet using VADER
    analyzer = SentimentIntensityAnalyzer()
    sentiment_scores = analyzer.polarity_scores(tweet_text)
    compound_score = sentiment_scores['compound']
    return compound_score