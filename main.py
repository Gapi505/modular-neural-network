# Event Loop to process "events" and get the "values" of the inputs
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QMessageBox
import sys
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor, QFont
from PyQt5.QtCore import Qt, QRect, QThread, QLine, QRectF, QLineF
import time
import pickle

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

def increase_distance(x):
    return (1 + math.log10(x))*0.5

Layers = [3, 4,2]
Nodes = []
In = [1,1,1]
Out = []

Weights_To_Save = []
Biases_To_Save = []

# GUI settings
Gui_Scale = 1
Max_Weight_Width = 5

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
    def load():
        return

    
    def save(self):
        for i in self.weights:
            Weights_To_Save.append(i)
        Biases_To_Save.append(self.bias)

        return
            

def Save_All():
    with open('model.fart', 'wb') as f:
        pickle.dump(Weights_To_Save, f)
        pickle.dump(Biases_To_Save, f)
    return  
def Load_All():
    with open('model.fart', 'rb') as f:
        Weights_To_Load = pickle.load(f)
        print(len(Weights_To_Load))
        Biases_To_Load = pickle.load(f)
        print(len(Biases_To_Load))
    i=0
    p=0
    for node in Nodes:
        node.bias = Biases_To_Load[i]

        for w in range(len(node.weights)):
            node.weights[w] = Weights_To_Load[p]
            p+=1

        i+=1



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

def CALL_ALL(func, *args):
    if len(In) != Layers[0]:
        print(f"{bcolors.WARNING}Error: len(In) does not match Layers[0]! Quitting!{bcolors.ENDC}")
        exit()
    for node in Nodes:
        function = getattr(node, func)
        function()

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
        Draw_Node_Locations = []
        Draw_Node_Colors = []
        Max_Nodes_In_Layer = 0
        Draw_Weight_Locations = []
        Draw_Weight_Width = []
        for num in Layers: 
            if num > Max_Nodes_In_Layer: Max_Nodes_In_Layer = num
        for x in range(len(Layers)):
            for y in range(Layers[x]):
                Draw_Node_Locations.append(QRectF(int(((50*x*increase_distance(Max_Nodes_In_Layer))+5)*Gui_Scale), int(((30*y+5) + ((Max_Nodes_In_Layer*30)-(Layers[x]*30))/2)*Gui_Scale), 20*Gui_Scale, 20*Gui_Scale))
                Draw_Node_Colors.append(QColor(int((Get_Node_By_Coord(x,y).value*220)),int(Get_Node_By_Coord(x,y).value*225),int(Get_Node_By_Coord(x,y).value*255)))
                

                for w in range(len(Get_Node_By_Coord(x,y).weights)):
                    ids = Get_Node_By_Coord(x,y).prev_layer_node_ids
                    weights = Get_Node_By_Coord(x,y).weights
                    for i in ids:
                        Draw_Weight_Locations.append(QLineF(Draw_Node_Locations[i].x() +10**Gui_Scale,   Draw_Node_Locations[i].y() +10*Gui_Scale,  int(((50*x*increase_distance(Max_Nodes_In_Layer))+15)*Gui_Scale),  int(((y*30 +15)+ int(((Max_Nodes_In_Layer*30)-(Layers[x]*30))/2))*Gui_Scale)))
                    for i in range(len(weights)):
                        Draw_Weight_Width.append(ModifiedSigmoid(weights[i])*Max_Weight_Width+1)


                
        return(Draw_Node_Locations,Draw_Node_Colors,Draw_Weight_Locations, Draw_Weight_Width)


    def draw_result(painter,result):
        Draw_Locations, Draw_Colors,Draw_Weights, Draw_Weights_Width = result
        for w in range(len(Draw_Weights)):
            painter.setPen(QPen(Qt.black, Draw_Weights_Width[w]))
            painter.drawLine(Draw_Weights[w])
        for i in range(len(Draw_Locations)):
            painter.setBrush(QBrush(Draw_Colors[i]))
            painter.setPen(QPen(Qt.black, 2))
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

            Max_Nodes_In_Layer = 0
            for num in Layers: 
                if num > Max_Nodes_In_Layer: Max_Nodes_In_Layer = num

            self.save_button = QPushButton("SAVE", self)
            self.save_button.move(int(len(Layers)*50*Gui_Scale*increase_distance(Max_Nodes_In_Layer)+10), 10)
            self.save_button.clicked.connect(self.on_save_button_clicked)

            self.load_button = QPushButton("LOAD", self)
            self.load_button.move(int(len(Layers)*50*Gui_Scale*increase_distance(Max_Nodes_In_Layer)+10), 50)
            self.load_button.clicked.connect(self.on_load_button_clicked)

            self.save_button.setStyleSheet("background-color: rgb(64,71,84);")
            self.load_button.setStyleSheet("background-color: rgb(64,71,84);")

            self.save_button.setFont(QFont("Arial", 13, QFont.Bold))
            self.load_button.setFont(QFont("Arial", 13, QFont.Bold))


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

        def on_save_button_clicked(self, event):
            message_box = QMessageBox(QMessageBox.Question, 'Confirmation', 'Are you shure you want to do this?\nThis wil overwrite the currently saved model', QMessageBox.Yes | QMessageBox.No)

            # Show the message box and store the result (either QMessageBox.Yes or QMessageBox.No)
            result = message_box.exec_()

            # If the result is "Yes", do something
            if result == QMessageBox.Yes:
                CALL_ALL('save')
                Save_All()
            # If the result is "No", do something else
            else:
                return




        def on_load_button_clicked(self, event):
            message_box = QMessageBox(QMessageBox.Question, 'Confirmation', 'Are you shure you want to do this?\nThis wil overwrite the current model', QMessageBox.Yes | QMessageBox.No)

            # Show the message box and store the result (either QMessageBox.Yes or QMessageBox.No)
            result = message_box.exec_()

            # If the result is "Yes", do something
            if result == QMessageBox.Yes:
                Load_All()
            # If the result is "No", do something else
            else:
                return


    app = QApplication(sys.argv)
    window = MyWidget()
    window.setGeometry(100, 100, 1028, 720)
    window.setStyleSheet("background-color: rgb(40,44,52);color: white;")
    window.show()

    # Create and start the computation thread
    computation_thread = ComputationThread(window)
    computation_thread.start()

    sys.exit(app.exec_())


            
INIT()
CALC_ALL()
Display()






"""

NOTES and IDEAS:

    -file format for models be named FART (Futuristic Ai Retention Technology)


"""