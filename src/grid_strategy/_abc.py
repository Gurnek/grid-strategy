"""Proof of concept code for MEP 30: Automatic subplot management."""
import itertools as it

from abc import ABCMeta, abstractmethod

from matplotlib import gridspec
import matplotlib.pyplot as plt
import numpy as np

from .backends.mtpltlib import Matplotlib
from .backends.bkh import Bokeh


class GridStrategy(metaclass=ABCMeta):
    """
    Static class used to compute grid arrangements given the number of subplots
    you want to show. By default, it goes for a symmetrical arrangement that is
    nearly square (nearly equal in both dimensions).
    """

    def __init__(self, alignment="center", backend="matplotlib"):
        self.alignment = alignment
        self.supported_backends = ["matplotlib", "bokeh"]
        self.library = None

        assert (
            backend in self.supported_backends
        ), f"Library {backend} is not a supported backend."
        if backend == "matplotlib":
            try:
                import matplotlib
            except ImportError:
                print(
                    "matplotlib not installed. Please install it to use it with grid_strategy."
                )
            self.library = Matplotlib(alignment=self.alignment)

        elif backend == "bokeh":
            try:
                import bokeh
            except ImportError:
                print(
                    "Bokeh is not installed. Please install it to use it with grid_strategy."
                )
            self.library = Bokeh(alignment=self.alignment)

        # elif backend == "plotly":
        #     try:
        #         import plotly
        #     except ImportError:
        #         print("plotly not installed. Please install it to use it with grid_strategy.")
        #     self.library = Plotly(alignment=self.alignment)

    def get_grid(self, n):
        """  
        Return a list of axes designed according to the strategy.
        Grid arrangements are tuples with the same length as the number of rows,
        and each element specifies the number of colums in the row.
        Ex (2, 3, 2) leads to the shape
             x x 
            x x x
             x x
        where each x would be a subplot.
        """

        if n < 0:
            raise ValueError
        grid_arrangement = self.get_grid_arrangement(n)
        return self.get_figures(grid_arrangement)

    @classmethod
    @abstractmethod
    def get_grid_arrangement(cls, n):  # pragma: nocover
        pass

    def get_figures(self, grid_arrangement):
        nrows = len(grid_arrangement)
        ncols = max(grid_arrangement)

        # If it has justified alignment, will not be the same as the other alignments
        if self.alignment == "justified":
            return self.library._justified(nrows, grid_arrangement)
        else:
            return self.library._ragged(nrows, ncols, grid_arrangement)
