from matplotlib.figure import Figure
from math import exp
import Calculator as cal


class Equation:
    x, y, N, X = 1, 2, 10, 6

    def __init__(self, x=1, y=2, N=10, X=6):
        self.x = x
        self.y = y
        self.N = N
        self.X = X

    def redefine(self, N=10):
        self.N = N

    # Runge-Kutta
    def runge_kutta(self):
        # y array
        y_arr = []

        # h is an increment
        h = float((self.X - self.x) / self.N)
        # initialize y and x, also it prevent initial x, y from rewrite
        y = float(self.y)
        x = float(self.x)

        for i in range(0, self.N):
            y_arr.append(y)

            k1 = float(h * cal.equation(x, y))
            k2 = float(h * cal.equation(x + 0.5 * h, y + 0.5 * k1))
            k3 = float(h * cal.equation(x + 0.5 * h, y + 0.5 * k2))
            k4 = float(h * cal.equation(x + h, y + k3))

            # Yi+1
            y = y + float(1.0 / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
            # Xi+1
            x = x + h

        return y_arr

    # Improved Euler
    def imp_euler(self):
        # y array
        y_arr = []

        # h is an increment
        h = float((self.X - self.x) / self.N)
        # initialize y and x, also it prevent initial x, y from rewrite
        y = float(self.y)
        x = float(self.x)

        for i in range(0, self.N):
            y_arr.append(y)

            k1 = float(h * cal.equation(x, y))
            k2 = float(h * cal.equation(x, y + k1))

            # Yi+1
            y = y + float((k1 + k2) / 2)
            # Xi+1
            x = x + h

        return y_arr

    # Euler
    def euler(self):
        # y array
        y_arr = []

        # h is an increment
        h = float((self.X - self.x) / self.N)
        # initialize y and x, also it prevent initial x, y from rewrite
        y = float(self.y)
        x = float(self.x)

        for i in range(0, self.N):
            y_arr.append(y)

            k1 = float(h * cal.equation(x, y))

            # Yi+1
            y = y + k1
            # Xi+1
            x = x + h

        return y_arr

    # Exact
    def exact(self):
        # y array
        y_arr = []

        # h is an increment
        h = float((self.X - self.x) / self.N)
        # initialize y as a float variable
        y = float(self.y)
        x = float(self.x)

        for i in range(0, self.N):
            y_arr.append(y)

            y = (((1 / 6 * (2 * x + 1)) + ((2**(2/3)-0.5) * exp(2 * x - 2))) ** (3 / 2))

            # Xi+1
            x = x + h

        return y_arr

    # x array
    def create_array(self):
        x_arr = []
        h = float((self.X - self.x) / self.N)

        x = float(self.x)

        for i in range(0, self.N):
            x_arr.append(x)
            x += h

        return x_arr


class Graph:

    equation = Equation()

    x0 = []  # x values
    y1 = []  # Euler
    y2 = []  # Improved Euler
    y3 = []  # Runge-Kutta
    y4 = []  # Exact

    y1_err = []  # Euler local errors
    y2_err = []  # Improved Euler local errors
    y3_err = []  # Runge-Kutta local errors

    gy1_err = []  # Euler global errors
    gy2_err = []  # Improved Euler global errors
    gy3_err = []  # Runge-Kutta global errors

    gl_y1_err = []  # Euler global errors by N
    gl_y2_err = []  # Improved Euler global errors by N
    gl_y3_err = []  # Runge-Kutta global errors by N

    def __init__(self, input_eq=equation):
        self.equation = input_eq

    def prepare_graph(self):
        # x0 - array of x, yi - array of y
        self.x0 = self.equation.create_array()
        self.y1 = self.equation.euler()
        self.y2 = self.equation.imp_euler()
        self.y3 = self.equation.runge_kutta()
        self.y4 = self.equation.exact()

    def prepare_lc_err(self):
        self.y1_err = cal.local_error(self.y4, self.y1)  # Euler
        self.y2_err = cal.local_error(self.y4, self.y2)  # Improved Euler
        self.y3_err = cal.local_error(self.y4, self.y3)  # Runge_Kutta

    def prepare_gl_err(self):
        self.gy1_err = cal.global_error(self.y4, self.y1)
        self.gy2_err = cal.global_error(self.y4, self.y2)
        self.gy3_err = cal.global_error(self.y4, self.y3)

    def get_gl_error(self, n0, N):
        self.gl_y1_err = []
        self.gl_y2_err = []
        self.gl_y3_err = []

        for i in range(n0, N):
            self.equation.redefine(i)
            Graph.prepare_graph(self)
            Graph.prepare_gl_err(self)

            self.gl_y1_err.append(cal.find_max(self.gy1_err))
            self.gl_y2_err.append(cal.find_max(self.gy2_err))
            self.gl_y3_err.append(cal.find_max(self.gy3_err))

    def plot_graph(self):
        Graph.prepare_graph(self)
        fig1 = Figure(figsize=(5, 4), dpi=100)
        ax1 = fig1.add_subplot(111)
        ax1.plot(self.x0, self.y1, label='Euler', color='c')
        ax1.plot(self.x0, self.y2, label='Improved Euler', color='g')
        ax1.plot(self.x0, self.y3, label='Runge-Kutta', color='b')
        ax1.plot(self.x0, self.y4, label='Exact', color='r')
        ax1.set_title("Exact and Numerical solutions")
        ax1.legend()
        return fig1

    def plot_error(self):
        Graph.prepare_lc_err(self)
        fig2 = Figure(figsize=(5, 4), dpi=100)
        ax2 = fig2.add_subplot(111)
        ax2.plot(self.x0, self.y1_err, label='Euler', color='c')
        ax2.plot(self.x0, self.y2_err, label='Improved Euler', color='g')
        ax2.plot(self.x0, self.y3_err, label='Runge-Kutta', color='b')
        ax2.set_title("Local errors")
        ax2.legend()
        return fig2

    def plot_gl_error(self, n0, N):
        # normalization
        if n0 <= 0:
            n0 = 1
        Graph.get_gl_error(self, n0, N)
        fig3 = Figure(figsize=(5, 4), dpi=100)
        ax3 = fig3.add_subplot(111)
        n_dom = cal.create_n_array(n0, N)
        ax3.plot(n_dom, self.gl_y1_err, label='Euler', color='c')
        ax3.plot(n_dom, self.gl_y2_err, label='Improved Euler', color='g')
        ax3.plot(n_dom, self.gl_y3_err, label='Runge-Kutta', color='b')
        ax3.set_title("Global errors by N size")
        ax3.legend()
        return fig3

