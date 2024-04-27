from dash import html
from wordcloud import WordCloud
import io
import base64
import plotly.graph_objs as go

def generate_wordcloud_image(topic_counts):
    # Generate word cloud from topic counts
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(topic_counts)

    # Convert word cloud to image
    img = io.BytesIO()
    wordcloud.to_image().save(img, format='PNG')
    img_str = base64.b64encode(img.getvalue()).decode()

    # Display the word cloud image
    return html.Img(src='data:image/png;base64,{}'.format(img_str))

def wordcloud_layout(topic_counts):
    wordcloud_image = generate_wordcloud_image(topic_counts)
    return html.Div([
        html.H2("Word Cloud of Topics Tweeted About"),
        wordcloud_image
    ])

def plot_topic_likes_views(topic_likes, topic_views):
    # Extract topics and their respective average likes and views
    topics = list(topic_likes.keys())
    avg_likes = list(topic_likes.values())
    avg_views = list(topic_views.values())

    # Create traces
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=topics,
        y=avg_likes,
        name='Average Likes',
        marker_color='red'
    ))
    fig.add_trace(go.Bar(
        x=topics,
        y=avg_views,
        name='Average Views',
        marker_color='blue'
    ))

    # Update layout
    fig.update_layout(
        title='Average Likes and Views per Topic',
        xaxis=dict(title='Topics'),
        yaxis=dict(title='Count'),
        barmode='group'
    )

    return fig

def visualize_trending_hashtags(hashtag_counts):
    # Sort the hashtags by frequency
    sorted_hashtags = sorted(hashtag_counts.items(), key=lambda x: x[1], reverse=True)
    top_hashtags = sorted_hashtags[:10]  # Get the top 10 hashtags

    # Extract hashtags and their frequencies for plotting
    hashtags, frequencies = zip(*top_hashtags)

    # Create a horizontal bar plot
    data = [go.Bar(
        x=frequencies,
        y=hashtags,
        orientation='h',
        marker=dict(color='skyblue')
    )]

    # Define layout
    layout = go.Layout(
        title=f'Top {len(hashtags)} Trending Hashtags',
        xaxis=dict(title='Frequency'),
        yaxis=dict(title='Hashtags'),
        margin=dict(l=150, r=50, t=50, b=50),  # Adjust margins for better layout
    )

    # Create figure
    fig = go.Figure(data=data, layout=layout)
    return fig

def visualize_sentiment_distribution(compound_scores):
    # Create a histogram plot
    data = [go.Histogram(
        x=compound_scores,
        xbins=dict(
            start=-1,
            end=1,
            size=0.1
        ),
        marker=dict(color='skyblue'),
        opacity=0.7
    )]

    # Define layout
    layout = go.Layout(
        title='Distribution of Compound Sentiment Scores',
        xaxis=dict(title='Sentiment Score', tickvals=[-1, -0.5, 0, 0.5, 1], ticktext=['Negative (-1)', '-0.5', 'Neutral (0)', '0.5', 'Positive (1)']),
        yaxis=dict(title='Frequency'),
        bargap=0.1,
        bargroupgap=0.1,
        margin=dict(l=50, r=50, t=50, b=50),  # Adjust margins for better layout
    )

    # Create figure
    fig = go.Figure(data=data, layout=layout)
    return fig