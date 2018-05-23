
# Mediia Player that can add, remove, play, stop, keep track of current media file and display and manage playlist.
# It supports media files in all formats
# Made with Python 3.6
# Author : Divya Agarwal

import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog
import os
import vlc

class Node:
 
    def __init__(self, data):

        '''
        Objective : Function to initialise the node object
        Input Parameters :
                            data : assigns data to node
        Return value : None
        '''
        
        self.data = data  # Assign data
        self.next = None  # Initialize next as null
        self.prev = None  # Initialize prev as null


# Playlist class contains a Node object
class playlist:

    '''
    Objective : class to create playlist of nodes
    approach : implemented as a doubly linked list
    '''
    
    def __init__(self,application_window):

        '''
        Objective : Funcion to initilaise playlist object and creates gui for media player
        Input parameters :
                            application_window : application window where gui is implemented
        Return value : None
        '''

        #head of playlist
        self.head = None

        #last node in playlist
        self.tail = None

        #current pointer which points to current file played 
        self.curr_pointer = None

        #temporary buffer to store currently playing media file
        self.temp_playing = None

        # to keep total count of nodes
        self.count = 0

        
        self.application_window = application_window
        
        application_window.title("Media Player")

        self.label = Label(application_window, text="\n\tMEDIA PLAYER\t\t\n", font='Helvetica 15 bold')
        self.label.pack()

        self.add_button = Button(application_window, text="Add", command=self.addMedia, bg="black", fg="white", height = 2, width = 10, font='Helvetica  10 bold')
        self.add_button.pack(fill=X, padx=10, pady=10, side=LEFT)

     
        self.play_button = Button(application_window, text="Play", command=self.playMedia, bg="black", fg="white", height = 2, width = 10, font='Helvetica  10 bold')
        self.play_button.pack(fill=X, padx=10, pady=10, side=LEFT)
  
        self.stop_button = Button(application_window, text="Stop", command=self.stopMedia, bg="black", fg="white", height = 2, width = 10, font='Helvetica  10 bold')
        self.stop_button.pack(fill=X, padx=10, pady=10, side=LEFT)
 

        self.playNext_button = Button(application_window, text="Play Next",  command=self.playNext, bg="black", fg="white", height = 2, width = 10, font='Helvetica  10 bold')
        self.playNext_button.pack(fill=X, padx=10, pady=10, side=LEFT)
     

        self.playPrev_button = Button(application_window, text="Play Previous",  command=self.playPrev, bg="black", fg="white", height = 2, width = 10, font='Helvetica  10 bold')
        self.playPrev_button.pack(fill=X, padx=10, pady=10, side=LEFT)
  

        self.remove_button = Button(application_window, text="Remove", command=self.removeMedia, bg="black", fg="white", height = 2, width = 10, font='Helvetica  10 bold')
        self.remove_button.pack(fill=X, padx=10, pady=10, side=LEFT)
    
        self.label = Label(application_window, text="\nPLAYLIST\n",  height = 2, width = 10, bg="#00cccc", font='Helvetica  13 bold')
        self.label.pack()
        self.displayAllMedia = Listbox(application_window, width=80)
        self.displayAllMedia.pack()
        self.displayAllMedia.bind("<Button-1>",self.display)
        
        
        self.close_button = Button(application_window, text="Close", command=application_window.quit)
        self.close_button.pack()

        self.label = Label(application_window, text="\n\tAuthor  :  Divya Agarwal\t\t\n", font='Helvetica  10 bold')
        self.label.pack()


    
    def addMedia(self):

        '''
        Objective : function to add media files at the end in playlist
        Input Parameters : None
        Return value : None

        approach : it asks user to select a file, then store its path in node of playlist. And append to previous nodes
        '''

        # Build a list of tuples for each file type the file dialog should display
        my_filetypes = [('media files', '.*')]

        # Ask the user to select a single file name.
        answer = filedialog.askopenfilename(initialdir=os.getcwd(), title="Please select a file:", filetypes=my_filetypes)


        #checking the condition if the user presses Cancel and no file is selected then don't add node
        if len(answer) > 1 :

            newNode = Node(answer)       #storing file path in playlist nodes
            self.count = self.count+1
            
            # if playlist is empty and no node is there
            if self.head == None :
                self.head = newNode
                self.tail = newNode
                self.curr_pointer = newNode

            else :
                self.tail.next = newNode
                newNode.prev = self.tail
                self.tail = newNode      



    def playMedia(self):

        '''
        Objective : function to play media file in playlist
        Input Parameters : None
        Return value : None

        approach : plays media file according to curr_pointer position. It picks address of file from node and use it to play file.
        '''
        
        # if playlist is empty and no node there
        if self.curr_pointer == None :
             messagebox.showinfo("CANNOT PLAY!", "No file added in playlist")
        else:
             self.temp_playing = vlc.MediaPlayer(self.curr_pointer.data)
             self.temp_playing.play()

                

    def stopMedia(self):
    	
        '''
        Objective :  function to stop media file currently playing
        Input Parameters : None
        Return value : None
        '''
 
        # if playlist is empty and no node there
        if self.curr_pointer == None :
            messagebox.showinfo("NO FILE!", "No file added in playlist")
        else:
             self.temp_playing.stop()

 	
        
    def playNext(self):

        '''
        Objective : function to play next media file in playlist
        Input Parameters : None
        Return value : None

        approach : plays next media file according to next of curr_pointer position. If next is null i.e. if reached at the end of playlist then restart from head. Sets current pointer to head
        '''


        # if playlist is empty
        if self.curr_pointer == None :
             messagebox.showinfo("CANNOT PLAY!", "No file added in playlist")
             
        else:

            # if next of current pointer is available
            if self.curr_pointer.next != None :
                self.curr_pointer = self.curr_pointer.next

            # if next of curr_pointer is none then set curr_pointer to head i.e. if reached at last then go to head
            else:
                self.curr_pointer = self.head
 			
 	    # if media file is already playing then stop it and then play next file
            if self.temp_playing != None:
                self.stopMedia()
            
            self.playMedia()
  

      

    def playPrev(self):

        '''
        Objective : function to play previous media file in playlist
        Input Parameters : None
        Return value : None

        approach : plays previous media file according to prev of curr_pointer position. If prev is null i.e. if reached at the head of playlist then go to last of playlist.
        '''

        # if playlist is empty
        if self.curr_pointer == None :
             messagebox.showinfo("CANNOT PLAY!", "No file added in playlist")
             
        else:

            # if prev of current pointer is available
            if self.curr_pointer.prev != None :
                self.curr_pointer = self.curr_pointer.prev

            # if prev of curr_pointer is none then set curr_pointer to tail i.e. if reached at head then go to last of playlist
            else :
                self.curr_pointer = self.tail

 	    # if media file is already playing then stop it and then play next file
            if self.temp_playing != None:
                self.stopMedia()
            
            self.playMedia()
            


    def removeMedia(self):

        '''
        Objective : function to delete last media file in playlist
        Input Parameters : None
        Return value : None

        approach : deletes last node of playlist
        '''

        # if playlist is not empty
        if self.head != None :

             #self.e = Entry(application_window,justify = CENTER)
             #self.e.pack(fill=X, padx=10, pady=10, side = LEFT)

             pos = simpledialog.askinteger("Remove", "Enter position :", parent=application_window, minvalue=0, maxvalue=self.count)


             if(pos > int(self.count)):
                 messagebox.showinfo("WRONG VALUE ENTERED", "Enter value between 1 and ",self.count)

             else:
                 temp = self.head  #initializing temp with head

                 if pos == 1:     #head is to be deleted

                     temp = self.head

                     # 1 node
                     if self.head == self.tail:
                         self.head = None
                         self.tail = None
                         self.curr_pointer = None
                         
                     # more than 1 node
                     else :
                         self.head = self.head.next
                         self.head.prev = None

                         if self.curr_pointer == temp :
                             self.curr_pointer = self.head

                     del temp
                     self.count = self.count-1

                         
                 elif pos == int(self.count):     #tail is to be deleted and it is a case with more than one node
                     temp = self.tail
                     self.tail = self.tail.prev
                     self.tail.next = None

                     if self.curr_pointer == temp:
                         self.curr_pointer = self.head

                     del temp
                     self.count = self.count-1

                     
                 #when position is between head and tail
                 else:

                     temp = self.head
                     pos = pos-1

                     # traversing till pos position
                     while(pos):
                         temp = temp.next
                         pos = pos-1

                     temp.prev.next = temp.next
                     temp.next.prev = temp.prev

                     if self.curr_pointer == temp:
                         self.curr_pointer = temp.next

                     del temp
                     self.count = self.count-1

        else:
            messagebox.showinfo("EMPTY!", "Playlist is empty")



    def display(self,event) :

        '''
        Objective : function to display all media files with their addresses in playlist
        Input Parameters : 
        					event : this function is triggered when respective event occurs (in this case one-click in listbox area)
        Return value : None

        approach : displays data in all nodes
        '''

        self.displayAllMedia.delete(0, END)     #deleting previous displays in listbox
        temp = self.head

        # if list is not empty
        if temp != None :

            i = 1	# maintains order in which data will be displayed

            # display data from head to tail
            while(temp):
                self.displayAllMedia.insert(i,i,temp.data)
                temp = temp.next
                i=i+1

            
        

application_window = tk.Tk()

# display image 
bg_image = PhotoImage(file ="tenor.gif")
x = Label (application_window,image = bg_image,bg="black")
x.pack(fill=BOTH)


application_window.configure(bg="#00cccc")

my_mediaPlayer = playlist(application_window)
application_window.mainloop()
