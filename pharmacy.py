# import libraries
from tkinter import *
import tkinter.messagebox
from tkinter import ttk
import pymysql


class Pharmacy:
    # Screen
    def __init__(self, root):
        self.root = root
        self.root.title("test")
        self.root.geometry('1400x690')
        self.root.resizable(True, True)
        mainframe = Frame(self.root)
        mainframe.pack()
        # ------- frames positions------
        TitleFrame = Frame(mainframe, bd=7, width=770, height=100, relief=RIDGE, bg="light blue")
        TitleFrame.grid(row=0, column=0)

        TopFrame3 = Frame(mainframe, bd=5, width=770, height=500, relief=RIDGE)
        TopFrame3.grid(row=1, column=0)

        Left_Frame = Frame(TopFrame3, bd=5, width=770, height=400, bg="cadet blue", relief=RIDGE)
        Left_Frame.pack(side=LEFT)

        Left_Frame1 = Frame(Left_Frame, bd=5, width=600, height=180, relief=RIDGE)
        Left_Frame1.pack(side=TOP)

        Right_Frame1 = Frame(TopFrame3, bd=5, width=100, height=400, bg="cadet blue", relief=RIDGE)
        Right_Frame1.pack(side=RIGHT)
        Right_Frame1a = Frame(Right_Frame1, bd=5, width=90, height=300, relief=RIDGE, bg="light blue")
        Right_Frame1a.pack(side=TOP)
        # -----Variables-------#
        self.Med_name = StringVar()
        self.Med_price = StringVar()
        self.Med_code = StringVar()
        # ------- labels positions------
        self.lbltitle = Label(TitleFrame, font=('arial', 40, 'bold'), text="pharmacy system", bd=6)
        self.lbltitle.grid(row=0, column=0, padx=132)
        #-----------------------------
        self.med_name = Label(Left_Frame1, font=('arial', 12, 'bold'), text="medicine name", bd=7)
        self.med_name.grid(row=1, column=0, padx=5)

        self.med_name1 = Entry(Left_Frame1, font=('arial', 12, 'bold'), bd=5, width=44, justify='left',
                               textvariable=self.Med_name)
        self.med_name1.grid(row=1, column=1, sticky=W, padx=5)
        # -----------------------------
        self.enter_code = Label(Left_Frame1, font=('arial', 12, 'bold'), text="barcode")
        self.enter_code.grid(row=2, column=0)

        self.enter_code1 = Entry(Left_Frame1, font=('arial', 12, 'bold'), bd=5, width=44, justify='left',
                                 textvariable=self.Med_code)
        self.enter_code1.grid(row=2, column=1, sticky=W, padx=5)
        # -----------------------------
        self.med_price = Label(Left_Frame1, font=('arial', 12, 'bold'), text="price", bd=7)
        self.med_price.grid(row=3, column=0, padx=5)

        self.med_price1 = Entry(Left_Frame1, font=('arial', 12, 'bold'), bd=5, width=44, justify='left',
                                textvariable=self.Med_price)
        self.med_price1.grid(row=3, column=1, sticky=W, padx=5)

       # scroller
        scroll_y = Scrollbar(Left_Frame, orient=VERTICAL)
        self.pharmacy_records = ttk.Treeview(Left_Frame, height=16, column=("med", "price", "code"),
                                             yscrollcommand=scroll_y.set)
        scroll_y.pack(side=RIGHT, fill=Y)
        #name the columns for the treeview
        self.pharmacy_records.heading("med", text="medicine ", )
        self.pharmacy_records.heading("price", text="price_EGP")
        self.pharmacy_records.heading("code", text="barcode")
        # dimension for the columns of treview
        self.pharmacy_records['show'] = 'headings'
        self.pharmacy_records.column("med", width=70)
        self.pharmacy_records.column("code", width=70)
        self.pharmacy_records.column("price", width=70)
        self.pharmacy_records.pack(fill=BOTH)
        #buttons
        self.btnAddItem = Button(Right_Frame1a, font=('arial', 16, 'bold'), text="Add Item", bd=4, command=self.add_new,
                                 width=8, height=2).grid(row=0, column=0, padx=1)
        self.btnDisplay = Button(Right_Frame1a, font=('arial', 16, 'bold'), text="Display", bd=4, pady=1, padx=24
                                 , command=self.Display, width=8, height=2).grid(row=1, column=0, )
        self.btnDelete = Button(Right_Frame1a, font=('arial', 16, 'bold'), text="Delete", bd=4, command=self.delete,
                                width=8, height=2).grid(row=3, column=0, padx=1)
        self.btnReset = Button(Right_Frame1a, font=('arial', 16, 'bold'), text="Reset", bd=4, command=self.Reset,
                               width=8, height=2).grid(row=5, column=0)
        self.btnExit = Button(Right_Frame1a, font=('arial', 16, 'bold'), text='Exit', bd=4, command=self.exit_button,
                              width=8, height=2).grid(row=6, column=0)

    def Reset(self): # Reset function
        self.med_name1.delete(0, END)
        self.enter_code1.delete(0, END)
        self.med_price1.delete(0, END)

    def add_new(self): # Add function
        conn = pymysql.connect(host="localhost", user='root', password='', database="newpharm") # connection of database
        cur = conn.cursor()
        name = self.Med_name.get()
        price = self.Med_price.get()
        code = self.Med_code.get()
        med = "medicines" # table name
        additem = "insert into " + med + " values ('" + name + "','" + price + "','" + code + "')" #columns name

        cur.execute(additem)
        conn.commit()
        # conn.connect()
        # conn.close()
        tkinter.messagebox.showinfo("data Entry Form", "data added successfully")

    def delete(self): # delete function
        conn = pymysql.connect(host="localhost", user='root', password='', database="newpharm") # connection of database
        cur = conn.cursor()
        code = self.Med_code.get()
        med = "medicines" # table name
        delete = "delete from  " + med + " where Med_code ='" + code + "'" #column name (primary key)

        cur.execute(delete)
        conn.commit()
        tkinter.messagebox.showinfo("data Entry Form", "data removed successfully")

    def Display(self): #display function
        conn = pymysql.connect(host="localhost", user='root', password='', database="newpharm")
        cur = conn.cursor()
        cur.execute("Select * from medicines")
        result = cur.fetchall()
        if len(result) != 0:
            self.pharmacy_records.delete(*self.pharmacy_records.get_children())
            for row in result:
                self.pharmacy_records.insert('', END, values=row)

        conn.commit()
        conn.close()

    def exit_button(self): # exit function
        exit_button = tkinter.messagebox.askyesno("Pharmacy Management System", "confirm to exit")
        if exit_button > 0:
            root.destroy()
            return


if __name__ == '__main__':
    root = Tk()
    ob = Pharmacy(root)
    root.mainloop()
