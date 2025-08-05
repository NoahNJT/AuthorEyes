#========================================================
# Program: AuthorEyes
# File: author_eyes.py
# Author: Noah True
# 
# Description: This is a writing tool that includes
#    functionality for a chapter planner, plot diagram,
#    timeline, and character map (with images). Created
#    with the PySimpleGUI and Pillow 3rd party modules.
#========================================================
import PySimpleGUI as sg 
from PIL import Image
import io
import json

def main():
    # Initialize Lists for File Save/Load
    g_elem_list = []
    m_elem_list = []
    t_elem_list = []
    chapter_contents = []

    # Set Theme
    sg.theme('LightBlue3')

    # INITIALIZE TAB LAYOUTS ===============================================================
    
    # Home Tab
    home_tab = [[sg.Col(create_home_layout(), element_justification = 'center', expand_x = True, expand_y = True)]]

    # Chapter Planner Tab
    vis = 1        # Tracks the number of tabs visible to the user
    chapters = 1   # Tracks the total number of tabs created in the program
    chapter_tab = [[sg.Col(create_chapt_col(chapters), key = "-CHAPTERCOL-", expand_x = True, expand_y = True, scrollable = True)],
                   [sg.Button("Add Chapter", key = "-ADD-"), 
                    sg.Button("Remove Chapter", key = "-DEL-"), 
                    sg.Text("Can restore removed contents with 'Add Chapter' until next load of file")]]
    
    # Plot Diagram Tab
    plot_tab = [[sg.Graph((720, 400),(0, 0),(720, 400), background_color="white", key = "-DIAGRAM-", change_submits=True, drag_submits=True, expand_x = True, expand_y = True), 
                 sg.Col(create_plot_col(), justification = 'right')]]

    # Timeline Tab
    time_tab = [[sg.Graph((720, 400),(0, 0),(720, 400), background_color="white", key = "-TIMELINE-", change_submits=True, drag_submits=True, expand_x = True, expand_y = True),
                 sg.Col(create_t_col(), justification = 'right')]]

    # Character Map Tab
    character_tab = [[sg.Graph((720, 400),(0, 0),(720, 400), background_color="white", key = "-CHARMAP-", change_submits=True, drag_submits=True, expand_x = True, expand_y = True), 
                      sg.Col(create_char_col(), justification = 'right')]]
    #=========================================================================================

    # CREATE WINDOW ==========================================================================
    layout = [[sg.TabGroup([[sg.Tab("Home", home_tab, expand_x = True, expand_y = True)], 
              [sg.Tab("Chapter Planner", chapter_tab, expand_x = True, expand_y = True)], 
              [sg.Tab("Plot Diagram", plot_tab, expand_x = True, expand_y = True)],
              [sg.Tab("Timeline", time_tab, expand_x = True, expand_y = True)],
              [sg.Tab("Character Map", character_tab, expand_x = True, expand_y = True)]], expand_x = True, expand_y = True)]]
    
    window = sg.Window("AuthorEyes", layout, resizable = True)
    window.finalize() 
    
    # Initialize Plot Diagram and Timeline (only possible after finalizing)
    initialize_plot(window, g_elem_list)
    initialize_tline(window, t_elem_list)

    # Initialize Event Variables
    l_draw = False                  # Marker for when line is done drawing for Plot Diagram
    l_draw_map = False              # Marker for when line is done drawing for Character Map
    l_draw_time = False             # Marker for when line is done drawing for Timeline
    dragging = False
    graph = window["-DIAGRAM-"]
    map_graph = window["-CHARMAP-"]
    t_graph = window["-TIMELINE-"]
    start_point = end_point = prior_rect = None
    #==========================================================================================


    # EVENT LOOP ==============================================================================
    while True:
        event, values = window.read()

        # End event loop if window closed by user
        if event == sg.WIN_CLOSED:
            break

        # HOME PAGE EVENTS ------------------------------------------------------------
        # Save To File
        if event == "-SAVE-":
            # Ensure user is saving to json file
            if not values["-FILENAME-"].endswith('.json'):
                sg.Popup("Ensure file has extension '.json'")
            else:
                # Open json file for writing (overwrite/create)
                with open(values["-FILENAME-"], 'w') as f:
                    # Save chapter tab (overwrite any data in structure)
                    chapter_contents.clear()
                    for chapt in range(1, vis + 1):
                        chapter_contents.append({'ch': chapt, 'chnum': values[("-CHNUM-", chapt)], 
                                                'pov': values[("-POV-", chapt)], 'cht': values[("-CHT-", chapt)],
                                                'chmul': values[("-CHMUL-", chapt)]})

                    # Save all other data in data structure (list of lists)
                    save_data = [[values["-TITLE-"], values["-AUTHOR-"], values["-FILENAME-"]], [vis, chapter_contents], g_elem_list, t_elem_list, m_elem_list]

                    # Save to json file
                    json.dump(save_data, f)
        
        # Load From File
        if event == "-LOAD-":
            # Attempt to open json file
            try:
                with open(values["-FILENAME-"], 'r') as f:
                    load_data = json.load(f)
            except:
                sg.Popup("File not found. Please ensure file name/path is correct.")
            else:
                # LOAD HOME PAGE DATA ------------------------
                window["-TITLE-"].update(load_data[0][0])
                window["-AUTHOR-"].update(load_data[0][1])
                window["-FILENAME-"].update(load_data[0][2])
                #---------------------------------------------

                # LOAD CHAPTER PLANNER DATA ------------------
                chapter_contents.clear()

                # Remove visibility for any chapters currently in layout
                while vis > 1:
                    window[('-ROW-', vis)].update(visible = False)
                    window.refresh()
                    window["-CHAPTERCOL-"].contents_changed()
                    vis -= 1

                # Load first layout's data
                window[("-CHNUM-", 1)].update(load_data[1][1][0]['chnum'])
                window[("-POV-", 1)].update(load_data[1][1][0]['pov'])
                window[("-CHT-", 1)].update(load_data[1][1][0]['cht'])
                window[("-CHMUL-", 1)].update(load_data[1][1][0]['chmul'])

                # Load additional layout data
                if load_data[1][0] > 1:
                    for ch in range(2, load_data[1][0] + 1):
                        # If chapter layouts exist but are invisible, use those first
                        if vis < chapters:
                            window[('-ROW-', ch)].update(visible = True)
                            window.refresh()
                            window["-CHAPTERCOL-"].contents_changed()
                        # If chapter layout doesn't exist, create it and update variables accordingly
                        else:  
                            chapters += 1
                            window.extend_layout(window["-CHAPTERCOL-"], [[sg.pin(sg.Col(layout = [[sg.Input("Ch #", size = (5, None), key = ("-CHNUM-", chapters)), 
                                sg.Input("Narrator/POV Character", size = (30, None), key = ("-POV-", chapters)), 
                                sg.Input("Chapter Title", expand_x = True, key = ("-CHT-", chapters))], 
                                [sg.Multiline(size = (125, 15), expand_x = True, key = ("-CHMUL-", chapters))]], key = ("-ROW-", chapters)))]])
                            window.refresh()
                            window["-CHAPTERCOL-"].contents_changed()
                            window[("-CHNUM-", ch)].update(load_data[1][1][ch-1]['chnum'])
                            window[("-POV-", ch)].update(load_data[1][1][ch-1]['pov'])
                            window[("-CHT-", ch)].update(load_data[1][1][ch-1]['cht'])
                            window[("-CHMUL-", ch)].update(load_data[1][1][ch-1]['chmul'])
                        vis += 1 # Updated regardless at the end
                #--------------------------------------------------

                # LOAD PLOT DIAGRAM DATA --------------------------
                graph.erase()
                g_elem_list.clear()
                for elem in load_data[2]:
                    if elem['type'] == 'text':
                        id = graph.draw_text(elem['text'], elem['point'], font = elem['font'])
                        g_elem_list.append({'id': id, 'type': 'text', 'text': elem['text'], 'point': elem['point'], 'font': elem['font']})
                    elif elem['type'] == 'line':
                        id = graph.draw_line(elem['point1'], elem['point2'], width = elem['width'])
                        g_elem_list.append({'id': id, 'type': 'line', 'point1': elem['point1'], 'point2': elem['point2'], 'width': elem['width']})
                #--------------------------------------------------

                # LOAD TIMELINE DATA ------------------------------
                t_graph.erase()
                t_elem_list.clear()
                for elem in load_data[3]:
                    if elem['type'] == 'text':
                        id = t_graph.draw_text(elem['text'], elem['point'], font = elem['font'])
                        t_elem_list.append({'id': id, 'type': 'text', 'text': elem['text'], 'point': elem['point'], 'font': elem['font']})
                    elif elem['type'] == 'line':
                        id = t_graph.draw_line(elem['point1'], elem['point2'], width = elem['width'])
                        t_elem_list.append({'id': id, 'type': 'line', 'point1': elem['point1'], 'point2': elem['point2'], 'width': elem['width']})
                #---------------------------------------------------

                # LOAD CHARACTER MAP DATA --------------------------
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
                #---------------------------------------------------

                # Refresh window for all updated data
                window.refresh()
        #---------------------------------------------------------------------

        # CHAPTER PLANNER EVENTS ---------------------------------------------
        # Add chapter
        if event == "-ADD-":
            vis += 1 # Update number of visible chapters regardless
            chapters += 1 # Update number of chapters for comparison (will decrement back if not extended)

            # If there are chapters created beyond what is visible, reveal those first
            if vis < chapters:
                window[('-ROW-', vis)].update(visible = True)
                window.refresh()
                window["-CHAPTERCOL-"].contents_changed()
                chapters -= 1
            # Create new chapter layout if no invisible ones available
            else:   
                window.extend_layout(window["-CHAPTERCOL-"], [[sg.pin(sg.Col(layout = [[sg.Input("Ch #", size = (5, None), key = ("-CHNUM-", chapters)), 
                sg.Input("Narrator/POV Character", size = (30, None), key = ("-POV-", chapters)), 
                sg.Input("Chapter Title", expand_x = True, key = ("-CHT-", chapters))], 
                [sg.Multiline(size = (125, 15), expand_x = True, key = ("-CHMUL-", chapters))]], key = ("-ROW-", chapters)))]])
                
                window.refresh()
                window["-CHAPTERCOL-"].contents_changed()

            

        # Delete chapter (make invisible to user)
        if event == "-DEL-":
            if vis > 1:
                window[('-ROW-', vis)].update(visible = False)
                window.refresh()
                window["-CHAPTERCOL-"].contents_changed()
                vis -= 1
        #---------------------------------------------------------------------

        # PLOT DIAGRAM EVENTS ------------------------------------------------
        # Graph events
        if event == "-DIAGRAM-":
            # Initialize values for tracking
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
                # Move an element by change in x and y
                if values['-MOVE-']:
                    for fig in drag_figures:
                        graph.move_figure(fig, delta_x, delta_y)
                        # Edit element location for saving/loading
                        for elem in g_elem_list:
                            if elem['id'] == fig:
                                if elem['type'] == 'text':
                                    elem['point'] = (elem['point'][0] + delta_x, elem['point'][1] + delta_y)
                                else:
                                    elem['point1'] = (elem['point1'][0] + delta_x, elem['point1'][1] + delta_y)
                                    elem['point2'] = (elem['point2'][0] + delta_x, elem['point2'][1] + delta_y)
                        graph.update()
                # Draw a line (draws and deletes constantly until mouse up)
                elif values['-LINE-']:
                    id = prior_rect = graph.draw_line(start_point, end_point, width = 2)
                    l_draw = True
                # Erase element and remove from data struct
                elif values['-ERASE-']:
                    for figure in drag_figures:
                        graph.delete_figure(figure)
                        for elem in g_elem_list:
                            if elem['id'] == figure:
                                g_elem_list.remove(elem)
                # Erase all elements and clear data struct
                elif values['-CLEAR-']:
                    graph.erase()
                    g_elem_list.clear()
        # Mouse up events for end of drawing (THIS APPLIES FOR ALL THREE GRAPHS)
        elif event.endswith('+UP'):
            # Plot Diagram line draw
            if l_draw == True:
                g_elem_list.append({'id': id, 'type': 'line', 'point1': start_point, 'point2': end_point, 'width': 2})
                l_draw = False
            # Character Map line draw
            if l_draw_map == True:
                m_elem_list.append({'id': id, 'type': 'line', 'point1': start_point, 'point2': end_point, 'width': 2, 'color': values["-LINECOL-"]})
                l_draw_map = False
            # Timeline line draw
            if l_draw_time == True:
                t_elem_list.append({'id': id, 'type': 'line', 'point1': start_point, 'point2': end_point, 'width': 2})
                l_draw_time = False

            start_point, end_point = None, None
            dragging = False
            prior_rect = None

        # Add Text to Plot Diagram Events
        if event == "-PLOTPOINT-":
            id = graph.draw_text(values["-POINTSTRING-"], (300, 300), font = ('Arial', 8))
            g_elem_list.append({'id': id, 'type': 'text', 'text': values["-POINTSTRING-"], 'point': (300, 300), 'font': ('Arial', 8)})
        if event == "-P&T-":
            id = graph.draw_text(values["-POINTSTRING-"], (300, 300), font = ('Arial', 8))
            g_elem_list.append({'id': id, 'type': 'text', 'text': values["-POINTSTRING-"], 'point': (300, 300), 'font': ('Arial', 8)})
            id = t_graph.draw_text(values["-POINTSTRING-"], (300, 300), font = ('Arial', 8))
            t_elem_list.append({'id': id, 'type': 'text', 'text': values["-POINTSTRING-"], 'point': (300, 300), 'font': ('Arial', 8)})
        #--------------------------------------------------------------------------------

        # TIMELINE EVENTS ---------------------------------------------------------------
        # Graph events
        if event == "-TIMELINE-":
            # Initialize values for tracking
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
                # Move an element by change in x and y
                if values['-MOVE1-']:
                    for fig in drag_figures:
                        t_graph.move_figure(fig, delta_x, delta_y)
                        # Edit element location for saving/loading
                        for elem in t_elem_list:
                            if elem['id'] == fig:
                                if elem['type'] == 'text':
                                    elem['point'] = (elem['point'][0] + delta_x, elem['point'][1] + delta_y)
                                else:
                                    elem['point1'] = (elem['point1'][0] + delta_x, elem['point1'][1] + delta_y)
                                    elem['point2'] = (elem['point2'][0] + delta_x, elem['point2'][1] + delta_y)
                        t_graph.update()
                # Draw a line (draws and deletes constantly until mouse up)
                elif values['-LINE1-']:
                    id = prior_rect = t_graph.draw_line(start_point, end_point, width = 2)
                    l_draw_time = True
                # Erase element and remove from data struct
                elif values['-ERASE1-']:
                    for figure in drag_figures:
                        t_graph.delete_figure(figure)
                        for elem in t_elem_list:
                            if elem['id'] == figure:
                                t_elem_list.remove(elem)
                # Erase all elements and clear data struct
                elif values['-CLEAR1-']:
                    t_graph.erase()
                    t_elem_list.clear()

        # Add dividers to timeline proportionally to predefined timeline size
        if event == "-ADDDIVS-":
            dividers = values["-DIVIDERS-"]
            try:
                dividers = int(dividers)
            except:
                sg.Popup("Please enter an integer.")
            else:
                space = 0
                if dividers > 0:
                    space = 670 / (dividers+1)
                    for divider in range(dividers):
                        id = t_graph.draw_line((space*(divider+1) + 30, 165), (space*(divider+1) + 30, 185), width = 2)
                        t_elem_list.append({'id': id, 'type': 'line', 'point1': (space*(divider+1) + 30, 165), 'point2': (space*(divider+1) + 30, 185), 'width': 2})

        # Add text to Timeline events
        if event == "-TIMEPOINT-":
            id = t_graph.draw_text(values["-TIMESTRING-"], (300, 300), font = ('Arial', 8))
            t_elem_list.append({'id': id, 'type': 'text', 'text': values["-TIMESTRING-"], 'point': (300, 300), 'font': ('Arial', 8)})
        if event == "-T&P-":
            id = graph.draw_text(values["-TIMESTRING-"], (300, 300), font = ('Arial', 8))
            g_elem_list.append({'id': id, 'type': 'text', 'text': values["-TIMESTRING-"], 'point': (300, 300), 'font': ('Arial', 8)})
            id = t_graph.draw_text(values["-TIMESTRING-"], (300, 300), font = ('Arial', 8))
            t_elem_list.append({'id': id, 'type': 'text', 'text': values["-TIMESTRING-"], 'point': (300, 300), 'font': ('Arial', 8)})
        #=======================================================================

        #===================== CHARACTER MAP EVENTS ============================
        # Graph events
        if event == "-CHARMAP-":
            # Initialize values for tracking
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
                # Move an element by change in x and y
                if values['-MOVE2-']:
                    for fig in drag_figures:
                        map_graph.move_figure(fig, delta_x, delta_y)
                        # Edit element location for saving/loading
                        for elem in m_elem_list:
                            if elem['id'] == fig:
                                if elem['type'] == 'text' or elem['type'] == 'image':
                                    elem['point'] = (elem['point'][0] + delta_x, elem['point'][1] + delta_y)
                                else:
                                    elem['point1'] = (elem['point1'][0] + delta_x, elem['point1'][1] + delta_y)
                                    elem['point2'] = (elem['point2'][0] + delta_x, elem['point2'][1] + delta_y)
                        map_graph.update()
                # Draw a line (draws and deletes constantly until mouse up)
                elif values['-LINE2-']:
                    id = prior_rect = map_graph.draw_line(start_point, end_point, width = 2, color = values["-LINECOL-"])
                    l_draw_map = True
                # Erase element and remove from data struct
                elif values['-ERASE2-']:
                    for figure in drag_figures:
                        map_graph.delete_figure(figure)
                        for elem in m_elem_list:
                            if elem['id'] == figure:
                                m_elem_list.remove(elem)
                # Erase all elements and clear data struct
                elif values['-CLEAR2-']:
                    map_graph.erase()
                    m_elem_list.clear()

        # Attempt insertion of image into the graph
        if event == "-CHARIMAGE-":
            try:
                formatted = get_img_data(values["-IMAGEPATH-"])
                id = map_graph.draw_image(data = formatted, location = (200, 200))
                m_elem_list.append({'id': id, 'type': 'image', 'path': values["-IMAGEPATH-"], 'point': (200, 200)})
            except:
                sg.Popup("Add Image Failed. Ensure file/path is correct and an image.")

        # Add text to Character Map
        if event == "-CHARTEXTBUTTON-":
            id = map_graph.draw_text(values["-CHARTEXT-"], (300, 300), font = ('Arial', 8))
            m_elem_list.append({'id': id, 'type': 'text', 'text': values["-CHARTEXT-"], 'point': (300, 300), 'font': ('Arial', 8)})
        #==========================================================================

    # Close window when exited
    window.close()

def create_home_layout():
    '''
    create_home_layout Function: Creates column of text/inputs/buttons for Home Tab

    Returns: home_layout: list of lists that contain all elements
    '''
    home_layout = [[sg.VPush()],
                   [sg.Text("Welcome to AuthorEyes!", font = ('Times New Roman', 35))],
                   [sg.Text("Enter information below to get started:", font = ('Times New Roman', 15))],
                   [sg.Input("Story Title", key = "-TITLE-")], 
                   [sg.Input("Author", key = "-AUTHOR-")], 
                   [sg.Input("File Name/Path (json only!)", key = "-FILENAME-", size = (36, None)),
                    sg.FileBrowse()], 
                   [sg.Button("Save All", key = "-SAVE-", size = (10, None)), 
                    sg.Button("Load", key = "-LOAD-", size = (10, None))],
                   [sg.VPush()],
                   [sg.VPush()]]
    return home_layout

def create_chapt_col(chapters):
    '''
    create_chapt_col Function: Creates column of inputs/buttons for Chapter Planner Tab

    Args: chapters: # of created chapters

    Returns: chapt_col: list of lists that contain all elements
    '''
    chapt_col = [[sg.pin(sg.Col(layout = [[sg.Input("Ch #", size = (5, None), key = ("-CHNUM-", chapters)), 
                  sg.Input("Narrator/POV Character", size = (30, None), key = ("-POV-", chapters)), 
                  sg.Input("Chapter Title", expand_x = True, key = ("-CHT-", chapters))], 
                 [sg.Multiline(size = (125, 15), expand_x = True, key = ("-CHMUL-", chapters))]], key = ("-ROW-", chapters)))]]
    return chapt_col

def create_plot_col():
    '''
    create_plot_col Function: Creates column of text/inputs/buttons for Plot Diagram Tab

    Returns: plot_col: list of lists that contain all elements
    '''
    plot_col = [[sg.Text('Choose what clicking/dragging does:', enable_events=True)],
                [sg.Radio('Draw Line', 1, key='-LINE-', enable_events=True)],
                [sg.Radio('Erase Item', 1, key='-ERASE-', enable_events=True)],
                [sg.Radio('Erase All (INCLUDES DIAGRAM!)', 1, key='-CLEAR-', enable_events=True)],
                [sg.Radio('Move Item', 1, True, key='-MOVE-', enable_events=True)],
                [sg.Text("-------------------------------------------------------\nInsert Plot Points:")],
                [sg.Multiline("Write a plot point here!\nType enter when going to new line\nfor multiple lines when added", key="-POINTSTRING-", size = (30, 10))],
                [sg.Button("Add Plot Point", key="-PLOTPOINT-")], 
                [sg.Button("Add to this and Timeline", key = "-P&T-")]]
    return plot_col

def create_t_col():
    '''
    create_t_col Function: Creates column of text/inputs/buttons for Timeline Tab

    Returns: t_col: list of lists that contain all elements
    '''
    t_col = [[sg.Text('Choose what clicking/dragging does:', enable_events=True)],
             [sg.Radio('Draw Line', 1, key='-LINE1-', enable_events=True)],
             [sg.Radio('Erase Item', 1, key='-ERASE1-', enable_events=True)],
             [sg.Radio('Erase All (INCLUDES DIAGRAM!)', 1, key='-CLEAR1-', enable_events=True)],
             [sg.Radio('Move Item', 1, True, key='-MOVE1-', enable_events=True)],
             [sg.Input('0', key = "-DIVIDERS-", size = (3, None)), 
              sg.Button('Add Timeline Dividers', key = "-ADDDIVS-")],
             [sg.Text("-------------------------------------------------------\nInsert Events:")],
             [sg.Multiline("Write timeline event here!\nType enter when going to new line\nfor multiple lines when added", key="-TIMESTRING-", size = (30, 10))],
             [sg.Button("Add Event", key="-TIMEPOINT-")], 
             [sg.Button("Add to this and Plot Diagram", key = "-T&P-")]]
    return t_col

def create_char_col():
    '''
    create_char_col Function: Creates column of text/inputs/buttons for Character Map Tab

    Returns: char_col: list of lists that contain all elements
    '''
    char_col = [[sg.Text("Choose what clicking/dragging does:", enable_events=True)],
                [sg.Radio("Draw Line", 1, key='-LINE2-', enable_events=True), 
                 sg.Input("#000000", size = (7, None), key = "-LINECOL-"),
                 sg.ColorChooserButton(button_text = "Line Color")],
                [sg.Radio("Erase Item", 1, key='-ERASE2-', enable_events=True)],
                [sg.Radio("Erase All", 1, key='-CLEAR2-', enable_events=True)],
                [sg.Radio("Move Item", 1, True, key='-MOVE2-', enable_events=True)],
                [sg.Text("-------------------------------------------------------\nInsert Character Images and Text:")],
                [sg.Input("Image Filepath", key = "-IMAGEPATH-", size = (20, None)), 
                 sg.FileBrowse()],
                [sg.Button("Add Character Image", key = "-CHARIMAGE-", size = (25, None))],
                [sg.Multiline("Write names, relationships, etc.\nType enter when going to new line\nfor multiple lines when adding", key = "-CHARTEXT-", size = (30, 10))],
                [sg.Button("Add Text", key = "-CHARTEXTBUTTON-", size = (25, None))]]
    return char_col

def initialize_plot(window, g_elem_list):
    '''
    initialize_plot Function: draws plot diagram to Plot Diagram graph and adds figures to data struct for save/load
    '''
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

def initialize_tline(window, t_elem_list):
    '''
    initialize_tline Function: draws timeline to Timeline graph and adds figures to data struct for save/load
    '''
    id = window["-TIMELINE-"].draw_line((30, 175), (700, 175), width = 2)
    t_elem_list.append({'id': id, 'type': 'line', 'point1': (30, 175), 'point2': (700, 175), 'width': 2})
    id = window["-TIMELINE-"].draw_line((30, 155), (30, 195), width = 2)
    t_elem_list.append({'id': id, 'type': 'line', 'point1': (30, 155), 'point2': (30, 195), 'width': 2})
    id = window["-TIMELINE-"].draw_line((700, 155), (700, 195), width = 2)
    t_elem_list.append({'id': id, 'type': 'line', 'point1': (700, 155), 'point2': (700, 195), 'width': 2})

def get_img_data(f, maxsize = (75, 75)):
    '''
    get_img_data Function: converts image to proper formatting for adding to Character Map graph

    Args:
        f: image file path as string
        maxsize: size for image to be resized to

    Returns: returns PNG image as bytes to be drawn
    '''
    img = Image.open(f)
    img.thumbnail(maxsize)
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    return bio.getvalue()

main()