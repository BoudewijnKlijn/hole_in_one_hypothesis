import pickle
import time
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from Levenshtein import distance


def calc_distances(df):
    unique_names = list(set(df['Member'].dropna()))

    distances = np.zeros((len(unique_names), len(unique_names)), dtype=np.uint8)
    for i, name1 in enumerate(unique_names):
        if i % 1000 == 0:
            print(i)
        for j, name2 in enumerate(unique_names):
            if j <= i:
                continue
            distances[i, j] = distance(name1, name2)

    timestamp = int(time.time())
    with open(f'distances_{timestamp}.obj', 'wb') as fh:
        pickle.dump(distances, fh)

    with open(f'unique_names_{timestamp}.obj', 'wb') as fh:
        pickle.dump(unique_names, fh)


def get_file(filename):
    with open(filename, 'rb') as fh:
        d = pickle.load(fh)
    return d


def get_close_names(distances, unique_names, diff=1):
    rows, cols = np.where(distances == diff)
    return [(unique_names[r], unique_names[c]) for r, c in zip(rows, cols)]


def main():
    file = '1628540489.csv'
    df = pd.read_csv(file)

    print(df.info())

    x = df['Member'].value_counts()
    Counter(x)

    # plt.figure()
    sns.histplot(x)
    # x.hist()
    plt.show()

    # calc_distances(df)

    distances = get_file('distances_1628592725.obj')
    unique_names = get_file('unique_names_1628592725.obj')

    close_names = get_close_names(distances=distances, unique_names=unique_names, diff=1)
    # prevent complete families from mapping to a single person
    close_names2 = [(name1, name2) for name1, name2 in close_names if name1[1:] != name2[1:]]

    mapping = dict(zip(unique_names, [[un] for un in unique_names]))

    for n1, n2 in close_names2:
        map_to = mapping.get(n1)[0]
        mapping[n2] = [map_to]
        mapping[map_to] += [n2]

    mapping2 = dict(zip(mapping.keys(), [v[0] for v in mapping.values()]))

    df['Member2'] = df['Member'].map(mapping2)

    df2 = df.drop_duplicates(subset=['Member2', 'Date'])

    df2.to_csv('member2.csv')

    # x = df2['Member2'].value_counts()
    # c = Counter(x)
    #
    # y, x = c.values(), c.keys()
    #
    # data = pd.DataFrame({'x': x, 'y': y})
    #
    # sns.barplot(data, x='x', y='y')
    # plt.ylabel('# players')
    # plt.xlabel('# holes in one / player')
    # plt.show()


if __name__ == '__main__':
    main()
