from collections import Counter

import pandas as pd

from utils import make_plot


def main():
    # Load data
    file_name = '1628540489.csv'
    df = pd.read_csv(file_name)

    # Plot over time.
    # df['date'] = pd.to_datetime(df['Date'])
    # df.set_index('date', inplace=True)
    # df.groupby(pd.Grouper(freq='Y'))['Member'].count().plot()

    # Count how many times each member has made a hole in one.
    x = df['Member'].value_counts()

    # Add zero to make the colors of the bars in the plot match the colors of the bars of other plots.
    index, values = zip(*Counter(x).items())
    index += (0,)
    values += (0,)

    # Divide by 1000 to make axis labels smaller.
    values = list(map(lambda a: a / 1000, values))

    df2 = pd.DataFrame({'n': index, 'y': values})
    df2 = df2[df2['n'] < 10]  # ignore the odd one that has more than 10 holes in one
    df2 = df2.sort_values(by='n', ascending=True)

    # make the plot
    make_plot(
        df=df2,
        title='Figuur 4, Empirische verdeling Bolsholeinone.com',
        file_name='plots/fig4.svg',
        x_label='aantal holes in one',
        y_label='aantal golfers x1.000',
        cutoff_numbers=(1,),
        use_limit=False,
    )


if __name__ == '__main__':
    main()
