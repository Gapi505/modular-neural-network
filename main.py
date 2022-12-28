# Event Loop to process "events" and get the "values" of the inputs
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
import sys
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor
from PyQt5.QtCore import Qt, QRect, QThread
import time

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

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def ModifiedSigmoid(x):
    if x < 0:
        x=0
    return (1 / (1 + math.exp(-x)))-0.5

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
        elif self.layer != 0:
            for i in self.prev_layer_node_ids:
                self.prev_layer_node_values.append(Nodes[i].value)
            for i in range(len(self.prev_layer_node_values)):
                self.value += self.prev_layer_node_ids[i]*self.weights[i]
            self.value += self.bias
            self.value = ModifiedSigmoid(self.value)
            #print(self.prev_layer_node_values)
            #print(self.layer)
        #print(self.value)
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

def Get_Node_By_Coord(layer, place_in_layer):
    if place_in_layer > Layers[layer]:
        print(f"{bcolors.WARNING}Error: place_in_layer out of range! Quitting!{bcolors.ENDC}")
        exit()
    id = 0
    for i in range(layer):
        id += Layers[i]
    id += place_in_layer
    return(Nodes[id])


def Display():

    def compute():
        Draw_Locations = []
        Draw_Colors = []
        for x in range(len(Layers)):
            for y in range(Layers[x]):
                Draw_Locations.append(QRect(50*x+5, 30*y+5, 20, 20))
                Draw_Colors.append(QColor(int(Get_Node_By_Coord(x,y).value*255),int(Get_Node_By_Coord(x,y).value*255),int(Get_Node_By_Coord(x,y).value*255)))
                #print(Get_Node_By_Coord(x,y).node_id)
                #print(Get_Node_By_Coord(x,y).value)
                
        return(Draw_Locations,Draw_Colors)


    def draw_result(painter,result):
        Draw_Locations, Draw_Colors = result
        for i in range(len(Draw_Locations)):
            painter.setBrush(QBrush(Draw_Colors[i]))
            painter.setPen(QPen(Qt.black, 3))
            painter.drawEllipse(Draw_Locations[i])
        return()

    class ComputationThread(QThread):
        def __init__(self, widget):
            super().__init__()
            self.widget = widget

        def run(self):
            # Perform the computations in a separate thread
            result = compute()

            # Update the widget in the main thread
            self.widget.update_result(result)

    class MyWidget(QWidget):
        def __init__(self):
            super().__init__()
            self.result = None

        def paintEvent(self, event):
            # Create and use the QPainter object within the paintEvent method
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)

            # Draw the result of the computations
            if self.result is not None:
                draw_result(painter, self.result)

        def update_result(self, result):
            # Update the result and redraw the widget
            self.result = result
            self.update()

    app = QApplication(sys.argv)
    window = MyWidget()
    window.setStyleSheet("background-color: rgb(20,20,20);")
    window.show()

    # Create and start the computation thread
    computation_thread = ComputationThread(window)
    computation_thread.start()

    sys.exit(app.exec_())


            
INIT()
CALC_ALL()
Display()
