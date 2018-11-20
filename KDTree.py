from collections import namedtuple
from operator import itemgetter
from pprint import pformat

class Node(namedtuple('Node', 'location left right')):
    def __repr__(self):
        return pformat(tuple(self))

    def __iter__(self):
        yield self.location
        if self.left is not None:
            yield from self.left
        if self.right is not None:
            yield from self.right


class KDTree:
    def __init__(self, points=[]):
        if not points:
            self._root = None
            self._k = 0
        self._k = len(points[0])
        self._root = self.create(points)

    def __iter__(self):
        if self._root is None:
            yield None
        else:
            yield from self._root

    def create(self, points, depth=0):
        if not points:
            return None
        axis = depth % self._k

        points.sort(key=itemgetter(axis))
        median = len(points) // 2

        return Node(location=points[median],
                    left=self.create(points[:median], depth+1),
                    right=self.create(points[median+1:], depth+1))

    
    def render(self, filename):
        '''Generate a Bokeh plot of the KD tree'''
        if self._k != 2:
            raise AttributeError('K must be 2')
        from bokeh.io import output_file
        from bokeh.plotting import figure, save

        # Find minimum and maximum point values for each axis
        min_x = min_y = 10000000
        max_x = max_y = -10000000
        for x, y in self:
            if x < min_x:
                min_x = x
            if x > max_x:
                max_x = x
            if y < min_y:
                min_y = y
            if y > max_y:
                max_y = y

        # Get figure ready
        output_file(filename)
        fig = figure(title='KD Tree',
                     plot_height=1000, plot_width=1000,
                     x_range=(min_x - 1, max_x + 1),
                     y_range=(min_y - 1, max_y + 1))

        def render_helper(node, x_bounds, y_bounds, depth=0):
            '''Recursive helper to plot increasingly smaller KD boundaries'''
            px, py = node.location
            axis = depth % self._k
            left_x_bounds = right_x_bounds = x_bounds
            left_y_bounds = right_y_bounds = y_bounds
            if axis == 0: # x (vertical line)
                lx = [px, px]
                ly = y_bounds
                left_x_bounds = [x_bounds[0], px]
                right_x_bounds = [px, x_bounds[1]]
            else: # y (horizontal line)
                lx = x_bounds
                ly = [py, py]
                left_y_bounds = [y_bounds[0], py]
                right_y_bounds = [py, y_bounds[1]]

            color = 'red' if axis else 'green'
            fig.line(lx, ly, color=color, line_width=2)
            fig.circle(px, py, color='black', size=5)

            if node.left is not None:
                render_helper(node.left, left_x_bounds, left_y_bounds, depth+1)
            if node.right is not None:
                render_helper(node.right, right_x_bounds, right_y_bounds, depth+1)

        # Initial bounds are entire plot area
        x_bounds = [fig.x_range.start, fig.x_range.end]
        y_bounds = [fig.y_range.start, fig.y_range.end]
        render_helper(self._root, x_bounds, y_bounds)

        save(fig)

if __name__ == '__main__':
    from random import randint, seed, shuffle
##    point_list = [(2,3), (5,4), (9,6), (4,7), (8,1), (7,2)]


    k = 2
    data_range = (1, 99)
    num_points = 20
    point_list = [tuple(randint(*data_range) for _ in range(k))
                  for _ in range(num_points)]
    point_list = list(set(point_list)) # Unique points only
    shuffle(point_list) # Just to prove it doesn't matter
    
    tree = KDTree(point_list)
    tree.render('points.html')
