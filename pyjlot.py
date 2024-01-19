#!/usr/bin/env python3

import json
import matplotlib.pyplot
import sys

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

def gen_plot(plot_file):
	legend = []
	if not 'curves' in plot_file:
		eprint('Input file does not contain any curves')
		return None

	for item in plot_file['curves']:
		if not 'data_points' in item:
			eprint('Item has no data points')
			return None

		data_points = item['data_points']

		if not 'x' in data_points:
			eprint('There are no x values in data_points')
			return None

		if not 'y' in data_points:
			eprint('There are no y values in data_points')
			return None

		x = data_points['x']
		y = data_points['y']

		if len(x) != len(y):
			eprint('x and y has different lengths')
			return None

		legend.append(item.get('label', ''))
		matplotlib.pyplot.plot(x, y)

	if all(map(lambda v: v=='', '')):
		matplotlib.pyplot.legend(legend)


	if 'axes_config' in plot_file:
		axes_config = plot_file['axes_config']

		ratio = axes_config.get('ratio', 'independent')
		if ratio == 'equal':
			matplotlib.pyplot.axis('equal')
		elif ratio == 'independent':
			matplotlib.pyplot.axis('auto')
		elif ratio == 'scaled':
			matplotlib.pyplot.axis('scaled')
		else:
			eprint('Usupported axis ratio %s'%ratio)
			return None

		if 'x' in axes_config:
			x = axes_config['x']

			x_scale = x.get('scale', {})
			x_scale_type = x_scale.get('type', 'lin')
			if x_scale_type == 'lin':
				matplotlib.pyplot.xscale('linear')

			elif x_scale_type == 'log':
				options = x_scale.get('options', {})
				log_base = options.get('base', 10)
				matplotlib.pyplot.xscale('log', base = log_base)

			else:
				eprint('Unsupported scale %s'%x_scale_type)
				return None

			if 'grid_lines' in x:
				matplotlib.pyplot.grid(axis = 'x')

			if 'label' in x:
				matplotlib.pyplot.xlabel(x['label'])

			if 'limits' in x:
				limits = x['limits']

				if 'min' in limits:
					matplotlib.pyplot.xlim(left = limits['min'])

				if 'max' in limits:
					matplotlib.pyplot.xlim(right = limits['max'])

		if 'y' in axes_config:
			y = axes_config['y']
			y_scale = y.get('scale', {})
			y_scale_type = y_scale.get('type', 'lin')
			if y_scale_type == 'lin':
				matplotlib.pyplot.xscale('linear')

			elif y_scale_type == 'log':
				options = y_scale.get('options', {})
				log_base = options.get('base', 10)
				matplotlib.pyplot.yscale('log', base = log_base)

			else:
				eprint('Unsupported scale %s'%y_scale_type)
				return None

			if 'grid_lines' in y:
				matplotlib.pyplot.grid(axis = 'y')

			if 'label' in y:
				matplotlib.pyplot.ylabel(y['label'])

			if 'limits' in y:
				limits = y['limits']

				if 'min' in limits:
					matplotlib.pyplot.ylim(bottom = limits['min'])

				if 'max' in limits:
					matplotlib.pyplot.ylim(top = limits['max'])

	return matplotlib.pyplot.gcf()

if __name__ == '__main__':
	if len(sys.argv) < 2:
		plot_file = json.load(sys.stdin)
	else:
		with open(sys.argv[1], 'r') as input:
			plot_file = json.load(input)

	gen_plot(plot_file)
	matplotlib.pyplot.show()
