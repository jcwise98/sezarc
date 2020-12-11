import tkinter


class DialogBox(object):
    root = None

    def __init__(self, msg, dict_key=None, width=400, height=250, options=None):
        tki = tkinter
        self.options_supplied=False
        self.top = tki.Toplevel(DialogBox.root)
        frm = tki.Frame(self.top, width=width, height=height, borderwidth=4, relief='ridge')
        frm.pack_propagate(0)
        frm.pack(fill='both', expand=False)
        label = tki.Label(frm, text=msg)
        label.pack(padx=4, pady=4)

        caller_wants_entry = dict_key is not None
        caller_supplied_options = options is not None

        if caller_wants_entry:
            if caller_supplied_options:
                self.options_supplied = True
                self.entry = tkinter.StringVar(frm)
                self.options = tkinter.OptionMenu(frm, self.entry, *options)
                self.options.pack()
            else:
                self.entry = tki.Entry(frm)
                self.entry.pack(pady=4)

            b_submit = tki.Button(frm, text='Submit')
            b_submit['command'] = lambda: self.entry_to_dict(dict_key)
            b_submit.pack()

        b_cancel = tki.Button(frm, text='Cancel')
        b_cancel['command'] = self.top.destroy
        b_cancel.pack(padx=4, pady=4)

    def entry_to_dict(self, dict_key):
        data = self.entry.get()
        print("fucking")
        if data:
            dict_key.set(self.entry.get())
            print(dict_key.get())
            print("bullshit")
            # d, key = dict_key
            # d[key] = data
            self.top.destroy()
