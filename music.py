from tkinter import *
from pygame import mixer
from tkinter import filedialog
import os
import tkinter.messagebox
from mutagen.mp3 import MP3
import time
import threading
from tkinter import ttk
from ttkthemes import themed_tk as tk
root=tk.ThemedTk()
root.get_themes()
root.set_theme('smog')
mixer.init() #inisialization
root.title("Music Player")
root.iconbitmap(r'C:\Users\Vasu Dadhich\Desktop\GUI project\Music_Player\musical-note.ico')
menubar=Menu(root)
root.config(menu=menubar)
#create sub
submenu=Menu(menubar,tearoff=0)
menubar.add_cascade(label="File",menu=submenu)
Playlist=[]
f1=Frame(root)
f1.pack(side=RIGHT,padx=7)
f2=Frame(root)
f2.pack(side=LEFT)
def open():
    global filename
    filename=filedialog.askopenfilename()
    Add_Playlist(filename)
def Add_Playlist(f):
    f=os.path.basename(f)
    index=0
    playlistbox.insert(index,f)
    playlistbox.pack()
    Playlist.insert(index,filename)
    index+=1



    
submenu.add_command(label="Open",command=open)
submenu.add_command(label="Exit",command=root.destroy)
submenu=Menu(menubar,tearoff=0)
menubar.add_cascade(label="Help",menu=submenu)
def About():
    tkinter.messagebox.showinfo("About","This Music Player Made By Python Tkinter By:\nInstagram: @_dadhich_boy_\nGmail: vasudadhich2000@gmail.com")
submenu.add_command(label="About Us",command=About)

L1=ttk.Label(f1,text="Total Time: --:--")
L1.pack(padx=7,pady=7)
L2=ttk.Label(f1,text="Current Time: --:--")
L2.pack(padx=7,pady=7)

#lstbox=Listbox(f2)
#lstbox.pack(padx=10)
playlistbox=Listbox(f2)
playlistbox.pack(padx=10)
btn1=ttk.Button(f2,text="+ Add",command=open)
btn1.pack(side=LEFT,padx=10)
def delete():
     select_song=playlistbox.curselection()
     select_song=int(select_song[0])
     playlistbox.delete(select_song)
     Playlist.pop(select_song)
    
btn2=ttk.Button(f2,text="- Del",command=delete)
btn2.pack(side=LEFT,padx=10)


m_frame=Frame(f1)
m_frame.pack(padx=7,pady=7)
img_play=PhotoImage(file='play.png')
def play():
    global pause
    if pause==True:
        mixer.music.unpause()
        status['text']="Music Resumed"
        pause=False
    else:
        try:
            stop()
            time.sleep(1)
            select_song=playlistbox.curselection()
            select_song=int(select_song[0])
            play_it=Playlist[select_song]
            
            mixer.music.load(play_it)
            mixer.music.play()
            status['text']='Playing Music'+'...'+os.path.basename(play_it)
            Showdetail(play_it) 
        except:
            tkinter.messagebox.showerror("Wrong file","Select Right File")

def Showdetail(play_song):
    L1['text']='Total Time'+os.path.basename(play_song)
    file_data=os.path.splitext(play_song)
    if file_data[1]== '.mp3':
        audio=MP3(play_song)
        total_length=audio.info.length
    else:
        a=mixer.sound(play_song)
        total_length=a.get_length()
    
    mint,sec=divmod(total_length,60)
    mint=round(mint)
    sec=round(sec)
    timeformat='{:02d}:{:02d}'.format(mint,sec)
    L1['text']='Total Time:'+' - '+ timeformat
    t1 = threading.Thread(target=Start_count, args=(total_length,))
    t1.start()
    
def Start_count(t):
    global pause
    
    current_time = 0
    while  current_time <= t and mixer.music.get_busy():
        if pause==True:
            continue
        else:
            mint, sec = divmod(current_time, 60)
            mint = round(mint)
            sec = round(sec)
            timeformat = '{:02d}:{:02d}'.format(mint,sec)
            L2['text'] = "Current Time" + ' - ' + timeformat
            time.sleep(1)
            current_time += 1
    
btn_play=ttk.Button(m_frame,image=img_play,command=play)
btn_play.grid(row=0,column=1,padx=7,pady=7)
img_stop=PhotoImage(file='Stop.png')
def stop():
    mixer.music.stop()
    status['text']="Music Is Stoped"
btn_stop=ttk.Button(m_frame,image=img_stop,command=stop)
btn_stop.grid(row=0,column=2,padx=7,pady=7)
img_pause=PhotoImage(file='pause.png')
pause=False
def pause():
    global pause
    pause= True
    mixer.music.pause()
    status['text']="Music Paused"
btn_pause=ttk.Button(m_frame,image=img_pause,command=pause)
btn_pause.grid(row=0,column=3,padx=7,pady=7)
def vol(event):
    vol=float(event)/100
    mixer.music.set_volume(vol)
B_frame=Frame(f1)
B_frame.pack(padx=7,pady=7)
scale=ttk.Scale(B_frame,from_=0,to=100,orient=HORIZONTAL,command=vol)
scale.set(80)
scale.grid(row=0,column=2,padx=7,pady=7)
status=ttk.Label(f1,text="Vasu Dadhich's Music Player",relief=SUNKEN,anchor=W)
status.pack(side=BOTTOM,fill=X)
img_rewind=PhotoImage(file='rewind.png')
def rewind():
    play()
    status['text']="Music Rewind"
btn_rewind=ttk.Button(B_frame,image=img_rewind ,command=rewind)
btn_rewind.grid(row=0,column=0,padx=7,pady=7)
img_mute=PhotoImage(file='mute.png')
img_unmute=PhotoImage(file='unmute.png')
muted=False
def mute():
    global muted
    if muted:
        scale.set(80)
        mixer.music.set_volume(0.8)
        btn_mute.config(image=img_unmute)
        muted=False
    else:
        scale.set(0)
        mixer.music.set_volume(0)
        btn_mute.config(image=img_mute)
        muted=True
        
btn_mute=ttk.Button(B_frame,image=img_unmute,command=mute)
btn_mute.grid(row=0,column=1,padx=7)

def on_closing():
    stop()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
