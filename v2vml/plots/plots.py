import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plots():
    sns.set()
    plot_accuracies()
    plot_details()


def plot_accuracies():

    df = pd.read_csv('./data/plots/plot_data/accuracies.csv', index_col=0)

    # sns.lineplot will plot columns as lines, but we want to plot the rows as lines
    # tranpose the DataFrame so that the rows become the columns
    df = df.T

    # Without using the sort parameter, the labels will be sorted and incorrectly plot the data
    plot = sns.lineplot(data=df, sort=False)
    plot.set_title('Average Model Accuracy')
    plot.set(xlabel='Sample Size (epochs)', ylabel='Accuracy')
    figure = plot.get_figure()
    figure.savefig('./data/plots/plot_img/accuracy_plot.png')

    # display the figure
    plt.show()


def plot_details():

    # mislabelled as percentages
    df = pd.read_csv('./data/plots/plot_data/svm_labelled_as.csv')
    plot = sns.catplot(x='Sample Size (epochs)', y='Percent', hue='Labelled', col='Sample Type', data=df, kind='bar', height=5, aspect=0.7)
    plot.fig.savefig('./data/plots/plot_img/svm_labelled_as.png')
    plt.show()
