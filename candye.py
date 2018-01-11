import collections
import logging
import math
import random


colors = {'blue', 'green', 'purple', 'red', 'yellow'}

Results = collections.namedtuple('Results', ['mean', 'stdev', 'min', 'max'])

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def get_initial_count():
	return random.randint(3, 6)

def get_initial_candies():
	candies = {color: 0 for color in colors}
	initial_colors = draw(get_initial_count())
	for color in initial_colors:
		candies[color] += 1
	return candies

def draw(n=1):
	color_list = list(colors)
	return [random.choice(color_list) for _ in range(n)]

def draw_one():
	return draw()[0]

def get_paired_color(candies):
	return next((color for color, count in candies.items() if count >= 2), None)

def done(candies):
	if all(count == 0 for count in candies.values()):
		return True		# nothing left
	if all(count == 1 for count in candies.values()):
		return True		# one of each color
	paired_color = get_paired_color(candies)	# 1 pair and nothing else
	return paired_color is not None and len([1 for count in candies.values() if count > 0]) == 0

def run():
	candies = get_initial_candies()
	logger.debug('starting candies: {}'.format(candies))
	steps = 0
	while not done(candies):
		paired_color = get_paired_color(candies)
		while paired_color is not None:
			logger.debug('eating {} pair'.format(paired_color))
			candies[paired_color] -= 2	# eat the pair
			paired_color = get_paired_color(candies)
		if not done(candies):
			next_candy = draw_one()		# draw another candy
			candies[next_candy] += 1
			logger.debug('drew a {} candy'.format(next_candy))
			steps += 1
		logger.debug('current candies: {}'.format(candies))
	logger.debug('took {} steps to finish'.format(steps))
	return steps

def run_test(n=10000):
	steps = [run() for _ in range(n)]
	avg_steps = sum(steps) / n
	stdev = math.sqrt(sum((x - avg_steps) ** 2 for x in steps) / (n - 1))
	return Results(mean=avg_steps, stdev=stdev, min=min(*steps), max=max(*steps))

