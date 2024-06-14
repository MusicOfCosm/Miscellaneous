#SMILES: https://en.wikipedia.org/wiki/Simplified_molecular-input_line-entry_system

import pubchempy as pcp

# n = pcp.get_compounds('Fructose', 'name')
# n = int(str(n[0])[9:-1])
# print(n)


# # c = pcp.Compound.from_cid(5793) #glucose
# c = pcp.Compound.from_cid(2723872)
# # print(c.molecular_formula)
# print(type(c))
# print(c.isomeric_smiles)

#Had to redownload rdkit with pip, old name was rdkit-pypi
from rdkit import Chem, DataStructs
from rdkit.Chem import Draw, Descriptors, AllChem
# import rdkit.Chem.Draw.IPythonConsole
import numpy as np

from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)
import os


def setup(title, root): #Just to gain some space
    root.title(title)
    root.iconbitmap('../Rosace.ico')
    root.state('zoom') #basically fullscreen but with the buttons on top, 'zoomed' does the same

    global canvas
    global scroll
    global content

    canvas = Canvas(root)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)

    scroll = ttk.Scrollbar(root, orient=VERTICAL, command=canvas.yview)
    scroll.pack(side=RIGHT, fill=Y)

    canvas.config(yscrollcommand=scroll.set) #configure and config do the same thing
    canvas.bind('<Configure>', lambda event: canvas.config(scrollregion=canvas.bbox('all'))) #e: event, bbox: bounding box

    from sys import platform
    if platform.startswith('win'):
        canvas.bind_all('<MouseWheel>', lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))
    else: canvas.bind_all('<MouseWheel>', lambda event: canvas.yview_scroll(int(-1*(event.delta/1)), "units"))

    def reset_scrollregion(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    content = Frame(canvas)
    content.bind("<Configure>", reset_scrollregion)
    canvas.create_window((0,0), window=content, anchor='nw')

img_global_list = []

def get_to_draw(root):
    root.destroy()
    Draw_molecules()

def draw_to_get(root):
    root.destroy()
    Get_molecules()

def Get_molecules():
    root = Tk()
    setup('Molecule from name', root)

    def formulae(name, zoom):
        try: 
            mol = pcp.get_compounds(name.get(), 'name')
            print(mol)
            mol = int(str(mol[0])[9:-1])

            compound = pcp.Compound.from_cid(mol)
            print(compound.molecular_formula)
            smiles = compound.isomeric_smiles
            print(smiles, end='\n\n')

            template = Chem.MolFromSmiles(smiles)

            image = Draw.MolToImage(template, (zoom.get(), zoom.get()))
            image.save('temp_image.png')
            image = 'temp_image.png'

            global img
            img = ImageTk.PhotoImage(Image.open(image))
            render.config(image=img)
            img_global_list.append(img)
        except:
            render.config(image='')

    Label(content, text="Enter a molecule's name")
    var = StringVar()
    zoom = IntVar(content, 500)

    write_in = ttk.Entry(content, textvariable=var, justify=CENTER, width=30)#, cursor='question_arrow')
    write_in.pack()
    write_in.bind('<Return>', lambda event, var=var, zoom=zoom: formulae(var, zoom))

    render = Label(content, image='')
    render.pack()

    import webbrowser
    link = Label(content, text="SMILES", fg='blue', cursor='hand2')
    link.pack()
    link.bind('<Button-1>', lambda event: webbrowser.open_new_tab('https://en.wikipedia.org/wiki/Simplified_molecular-input_line-entry_system'))

    def zooming(yes):
        if yes:
            zoom.set(zoom.get() + 100)
        else: 
            zoom.set(zoom.get() - 100)

        formulae(var, zoom)

    Z_in = ttk.Button(content, text='Zoom in', command=lambda: zooming(True))
    Z_in.pack()
    Z_out = ttk.Button(content, text='Zoom out', command=lambda: zooming(False))
    Z_out.pack()

    ttk.Label(content, width=190).pack()

    ttk.Button(content, text='Draw molecules', command=lambda: get_to_draw(root)).pack()

    ttk.Label(content, width=190).pack()

    '''
    Fun molecules:

    teicoplanin
    vitamin B12
    iberiotoxin (a little bugged)
    somatorelin (bugged)
    calcitonin (bugged)
    '''

    root.mainloop()



def Draw_molecules():
    root = Tk()
    setup('Molecule from SMILES', root)

    def formulae(smiles, zoom):
        try: 
            template = Chem.MolFromSmiles(smiles.get())
            
            image = Draw.MolToImage(template, (zoom.get(), zoom.get()))
            image.save('temp_image.png')
            image = 'temp_image.png'

            global img
            img = ImageTk.PhotoImage(Image.open(image))
            render.config(image=img)
            img_global_list.append(img)
        except: pass

    var = StringVar()
    zoom = IntVar(content, 500)

    write_in = ttk.Entry(content, textvariable=var, justify=CENTER, width=30)#, cursor='question_arrow')
    write_in.pack()

    write_in.bind('<KeyRelease>', lambda event, var=var, zoom=zoom: formulae(var, zoom))

    render = Label(content, image='')
    render.pack()

    import webbrowser
    link = Label(content, text="SMILES", fg='blue', cursor='hand2')
    link.pack()
    link.bind('<Button-1>', lambda event: webbrowser.open_new_tab('https://en.wikipedia.org/wiki/Simplified_molecular-input_line-entry_system'))

    def zooming(yes):
        if yes:
            zoom.set(zoom.get() + 100)
        else: 
            zoom.set(zoom.get() - 100)

        formulae(var, zoom)

    Z_in = ttk.Button(content, text='Zoom in', command=lambda: zooming(True))
    Z_in.pack()
    Z_out = ttk.Button(content, text='Zoom out', command=lambda: zooming(False))
    Z_out.pack()

    ttk.Label(content, width=190).pack()

    bt = ttk.Button(content, text='Get molecule from name', command=lambda: draw_to_get(root))
    bt.pack()

    ttk.Label(content, width=190).pack()

    root.mainloop()

root = Tk()
setup("What would you like to do?", root)
ttk.Label(content, width=190).pack()

bt1 = ttk.Button(content, text='Draw molecules', command=lambda: get_to_draw(root))
bt2 = ttk.Button(content, text='Get molecule from name', command=lambda: draw_to_get(root))
bt2.pack()
bt1.pack()

ttk.Label(content, width=190).pack()

root.mainloop()

try: os.remove('temp_image.png')
except: pass


#TD4 biochimie
#acide sialique CC(=O)N[C@@H]1[C@@H](O)C[C@](OF)(O[C@H]1[C@H](O)[C@H](O)CO)C(O)=O
#galactose C([C@@H]1[C@@H]([C@@H]([C@H](C(O1)O)O)O)O)O