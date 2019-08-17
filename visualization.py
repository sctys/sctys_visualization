import os
from plotly import tools
from plotly.offline import plot
import plotly.graph_objs as go
from visualization_setting import VisualizationSetting


class Visualization(VisualizationSetting):

    def __init__(self):
        self.reset_graph_object()

    def reset_graph_object(self):
        self.data = []
        self.layout = dict()

    def _set_graph_title(self, title='Title', x_title='x-title', y_title='y-title'):
        self.layout['title'] = title
        self.layout['xaxis'] = dict(title=x_title)
        self.layout['yaxis'] = dict(title=y_title)

    def _set_axis_range(self, axis, min, max):
        self.layout['{}axis'.format(axis)]['range'] = [min, max]

    def _additional_layout_options(self, **kwargs):
        self.layout.update(kwargs)

    def set_single_graph_layout(self, title_dict=None, x_range=None, y_range=None, z_range=None, **kwargs):
        if title_dict is not None:
            self._set_graph_title(**title_dict)
        if x_range is not None:
            self._set_axis_range('x', *x_range)
        if y_range is not None:
            self._set_axis_range('y', *y_range)
        if z_range is not None:
            self._set_axis_range('z', *z_range)
        self._additional_layout_options(**kwargs)

    def _scatter_trace_add(self, x_data, y_data, label, **kwargs):
        trace = go.Scattergl(x=x_data, y=y_data, name=label, **kwargs)
        self.data.append(trace)

    def _histogram_trace_add(self, x_data, label, **kwargs):
        trace = go.Histogram(x=x_data, name=label, **kwargs)
        self.data.append(trace)

    def time_series_plot(self, file_name, data, time_label, y_labels, labels=None, options_list=None, single_plot=True,
                         multiplot_options=None, title_dict=None, time_range=None, y_range=None, **layout_kwargs):
        self.reset_graph_object()
        if not isinstance(y_labels, list):
            y_labels = [y_labels]
        if labels is None:
            labels = y_labels
        if options_list is None:
            options_list = [{} for _ in range(len(y_labels))]
        x_data = data.loc[:, time_label].values
        y_data = [data.loc[:, y_label].values for y_label in y_labels]
        [self._scatter_trace_add(x_data, y, label, **options)
         for y, label, options in zip(y_data, labels, options_list)]
        if single_plot:
            self.plot_single_graph(file_name, title_dict, time_range, y_range, **layout_kwargs)
        else:
            if multiplot_options is None:
                multiplot_options = {'positions': None, 'n_row': None, 'n_col': None}
            self.plot_multiple_graph(file_name, **multiplot_options)

    def scatter_plot(self, file_name, data, x_labels, y_labels, labels=None, options_list=None, single_plot=True,
                     multiplot_options=None, title_dict=None, x_range=None, y_range=None, **layout_kwargs):
        self.reset_graph_object()
        if not isinstance(x_labels, list):
            x_labels = [x_labels]
        if not isinstance(y_labels, list):
            y_labels = [y_labels]
        n_row = 1
        n_col = 1
        if len(x_labels) == 1 and len(y_labels) == 1:
            if labels is None:
                labels = y_labels
        if len(x_labels) == 1 and len(y_labels) > 1:
            x_labels = [x_labels[0] for _ in range(len(y_labels))]
            if labels is None:
                labels = y_labels
            n_row = len(y_labels)
        elif len(x_labels) > 1 and len(y_labels) == 1:
            y_labels = [y_labels[0] for _ in range(len(x_labels))]
            if labels is None:
                labels = x_labels
            n_col = len(x_labels)
        if options_list is None:
            options_list = [{'mode': 'markers'} for _ in range(len(labels))]
        x_data = [data.loc[:, x_label].values for x_label in x_labels]
        y_data = [data.loc[:, y_label].values for y_label in y_labels]
        [self._scatter_trace_add(x, y, label, **options)
         for x, y, label, options in zip(x_data, y_data, labels, options_list)]
        if single_plot:
            self.plot_single_graph(file_name, title_dict, x_range, y_range, **layout_kwargs)
        else:
            if multiplot_options is None:
                multiplot_options = {'positions': None, 'n_row': n_row, 'n_col': n_col}
            self.plot_multiple_graph(file_name, **multiplot_options)

    def histogram_plot(self, file_name, data, labels, options_list=None, single_plot=True,
                       multiplot_options=None, title_dict=None, label_range=None, **layout_kwargs):
        self.reset_graph_object()
        if not isinstance(labels, list):
            labels = [labels]
        if options_list is None:
            options_list = [{} for _ in range(len(labels))]
        label_data = [data.loc[:, label].values for label in labels]
        [self._histogram_trace_add(x_data, label, **options)
         for x_data, label, options in zip(label_data, labels, options_list)]
        if single_plot:
            self.plot_single_graph(file_name, title_dict, label_range, **layout_kwargs)
        else:
            if multiplot_options is None:
                multiplot_options = {'positions': None, 'n_row': None, 'n_col': None}
            self.plot_multiple_graph(file_name, **multiplot_options)

    def scatter_matrix_plot(self, file_name, data, labels_list, options_dict=None, **layout_kwargs):
        self.reset_graph_object()
        dimensions_list = [dict(label=label, values=data.loc[:, label]) for label in labels_list]
        if options_dict is None:
            options_dict = {}
        options_dict = {**dict(diagonal=dict(visible=False), showupperhalf=False), **options_dict}
        self.data = [go.Splom(dimensions=dimensions_list, **options_dict)]
        self.plot_single_graph(file_name, **layout_kwargs)

    def mesh_plot(self, file_name, data, x_label, y_label, z_label, options_dict=None, title_dict=None, x_range=None,
                  y_range=None, z_range=None, **layout_kwargs):
        self.reset_graph_object()
        if options_dict is None:
            options_dict = {}
        options_dict = {**dict(colorbar=go.ColorBar(title=z_label)), **options_dict}
        self.data = [go.Mesh3d(x=data.loc[:, x_label].values, y=data.loc[:, y_label].values,
                               z=data.loc[:, z_label].values, **options_dict)]
        self.plot_single_graph(file_name, title_dict, x_range, y_range, z_range, **layout_kwargs)

    def heatmap_plot(self, file_name, pivot_data, options_dict=None, title_dict=None, **layout_kwargs):
        self.reset_graph_object()
        if options_dict is None:
            options_dict = {}
        self.data = [go.Heatmap(z=pivot_data.values, x=pivot_data.index, y=pivot_data.values, **options_dict)]
        self.plot_single_graph(file_name, title_dict, **layout_kwargs)

    def plot_single_graph(self, file_name, title_dict=None, x_range=None, y_range=None, z_range=None, **layout_kwargs):
        full_file_name = os.path.join(self.VISUAL_PATH, file_name)
        self.set_single_graph_layout(title_dict, x_range, y_range, z_range, **layout_kwargs)
        fig = dict(data=self.data, layout=self.layout)
        plot(fig, filename=full_file_name, auto_open=False)

    def plot_multiple_graph(self, file_name, positions=None, n_row=None, n_col=None):
        full_file_name = os.path.join(self.VISUAL_PATH, file_name)
        if n_row is None or n_col is None:
            n_row = len(self.data)
            n_col = 1
        if positions is None:
            positions = [(row + 1, col + 1) for row in range(n_row) for col in range(n_col)]
        fig = tools.make_subplots(rows=n_row, cols=n_col)
        [fig.append_trace(trace, *pos) for trace, pos in zip(self.data, positions)]
        plot(fig, filename=full_file_name, auto_open=False)
