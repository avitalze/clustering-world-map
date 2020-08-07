from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
import os
from clustering import Clustering
import PIL
from PIL import ImageTk


class Clustering_Gui:
    """ Responsible for the display of all UI and input validity """

    def __init__(self, master):
        """" Initialization of all parameters of the class, buttons, labels """
        self.master = master
        master.title("K Means Clustering")
        master.minsize(750, 400)

        self.num_of_clusters = 0
        self.num_of_runs = 0
        self.cluster_ok = False
        self.runs_ok = False
        self.cluster = Clustering()

        self.file_path = StringVar()
        self.file_name_entered = Entry(master, width=100, textvariable=self.file_path)
        self.file_name_entered.grid(column=0, columnspan=3, row=0)
        self.file_path.trace('w', self.showPreProcessButton)

        self.button = Button(master, text="Browse A File", command=self.fileDialog)
        self.button.grid(column=3, row=0, pady=5)

        self.error_file_path = StringVar()
        self.error_file_label = Label(master, textvariable=self.error_file_path, foreground="red", width=40)
        self.error_file_label.grid(column=0, row=1, pady=10)

        self.num_cluster_label = Label(master, text="Number of clusters k")
        self.num_cluster_label.grid(column=0, row=2)

        self.num_cluster_text = StringVar()
        self.num_cluster_text.set(self.num_of_clusters)
        self.num_cluster_entry = Entry(master, width=15, textvariable=self.num_cluster_text)
        self.num_cluster_entry.grid(column=1, row=2)
        self.num_cluster_text.trace('w', self.validate_cluster)

        self.error_cluster_text = StringVar()
        self.error_cluster_label = Label(master, textvariable=self.error_cluster_text, foreground="red", width=40)
        self.error_cluster_label.grid(column=2, row=2)

        self.num_runs_label = Label(master, text="Number of runs")
        self.num_runs_label.grid(column=0, row=3)

        self.num_runs_text = StringVar()
        self.num_runs_text.set(self.num_of_runs)
        self.num_runs_entry = Entry(master, width=15, textvariable=self.num_runs_text)
        self.num_runs_entry.grid(column=1, row=3)
        self.num_runs_text.trace('w', self.validate_runs)

        self.error_run_text = StringVar()
        self.error_run_label = Label(master, textvariable=self.error_run_text, foreground="red", width=40)
        self.error_run_label.grid(column=2, row=3)

        self.prep_button = Button(master, text="Pre-process", command=self.call_preprocess, state='disabled')
        self.prep_button.grid(column=0, row=4, pady=20)
        self.cluster_button = Button(master, text="Cluster", state='disabled', command=self.call_cluster)
        self.cluster_button.grid(column=1, row=4, pady=20)

        self.scatter_pic_label = Label(master)
        self.scatter_pic_label.grid(column=0, row=5, pady=10)

        self.world_map_label= Label(master)
        self.world_map_label.grid(column=1, row=5, pady=10)


    def validate_runs(self, *args):
        """" Validate the input variable - number of runs - and display messages to the user accordingly """
        if (self.num_runs_text.get()):
            try:
                self.num_of_runs = int(self.num_runs_text.get())
                if self.num_of_runs <= 0:
                    self.error_run_text.set('Enter a number greater than zero')
                    self.runs_ok = False
                    self.cluster_button.config(state='disabled')
                elif self.num_of_runs >= 50:
                    self.error_run_text.set('Enter a number smaller than 50')
                    self.runs_ok = False
                    self.cluster_button.config(state='disabled')
                else:
                    self.error_run_text.set('')
                    self.runs_ok = True
                    self.showClusterButton()
            except ValueError:  # problem
                self.runs_ok = False
                self.error_run_text.set('Enter only numbers')
                self.cluster_button.config(state='disabled')

        else:  # empty
            self.runs_ok = False
            self.error_run_text.set('')
            self.cluster_button.config(state='disabled')

    def validate_cluster(self, *args):
        """" Validate the input variable - number of clusters - and display messages to the user accordingly """
        if self.num_cluster_text.get():
            try:
                self.num_of_clusters = int(self.num_cluster_text.get())
                if self.num_of_clusters <= 1:
                    self.cluster_ok = False
                    self.error_cluster_text.set('Enter a number greater than 1')
                    self.cluster_button.config(state='disabled')
                elif self.num_of_clusters > 164:
                    self.cluster_ok = False
                    self.error_cluster_text.set('Enter a number smaller than 165')
                    self.cluster_button.config(state='disabled')
                else:
                    self.cluster_ok = True
                    self.error_cluster_text.set('')
                    self.showClusterButton()

            except ValueError:
                self.cluster_ok = False
                self.error_cluster_text.set('Enter only numbers')
                self.cluster_button.config(state='disabled')
        else:
            self.cluster_ok = False
            self.error_cluster_text.set('')
            self.cluster_button.config(state='disabled')

    def fileDialog(self):
        """" Input the data file into a variable and save its path in the file path field. """
        file_path = filedialog.askopenfilename(initialdir="/", title="Select A File",
                                               filetype=(("xlsx files", "*.xlsx"), ("all files", "*.*")))
        self.file_path.set(file_path)
        self.showPreProcessButton()

    def showClusterButton(self, *args):
        """" Checking whether to enable "clustering" button-
            The number of runs and the number of threads entered by the user is correct"""
        if self.runs_ok & self.cluster_ok:
            self.cluster_button.config(state='normal')
        else:
            self.cluster_button.config(state='disabled')

    def showPreProcessButton(self, *args):
        """" Checking whether to enable "pre-processing" button-
            The file path contains an existing and empty file"""
        self.prep_button.config(state='disabled')

        if self.file_path.get():
            try:
                if os.stat(self.file_path.get()).st_size == 0:
                    self.error_file_path.set('This file is empty')
                else:
                    self.error_file_path.set('')
                    self.prep_button.config(state='normal')
            except FileNotFoundError:
                self.error_file_path.set('File not found')
            except Exception:
                self.error_file_path.set('Please choose a different file')

    def call_preprocess(self, *args):
        """" call preProcess function in Cluster class.
         Operates a popup if the data cleaning process was successful or not """
        if (self.cluster.preProcess(self.file_path.get())):
            messagebox.showinfo("K Means Clustering", "Pre-Processing completed successfully!")
        else:
            messagebox.showerror("K Means Clustering", "There was a problem running the Pre-Processing")

    def call_cluster(self, *args):
        """" call clustering function in Cluster class.
         Operates a popup if the data clustering was successful or not """
        if (self.cluster.clustering(self.num_of_clusters, self.num_of_runs)):
            # show plots
            scatterImg = PIL.Image.open("scatter.png").resize((350, 300), PIL.Image.ANTIALIAS)
            self.scatter_pic = ImageTk.PhotoImage(scatterImg)
            self.scatter_pic_label.config(image=self.scatter_pic)

            worldImg=PIL.Image.open("map.png").resize((350, 300), PIL.Image.ANTIALIAS)
            self.world_pic=ImageTk.PhotoImage(worldImg)
            self.world_map_label.config(image=self.world_pic)

            response = messagebox.askquestion("K Means Clustering ",
                                              "Clustering completed successfully! Would you like to exit the program?",
                                              icon='warning')

            if response == "yes":
                self.master.destroy()

        else:
            messagebox.showerror("K Means Clustering", "There was a problem running the clustering")
