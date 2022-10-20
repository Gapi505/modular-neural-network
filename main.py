import PySimpleGUI as sg

sg.theme('DarkBlack')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Some text on Row 1')],
            [sg.Text('Enter something on Row 2'), sg.InputText()],
            [sg.Button('Ok'), sg.Button('Cancel')] ]

# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events" and get the "values" of the inputs

Layers = [3, 4, 2]
Nodes = []

class NODE():
    def __init__(self, layer, node_id):
        self.layer = layer  #                                   !
        self.bias = 0    #                                   !
        self.node_id = node_id    #                       !   set up basic variables
        self.this_layer_node_count = Layers[self.layer]    #               !
        self.prev_layer_node_count = Layers[self.layer-1]   #   !

        self.all_layers_from_start_node_count_arr = Layers[0:self.layer]
        self.all_layers_from_start_node_count = 0
        for i in range(len(self.all_layers_from_start_node_count_arr)):
            self.all_layers_from_start_node_count += self.all_layers_from_start_node_count_arr[i]
        self.all_layers_from_start_node_count += self.this_layer_node_count
        self.prev_layer_node_ids = []
        if layer!=0:
            for i in range(self.prev_layer_node_count):
               self.prev_layer_node_ids.append(self.all_layers_from_start_node_count - self.prev_layer_node_count - self.this_layer_node_count + i)

        self.weights = []
        if layer!=0:
            for i in range(len(self.prev_layer_node_ids)):
               self.weights.append(0)
        
        self.value = 0


    def calculate(self):
        return


        
        

def INIT():
    node_count = []
    for i in range(len(Layers)):
        node_count.append(Layers[i])# gets the number of neurons in this layer
    id = 0
    for n in range(len(Layers)):
        for i in range(node_count[n]):
            Nodes.append(NODE(n, id))
            id += 1
        for i in range(node_count[n]):
            Nodes[i].calculate()
INIT()
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    print('You entered ', values[0])

window.close()