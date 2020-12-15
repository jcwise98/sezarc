from tkinter.ttk import Style

import matplotlib
import pandas as pd
import numpy as np
import scipy.spatial as ss
import PIL.Image
from PIL import ImageTk

from src.main.heatmap import HeatMapOptionsBox
import matplotlib.cm as cm
import matplotlib.image as mpimg

# TODO: add point data_frame index print when clicking a point
# TODO: add area for each shark to display on heatmaps
# TODO: kernel density checkbox to change the points into a kernel density function plot thing

matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import PIL.Image
import PIL.ImageTk
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

LARGE_FONT = ("Fixedsys", 24)
BUTTON_FONT = ('Calibiri', 14, 'bold')
BACKGROUND_COLOR = '#f2ffe5'

class ZooMapper(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default="clienticon.ico")
        tk.Tk.wm_title(self, "ZooMonitor Data Mapper")
        tk.Tk.wm_geometry(self, "1440x810")

        menu = Menu(self)
        tk.Tk.config(self, menu=menu)

        # Define Menus
        file_menu = Menu(menu, tearoff=0)
        edit_menu = Menu(menu, tearoff=0)
        view_menu = Menu(menu, tearoff=0)
        about_menu = Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        menu.add_cascade(label="Edit", menu=edit_menu)
        menu.add_cascade(label="View", menu=view_menu)
        menu.add_cascade(label="About", menu=about_menu)

        # File Menu Options
        file_menu.add_command(label="Import Spreadsheet", command=self.get_spreadsheet)
        #file_menu.add_command(label="Import Habitat", command=self.get_image)

        # Edit Menu Options

        # View Menu Options
        # view_menu.add_command(label="Display Coordinates", command=self.get_list)
        # view_menu.add_command(label="Hide Coordinates", command=self.remove_list)

        # About Menu Options
        about_menu.add_command(label="Developers", command=self.print_dev)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.container_please = container

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, HeatMapPage):
            frame = F(container, self)
            frame.config(bg=BACKGROUND_COLOR)
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def get_plot_creation_options(self, data_frame):
        plot_options = {'heatmap_options': {}}
        heat_options_box = HeatMapOptionsBox(data_frame, (plot_options, 'heatmap_options'))

        heat_options_box.wait_window(heat_options_box)

        return plot_options['heatmap_options']

    # Function for opening the
    # file explorer window
    def get_spreadsheet(self):
        filename = filedialog.askopenfilename(initialdir="",
                                              title="Select a File",
                                              filetypes=(("Excel files",
                                                          "*.xlsx*"),
                                                         ("all files",
                                                          "*.*")))
        # print(filename)
        data = pd.read_excel(filename)

        heatmap_options = self.get_plot_creation_options(data)
        heat_frame = HeatMapPage(self.container_please, self, data, heatmap_options)
        heat_frame.config(bg=BACKGROUND_COLOR)
        heat_frame.grid(row=0, column=0, sticky="nsew")
        self.frames[HeatMapPage] = heat_frame

    def print_dev(self):
        messagebox.showinfo("Developers",
                            "Farah Aljishi\nDerek Baum\nRyan Bonacquisti\nDebra Lymon\nNtsee Ndingwan\nJake Wise")

    def show_frame(self, cont):
        print("called")
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Welcome to Zoo Monitor Data Mapper", font=LARGE_FONT, bg=BACKGROUND_COLOR)
        label.pack(pady=10, padx=10)

        style = Style()
        style.configure('TButton', font=BUTTON_FONT,
                        borderwidth='4')
        style.map('TButton', foreground=[('active', '!disabled', 'green')],
                  background=[('active', 'black')])

        button = ttk.Button(self, text="Import Spreadsheet", style="TButton",
                            command=lambda: controller.get_spreadsheet())
        button.pack()

        button3 = ttk.Button(self, text="Graph Page",
                            command=lambda: controller.show_frame(HeatMapPage))
        button3.pack()

        canvas = Canvas(self, width=600, height=600)
        canvas.pack()
        img = ImageTk.PhotoImage(PIL.Image.open('zoo-logo.png'))
        canvas.background = img  # Keep a reference in case this code is put in a function.
        canvas.create_rectangle(0, 0, 600, 600, fill=BACKGROUND_COLOR, outline=BACKGROUND_COLOR)
        bg = canvas.create_image(0, 0, anchor=tk.NW, image=img)


        enclosure_image = Label(image="")
        enclosure_image.pack()




class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page Two",
                             command=lambda: controller.show_frame(PageTwo))
        button2.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page One",
                             command=lambda: controller.show_frame(PageOne))
        button2.pack()


class HeatMapPage(tk.Frame):
    def __init__(self, parent, controller, data_frame=None, options=None):
        self.old_x = -1
        self.old_y = -1
        self.old_z = -2
        self.image_name = ''

        if options is not None:
            self.unit_string = options['unit_type']
            if options['habitat_image'] != '':
                self.image_name = options['habitat_image']
                self.img = mpimg.imread(self.image_name)

        if (data_frame is not None) and (options is not None):
            tk.Frame.__init__(self, parent)

            # df[end] - df[begin]/(end-begin)
            self.label_var = tk.StringVar()
            if options['z_column'] != '':
                self.label_var.set("3d Graph Page")
            else:
                self.label_var.set("click points for distance NOTE: doesn't work if you click overlapping points.")
            self.label = tk.Label(self, textvariable=self.label_var, font=LARGE_FONT, bg=BACKGROUND_COLOR)
            self.label.pack(pady=10, padx=10)

            button1 = ttk.Button(self, text="Back to Home",
                                 command=lambda: controller.show_frame(StartPage))
            button1.pack()

            fig = Figure()

            canvas = FigureCanvasTkAgg(fig, self)
            #canvas.create_image(20, 20, anchor=NW, image=options['habitat_image'])
            canvas.draw()

            cal_ratio = self.get_calibration_ratio(data_frame, options)

            # filtering the data frame into the row range specified in options
            if options['begin_index'] != '' and options['end_index'] != '':
                data_frame = data_frame.iloc[int(options['begin_index']):int(options['end_index'])]

            # loop through column filters and filter data frame
            for k, v in options['filters'].items():
                data_frame = data_frame.loc[(data_frame[k] == v)]

            self.x_col, self.y_col, self.z_col = self.get_columns_from_options(options)

            q_low = data_frame[self.x_col].quantile(0.01)
            q_hi = data_frame[self.x_col].quantile(0.99)

            data_frame = data_frame[(data_frame[self.x_col] < q_hi) &
                                    (data_frame[self.x_col] > q_low)]

            # now we filter out null values for .x/self.y/self.z columns
            if self.z_col != '':
                data_frame = data_frame.loc[(pd.notnull(data_frame[self.x_col])) &
                                            (pd.notnull(data_frame[self.y_col])) &
                                            (pd.notnull(data_frame[self.z_col]))]
            else:
                data_frame = data_frame.loc[(pd.notnull(data_frame[self.x_col])) &
                                            (pd.notnull(data_frame[self.y_col]))]

            if self.z_col != '':
                self.ax = fig.add_subplot(111, projection='3d')
                self.ax.set_zlabel(options['unit_type'])
            else:
                self.ax = fig.add_subplot(111)

            self.ax.set_xlabel(options['unit_type'])
            self.ax.set_ylabel(options['unit_type'])

            #self.ax.set_xlim(0,16)
            #self.ax.set_ylim(0,16)

            if options['name_column'] != '':
                names = data_frame[options['name_column']].unique()
                self.filter_names_from_user_options(names, options)
                print(names)
                colors = cm.rainbow(np.linspace(0, 1, len(names)))
                print(colors)
                for i in range(len(names)):
                    name = names[i]
                    color = colors[i]
                    df_filtered = data_frame.loc[data_frame[options['name_column']] == name]
                    self.x = df_filtered[self.x_col].values.flatten()
                    self.y = df_filtered[self.y_col].values.flatten()
                    self.x /= cal_ratio
                    self.y /= cal_ratio
                    if self.z_col != '':
                        self.z = df_filtered[self.z_col].values.flatten()
                        self.z *= -1
                        hull = ss.ConvexHull(np.vstack((self.x,self.y,self.z)).T)
                        self.ax.scatter(self.x, self.y, self.z, color=color, label=name+": "+str(hull.volume) + " " + options['unit_type'] + "$^{3}$")
                    else:
                        self.ax.scatter(self.x, self.y, color=color, label=name, picker=True)
                self.ax.legend()

            else:
                self.x = data_frame[self.x_col].values.flatten()
                self.y = data_frame[self.y_col].values.flatten()
                self.x /= cal_ratio
                self.y /= cal_ratio
                if self.z_col != '':
                    self.z = data_frame[self.z_col].values.flatten()
                    self.z *= -1
                    self.ax = fig.add_subplot(111, projection='3d')
                    self.ax.scatter(self.x, self.y, self.z, color='#1f77b4')
                else:
                    self.ax = fig.add_subplot(111)
                    self.ax.scatter(self.x, self.y, color='#1f77b4', picker=True)

            if self.image_name != '' and self.z_col == '':
                self.ax.imshow(self.img, extent=[self.get_min(self.x),self.get_max(self.x),self.get_min(self.y),self.get_max(self.y)])

            canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
            toolbar = NavigationToolbar2Tk(canvas, self)
            toolbar.update()
            canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            fig.canvas.mpl_connect('pick_event', self.onpick3)
        else:
            tk.Frame.__init__(self, parent)
            button1 = ttk.Button(self, text="Back to Home",
                                 command=lambda: controller.show_frame(StartPage))
            button1.pack()

    def get_min(self, arr):
        min_val = arr[0]
        for x in arr:
            if x < min_val:
                min_val = x
        return min_val

    def get_max(self, arr):
        max_val = arr[0]
        for x in arr:
            if x > max_val:
                max_val = x
        return max_val

    def onpick3(self, event):
        # print("xdata: ", event.mouseevent.xdata)
        # print("ydata: ", event.mouseevent.ydata)

        ind = event.ind
        x_data = event.mouseevent.xdata
        y_data = event.mouseevent.ydata

        real_x, real_y = self.select_closest_point_2d(x_data, y_data, self.ax.collections, event.ind)
        # print('onpick3 scatter:', ind, real_x, real_y)
        if self.old_x != -1 and self.old_y != -1:
            self.label_var.set("Distance Between Last Two Selected Points: " + str(
                np.sqrt((self.old_x - real_x) * (self.old_x - real_x)
                        + (self.old_y - real_y) * (self.old_y - real_y)))
                               + " " + str(self.unit_string))
        self.old_x = real_x
        self.old_y = real_y

    def select_closest_point_2d(self, x_target, y_target, collections, event_index):

        potential_pairs = []

        for thang in collections:
            thang.set_offset_position('data')
            if len(thang.get_offsets()) > event_index:
                potential_pairs.append(thang.get_offsets()[event_index].data[0])

        for thang in collections:
            thang.set_offset_position('screen')

        error = 1000
        out_x = None
        out_y = None
        for pair_arr in potential_pairs:
            x = pair_arr[0]
            y = pair_arr[1]
            # some sort of standard error, probably doesn't need to be this good though, but it is.
            curr_err = np.sqrt((x_target - x) * (x_target - x) + (y_target - y) * (y_target - y))
            if curr_err < error:
                out_x = x
                out_y = y
                error = curr_err
        return out_x, out_y

    def calc_distance_3d(self, x1, y1, z1, x2, y2, z2):
        return np.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1) + (z2 - z1) * (z2 - z1))

    def filter_names_from_user_options(self, names, options):
        if options['names_list'] != '':
            names_input = options['names_list'].split(",")
            for i in range(len(names)):
                if names[i] not in names_input:
                    names[i] = None

    def get_columns_from_options(self, options):
        return options['x_column'], options['y_column'], options['z_column']

    def get_calibration_ratio(self, data_frame, options):
        i1 = options['begin_calibration_index']
        i2 = options['end_calibration_index']
        if i1 == '' or i2 == '' or options['known_distance'] == '':
            return 1
        x1 = data_frame[options['x_column']][int(i1)]
        y1 = data_frame[options['y_column']][int(i1)]
        x2 = data_frame[options['x_column']][int(i2)]
        y2 = data_frame[options['y_column']][int(i2)]

        return np.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1)) / float(options['known_distance'])


class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack()

        f = Figure(figsize=(5, 5), dpi=100)
        a = f.add_subplot(111)
        a.plot([1, 2, 3, 4, 5, 6, 7, 8], [5, 6, 1, 3, 8, 9, 3, 5])

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


app = ZooMapper()
app.mainloop()
