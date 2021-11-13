import pandas as pd
import numpy as np
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components


def spit_html_embedding(statistics_path='Data Files/spatial.csv', save_locally=True):
    """This module return  a script and HTML wrapped div tag created from a csv file
        Returns :-
        1. plot_script
        2. plot_div

        use these two along with js_resources and css_resources to embed figure into HTML webpage
    """
    my_dataframe = pd.read_csv(statistics_path, sep=',')
    source = ColumnDataSource(my_dataframe)
    fig = figure(plot_height=600, plot_width=720, tooltips=[('Person in frame ','@Person Count'), ('Frame active ','@Activity Indicator')])
    fig.line(x="Frame Number", y="Person Count", source=source, legend_label='Person Count')
    fig.line(x="Frame Number", y="Activity Indicator", source=source, color='red', legend_label='Activity Indicator')
    fig.legend.location = "top_left"
    fig.legend.title = "Objects Identified"
    fig.legend.background_fill_color = "navy"
    fig.legend.background_fill_alpha = 0.2
    fig.xaxis.axis_label = "Frame Number"
    fig.yaxis.axis_label = "Video Statistics"
    if save_locally:
        output_file("static/Graphs/graph.html") # to create a html webpage of a graph and store it locally
    else:
        pass
    script, div = components(fig)
    return script, div
    
    