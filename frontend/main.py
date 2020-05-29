from gui.Application import Application

if __name__ == '__main__':
    app = Application()
    app.init_components()

    # set full screen
    w = app.winfo_screenwidth()
    h = app.winfo_screenheight()
    app.geometry("%dx%d+0+0" % (w, h))

    app.mainloop()