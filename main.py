import PySimpleGUI as sg

sg.theme('DarkBlack')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Some text on Row 1')],
            [sg.Text('Enter something on Row 2'), sg.InputText()],
            [sg.Button('Ok'), sg.Button('Cancel')] ]

# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events" and get the "values" of the inputs
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



Layers = [3, 4, 2]
Nodes = []
In = [1,1,1]
Out = []

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
        self.prev_layer_node_values = []
    def calculate(self):
        if self.layer == 0:
            self.value = In[self.node_id]
        if self.layer != 0:
            for i in self.prev_layer_node_ids:
                self.prev_layer_node_values.append(Nodes[i].value)
            for i in range(len(self.prev_layer_node_values)):
                self.value += self.prev_layer_node_ids[i]*self.weights[i]
            self.value += self.bias
            print(self.prev_layer_node_values)
            print(self.layer)
        print(self.value)
        if self.layer == len(Layers):
            Out.append(self.value)
            


def INIT():
    node_arr = []
    for i in range(len(Layers)):
        node_arr.append(Layers[i])# gets the number of neurons in this layer
    id = 0
    for layer in range(len(Layers)):
        for i in range(node_arr[layer]):
            Nodes.append(NODE(layer, id))
            id += 1

def CALC_ALL():
    if len(In) != Layers[0]:
        print(f"{bcolors.WARNING}Error: len(In) does not match Layers[0]! Quitting!{bcolors.ENDC}")
        exit()
    node_count = 0
    for i in range(len(Layers)):
        node_count += Layers[i]
    for i in range(node_count):
            Nodes[i].calculate()
            
INIT()
CALC_ALL()
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    print('You entered ', values[0])

window.close()