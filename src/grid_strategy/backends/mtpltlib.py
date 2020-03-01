from matplotlib import gridspec
import matplotlib.pyplot as plt
import numpy as np

class Matplotlib:

    def __init__(self, alignment="center"):
        self.alignment = alignment

    def _justified(self, nrows, grid_arrangement):
        ax_specs = []
        num_small_cols = np.lcm.reduce(grid_arrangement)
        gs = gridspec.GridSpec(
            nrows, num_small_cols, figure=plt.figure(constrained_layout=True)
        )
        for r, row_cols in enumerate(grid_arrangement):
            skip = num_small_cols // row_cols
            for col in range(row_cols):
                s = col * skip
                e = s + skip

                ax_specs.append(gs[r, s:e])
        return ax_specs

    def _ragged(self, nrows, ncols, grid_arrangement):
        if len(set(grid_arrangement)) > 1:
            col_width = 2
        else:
            col_width = 1

        gs = gridspec.GridSpec(
            nrows, ncols * col_width, figure=plt.figure(constrained_layout=True)
        )

        ax_specs = []
        for r, row_cols in enumerate(grid_arrangement):
            # This is the number of missing columns in this row. If some rows
            # are a different width than others, the column width is 2 so every
            # column skipped at the beginning is also a missing slot at the end.
            if self.alignment == "left":
                # This is left-justified (or possibly full justification)
                # so no need to skip anything
                skip = 0
            elif self.alignment == "right":
                # Skip two slots for every missing plot - right justified.
                skip = (ncols - row_cols) * 2
            else:
                # Defaults to centered, as that is the default value for the class.
                # Skip one for each missing column - centered
                skip = ncols - row_cols

            for col in range(row_cols):
                s = skip + col * col_width
                e = s + col_width

                ax_specs.append(gs[r, s:e])

        return ax_specs




# class Plotly:
#     from plotly.subplots import make_subplots
#     import numpy as np

#     def __init__(self, alignment="center"):
#         self.alignment = alignment

#     def _justified(self, nrows, grid_arrangement):
#         num_small_cols = int(self.np.lcm.reduce(grid_arrangement))

#         specs = []

#         for row_cols in grid_arrangement:
#             width = num_small_cols // row_cols

#             row = []
#             for _ in range(row_cols):
#                 row.append({"colspan":width})
#                 row.extend([None]*(width-1))
#             specs.append(row)

#         fig = self.make_subplots(
#             nrows,
#             num_small_cols,
#             specs = specs
#         )
#         return fig, grid_arrangement

#     def _ragged(self, nrows, ncols, grid_arrangement):
#         pass