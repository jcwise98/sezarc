import argparse
import matplotlib.pyplot as plt
import pandas as pd


# Filters a pandas 'data_frame' for values with the date between 'start' and 'end'
# date_column is the name of the column storing the date (default 'Date')
# Returns the filtered data frame. If no start and end is specified returns the original data frame
def filter_date(data_frame, start=None, end=None, date_column='Date'):
    if start and end:
        return data_frame[(data_frame[date_column] > start) & (data_frame[date_column] < end)]
    else:
        return data_frame


# Gets the frequencies of each unique value for the 'column' inside of the given 'data_frame'
# Returns the names, and frequencies
def create_frequency_data(data_frame, column):
    x = data_frame[column].value_counts().index
    y = data_frame[column].value_counts()
    return x, y


# Filters the given data frame with entries only between start and end
# Creates a frequency bar plot and saves it with the given 'output' name
def create_frequency_figure(data_frame, column, start, end, output):
    df = filter_date(data_frame, start, end)
    title = '%s (%s to %s)' % (column, start, end) if start and end else column
    x, y = create_frequency_data(df, column)
    fig, ax = plt.subplots()
    bars = plt.bar(x, y)
    plt.title(title)
    plt.xlabel(column)
    plt.ylabel("Frequency")
    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height, '%d' % int(height), ha='center', va='bottom')

    fig.savefig(output, bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create a graph of data frequencies, filterable by date')
    parser.add_argument('file', type=str, help='the path to the excel file')
    parser.add_argument('column', type=str, help='the column name to collect data from in the excel file')
    parser.add_argument('output', type=str, help='the path to the output image (default ./graph.png)')
    parser.add_argument('--start', type=str, help='the start date in the format: (d/m/y)')
    parser.add_argument('--end', type=str, help='the end date in the format: (d/m/y)')
    args = parser.parse_args()

    data = pd.read_excel(args.file)
    create_frequency_figure(data, args.column, args.start, args.end, args.output)
    print(args.output, "successfully generated.")
