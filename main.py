import PySimpleGUI as sg 

# Always check for a Window Closed event immediately following your window.read() call
# if event == sg.WIN_CLOSED or even == 'Exit': break ; assume the values variable will ahvea  value that's not usable

character_list = ["Thellon", "Aila", "Root", "Lita"]

cp_tab_layout = [[sg.OptionMenu(character_list)], [sg.Multiline(size = (125, 15))]]
chapter_tab = [[sg.TabGroup([[sg.Tab("Chapter 1", cp_tab_layout, key="-tabs-")]])], [sg.Button("Add Chapter")], [sg.Button("Remove Chapter")]]

# TRY TO IMPLEMENT PILLOW: for images; can maybe see if there is a way of doing graph for the character map
# Maybe could do classes with characters where main characters are at the top of the tree and have preset connection points?
# Could color code lines instead of it being labeled; could do a circle of characters and keep position information for lines
# Make each character a box with their name and (optionally) a picture (use default person if not)
character_tab = [[sg.Button('Test Button')]]

# MAYBE: try to do a plot points in a container element with extend layout/make invisible; try text box with an update button
plot_tab = [[sg.Graph((1000, 400),(0, 0),(1000, 400), background_color="white", key = "-DIAGRAM-")], [sg.Button("Add Plot Point"), sg.OptionMenu([1,2,3,4]), sg.Input()]]

layout = [[sg.TabGroup([[sg.Tab("Chapter Planner", chapter_tab)], [sg.Tab("Character Map", character_tab)], [sg.Tab("Plot Diagram", plot_tab)]])]]

window = sg.Window("AuthorEyes", layout, size=(1000,500))
window.finalize()
window["-DIAGRAM-"].draw_text("Exposition", (100, 100), font = ('Arial', 7))
window["-DIAGRAM-"].draw_line((50, 50), (200, 50), width = 2)
window["-DIAGRAM-"].draw_line((200, 50), (500, 350), width = 2)
window["-DIAGRAM-"].draw_line((500, 350), (700, 150), width = 2)
window["-DIAGRAM-"].draw_line((700, 150), (900, 150), width = 2)

chapter = 0

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == "Add Chapter":
        chapter += 1
        chapter_tab[0][0].add_tab(sg.Tab(f'Chapter {chapter+1}', [[sg.OptionMenu(character_list)], [sg.Multiline(size = (125, 15))]]))

    if event == "Add Plot Point":
        window["-DIAGRAM-"].draw_text("Plot Point", (500, 300), font = ('Arial', 7))

window.close()