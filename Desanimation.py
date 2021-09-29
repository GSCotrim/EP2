from Truss import *
from matplotlib import pyplot as plt
import imageio


class Animation:
    def __init__(self, truss, vibes, magnitude=3000):
        self.truss = truss
        self.vibes = vibes
        self.points = [None] * len(self.truss.nodes)
        self.points[len(self.truss.nodes) - 1] = Point(0, 0, len(self.truss.nodes))
        self.point_array = [[None] * len(self.truss.nodes)] * len(self.vibes)
        for x in self.point_array:
            x[len(self.truss.nodes) - 1] = Point(0, 0, len(self.truss.nodes))
        self.__make_bars_into_points()
        self.lines = []
        self.line_array = [[]] * len(self.vibes)
        self.__make_points_into_lines()
        self.magnitude = magnitude
        self.figures = [[]] * len(self.vibes)
        # self.megagambeta()
        self.__shift_points_horizontally()

    def __make_bars_into_points(self):
        for i in range(len(self.truss.bars) - 1, -1, -1):
            bar = self.truss.bars[i]
            node1, node2 = bar.node_numbers[0], bar.node_numbers[1]
            if self.points[node1 - 1] is None and self.points[node2 - 1] is None:
                print("We has problem")
            if self.points[node1 - 1] is not None and self.points[node2 - 1] is not None:
                continue
            current_point = self.points[node1 - 1] or self.points[node2 - 1]
            other_node_index = node1 + node2 - current_point.node_index
            if current_point.node_index > other_node_index:
                delta_x = bar.cos * bar.length
                delta_y = bar.sin * bar.length
            else:
                delta_x = -1 * bar.cos * bar.length
                delta_y = -1 * bar.sin * bar.length
            new_point = Point(current_point.x() + delta_x, current_point.y() + delta_y, other_node_index)
            self.points[other_node_index - 1] = new_point

            for x in self.point_array:
                x[other_node_index - 1] = new_point.copy()

    def __shift_points_horizontally(self):
        min_x = 0
        for point in self.points:
            min_x = min(min_x, point.x())
        for point in self.points:
            point.shift_x(-min_x)

        for x in self.point_array:
            min_x = 0
            for point in x:
                min_x = min(min_x, point.x())
            for point in x:
                point.shift_x(-min_x)

    def __make_points_into_lines(self):
        for bar in self.truss.bars:
            node1, node2 = bar.node_numbers[0], bar.node_numbers[1]
            point1, point2 = self.points[node1 - 1], self.points[node2 - 1]
            self.lines.append(Line(point1, point2))
            for x in range(len(self.point_array)):
                parray = self.point_array[x]
                point1, point2 = parray[node1 - 1], parray[node2 - 1]
                self.line_array[x].append(Line(point1, point2))

    def plot_points(self):
        x = []
        y = []
        for point in self.points:
            x.append(point.x)
            y.append(point.y)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.scatter(x, y)

    def show_plot_points(self):
        self.plot_points()
        plt.show()

    def plot_lines(self, vibe_index):
        plt.gca().set_aspect('equal', adjustable='box')
        for line in self.line_array[vibe_index]:
            plt.plot(line.xs(), line.ys())

    def create_lines_figures(self, name):
        for vibe_index in range(len(self.vibes)):
            self.create_lines_figure(name, vibe_index)

    def create_lines_figure(self, name, index):
        plt.figure()
        self.plot_lines(index)
        figure_name = name + "_" + str(index) + '.png'
        self.figures[index].append(figure_name)
        plt.savefig(figure_name)
        plt.close()

    def build_gifs(self):
        for index in range(len(self.vibes)):
            with imageio.get_writer('mygif_'+str(index)+'.gif', mode='I') as writer:
                for filename in self.figures[index]:
                    image = imageio.imread(filename)
                    writer.append_data(image)

    def megagambeta(self):
        good_vibes = self.vibes[0]
        for point in self.points:
            if point.node_index >= self.truss.first_fixed_node_number:
                continue
            index = point.node_index
            xx = good_vibes.vib_modes[2 * index - 1 - 1] * self.magnitude
            yy = good_vibes.vib_modes[2 * index - 1] * self.magnitude
            point.set_xy(xx, yy)

    def timelapse(self, time_in_seconds):
        t = time_in_seconds
        for vibe_index in range(len(self.vibes)):
            good_vibes = self.vibes[vibe_index]
            zs = good_vibes.vib_modes
            w = good_vibes.vib_freq
            points = self.point_array[vibe_index]
            for point in points:
                if point.node_index >= self.truss.first_fixed_node_number:
                    continue
                zh = zs[2 * point.node_index - 1 - 1] * self.magnitude
                zv = zs[2 * point.node_index - 1] * self.magnitude
                delta_x = zh * math.cos(w * t)
                delta_y = zv * math.cos(w * t)
                point.apply_delta(delta_x, delta_y)


class Point:
    def __init__(self, x, y, node_index):
        self.__x = x
        self.__y = y
        self.node_index = node_index
        self.__delta_x = 0
        self.__delta_y = 0

    def __str__(self):
        return f"( {self.x()} , {self.y()} ) - Node {self.node_index}"

    def shift_x(self, shift):
        self.__x += shift

    def apply_delta(self, delta_x, delta_y):
        self.__delta_x = delta_x
        self.__delta_y = delta_y

    def set_xy(self, x, y):
        self.__x = x
        self.__y = y

    def x(self):
        return self.__x + self.__delta_x

    def y(self):
        return self.__y + self.__delta_y

    def copy(self):
        return Point(self.__x, self.__y, self.node_index)


class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def xs(self):
        return [self.point1.x(), self.point2.x()]

    def ys(self):
        return [self.point1.y(), self.point2.y()]
