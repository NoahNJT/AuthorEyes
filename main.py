import PySimpleGUI as sg 
from PIL import Image, ImageTk
import json
import io

# Always check for a Window Closed event immediately following your window.read() call
# if event == sg.WIN_CLOSED or even == 'Exit': break ; assume the values variable will have a  value that's not usable

def get_img_data(f, maxsize=(75, 75)):
    """Generate image data using PIL"""
    img = Image.open(f)
    img.thumbnail(maxsize)
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    return bio.getvalue()

main_layout = [[sg.Input("Story Title", key = "-TITLE-")], 
               [sg.Input("Author", key = "-AUTHOR-")], 
               [sg.Input("Enter file name (.json only) here to save to or load from!", key = "-FILENAME-")], 
               [sg.Button("Save All", key = "-SAVE-"), sg.Button("Load", key = "-LOAD-")]]

character_list = ["Thellon", "Aila", "Root", "Lita"]

g_elem_list = []
m_elem_list = []
t_elem_list = []

#=================================== CHAPTER PLANNER TAB ===============================
cp_tab_layout = [[sg.OptionMenu(character_list), 
                  sg.Input("Chapter Title", size = (113, None))], 
                 [sg.Multiline(size = (125, 15))]]

chapter_tab = [[sg.TabGroup([[sg.Tab("Chapter 1", cp_tab_layout, key="-tabs-")]])], 
               [sg.Button("Add Chapter")], 
               [sg.Button("Remove Chapter")]]
#========================================================================================

#==================================== CHARACTER MAP TAB =================================
# TRY TO IMPLEMENT PILLOW: for images; can maybe see if there is a way of doing graph for the character map
# Maybe could do classes with characters where main characters are at the top of the tree and have preset connection points?
# Could color code lines instead of it being labeled; could do a circle of characters and keep position information for lines
# Make each character a box with their name and (optionally) a picture (use default person if not)
character_frame_layout = [[sg.OptionMenu(character_list),
                           sg.OptionMenu(character_list),
                           sg.Input(), 
                           sg.ColorChooserButton("Select Color")]]

char_col = [[sg.Text('Choose what clicking/dragging does:', enable_events=True)],
            [sg.Radio('Draw Line', 1, key='-LINE2-', enable_events=True), 
             sg.Input("#000000", size = (7, None), key = "-LINECOL-"),
             sg.ColorChooserButton(button_text = "Line Color")],
            [sg.Radio('Erase Item', 1, key='-ERASE2-', enable_events=True)],
            [sg.Radio('Erase All', 1, key='-CLEAR2-', enable_events=True)],
            [sg.Radio('Move All Items', 1, key='-MOVEALL2-', enable_events=True)],
            [sg.Radio('Move Item', 1, True, key='-MOVE2-', enable_events=True)],
            [sg.Input("Character Name", key="-POINTSTRING2-")],
            [sg.Input("Image Filepath", key = "-IMAGEPATH-", size = (20, None)), sg.FileBrowse()],
            [sg.Button("Add Character", key = "-CHARIMAGE-", size = (25, None))]]

character_tab = [[sg.Graph((720, 400),(0, 0),(720, 400), background_color="white", key = "-CHARMAP-", change_submits=True, drag_submits=True), sg.Col(char_col)]]
#=========================================================================================

#==================================== PLOT DIAGRAM TAB ===================================
col = [[sg.Text('Choose what clicking/dragging does:', enable_events=True)],
       [sg.Radio('Draw Line', 1, key='-LINE-', enable_events=True)],
       [sg.Radio('Erase Item', 1, key='-ERASE-', enable_events=True)],
       [sg.Radio('Erase All (INCLUDES DIAGRAM!)', 1, key='-CLEAR-', enable_events=True)],
       [sg.Radio('Move Item', 1, True, key='-MOVE-', enable_events=True)],
       [sg.Multiline("Write a plot point here!",size = (None, 10), key="-POINTSTRING-")],
       [sg.Button("Add Plot Point", key="-PLOTPOINT-")]]

plot_tab = [[sg.Graph((720, 400),(0, 0),(720, 400), background_color="white", key = "-DIAGRAM-", change_submits=True, drag_submits=True), sg.Col(col)]]
#=========================================================================================

#======================================= CREATE WINDOW ==========================================================
layout = [[sg.TabGroup([[sg.Tab("Home", main_layout)], 
          [sg.Tab("Chapter Planner", chapter_tab)], 
          [sg.Tab("Character Map", character_tab)], 
          [sg.Tab("Plot Diagram", plot_tab)]])]]

window = sg.Window("AuthorEyes", layout, size=(1000,500))
window.finalize()
#=================================================================================================================

#======================================= INITIALIZE PLOT DIAGRAM =================================================
id = window["-DIAGRAM-"].draw_text("Exposition", (100, 110), font = ('Arial', 8))
g_elem_list.append({'id': id, 'type': 'text', 'text': "Exposition", 'point': (100, 110), 'font': ('Arial', 8)})
id = window["-DIAGRAM-"].draw_text("Rising Action", (260, 240), font = ('Arial', 8))
g_elem_list.append({'id': id, 'type': 'text', 'text': "Rising Action", 'point': (260, 240), 'font': ('Arial', 8)})
id = window["-DIAGRAM-"].draw_text("Climax", (420, 360), font = ('Arial', 8))
g_elem_list.append({'id': id, 'type': 'text', 'text': "Climax", 'point': (420, 360), 'font': ('Arial', 8)})
id = window["-DIAGRAM-"].draw_text("Falling Action", (530, 290), font = ('Arial', 8))
g_elem_list.append({'id': id, 'type': 'text', 'text': "Falling Action", 'point': (530, 290), 'font': ('Arial', 8)})
id = window["-DIAGRAM-"].draw_text("Resolution", (625, 230), font = ('Arial', 8))
g_elem_list.append({'id': id, 'type': 'text', 'text': "Resolution", 'point': (625, 230), 'font': ('Arial', 8)})
id = window["-DIAGRAM-"].draw_line((30, 100), (170, 100), width = 2)
g_elem_list.append({'id': id, 'type': 'line', 'point1': (30, 100), 'point2': (170, 100), 'width': 2})
id = window["-DIAGRAM-"].draw_line((170, 100), (420, 350), width = 2)
g_elem_list.append({'id': id, 'type': 'line', 'point1': (170, 100), 'point2': (420, 350), 'width': 2})
id = window["-DIAGRAM-"].draw_line((420, 350), (550, 220), width = 2)
g_elem_list.append({'id': id, 'type': 'line', 'point1': (420, 350), 'point2': (550, 220), 'width': 2})
id = window["-DIAGRAM-"].draw_line((550, 220), (700, 220), width = 2)
g_elem_list.append({'id': id, 'type': 'line', 'point1': (550, 220), 'point2': (700, 220), 'width': 2})
#==================================================================================================================

l_draw = False
dragging = False
graph = window["-DIAGRAM-"]
map_graph = window["-CHARMAP-"]
start_point = end_point = prior_rect = None

chapter = 0

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == "-LOAD-":
        with open(values["-FILENAME-"], 'r') as f:
            load_data = json.load(f)
            window["-TITLE-"].update(load_data[0][0])
            window["-AUTHOR-"].update(load_data[0][1])
            window["-FILENAME-"].update(load_data[0][2])

            graph.erase()
            g_elem_list = []
            for elem in load_data[1]:
                if elem['type'] == 'text':
                    id = graph.draw_text(elem['text'], elem['point'], font = elem['font'])
                    g_elem_list.append({'id': id, 'type': 'text', 'text': elem['text'], 'point': elem['point'], 'font': elem['font']})
                else:
                    id = graph.draw_line(elem['point1'], elem['point2'], width = elem['width'])
                    g_elem_list.append({'id': id, 'type': 'line', 'point1': elem['point1'], 'point2': elem['point2'], 'width': elem['width']})


    if event == "-SAVE-":
        with open(values["-FILENAME-"], 'w') as f:
            save_data = [[values["-TITLE-"], values["-AUTHOR-"], values["-FILENAME-"]], g_elem_list]
            json.dump(save_data, f)

    if event == "Add Chapter":
        chapter += 1
        chapter_tab[0][0].add_tab(sg.Tab(f'Chapter {chapter+1}', [[sg.OptionMenu(character_list), 
                                                                   sg.Input("Chapter Title", size = (113, None))], 
                                                                  [sg.Multiline(size = (125, 15))]]))

    if event in ('-MOVE-'):
        graph.Widget.config(cursor='fleur')
    elif not event.startswith('-DIAGRAM-'):
        graph.Widget.config(cursor='left_ptr')

    if event == "-DIAGRAM-":
        x, y = values["-DIAGRAM-"]
        if not dragging:
            start_point = (x, y)
            dragging = True
            drag_figures = graph.get_figures_at_location((x,y))
            lastxy = x, y
        else:
            end_point = (x, y)
        if prior_rect:
            graph.delete_figure(prior_rect)
        delta_x, delta_y = x - lastxy[0], y - lastxy[1]
        lastxy = x,y
        if None not in (start_point, end_point):
            if values['-MOVE-']:
                for fig in drag_figures:
                    graph.move_figure(fig, delta_x, delta_y)
                    for elem in g_elem_list:
                        if elem['id'] == fig:
                            if elem['type'] == 'text':
                                elem['point'] = (x, y)
                            else:
                                elem['point1'] = (elem['point1'][0] + delta_x, elem['point1'][1] + delta_y)
                                elem['point2'] = (elem['point2'][0] + delta_x, elem['point2'][1] + delta_y)
                    graph.update()
            elif values['-LINE-']:
                id = prior_rect = graph.draw_line(start_point, end_point, width = 2)
                l_draw = True
            elif values['-ERASE-']:
                for figure in drag_figures:
                    graph.delete_figure(figure)
                    for elem in g_elem_list:
                        if elem['id'] == figure:
                            g_elem_list.remove(elem)
            elif values['-CLEAR-']:
                graph.erase()
                g_elem_list.clear()
    elif event.endswith('+UP'):  # The drawing has ended because mouse up
        if l_draw == True:
            g_elem_list.append({'id': id, 'type': 'line', 'point1': start_point, 'point2': end_point, 'width': 2})
            l_draw = False
        start_point, end_point = None, None
        dragging = False
        prior_rect = None

    if event == "-PLOTPOINT-":
        id = graph.draw_text(values["-POINTSTRING-"], (300, 300), font = ('Arial', 8))
        g_elem_list.append({'id': id, 'type': 'text', 'text': values["-POINTSTRING-"], 'point': (300, 300), 'font': ('Arial', 8)})


    if event == "-CHARMAP-":
        x, y = values["-CHARMAP-"]
        if not dragging:
            start_point = (x, y)
            dragging = True
            drag_figures = map_graph.get_figures_at_location((x,y))
            lastxy = x, y
        else:
            end_point = (x, y)
        if prior_rect:
            map_graph.delete_figure(prior_rect)
        delta_x, delta_y = x - lastxy[0], y - lastxy[1]
        lastxy = x,y
        if None not in (start_point, end_point):
            if values['-MOVE2-']:
                for fig in drag_figures:
                    map_graph.move_figure(fig, delta_x, delta_y)
                    map_graph.update()
            elif values['-LINE2-']:
                prior_rect = map_graph.draw_line(start_point, end_point, width = 2, color = values["-LINECOL-"])
            elif values['-ERASE2-']:
                for figure in drag_figures:
                    map_graph.delete_figure(figure)
            elif values['-CLEAR2-']:
                map_graph.erase()
            elif values['-MOVEALL2-']:
                map_graph.move(delta_x, delta_y)
    elif event.endswith('+UP'):  # The drawing has ended because mouse up
        start_point, end_point = None, None  # enable grabbing a new rect
        dragging = False
        prior_rect = None

    if event == "-CHARIMAGE-":
        formatted = get_img_data(values["-IMAGEPATH-"])
        map_graph.draw_image(data = formatted, location = (200, 200))

window.close()