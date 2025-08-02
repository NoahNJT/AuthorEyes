import PySimpleGUI as sg 

# Always check for a Window Closed event immediately following your window.read() call
# if event == sg.WIN_CLOSED or even == 'Exit': break ; assume the values variable will ahvea  value that's not usable

character_list = ["Thellon", "Aila", "Root", "Lita"]
character_locations = [(50,50),(50, 300),(300, 50), (300, 300)]

cp_tab_layout = [[sg.OptionMenu(character_list), sg.Input("Chapter Title", size = (113, None))], [sg.Multiline(size = (125, 15))]]
chapter_tab = [[sg.TabGroup([[sg.Tab("Chapter 1", cp_tab_layout, key="-tabs-")]])], [sg.Button("Add Chapter")], [sg.Button("Remove Chapter")]]

# TRY TO IMPLEMENT PILLOW: for images; can maybe see if there is a way of doing graph for the character map
# Maybe could do classes with characters where main characters are at the top of the tree and have preset connection points?
# Could color code lines instead of it being labeled; could do a circle of characters and keep position information for lines
# Make each character a box with their name and (optionally) a picture (use default person if not)
character_frame_layout = [[sg.OptionMenu(character_list),
                           sg.OptionMenu(character_list),
                           sg.Input(), 
                           sg.ColorChooserButton("Select Color")]]

character_tab = [[sg.Graph((1000, 400),(0, 0),(1000, 400), background_color="white", key = "-CMAP-")], 
                 [sg.Frame('Characters', character_frame_layout)]]

# MAYBE: try to do a plot points in a container element with extend layout/make invisible; try text box with an update button
col = [[sg.Text('Choose what clicking/dragging does:', enable_events=True)],
       [sg.Radio('Draw Rectangle', 1, key='-RECT-', enable_events=True)],
       [sg.Radio('Draw Line', 1, key='-LINE-', enable_events=True)],
       [sg.Radio('Erase Item', 1, key='-ERASE-', enable_events=True)],
       [sg.Radio('Erase All', 1, key='-CLEAR-', enable_events=True)],
       [sg.Radio('Move All Items', 1, key='-MOVEALL-', enable_events=True)],
       [sg.Radio('Move Item', 1, True, key='-MOVE-', enable_events=True)]]

plot_tab = [[sg.Graph((720, 400),(0, 0),(720, 400), background_color="white", key = "-DIAGRAM-", change_submits=True, drag_submits=True), sg.Col(col)], 
            [sg.Button("Add Plot Point", key="-PLOTPOINT-"), sg.Multiline(key="-POINTSTRING-")]]

layout = [[sg.TabGroup([[sg.Tab("Chapter Planner", chapter_tab)], [sg.Tab("Character Map", character_tab)], [sg.Tab("Plot Diagram", plot_tab)]])]]

window = sg.Window("AuthorEyes", layout, size=(1000,500))
window.finalize()
window["-DIAGRAM-"].draw_text("Exposition", (100, 110), font = ('Arial', 8))
window["-DIAGRAM-"].draw_text("Rising Action", (260, 240), font = ('Arial', 8))
window["-DIAGRAM-"].draw_text("Falling Action", (530, 290), font = ('Arial', 8))
window["-DIAGRAM-"].draw_text("Resolution", (625, 230), font = ('Arial', 8))
window["-DIAGRAM-"].draw_line((30, 100), (170, 100), width = 2)
window["-DIAGRAM-"].draw_line((170, 100), (420, 350), width = 2)
window["-DIAGRAM-"].draw_line((420, 350), (550, 220), width = 2)
window["-DIAGRAM-"].draw_line((550, 220), (700, 220), width = 2)


dragging = False
graph = window["-DIAGRAM-"]
start_point = end_point = prior_rect = None
graph.bind('<Button-3>', '+RIGHT+')

chapter = 0

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == "Add Chapter":
        chapter += 1
        chapter_tab[0][0].add_tab(sg.Tab(f'Chapter {chapter+1}', [[sg.OptionMenu(character_list), 
                                                                   sg.Input("Chapter Title", size = (113, None))], 
                                                                  [sg.Multiline(size = (125, 15))]]))

    if event in ('-MOVE-', '-MOVEALL-'):
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
                    graph.update()
            elif values['-RECT-']:
                prior_rect = graph.draw_rectangle(start_point, end_point)
            elif values['-LINE-']:
                prior_rect = graph.draw_line(start_point, end_point, width = 2)
            elif values['-ERASE-']:
                for figure in drag_figures:
                    graph.delete_figure(figure)
            elif values['-CLEAR-']:
                graph.erase()
            elif values['-MOVEALL-']:
                graph.move(delta_x, delta_y)
    elif event.endswith('+UP'):  # The drawing has ended because mouse up
        start_point, end_point = None, None  # enable grabbing a new rect
        dragging = False
        prior_rect = None

    if event == "-PLOTPOINT-":
        graph.draw_text(values["-POINTSTRING-"], (100, 100), font = ('Arial', 8))

window.close()