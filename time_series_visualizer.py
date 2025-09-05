import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.ticker import MaxNLocator
from pandas.plotting import register_matplotlib_converters
import numpy as np


if not hasattr(np, 'float'):
    np.float = float #fix for error that was happening
    
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date')

# Clean data
low = df['value'].quantile(0.025)
high = df['value'].quantile(0.975)
df = df[(df['value'] >= low) & (df['value'] <= high)]


def draw_line_plot():
    fig, ax = plt.subplots(figsize = (12, 5))


    ax.plot(df.index, df['value'], linestyle = '-', color = 'red')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.xaxis.set_major_locator(MaxNLocator(nbins=8)) #gets 8 even dates just like figure 1
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    df_bar = df.copy()
    df_bar.index = pd.to_datetime(df_bar.index)
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month
    
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack() #unstack used to have months as columns
    
    fig, ax = plt.subplots(figsize = (12, 5))
    
    df_bar.plot( #using df_bar.plot instead of ax.plot because by using ax.plot need to do everything manual
        kind = 'bar',
        ax = ax
    )

    ax.set_ylabel('Average Page Views')
    ax.set_xlabel('Years')
    ax.legend(title='Months')
    
    legend = ax.get_legend()
    labels = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
    for text, label in zip(legend.get_texts(), labels):
        text.set_text(label) #sets months as names instead of numbers


    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['date'] = pd.to_datetime(df_box['date']) #should have probably done that in df, but 
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    
    labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Draw box plots (using Seaborn)
    
    fig, ax = plt.subplots(1, 2, figsize = (12, 5)) #1 row, 2 columns of plots
    #Year box plot
    sns.boxplot(x = df_box['year'], y = df_box['value'], ax = ax[0])
    ax[0].set_title('Year-wise Box Plot (Trend)')
    ax[0].set_xlabel('Year')
    ax[0].set_ylabel('Page Views')
    
    #Months box plot
    sns.boxplot(x = df_box['month'], y = df_box['value'], order = labels, ax = ax[1])
    ax[1].set_title('Month-wise Box Plot (Seasonality)')
    ax[1].set_xlabel('Month')
    ax[1].set_ylabel('Page Views')




    fig.tight_layout()
    fig.savefig('box_plot.png')
    return fig
