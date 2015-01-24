#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This software is a little GUI using PIL and tkinter to modify Jpeg resolution and quality

import PIL.Image 
import PIL.ImageTk as ImageTk
#import PIL.ImageTk as ImageTk
import os, sys, getopt
from tkinter import *
import tkinter.messagebox
import tkinter.filedialog


def Ouvrir():
    global photo, ratio, im, filename
    size_thumbnail = 256, 256
    Canevas.delete(ALL) # on efface la zone graphique
    
    filetypes_image = [
            ("Image Files", ("*.jpg", "*.JPG", "*.jpeg","*.JPEG")),
            ("JPEG",'*.jpg'),
            ("GIF",'*.gif'),
            ('All','*')
            ] 
    filename = tkinter.filedialog.askopenfilename(title="Ouvrir une image",filetypes=filetypes_image)
    print(filename)
    
    im = PIL.Image.open(filename)
    im_thumb =  im.copy()
    im_thumb.thumbnail(size_thumbnail, PIL.Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(im_thumb)
    Canevas.create_image(0,0,anchor=NW,image=photo)
    Canevas.config(height=photo.height(),width=photo.width())

    ValeurLargeur.set(im.size[0])
    ValeurHauteur.set(im.size[1])
    ratio = float(im.size[0]) / im.size[1]

    #Mafenetre.title("Image "+str(photo.width())+" x "+str(photo.height()))

def Fermer():
    Canevas.delete(ALL)
    Mafenetre.title("Image")

def Apropos():
    tkinter.messagebox.showinfo("A propos","SimplIm\n(C) Adrian Poiget")

def Convertir():
    global photo,ratio, im, filename
    try:
        photo
    except NameError:
        photo=None

    if photo == None:
        tkinter.messagebox.showerror("Erreur","Pas de photo ouverte")
    else:
        print("Conversion")
        largeur = ValeurLargeur.get()
        hauteur = ValeurHauteur.get()
        ratio_b = ValeurRatio_b.get()
        qualityValue = ValeurQuality.get()
        print(ratio_b)
        if ratio_b == 1: 
            print('Keep ratio')
            if largeur != 0:
                hauteur = int (largeur / ratio)   
            elif hauteur != 0:
                largeur = int (hauteur * ratio)   
            else:
                hauteur = im.size[1]
                largeur = im.size[0]

        print(str(hauteur) + 'x' + str(largeur) + ' -- ' + str(ratio))

        out = im.resize((hauteur,largeur))
        output_file = os.path.splitext(filename)[0] + '_resized.'+format_output
##optimize=True, progressive=True
        out.save(output_file, format_output, quality = qualityValue )

def maj_hauteur(a,b,c):
    global ratio, ValeurRatio_b
    try:
        if ValeurRatio_b.get() == 1 and ValeurHauteur.get() != 0:
            ValeurLargeur.set(int(ValeurHauteur.get() * ratio))
    except ValueError:
        pass

def maj_largeur(a,b,c):
    global ratio, ValeurRatio_b
    try:
        if ValeurRatio_b.get() == 1:
            ValeurHauteur.set(int(ValeurLargeur.get() / ratio))
    except ValueError:
        pass


global Canevas
largeur = 0
hauteur = 0
ratio = 0
inputfile = ''
output_file = 'resize'
qualityValue = 85
format_output  = 'jpeg'

# Main window
Mafenetre = Tk()
Mafenetre.title("SimplIm")

# Création d'un widget Menu
menubar = Menu(Mafenetre)

menufichier = Menu(menubar,tearoff=0)
menufichier.add_command(label="Ouvrir une image",command=Ouvrir)
menufichier.add_command(label="Fermer l'image",command=Fermer)
menufichier.add_command(label="Quitter",command=Mafenetre.destroy)
menubar.add_cascade(label="Fichier", menu=menufichier)

menuaide = Menu(menubar,tearoff=0)
menuaide.add_command(label="A propos",command=Apropos)
menubar.add_cascade(label="Aide", menu=menuaide)

#Bouton Ouvrir Image
BoutonOuvrir = Button(Mafenetre, text ='Ouvrir Image', command = Ouvrir)
BoutonOuvrir.pack(side = TOP, padx = 5, pady = 5)

FrameAll = Frame(Mafenetre, relief=GROOVE)
FrameAll.pack()

# création d'un widget Frame dans la fenêtre principale
FrameParameter = Frame(FrameAll,relief=GROOVE,width=450)
#FrameParameter.pack_propagate(0)
FrameParameter.pack(side=LEFT,padx=10,pady=10)

# création d'un second widget Frame dans la fenêtre principale
FrameImage = Frame(FrameAll,borderwidth=2,relief=GROOVE )
FrameImage.pack(side=RIGHT,padx=10,pady=10)

ValeurLargeur = IntVar()
ValeurLargeur.set(0)
ValeurLargeur.trace('w',maj_largeur)

ValeurHauteur = IntVar()
ValeurHauteur.set(0)
ValeurHauteur.trace('w',maj_hauteur)

ValeurQuality = IntVar()
ValeurQuality.set(95)

ValeurRatio_b = IntVar()
ValeurRatio_b.set(0) 
ValeurRatio_b.trace('w',maj_largeur)

# Affichage du menu
Mafenetre.config(menu=menubar)

# Création d'un widget Canvas
Canevas = Canvas(FrameImage, width=256, height=256)
Canevas.pack(padx=5,pady=5)

Label(FrameParameter,text="Largeur").grid(row = 0 , column = 0 , padx = 10, pady = 5)#pack(padx=10,pady=10,fill=X)
boite = Spinbox(FrameParameter,from_=0,to=10000,increment=1,textvariable=ValeurLargeur,width=5)
boite.grid(row=0,column=1)#pack(side = BOTTOM,padx=30,pady=10, fill=X)

Label(FrameParameter,text="Hauteur").grid(row=1, column=0, padx=10, pady=5)
boite = Spinbox(FrameParameter,from_=0,to=10000,increment=1,textvariable=ValeurHauteur,width=5)
boite.grid(row=1,column=1)

Label(FrameParameter,text="Qualité").grid(row=2, column=0, padx=10, pady=5)
boite = Spinbox(FrameParameter,from_=0,to=95,increment=1,textvariable=ValeurQuality,width=5)
boite.grid(row=2,column=1)

Label(FrameParameter,text="Conserver le ratio").grid(row=3, column=0, padx=10, pady=5)
c = Checkbutton(FrameParameter, text="", variable=ValeurRatio_b)
c.grid(row=3,column=1)


#Bouton Convertir
BoutonConvert= Button(Mafenetre, text ='Convertir Image', command = Convertir)
BoutonConvert.pack(side = BOTTOM, padx = 5, pady = 5,fill=X)

Mafenetre.mainloop()

