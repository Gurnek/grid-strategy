from bokeh.layouts import layout, Spacer
from bokeh.io import show, output_file


class JustifiedGrid:
    def __init__(self, nrows, grid_arrangement):
            self.plots = [[]]
            self.grid_arrangement = grid_arrangement
            self.current_row = 0
            self.nrows = nrows

    def add_plot(self, plot):
        self.plots[self.current_row].append(plot)
        if len(self.plots[self.current_row]) == self.grid_arrangement[self.current_row]:
            self.plots.append([])
            self.current_row += 1
            assert self.current_row <= self.nrows, "Error: More graphs added to layout than previously specified."

    def add_plots(self, plot_list):
        for plot in plot_list:
            self.add_plot(plot)

    def output_dest(self, file):
        output_file(file)

    def show_plot(self):
        l = layout(self.plots, sizing_mode="stretch_width")
        show(l)


class AlignedGrid:
    def __init__(self, nrows, ncols, grid_arrangement, alignment):
        self.plots = [[]]
        self.grid_arrangement = grid_arrangement
        self.alignment = alignment
        self.current_row = 0
        self.nrows = nrows

    def add_plot(self, plot):
        self.plots[self.current_row].append(plot)
        if len(self.plots[self.current_row]) == self.grid_arrangement[self.current_row]:
            self.plots.append([])
            self.current_row += 1
        assert self.current_row <= self.nrows, "Error: More graphs added to the layout than previously specified."

    def add_plots(self, plots):
        for plot in plots:
            self.add_plot(plot)

    def output_dest(self, file):
        output_file(file)
    
    def show_plot(self):
        for row in self.plots:
            if len(row) == max(self.grid_arrangement):
                continue
            else:
                if self.alignment == "left":
                    row.append(Spacer())
                elif self.alignment == "right":
                    row.insert(0, Spacer())
                elif self.alignment == "center":
                    row.append(Spacer())
                    row.insert(0, Spacer())
        l = layout(self.plots, sizing_mode="scale_both")
        show(l)

class Bokeh:
    
    def __init__(self, alignment):
        self.alignment = alignment

    def _justified(self, nrows, grid_arrangement):
        return JustifiedGrid(nrows, grid_arrangement)

    def _ragged(self, nrows, ncols, grid_arrangement):
        return AlignedGrid(nrows, ncols, grid_arrangement, self.alignment)