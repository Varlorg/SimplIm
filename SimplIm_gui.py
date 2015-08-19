#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This software is a little GUI using PIL and tkinter
# to modify Jpeg resolution and quality

import PIL.Image
import PIL.ImageTk as ImageTk
# import PIL.ImageTk as ImageTk
import os, sys, getopt
from tkinter import *
# import tkinter
import tkinter.messagebox
import tkinter.filedialog


class SimplIm(tkinter.Tk):
    def __init__(self):
        self.largeur = 0
        self.hauteur = 0
        self.m_largeur = False
        self.m_hauteur = False
        self.ratio = 0
        self.inputfile = ''
        self.output_file = 'resize'
        self.qualityValue = 85
        self.photo = ''
        self.photo_GS = ''

        Tk.__init__(self)
# Main window
        self.title("SimplIm")

# Création d'un Menu
        menubar = Menu(self)

        menufichier = Menu(menubar, tearoff=0)
        menufichier.add_command(label="Ouvrir une image", command=self.Ouvrir,
                                accelerator="Ctrl+O")
        menufichier.add_command(label="Convertir", command=self.Convertir,
                                accelerator="Ctrl+C")
        menufichier.add_command(label="Fermer l'image", command=self.Fermer,
                                accelerator="Ctrl+F")
        menufichier.add_command(label="Quitter", command=self.destroy,
                                accelerator="Ctrl+Q")
        menubar.add_cascade(label="Fichier", menu=menufichier)

        self.config(menu=menufichier)

# Ajout des raccourcis
        self.bind_all("<Control-q>", self.destroy)
        self.bind_all("<Control-c>", self.Convertir)
        self.bind_all("<Control-f>", self.Fermer)
        self.bind_all("<Control-o>", self.Ouvrir)

        menuaide = Menu(menubar, tearoff=0)
        menuaide.add_command(label="A propos", command=self.Apropos)
        menubar.add_cascade(label="Aide", menu=menuaide)

# Bouton Ouvrir Image
        BoutonOuvrir = Button(self, text='Ouvrir Image', command=self.Ouvrir)
        BoutonOuvrir.pack(side=tkinter.TOP, padx=5, pady=5)

        FrameAll = Frame(self, relief=GROOVE)
        FrameAll.pack()

# création d'un widget Frame  pour les différents paramètres modifiables dans la fenêtre principale
        FrameParameter = Frame(FrameAll, relief=GROOVE, width=450)
        FrameParameter.pack(side=LEFT, padx=10, pady=10)

# création d'un second widget Frame  pour l'affichage de l'image dans la fenêtre principale
        FrameImage = Frame(FrameAll, borderwidth=2, relief=GROOVE)
        FrameImage.pack(side=RIGHT, padx=10, pady=10)

        self.ValeurLargeur = IntVar()
        self.ValeurLargeur.set(0)
        self.ValeurLargeur.trace('w', self.maj_largeur)

        self.ValeurHauteur = IntVar()
        self.ValeurHauteur.set(0)
        self.ValeurHauteur.trace('w', self.maj_hauteur)

        self.ValeurQuality = IntVar()
        self.ValeurQuality.set(95)

        self.ValeurRatio_b = IntVar()
        self.ValeurRatio_b.set(0)
        self.ValeurRatio_b.trace('w', self.maj_largeur)

        self.ValeurGS = IntVar()
        self.ValeurGS.set(0)
        self.ValeurGS.trace('w', self.grayscale)

# Affichage du menu
        self.config(menu=menubar)

# Création d'un widget Canvas
        self.Canevas = Canvas(FrameImage, width=256, height=256)
        self.Canevas.pack(padx=5, pady=5)

# Ajout des paramètres modifiables par l'utilisateur
        Label(FrameParameter, text="Largeur").grid(row=0, column=0,
                                                   padx=10, pady=5)
        # pack(padx=10,pady=10,fill=X)
        boite = tkinter.Spinbox(FrameParameter, from_=0, to=10000, increment=1,
                                textvariable=self.ValeurLargeur, width=5)
        boite.grid(row=0, column=1)
        # pack(side = BOTTOM,padx=30,pady=10, fill=X)

        Label(FrameParameter, text="Hauteur").grid(row=1, column=0,
                                                   padx=10, pady=5)
        boite = tkinter.Spinbox(FrameParameter, from_=0, to=10000, increment=1,
                                textvariable=self.ValeurHauteur, width=5)
        boite.grid(row=1, column=1)

        Label(FrameParameter, text="Qualité").grid(row=2, column=0, padx=10, pady=5)
        boite = tkinter.Spinbox(FrameParameter, from_=0, to=95, increment=1,
                                textvariable=self.ValeurQuality, width=5)
        boite.grid(row=2, column=1)

        Label(FrameParameter, text="Conserver le ratio").grid(row=3, column=0,
                                                              padx=10, pady=5)
        c = tkinter.Checkbutton(FrameParameter, text="", variable=self.ValeurRatio_b)
        c.grid(row=3, column=1)

        Label(FrameParameter, text="Noir et Blanc").grid(row=4, column=0, padx=10, pady=5)
        c_grayscale = tkinter.Checkbutton(FrameParameter, text="", variable=self.ValeurGS)
        c_grayscale.grid(row=4, column=1)

# Nom des formats de sortie et création de bouttons radio
        output_format_list =["jpeg", "png", "gif"]
        self.format_output = StringVar()
        self.format_output.set("jpeg")

        Label(FrameParameter, text="Format de sortie :").grid(row=5, column=0, padx=10, pady=5)
        for n in range(3):
            bout = tkinter.Radiobutton(FrameParameter,
                            text = output_format_list[n],
                            variable = self.format_output,
                            value = output_format_list[n]) # ,
            bout.grid(row=5, column=n+1,pady=0, padx=0)

# Bouton Convertir
        BoutonConvert = Button(self, text='Convertir Image', command=self.Convertir)
        BoutonConvert.pack(side=BOTTOM, padx=5, pady=5, fill=X)

    def Ouvrir(self, event=None):
        # global photo, photoGS
        global im, filename
        size_thumbnail = 256, 256
        self.Canevas.delete(ALL)  # on efface la zone graphique

        filetypes_image = [
            ("Image Files", ("*.jpg", "*.JPG", "*.jpeg", "*.JPEG",
                             "*.png", "*.gif")),
            ("JPEG", '*.jpg'),
            ("PNG", '*.png'),
            ("GIF", '*.gif'),
            ('All', '*')
            ]
        filename = tkinter.filedialog.askopenfilename(title="Ouvrir une image",
                                                      filetypes=filetypes_image)
        print(filename)

        if filename is not None:
            im = PIL.Image.open(filename)
            im_thumb = im.copy()
            im_thumb.thumbnail(size_thumbnail, PIL.Image.ANTIALIAS)
            im_thumb_GS = im_thumb.copy().convert('L')
            self.photo = ImageTk.PhotoImage(im_thumb)
            self.photo_GS = ImageTk.PhotoImage(im_thumb_GS)
            self.Canevas.create_image(0, 0, anchor=NW, image=self.photo)
            self.Canevas.config(height=self.photo.height(),
                                width=self.photo.width())

            self.ValeurLargeur.set(im.size[0])
            self.ValeurHauteur.set(im.size[1])
            self.ratio = float(im.size[0]) / im.size[1]

    def grayscale(self, *args):
        # global photo, photo_GS
        if self.ValeurGS.get() == 1:
            self.Canevas.create_image(0, 0, anchor=NW, image=self.photo_GS)
        else:
            self.Canevas.create_image(0, 0, anchor=NW, image=self.photo)
# Mafenetre.title("Image "+str(photo.width())+" x "+str(photo.height()))

    def Fermer(self, *args):
        self.Canevas.delete(ALL)
        self.title("Image")

    def Apropos(self):
        tkinter.messagebox.showinfo("A propos", "SimplIm\n"\
                                    "Licence GNU GPL2\n"\
                                    "(C) Adrian Poiget")

    def Convertir(self, *args):
        # global ratio, im, filename
        global im, filename
        erreur = False

        try:
            self.photo
        except NameError:
            self.photo = None
            erreur = True
            tkinter.messagebox.showerror("Erreur fichier", "Largeur n'est pas valide")

        if self.photo is None:
            tkinter.messagebox.showerror("Erreur", "Pas de photo ouverte")
        else:
            print("Conversion")
            try:
                self.largeur = self.ValeurLargeur.get()
            except ValueError:
                erreur = True
                tkinter.messagebox.showerror("Erreur Dimension", "Largeur n'est pas valide")

            try:
                self.hauteur = self.ValeurHauteur.get()
            except ValueError:
                erreur = True
                tkinter.messagebox.showerror("Erreur Dimension", "Hauteur n'est pas valide")

            self.ratio_b = self.ValeurRatio_b.get()
            self.qualityValue = self.ValeurQuality.get()
            print(self.ratio_b)
            if self.ratio_b == 1:
                print('Keep ratio')
                if self.largeur != 0:
                    self.hauteur = int(self.largeur / self.ratio)
                elif self.hauteur != 0:
                    self.largeur = int(self.hauteur * self.ratio)
                else:
                    self.hauteur = im.size[1]
                    self.largeur = im.size[0]

            print(str(self.hauteur) + 'x' + str(self.largeur) + ' -- ' + str(self.ratio))

            if erreur is False: 
                out = im.resize((self.largeur, self.hauteur))
                out = out.convert('L')
                print(self.format_output)
                self.output_file = os.path.splitext(filename)[0] + '_resized.' + str(self.format_output.get())
# optimize=True, progressive=True
                out.save(self.output_file, self.format_output.get(), quality=self.qualityValue)


    def check_size(self, *args):

        global ValeurLargeur, ValeurHauteur
        print("Check size")
        print(str(self.ValeurLargeur.get()) + "---" + str(self.ValeurHauteur.get()))
        if self.ValeurLargeur.get() >= 10000:
            print("Largeur trop grande")
            self.ValeurLargeur.set(10000)
            self.ValeurHauteur.set(int(self.ValeurLargeur.get() / self.ratio))

        if self.ValeurHauteur.get() > 10000:
            print("Hauteur trop grande")
            self.ValeurHauteur.set(10000)
            self.ValeurLargeur.set(int(self.ValeurHauteur.get() / self.ratio))

    def maj_hauteur(self, *args):
        print('maj H' + str(self.m_largeur) + ' m ' + str(self.m_hauteur))
        try:
            print(str(self.ValeurLargeur.get()) + "---" + str(self.ValeurHauteur.get()))
            if self.ValeurRatio_b.get() == 1 and self.m_largeur is False:
                self.m_hauteur = True
                try:
                    if self.ValeurHauteur.get() != 0:
                        self.ValeurLargeur.set(int(self.ValeurHauteur.get() * self.ratio))
                        self.check_size(self, *args)

                    self.m_hauteur = False
                except ValueError:
                    self.m_hauteur = False
                    pass
        except ValueError:
            pass
        
    def maj_largeur(self, *args):
        print('maj L' + str(self.m_largeur) + ' m ' + str(self.m_hauteur))
        try:
            print(str(self.ValeurLargeur.get()) + "---" + str(self.ValeurHauteur.get()))
            if self.ValeurRatio_b.get() == 1 and self.m_hauteur is False:
                self.m_largeur = True
                try:
                    if self.ValeurLargeur.get() != 0:
                        self.ValeurHauteur.set(int(self.ValeurLargeur.get() / self.ratio))
                        print(str(self.ValeurLargeur.get()) + "--" + str(self.ratio))
                        self.check_size(self, *args)

                    self.m_largeur = False
                except ValueError:
                    self.m_largeur = False
                    pass
        except ValueError:
            pass


if __name__ == "__main__":
    app = SimplIm()
    app.mainloop()
