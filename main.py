import PySimpleGUI as sg 

# Always check for a Window Closed event immediately following your window.read() call
# if event == sg.WIN_CLOSED or even == 'Exit': break ; assume the values variable will ahvea  value that's not usable

cp_tab_layout = [[sg.Multiline(size = (None, 1))]]
tab_layout2 = [[sg.Button('Test Button')]]

layout = [[sg.TabGroup([[sg.Tab("Chapter Planner", cp_tab_layout), sg.Tab("Button Tab", tab_layout2)]])]]

window = sg.Window("AuthorEyes", layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

window.close()