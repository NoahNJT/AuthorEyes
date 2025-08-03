import PySimpleGUI as sg 
from PIL import Image
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

home_layout = [[sg.Input("Story Title", key = "-TITLE-")], 
               [sg.Input("Author", key = "-AUTHOR-")], 
               [sg.Input("Enter file name (json only) here to save to or load from!", key = "-FILENAME-")], 
               [sg.Button("Save All", key = "-SAVE-"), sg.Button("Load", key = "-LOAD-")]]

g_elem_list = []
m_elem_list = []
t_elem_list = []

#=================================== CHAPTER PLANNER TAB ===============================
vis = 1
chapters = 1

chapt_col = [[sg.pin(sg.Col(layout = [[sg.Input("Ch #", size = (5, None), key = ("-CHNUM-", chapters)), 
              sg.Input("Narrator/POV Character", size = (30, None), key = ("-POV-", chapters)), 
              sg.Input("Chapter Title", expand_x = True, key = ("-CHT-", chapters))], 
             [sg.Multiline(size = (125, 15), expand_x = True, key = ("-CHMUL-", chapters))]], key = ("-ROW-", chapters)))]]

chapter_tab = [[sg.Col(chapt_col, key = "-CHAPTERCOL-", expand_x = True, expand_y = True, scrollable = True)],
               [sg.Button("Add Chapter", key = "-ADD-"), sg.Button("Remove Chapter", key = "-DEL-"), sg.Text("Can restore removed contents with 'Add Chapter' until next load of file")]]
#========================================================================================

#==================================== PLOT DIAGRAM TAB ===================================
col = [[sg.Text('Choose what clicking/dragging does:', enable_events=True)],
       [sg.Radio('Draw Line', 1, key='-LINE-', enable_events=True)],
       [sg.Radio('Erase Item', 1, key='-ERASE-', enable_events=True)],
       [sg.Radio('Erase All (INCLUDES DIAGRAM!)', 1, key='-CLEAR-', enable_events=True)],
       [sg.Radio('Move Item', 1, True, key='-MOVE-', enable_events=True)],
       [sg.Text("-------------------------------------------------------\nInsert Plot Points:")],
       [sg.Multiline("Write a plot point here!\nType enter when going to new line\nfor multiple lines when adding", key="-POINTSTRING-", size = (30, 10))],
       [sg.Button("Add Plot Point", key="-PLOTPOINT-")]]

plot_tab = [[sg.Graph((720, 400),(0, 0),(720, 400), background_color="white", key = "-DIAGRAM-", change_submits=True, drag_submits=True, expand_x = True, expand_y = True), 
             sg.Col(col, justification = 'right')]]
#=========================================================================================

#==================================== TIMELINE TAB =====================================
t_col = [[sg.Text('Choose what clicking/dragging does:', enable_events=True)],
         [sg.Radio('Draw Line', 1, key='-LINE1-', enable_events=True)],
         [sg.Radio('Erase Item', 1, key='-ERASE1-', enable_events=True)],
         [sg.Radio('Erase All (INCLUDES DIAGRAM!)', 1, key='-CLEAR1-', enable_events=True)],
         [sg.Radio('Move Item', 1, True, key='-MOVE1-', enable_events=True)],
         [sg.Text("-------------------------------------------------------\nInsert Events:")],
         [sg.Multiline("Write timeline event here!\nType enter when going to new line\nfor multiple lines when adding", key="-TIMESTRING-", size = (30, 10))],
         [sg.Button("Add Event", key="-TIMEPOINT-")]]

t_g_col = []

time_tab = [[sg.Graph((720, 400),(0, 0),(720, 400), background_color="white", key = "-TIMELINE-", change_submits=True, drag_submits=True, expand_x = True, expand_y = True),
             sg.Col(t_col, justification = 'right')]]
#=========================================================================================

#==================================== CHARACTER MAP TAB =================================
char_col = [[sg.Text("Choose what clicking/dragging does:", enable_events=True)],
            [sg.Radio("Draw Line", 1, key='-LINE2-', enable_events=True), 
             sg.Input("#000000", size = (7, None), key = "-LINECOL-"),
             sg.ColorChooserButton(button_text = "Line Color")],
            [sg.Radio("Erase Item", 1, key='-ERASE2-', enable_events=True)],
            [sg.Radio("Erase All", 1, key='-CLEAR2-', enable_events=True)],
            [sg.Radio("Move Item", 1, True, key='-MOVE2-', enable_events=True)],
            [sg.Text("-------------------------------------------------------\nInsert Character Images and Items:")],
            [sg.Input("Image Filepath", key = "-IMAGEPATH-", size = (20, None)), sg.FileBrowse()],
            [sg.Button("Add Character Image", key = "-CHARIMAGE-", size = (25, None))],
            [sg.Multiline("Write names, relationships, etc.\nType enter when going to new line\nfor multiple lines when adding", key = "-CHARTEXT-", size = (30, 10))],
            [sg.Button("Add Text", key = "-CHARTEXTBUTTON-", size = (25, None))]]

character_tab = [[sg.Graph((720, 400),(0, 0),(720, 400), background_color="white", key = "-CHARMAP-", change_submits=True, drag_submits=True, expand_x = True, expand_y = True), 
                  sg.Col(char_col, justification = 'right')]]
#=========================================================================================

#======================================= CREATE WINDOW ==========================================================
layout = [[sg.TabGroup([[sg.Tab("Home", home_layout, expand_x = True, expand_y = True)], 
          [sg.Tab("Chapter Planner", chapter_tab, expand_x = True, expand_y = True)], 
          [sg.Tab("Plot Diagram", plot_tab, expand_x = True, expand_y = True)],
          [sg.Tab("Timeline", time_tab, expand_x = True, expand_y = True)],
          [sg.Tab("Character Map", character_tab, expand_x = True, expand_y = True)]], expand_x = True, expand_y = True)]]

window = sg.Window("AuthorEyes", layout, resizable = True)
window.finalize()
#=================================================================================================================

#======================================= INITIALIZE PLOT DIAGRAM =================================================
id = window["-DIAGRAM-"].draw_text("Exposition", (100, 60), font = ('Arial', 8))
g_elem_list.append({'id': id, 'type': 'text', 'text': "Exposition", 'point': (100, 60), 'font': ('Arial', 8)})
id = window["-DIAGRAM-"].draw_text("Rising Action", (260, 190), font = ('Arial', 8))
g_elem_list.append({'id': id, 'type': 'text', 'text': "Rising Action", 'point': (260, 190), 'font': ('Arial', 8)})
id = window["-DIAGRAM-"].draw_text("Climax", (420, 310), font = ('Arial', 8))
g_elem_list.append({'id': id, 'type': 'text', 'text': "Climax", 'point': (420, 310), 'font': ('Arial', 8)})
id = window["-DIAGRAM-"].draw_text("Falling Action", (530, 240), font = ('Arial', 8))
g_elem_list.append({'id': id, 'type': 'text', 'text': "Falling Action", 'point': (530, 240), 'font': ('Arial', 8)})
id = window["-DIAGRAM-"].draw_text("Resolution", (625, 180), font = ('Arial', 8))
g_elem_list.append({'id': id, 'type': 'text', 'text': "Resolution", 'point': (625, 180), 'font': ('Arial', 8)})
id = window["-DIAGRAM-"].draw_line((30, 50), (170, 50), width = 2)
g_elem_list.append({'id': id, 'type': 'line', 'point1': (30, 50), 'point2': (170, 50), 'width': 2})
id = window["-DIAGRAM-"].draw_line((170, 50), (420, 300), width = 2)
g_elem_list.append({'id': id, 'type': 'line', 'point1': (170, 50), 'point2': (420, 300), 'width': 2})
id = window["-DIAGRAM-"].draw_line((420, 300), (550, 170), width = 2)
g_elem_list.append({'id': id, 'type': 'line', 'point1': (420, 300), 'point2': (550, 170), 'width': 2})
id = window["-DIAGRAM-"].draw_line((550, 170), (700, 170), width = 2)
g_elem_list.append({'id': id, 'type': 'line', 'point1': (550, 170), 'point2': (700, 170), 'width': 2})
#==================================================================================================================

#======================================== INITIALIZE TIMELINE =====================================================
id = window["-TIMELINE-"].draw_line((30, 175), (700, 175), width = 2)
t_elem_list.append({'id': id, 'type': 'line', 'point1': (30, 175), 'point2': (700, 175), 'width': 2})
id = window["-TIMELINE-"].draw_line((30, 155), (30, 195), width = 2)
t_elem_list.append({'id': id, 'type': 'line', 'point1': (30, 175), 'point2': (700, 175), 'width': 2})
id = window["-TIMELINE-"].draw_line((700, 155), (700, 195), width = 2)
t_elem_list.append({'id': id, 'type': 'line', 'point1': (30, 175), 'point2': (700, 175), 'width': 2})

l_draw = False
l_draw_map = False
l_draw_time = False
dragging = False
graph = window["-DIAGRAM-"]
map_graph = window["-CHARMAP-"]
t_graph = window["-TIMELINE-"]
start_point = end_point = prior_rect = None

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    #====================== HOME PAGE EVENTS ===========================
    if event == "-LOAD-":
        with open(values["-FILENAME-"], 'r') as f:
            load_data = json.load(f)
            window["-TITLE-"].update(load_data[0][0])
            window["-AUTHOR-"].update(load_data[0][1])
            window["-FILENAME-"].update(load_data[0][2])

            window[("-CHNUM-", 1)].update(load_data[1][1]['chnum'])
            window[("-POV-", 1)].update(load_data[1][1]['pov'])
            window[("-CHT-", 1)].update(load_data[1][1]['cht'])
            window[("-CHMUL-", 1)].update(load_data[1][1]['ch'])
            for ch in range(2, load_data[1][0] + 1):
                vis += 1
                chapters += 1
                window.extend_layout(window["-CHAPTERCOL-"], [[sg.pin(sg.Col(layout = [[sg.Input("Ch #", size = (5, None), key = ("-CHNUM-", chapters)), 
                sg.Input("Narrator/POV Character", size = (30, None), key = ("-POV-", chapters)), 
                sg.Input("Chapter Title", expand_x = True, key = ("-CHT-", chapters))], 
                [sg.Multiline(size = (125, 15), expand_x = True, key = ("-CHMUL-", chapters))]], key = ("-ROW-", chapters)))]])
                window.refresh()
                window["-CHAPTERCOL-"].contents_changed()
                window[("-CHNUM-", ch)].update(load_data[1][1]['chnum'])
                window[("-POV-", ch)].update(load_data[1][1]['pov'])
                window[("-CHT-", ch)].update(load_data[1][1]['cht'])
                window[("-CHMUL-", ch)].update(load_data[1][1]['ch'])

            graph.erase()
            g_elem_list.clear()
            for elem in load_data[2]:
                if elem['type'] == 'text':
                    id = graph.draw_text(elem['text'], elem['point'], font = elem['font'])
                    g_elem_list.append({'id': id, 'type': 'text', 'text': elem['text'], 'point': elem['point'], 'font': elem['font']})
                elif elem['type'] == 'line':
                    id = graph.draw_line(elem['point1'], elem['point2'], width = elem['width'])
                    g_elem_list.append({'id': id, 'type': 'line', 'point1': elem['point1'], 'point2': elem['point2'], 'width': elem['width']})

            t_graph.erase()
            t_elem_list.clear()
            for elem in load_data[3]:
                if elem['type'] == 'text':
                    id = t_graph.draw_text(elem['text'], elem['point'], font = elem['font'])
                    t_elem_list.append({'id': id, 'type': 'text', 'text': elem['text'], 'point': elem['point'], 'font': elem['font']})
                elif elem['type'] == 'line':
                    id = t_graph.draw_line(elem['point1'], elem['point2'], width = elem['width'])
                    t_elem_list.append({'id': id, 'type': 'line', 'point1': elem['point1'], 'point2': elem['point2'], 'width': elem['width']})

            map_graph.erase()
            m_elem_list.clear()
            for elem in load_data[4]:
                if elem['type'] == 'text':
                    id = map_graph.draw_text(elem['text'], elem['point'], font = elem['font'])
                    m_elem_list.append({'id': id, 'type': 'text', 'text': elem['text'], 'point': elem['point'], 'font': elem['font']})
                elif elem['type'] == 'line':
                    id = map_graph.draw_line(elem['point1'], elem['point2'], width = elem['width'], color = elem['color'])
                    m_elem_list.append({'id': id, 'type': 'line', 'point1': elem['point1'], 'point2': elem['point2'], 'width': elem['width'], 'color': elem['color']})
                elif elem['type'] == 'image':
                    formatted = get_img_data(elem['path'])
                    id = map_graph.draw_image(data = formatted, location = elem['point'])
                    m_elem_list.append({'id': id, 'type': 'image', 'path': elem['path'], 'point': elem['point']})

            

    if event == "-SAVE-":
        with open(values["-FILENAME-"], 'w') as f:
            chapter_contents = []
            for chapt in range(1, vis + 1):
                chapter_contents.append({'ch': chapt, 'chnum': values[("-CHNUM-", chapt)], 
                                         'pov': values[("-POV-", chapt)], 'cht': values[("-CHT-", chapt)],
                                         'chmul': values[("-CHMUL-", chapt)]})

            save_data = [[values["-TITLE-"], values["-AUTHOR-"], values["-FILENAME-"]], [vis, chapter_contents], g_elem_list, t_elem_list, m_elem_list]
            json.dump(save_data, f)
    #=====================================================================

    #======================= CHAPTER PLANNER EVENTS ======================
    if event == "-ADD-":
        vis += 1
        chapters += 1

        if vis < chapters:
            window[('-ROW-', vis)].update(visible = True)
            window.refresh()
            window["-CHAPTERCOL-"].contents_changed()
            chapters -= 1
        else:
            window.extend_layout(window["-CHAPTERCOL-"], [[sg.pin(sg.Col(layout = [[sg.Input("Ch #", size = (5, None), key = ("-CHNUM-", chapters)), 
              sg.Input("Narrator/POV Character", size = (30, None), key = ("-POV-", chapters)), 
              sg.Input("Chapter Title", expand_x = True, key = ("-CHT-", chapters))], 
             [sg.Multiline(size = (125, 15), expand_x = True, key = ("-CHMUL-", chapters))]], key = ("-ROW-", chapters)))]])
            
            window.refresh()
            window["-CHAPTERCOL-"].contents_changed()

        print(chapters, vis)


    if event == "-DEL-":
        if vis > 1:
            window[('-ROW-', vis)].update(visible = False)
            window.refresh()
            window["-CHAPTERCOL-"].contents_changed()
            vis -= 1
        print(chapters, vis)
    #=====================================================================

    #====================== PLOT DIAGRAM EVENTS ==========================
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
                                elem['point'] = (elem['point'][0] + delta_x, elem['point'][1] + delta_y)
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
        if l_draw_map == True:
            m_elem_list.append({'id': id, 'type': 'line', 'point1': start_point, 'point2': end_point, 'width': 2, 'color': values["-LINECOL-"]})
            l_draw_map = False
        if l_draw_time == True:
            t_elem_list.append({'id': id, 'type': 'line', 'point1': start_point, 'point2': end_point, 'width': 2})
            l_draw_time = False

        start_point, end_point = None, None
        dragging = False
        prior_rect = None

    if event == "-PLOTPOINT-":
        id = graph.draw_text(values["-POINTSTRING-"], (300, 300), font = ('Arial', 8))
        g_elem_list.append({'id': id, 'type': 'text', 'text': values["-POINTSTRING-"], 'point': (300, 300), 'font': ('Arial', 8)})
    #=======================================================================

    #====================== TIMELINE EVENTS ==========================
    if event == "-TIMELINE-":
        x, y = values["-TIMELINE-"]
        if not dragging:
            start_point = (x, y)
            dragging = True
            drag_figures = t_graph.get_figures_at_location((x,y))
            lastxy = x, y
        else:
            end_point = (x, y)
        if prior_rect:
            t_graph.delete_figure(prior_rect)
        delta_x, delta_y = x - lastxy[0], y - lastxy[1]
        lastxy = x,y
        if None not in (start_point, end_point):
            if values['-MOVE1-']:
                for fig in drag_figures:
                    t_graph.move_figure(fig, delta_x, delta_y)
                    for elem in t_elem_list:
                        if elem['id'] == fig:
                            if elem['type'] == 'text':
                                elem['point'] = (elem['point'][0] + delta_x, elem['point'][1] + delta_y)
                            else:
                                elem['point1'] = (elem['point1'][0] + delta_x, elem['point1'][1] + delta_y)
                                elem['point2'] = (elem['point2'][0] + delta_x, elem['point2'][1] + delta_y)
                    t_graph.update()
            elif values['-LINE1-']:
                id = prior_rect = t_graph.draw_line(start_point, end_point, width = 2)
                l_draw_time = True
            elif values['-ERASE1-']:
                for figure in drag_figures:
                    t_graph.delete_figure(figure)
                    for elem in t_elem_list:
                        if elem['id'] == figure:
                            t_elem_list.remove(elem)
            elif values['-CLEAR1-']:
                t_graph.erase()
                t_elem_list.clear()

    if event == "-TIMEPOINT-":
        id = t_graph.draw_text(values["-TIMESTRING-"], (300, 300), font = ('Arial', 8))
        t_elem_list.append({'id': id, 'type': 'text', 'text': values["-TIMESTRING-"], 'point': (300, 300), 'font': ('Arial', 8)})
    #=======================================================================

    #===================== CHARACTER MAP EVENTS ============================
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
                    for elem in m_elem_list:
                        if elem['id'] == fig:
                            if elem['type'] == 'text' or elem['type'] == 'image':
                                elem['point'] = (elem['point'][0] + delta_x, elem['point'][1] + delta_y)
                            else:
                                elem['point1'] = (elem['point1'][0] + delta_x, elem['point1'][1] + delta_y)
                                elem['point2'] = (elem['point2'][0] + delta_x, elem['point2'][1] + delta_y)
                    map_graph.update()
            elif values['-LINE2-']:
                id = prior_rect = map_graph.draw_line(start_point, end_point, width = 2, color = values["-LINECOL-"])
                l_draw_map = True
            elif values['-ERASE2-']:
                for figure in drag_figures:
                    map_graph.delete_figure(figure)
                    for elem in m_elem_list:
                        if elem['id'] == figure:
                            m_elem_list.remove(elem)
            elif values['-CLEAR2-']:
                map_graph.erase()
                m_elem_list.clear()

    if event == "-CHARIMAGE-":
        formatted = get_img_data(values["-IMAGEPATH-"])
        id = map_graph.draw_image(data = formatted, location = (200, 200))
        m_elem_list.append({'id': id, 'type': 'image', 'path': values["-IMAGEPATH-"], 'point': (200, 200)})

    if event == "-CHARTEXTBUTTON-":
        id = map_graph.draw_text(values["-CHARTEXT-"], (300, 300), font = ('Arial', 8))
        m_elem_list.append({'id': id, 'type': 'text', 'text': values["-CHARTEXT-"], 'point': (300, 300), 'font': ('Arial', 8)})
    #==========================================================================

window.close()