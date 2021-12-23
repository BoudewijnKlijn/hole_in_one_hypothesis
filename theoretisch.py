import math

import numpy as np
import pandas as pd

from utils import make_plot


def geometric(p: float, k: int) -> float:
    """Chance decreases with constant factor p."""
    return (1-p) ** k * p


def poisson(lambda_: float, k: int) -> float:
    return lambda_ ** k * np.exp(-lambda_) / math.factorial(k)


def main():
    df = pd.DataFrame({'n': list(range(10))})

    # Geometric
    for i, p in enumerate([0.5, 0.9], start=1):
        df['y'] = df['n'].transform(lambda x: geometric(p, x)) * 100
        make_plot(
            df=df,
            title=f'Figuur {i}, Geometrische (p={p:.1f}) verdeling',
            file_name=f'plots/fig{i}.svg',
        )

    # Poisson
    lambda_ = 0.2
    df['y'] = df['n'].transform(lambda x: poisson(lambda_, x)) * 100
    make_plot(
        df=df,
        title=f'Figuur 3, Poisson (λ={lambda_:.1f}) verdeling',
        file_name='plots/fig3.svg',
    )


if __name__ == '__main__':
    main()
