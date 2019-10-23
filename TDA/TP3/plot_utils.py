
from matplotlib import rcParams

PPI = 72.0

class PlotData:

    def __init__(self, ax):
        self.ax = ax

    @property
    def xticks(self):
        return self.ax.get_xticks()

    @property
    def yticks(self):
        return self.ax.get_yticks()

    @xticks.setter
    def xticks(self, ticks):
        self.ax.set_xticks(ticks)

    @yticks.setter
    def yticks(self, ticks):
        self.ax.set_yticks(ticks)

    @property
    def ticks(self):
        return self.xticks + self.yticks

    @ticks.setter
    def ticks(self, ticks):
        if ticks:
            self.xticks = ticks[:2]
            self.yticks = ticks[2:]
            return
        self.xticks = []
        self.yticks = []

    @property
    def xlim(self):
        return self.ax.get_xlim()

    @xlim.setter
    def xlim(self, xlim):
        self.ax.set_xlim(xlim)

    @property
    def ylim(self):
        return self.ax.get_ylim()

    @ylim.setter
    def ylim(self, ylim):
        self.ax.set_ylim(ylim)

    @property
    def lim(self):
        return self.xlim + self.ylim

    @lim.setter
    def lim(self, lim):
        self.xlim = lim[:2]
        self.ylim = lim[2:]

    @property
    def width(self):
        return self._width


    @property
    def fig(self):
        return self.ax.get_figure()

    @property
    def axes_width(self):
        return self.ax.get_position().width

    @axes_width.setter
    def axes_width(self, new_width):
        pos = self.ax.get_position()
        self.ax.set_position((pos.xmin, pos.ymin, new_width, pos.height))

    @property
    def axes_height(self):
        return self.ax.get_position().height

    @axes_height.setter
    def axes_height(self, new_height):
        pos = self.ax.get_position()
        self.ax.set_position((pos.xmin, pos.ymin, pos.width, new_height))

    @property
    def axes_size(self):
        return self.axes_width, self.axes_height

    @axes_size.setter
    def axes_size(self, new_size):
        new_width, new_height = new_size
        pos = self.ax.get_position()
        self.ax.set_position((pos.xmin, pos.ymin, new_width, new_height))

    def center_axes(self):
        pos = self.ax.get_position()
        xmin, ymin = (1 - pos.width)/2, (1 - pos.height)/2
        self.ax.set_position((xmin, ymin, pos.width, pos.height))

    @property
    def height_in_points(self):
        return self.fig.get_figheight()*self.axes_height*PPI

    @property
    def width_in_points(self):
        return self.fig.get_figwidth()*self.axes_width*PPI

    @property
    def marker_radius(self):
        return rcParams['lines.markersize']/2

    def clean_plot_lines(self):
        while self.ax.lines:
            line = self.ax.lines[0]
            line.remove()
            del line

    def clean_collections(self):
        while self.ax.collections:
            collection = self.ax.collections[0]
            collection.remove()
            del collection

    def clean_plot(self, which='all'):
        if which == 'all':
            self.clean_plot_lines()
            self.clean_collections()
        elif which == 'lines':
            self.clean_plot_lines()

