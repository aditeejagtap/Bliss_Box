from tkinter import *
import pygame
import os
from tkinter import filedialog, Button
from tkinter import ttk
from PIL import Image, ImageTk
import tkinter.messagebox
from ttkthemes import themed_tk as tk
from ttkthemes import ThemedStyle
from mutagen.mp3 import MP3
import time

# from progress.bar import IncrementalBar

#root = tk.ThemedTk('clam')
root =Tk()
root.title('Bliss Box - MP3 Player')
root.geometry('320x450')
photo = ImageTk.PhotoImage(Image.open("images/logo.png"))
root.iconphoto(True, photo)

bgcolour = '#ADB3BD'
stat_bg = '#7D8089'
list_bg = '#3A3B50'
root.config(bg=bgcolour)

# style = ThemedStyle(root)
# style.set_theme("vista")

pygame.mixer.init()

#status_img = ImageTk.PhotoImage(Image.open("bg.jpg").resize((500, 20)))
statusbar = ttk.Label(root, text="Welcome to Bliss Box", anchor=W, font='Times 12 ', background=stat_bg )
statusbar.pack(side=BOTTOM, fill=X)

playlist = []



def add_songs():
    songs = filedialog.askopenfilenames(initialdir='D:/songs', title="Select Songs",
                                        filetypes=(('mp3 files', '*.mp3'),))
    global s
    for s in songs:
        filename = os.path.basename(s)
        index = 0
        songs_list.insert(index, filename)
        playlist.insert(index, s)
        index+=1


songs_list = Listbox(root, fg='#E2EAED', bg=list_bg, width=37, font='Helvetica 11 italic', selectforeground='#FFFFFF',
                     activestyle = 'dotbox', relief=RAISED)



scroll = Scrollbar(root)
scroll.pack(side=RIGHT, fill=BOTH)
songs_list.config(yscrollcommand=scroll.set)
songs_list.pack(pady=5)
scroll.config(command=songs_list.yview)


cur_playing = Label(root, text='Song Name', fg='black', bg=bgcolour, width=20,
                  font = 'Italic 15 underline bold',justify=LEFT)

cur_playing.pack(pady=10)

global paused
paused = FALSE

def play():
    global paused
    if paused == TRUE:
        pygame.mixer.music.unpause()
        selected_song = songs_list.curselection()
        selected_song = int(selected_song[0])
        play_it = playlist[selected_song]

        statusbar['text'] = "Bliss Box - Playing "
        name = os.path.basename(play_it)
        cur_playing.config(text=name[0:20])
        paused = FALSE

    else:
        try:
            selected_song = songs_list.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]

            pygame.mixer.music.load(play_it)
            pygame.mixer.music.play()
            statusbar['text'] = "Bliss Box - Playing "
            name = os.path.basename(play_it)
            cur_playing.config(text=name[0:20])

        except:
            tkinter.messagebox.showerror('File not found', 'Player could not find the file. Please check again.')


def stop():
    pygame.mixer.music.stop()

    statusbar['text'] = "Bliss Box - Stopped"


def rewind():
    pygame.mixer.music.rewind()
    statusbar['text'] = "Music Rewinded"


def pausesong():
    global paused
    paused = TRUE
    pygame.mixer.music.pause()
    statusbar['text'] = "Bliss Box - Paused"


def next_():
    try:
        selected_song = songs_list.curselection()
        selected_song = int(selected_song[0])
        next_song = selected_song + 1

        play_it = playlist[next_song]

        pygame.mixer.music.load(play_it)
        pygame.mixer.music.play()

        songs_list.selection_clear(0, END)
        songs_list.select_set(next_song)
        songs_list.activate(next_song)

        statusbar['text'] = "Bliss Box - Playing "
        name = os.path.basename(play_it)
        cur_playing.config(text=name[0:20])

    except IndexError:
        tkinter.messagebox.showerror('File not found', 'This is the last song of playlist')


def prev_():
    try:
        selected_song = songs_list.curselection()
        selected_song = int(selected_song[0])
        next_song = selected_song - 1

        play_it = playlist[next_song]

        pygame.mixer.music.load(play_it)
        pygame.mixer.music.play()

        songs_list.selection_clear(0, END)
        songs_list.select_set(next_song)
        songs_list.activate(next_song)

        statusbar['text'] = "Bliss Box - Playing "
        name = os.path.basename(play_it)
        cur_playing.config(text=name[0:20])
    except IndexError:
        tkinter.messagebox.showerror('File not found', 'This is the first song of playlist')



def set_vol(val):
    volume = float(val) / 100
    pygame.mixer.music.set_volume(volume)


muted =FALSE


def mute_music():
    global muted
    if muted:  # Unmute the music
        pygame.mixer.music.set_volume(50)
        volumeBtn.configure(image=volumephoto)
        scale.set(50)
        muted = FALSE
    else:  # mute the music
        pygame.mixer.music.set_volume(0)
        volumeBtn.configure(image=mutephoto)
        scale.set(0)
        muted = TRUE


volumephoto =ImageTk.PhotoImage(Image.open("images/volume.png").resize((30, 30)))
mutephoto =ImageTk.PhotoImage(Image.open("images/mute.png").resize((30, 30)))


def del_song():
    try:
        selected_song = songs_list.curselection()
        selected_song = int(selected_song[0])
        songs_list.delete(selected_song)
        stop()
    except:
        tkinter.messagebox.showerror('File not found', 'Please select file from the playlist first')





'''
def play_time():
    current_song =  songs_list.curselection()
    current_time = pygame.mixer.music.get_pos() / 1000

    converted_current_time = time.strftime('%m:%s', time.gmtime(current_time))

    song= songs_list.get(current_song)
    song =MP3(song)
    song_length =song.info.length
    converted_song_length  = time.strftime('%m:%s', time.gmtime(song_length))

    time_bar.config(text=f+'{converted_current_time} // {converted_song_length}')
    time_bar.after(1000, play_time())


time_bar = Label(root, text="Time", bd=1, relief=GROOVE, anchor=E)
time_bar.pack(fill=X, side=BOTTOM, ipady=2)
'''
control_frame = Frame(root, background=bgcolour)
control_frame.pack(pady=25)

prev_img = ImageTk.PhotoImage(Image.open("images/prev.png").resize((50, 50)))
pause_img = ImageTk.PhotoImage(Image.open("images/pause.png").resize((50, 50)))
play_img = ImageTk.PhotoImage(Image.open("images/play.png").resize((42,42)))
stop_img = ImageTk.PhotoImage(Image.open("images/stop.png").resize((50, 50)))
next_img = ImageTk.PhotoImage(Image.open("images/next.png").resize((50, 50)))

# Create Buttons
prev_button = Button(control_frame, image=prev_img, borderwidth=0, background=bgcolour,activebackground=bgcolour, command=prev_)
pause_button = Button(control_frame, image=pause_img, borderwidth=0, background=bgcolour, activebackground=bgcolour, command=pausesong)
play_button = Button(control_frame, image=play_img, borderwidth=0, background=bgcolour,activebackground=bgcolour,  command=play)
stop_button = Button(control_frame, image=stop_img, borderwidth=0, background=bgcolour,activebackground=bgcolour, command=stop)
next_button = Button(control_frame, image=next_img, borderwidth=0, background=bgcolour,activebackground=bgcolour, command=next_)


prev_button.grid(column=1, row=3)
pause_button.grid(column=2, row=3)
play_button.grid(column=3, row=3)
stop_button.grid(column=4, row=3)
next_button.grid(column=5, row=3)

volumeBtn = Button(root, image=volumephoto, borderwidth=0,background=bgcolour,activebackground=bgcolour, command=mute_music)
volumeBtn.pack(side=LEFT, padx=5)

scale = ttk.Scale(from_=0, to=100, orient=HORIZONTAL, cursor='dot',  command=set_vol)
#bg='#1E222C', fg='#80868B', activebackground='#9AA0A6',
scale.set(40)
scale.pack(side=LEFT, padx=10,pady=10)

# Adding Menus
my_menu = Menu(root)
root.config(menu= my_menu)

files = Menu(my_menu)
my_menu.add_cascade(label='File', menu=files)
files.add_command(label="New ", command=add_songs)
files.add_command(label="Delete", command=del_song)

def about():
    tkinter.messagebox.showinfo('About us', 'This music player is build using Python Tkinter ')


my_menu.add_cascade(label='About us', command=about)


def exit_():
    stop()
    root.destroy()


my_menu.add_cascade(label='Exit', command=exit_)

# scale = Scale(from_=0, to=100, orient=HORIZONTAL, width=15, activebackground="skyblue", highlightbackground="skyblue",
# relief=RAISED ,cursor='dot', command=set_vol)




root.mainloop()
