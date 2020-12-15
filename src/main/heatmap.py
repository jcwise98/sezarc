import tkinter
from tkinter.ttk import Style

import pandas
from PIL import ImageTk, Image


class HeatMapOptions:

    def __init__(self, begin_index, end_index, filters, x_column, y_column, z_column=None):
        self.begin_index = begin_index
        self.end_index = end_index
        self.filters = filters
        self.x_column = x_column
        self.y_column = y_column
        self.x_column = z_column


class HeatMapOptionsBox(tkinter.Toplevel):
    # given a data frame that holds a spreadsheet,
    # create a window for selecting columns from that spreadsheet, basically.
    # when you supply 'out_dict', you will do it in a tuple, and give the dictionary, followed by the key you want to use.

    def __init__(self, data_frame, out_dict, width=800, height=800):
        tkinter.Toplevel.__init__(self)
        self.x_column_var = tkinter.StringVar()
        self.y_column_var = tkinter.StringVar()
        self.z_column_var = tkinter.StringVar()
        self.name_column_var = tkinter.StringVar()



        self.filter_entry_dict = {}
        self.entry_dict_ind = 0
        self.filter_entries_list = []

        self.habitat_image = ''

        self.columns_list = data_frame.columns
        print("out here right now")
        print(self.columns_list)
        # self.top = tkinter.Toplevel(None)
        frm = tkinter.Frame(self, width=width, height=height, borderwidth=4, relief='ridge')
        self.frame = frm
        self.frame.config(bg='white')
        # frm.pack_propagate(0)
        frm.pack(fill='both', expand=True)

        self.begin_ind_calibration = tkinter.Label(frm, text='Begin Calibration Point Index', bg='#f2ffe5')
        self.begin_ind_calibration.pack(pady=4)


        self.begin_ind_calibration_entry = tkinter.Entry(frm)
        self.begin_ind_calibration_entry.pack(pady=4)

        self.end_ind_calibration = tkinter.Label(frm, text='End Calibration Point Index', bg='#f2ffe5')
        self.end_ind_calibration.pack(pady=4)

        self.end_ind_calibration_entry = tkinter.Entry(frm)
        self.end_ind_calibration_entry.pack(pady=4)

        self.known_distance_label = tkinter.Label(frm, text='Known Distance Between Calibration Points', bg='#f2ffe5')
        self.known_distance_label.pack(pady=4)

        self.known_distance_entry = tkinter.Entry(frm)
        self.known_distance_entry.pack(pady=4)

        self.unit_type_label = tkinter.Label(frm, text='Unit of Measurement(plural)', bg='#f2ffe5')
        self.unit_type_label.pack(pady=4)

        self.unit_type_entry = tkinter.Entry(frm)
        self.unit_type_entry.pack(pady=4)

        self.begin_ind_label = tkinter.Label(frm, text='Begin Index:', bg='#f2ffe5')
        self.begin_ind_label.pack(padx=4, pady=4)

        self.begin_ind_entry = tkinter.Entry(frm)
        self.begin_ind_entry.insert(0, '0')
        self.begin_ind_entry.pack(pady=4)

        self.end_ind_label = tkinter.Label(frm, text='End Index:', bg='#f2ffe5')
        self.end_ind_label.pack(padx=4, pady=4)

        self.end_ind_entry = tkinter.Entry(frm)
        self.end_ind_entry.insert(0, str(data_frame.index.stop))
        self.end_ind_entry.pack(pady=4)

        self.name_column_label = tkinter.Label(frm, text='Name Column', bg='#f2ffe5')
        self.name_column_label.pack(pady=4)

        self.name_column_dropdown = tkinter.OptionMenu(frm, self.name_column_var, *self.columns_list)
        self.name_column_dropdown.pack(pady=4)

        self.names_list_label = tkinter.Label(frm, text='List Selected Names seperated by comma', bg='#f2ffe5')
        self.names_list_label.pack(pady=4)

        self.names_list_entry = tkinter.Entry(frm)
        self.names_list_entry.pack(pady=4)

        self.x_column_label = tkinter.Label(frm, text='X Column', bg='#f2ffe5')
        self.x_column_label.pack(pady=4)

        self.x_column_dropdown = tkinter.OptionMenu(frm, self.x_column_var, *self.columns_list)
        self.x_column_dropdown.pack(pady=4)

        self.y_column_label = tkinter.Label(frm, text='Y Column', bg='#f2ffe5')
        self.y_column_label.pack(pady=4)

        self.y_column_dropdown = tkinter.OptionMenu(frm, self.y_column_var, *self.columns_list)
        self.y_column_dropdown.pack(pady=4)

        self.z_column_label = tkinter.Label(frm, text='Z Column', bg='#f2ffe5')
        self.z_column_label.pack(pady=4)

        self.z_column_dropdown = tkinter.OptionMenu(frm, self.z_column_var, *self.columns_list)
        self.z_column_dropdown.pack(pady=4)

        b_submit = tkinter.Button(frm, text='Submit')
        b_submit['command'] = lambda: self.send_options_to_dict(out_dict)
        b_submit.pack()

        b_cancel = tkinter.Button(frm, text='Cancel', )
        b_cancel['command'] = self.destroy
        b_cancel.pack(padx=4, pady=4)

        b_add_new_filter = tkinter.Button(frm, text='Add Filter')
        b_add_new_filter['command'] = lambda: self.add_filter_entry()
        b_add_new_filter.pack()

        b_add_new_filter = tkinter.Button(frm, text='Add Habitat')
        b_add_new_filter['command'] = lambda: self.get_image()
        b_add_new_filter.pack(pady=4)

        self.image_column_label = tkinter.Label(frm, text=self.habitat_image)
        self.image_column_label.pack()


    # Function to get image for enclosure
    def get_image(self):
        imagename = tkinter.filedialog.askopenfilename(initialdir="",
                                               title="Select a File",
                                               filetypes=(("Image files",
                                                           "*.png*"),
                                                          ("all files",
                                                           "*.*")))
        img = ImageTk.PhotoImage(Image.open(imagename))

        print(imagename)
        self.habitat_image = imagename

    #
    def add_filter_entry(self):
        new_filter_label = tkinter.Label(self.frame, text='Custom Column Filter:')
        new_filter_label.pack(pady=4)

        my_str = tkinter.StringVar()

        new_filter_columns = tkinter.OptionMenu(self.frame, my_str, *self.columns_list)
        new_filter_columns.pack(pady=4)

        new_filter_entry = tkinter.Entry(self.frame)
        new_filter_entry.pack(pady=4)

        new_filter_columns.wait_variable(my_str)
        print("we out the wait")
        self.filter_entries_list.append((new_filter_entry, my_str))
        self.filter_entry_dict[my_str.get()] = new_filter_entry.get()

    def send_options_to_dict(self, out_dict):
        for entry, var in self.filter_entries_list:
            self.filter_entry_dict[var.get()] = entry.get()
        options = {}
        options['begin_calibration_index'] = self.begin_ind_calibration_entry.get()
        options['end_calibration_index'] = self.end_ind_calibration_entry.get()
        options['known_distance'] = self.known_distance_entry.get()
        options['unit_type'] = self.unit_type_entry.get()
        options['begin_index'] = self.begin_ind_entry.get()
        options['end_index'] = self.end_ind_entry.get()
        options['names_list'] = self.names_list_entry.get()
        options['name_column'] = self.name_column_var.get()
        options['x_column'] = self.x_column_var.get()
        options['y_column'] = self.y_column_var.get()
        options['z_column'] = self.z_column_var.get()
        options['filters'] = self.filter_entry_dict
        options['habitat_image'] = self.habitat_image

        d, key = out_dict
        print(options)
        d[key] = options
        self.destroy()
