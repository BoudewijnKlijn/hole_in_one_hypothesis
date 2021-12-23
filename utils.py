import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def make_plot(
        df: pd.DataFrame,
        title: str,
        file_name: str,
        x_label: str = 'aantal holes in one',
        y_label: str = 'percentage golfers',
        cutoff_numbers=(0, 1),
        use_limit=True,
) -> None:
    palette = 'colorblind'
    colors = sns.color_palette(palette)
    fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
    if use_limit:
        plt.ylim([0, 100])

    df.plot.bar(x='n', y='y', rot=0, ax=ax1, color=colors, legend=False)

    ax1.set_xlabel(x_label)
    ax1.set_ylabel(y_label)

    cols = list()
    for cutoff_number in cutoff_numbers:
        single = np.array([cutoff_number])
        combine = np.arange(cutoff_number + 1, 10)

        equal_col = f'exact\n{cutoff_number}'
        greater_combined_col = f'meer\ndan {cutoff_number}'

        cols.extend([equal_col, greater_combined_col])

        equal_mask = df['n'].isin(single)
        df.loc[equal_mask, equal_col] = df.loc[equal_mask, 'y']

        greater_combined_mask = df['n'].isin(combine)
        df.loc[greater_combined_mask, greater_combined_col] = df.loc[greater_combined_mask, 'y']

    df[cols].T.plot(kind='bar', stacked=True, ax=ax2, color=colors, rot=0, legend=False)

    plt.suptitle(title)
    fig.savefig(file_name)
