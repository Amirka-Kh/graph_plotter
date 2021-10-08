import tkinter as tk
from tkinter.ttk import Style
import GraphPlotter as gp
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure


# Framework Initialization -----------------------------------
class Graph(tk.Frame):
    def __init__(self, parent):
        super().__init__()
        self.next2 = tk.Button(self, text="local error", command=self.local_error)

        self.our_gr = gp.Graph()
        self.start_gr = self.our_gr.plot_graph()

        self.frame = tk.Frame(self, relief=tk.RAISED, borderwidth=1)
        self.chart = tk.LabelFrame(self.frame, text="Graph", padx=50, pady=30)
        self.menu = tk.LabelFrame(self.frame, text="Settings", padx=50, pady=30)
        self.style = Style()

        self.initUI()
        self.centerWindow()

    def centerWindow(self):
        w = 910
        h = 560

        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()

        x = (sw - w) / 2
        y = (sh - h) / 2
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def initUI(self):
        self.master.title("Graph Plotter")
        self.style.theme_use("default")

        self.frame.pack(fill=tk.BOTH, expand=True)

        self.add_graph()
        self.set_menu()

        self.pack(fill=tk.BOTH, expand=1)

        closeButton = tk.Button(self, text="Close", command=self.master.quit)
        closeButton.pack(side=tk.RIGHT, padx=5, pady=5)

        self.next2.pack(side=tk.RIGHT, padx=5, pady=5)

    # Functions to view graphs ---------------------------------------------
    def back_to(self):
        return

    def local_error(self):
        self.start_gr = self.our_gr.plot_error()
        # initialize the graph
        self.update_chart()
        self.do_the_work()

    def global_error(self, nm, Nnm):
        # normalization for nm
        if int(nm.get()) <= 1:
            n0 = 2
        else:
            n0 = int(nm.get())

        self.start_gr = self.our_gr.plot_gl_error(n0, int(Nnm.get()))
        # initialize the graph
        self.update_chart()
        self.do_the_work()

    # Temp function to add OOP -------------------------------------------
    def add_graph(self):
        self.chart.grid(row=0, column=0, sticky="w")
        # initialize the graph
        self.update_chart()
        self.do_the_work()

    def update_graph(self, xm, ym, Nm, Xm):
        # normalization
        if int(xm.get()) < 0:
            x = 0
        else:
            x = float(xm.get())

        # create an equation
        our_eq = gp.Equation(x, float(ym.get()),
                             int(Nm.get()), float(Xm.get())
                             )
        # create a graph
        self.our_gr = gp.Graph(our_eq)
        self.start_gr = self.our_gr.plot_graph()

        # initialize the graph
        self.update_chart()
        self.do_the_work()

    def update_chart(self):
        self.chart.destroy()
        self.chart = tk.LabelFrame(self.frame, text="Graph", padx=50, pady=30)
        self.chart.grid(row=0, column=0, sticky="w")

    def do_the_work(self):
        # add graph to the 'chart' LabelFrame
        graphic = FigureCanvasTkAgg(self.start_gr, master=self.chart)
        graphic.draw()
        graphic.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # add toolbar for the graph
        toolbar = NavigationToolbar2Tk(graphic, self.chart)
        toolbar.update()
        graphic.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        def on_key(event):
            print("you pressed {}".format(event.key))
            key_press_handler(event, graphic, toolbar)

        graphic.mpl_connect("key_press_event", on_key)

    # Menu setter -----------------------------------------------------------
    def set_menu(self):
        self.menu.grid(row=0, column=1, sticky="w")

        # for menu1
        menu1 = tk.LabelFrame(self.menu)
        menu1.pack()

        xm = tk.StringVar()
        ym = tk.StringVar()
        Nm = tk.StringVar()
        Xm = tk.StringVar()

        x_sms = tk.Label(menu1, text="Enter x: ")
        y_sms = tk.Label(menu1, text="Enter y: ")
        N_sms = tk.Label(menu1, text="Enter N: ")
        X_sms = tk.Label(menu1, text="Enter X: ")

        x_sms.grid(row=1, column=0, sticky="w")
        y_sms.grid(row=2, column=0, sticky="w")
        N_sms.grid(row=3, column=0, sticky="w")
        X_sms.grid(row=4, column=0, sticky="w")

        x_entry = tk.Entry(menu1, borderwidth=5, bg="white",
                           fg="black", textvariable=xm)
        x_entry.grid(row=1, column=1, padx=5, pady=5)
        x_entry.insert(0, 1)

        y_entry = tk.Entry(menu1, borderwidth=5, bg="white",
                           fg="black", textvariable=ym)
        y_entry.grid(row=2, column=1, padx=5, pady=5)
        y_entry.insert(0, 2)

        N_entry = tk.Entry(menu1, borderwidth=5, bg="white",
                           fg="black", textvariable=Nm)
        N_entry.grid(row=3, column=1, padx=5, pady=5)
        N_entry.insert(0, 10)

        X_entry = tk.Entry(menu1, borderwidth=5, bg="white",
                           fg="black", textvariable=Xm)
        X_entry.grid(row=4, column=1, padx=5, pady=5)
        X_entry.insert(0, 6)

        plot_graph = tk.Button(menu1, text="Plot graphs", padx=64, pady=5,
                               fg="green", bg="yellow",
                               command=lambda: self.update_graph(xm, ym, Nm, Xm))
        plot_graph.grid(row=5, column=0, columnspan=2)

        # for menu2
        menu2 = tk.LabelFrame(self.menu)
        menu2.pack()

        nm = tk.StringVar()
        Nnm = tk.StringVar()

        n_sms = tk.Label(menu2, text="Enter n0: ")
        Nn_sms = tk.Label(menu2, text="Enter N: ")

        n_sms.grid(row=1, column=0, sticky="w")
        Nn_sms.grid(row=2, column=0, sticky="w")

        n_entry = tk.Entry(menu2, borderwidth=5, bg="white",
                           fg="black", textvariable=nm)
        n_entry.grid(row=1, column=1, padx=5, pady=5)
        n_entry.insert(0, 2)

        Nn_entry = tk.Entry(menu2, borderwidth=5, bg="white",
                            fg="black", textvariable=Nnm)
        Nn_entry.grid(row=2, column=1, padx=5, pady=5)
        Nn_entry.insert(0, 10)

        plot_gl = tk.Button(menu2, text="Global errors", padx=64, pady=5,
                            fg="green", bg="yellow",
                            command=lambda: self.global_error(nm, Nnm))
        plot_gl.grid(row=3, column=0, columnspan=2)


def main():
    root = tk.Tk()
    root.geometry("820x580+300+300")
    app = Graph(root)
    root.mainloop()


if __name__ == '__main__':
    main()
