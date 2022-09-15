import graphviz as gp
class Cola:
    def __init__(self):
        self.top = None

    def enqueue(self, nodo):
        tmp = self.top

        if tmp == None:
            self.top = nodo
        else:
            while tmp.sig != None:
                tmp = tmp.sig
            tmp.sig = nodo
        self.update_values()

    def dequeue(self):
        tmp = self.top
        tmp.espera = 0
        self.top = self.top.sig
        self.update_values()
        return tmp

    def update_values(self):
        tmp = self.top
        acum = 0
        while tmp != None:
            tmp.espera = acum
            acum += tmp.tiempo
            tmp = tmp.sig
        
class HotDog:
    def __init__(self, cliente, ingrediente, tiempo):
        self.cliente = cliente
        self.ingrediente = ingrediente
        self.tiempo = tiempo
        self.espera = None
        self.sig = None

ingredientes={"op1" : "Salchicha",
              "op2" : "Chorizo",
              "op3" : "Salami",
              "op4" : "Longaniza",
              "op5" : "Costilla"}

duracion = {"Salchicha" : 2,
            "Chorizo" : 3,
            "Salami" : 1.5,
            "Longaniza" : 4,
            "Costilla" : 6}

cola_de_pedidos = Cola()
opcion = None

def ponerOrden():
    nombre = input("Ingresa tu nombre: ")
    ordenes = int(input("Ingresa el numero de shucos que quieres pedir: "))
    print("""########## Menú ##########
# 1.- Salchicha          #
# 2.- Chorizo            #
# 3.- Salami             #
# 4.- Longaniza          #
# 5.- Costilla           #
##########################""")
    for i in range(ordenes):
        opciones = input("ingrese el numero de las opciones que desea añadir para el shuco No."+str(i+1)+", separado por una coma: ")
        opciones = opciones.split(",")
        orden = []

        for op in opciones:
            orden.append(ingredientes["op"+op])
        tiempo = 0
        for ing in orden:
            tiempo+=duracion[ing]
            
        cola_de_pedidos.enqueue(HotDog(nombre+", Orden No."+str(i+1),orden,tiempo))

        print("Orden añadida a la cola")

def ver_orden():
    s = gp.Digraph("Lista de pedidos", filename = 'pedidos.gv',
               node_attr={'shape': 'record'})
    tmp = cola_de_pedidos.top
    ant = None
    s.attr(rankdir='LR', size='8,5')
    while tmp != None:
        label = ""
        label += "{Nombre: " + tmp.cliente + "}|{Ingredientes:"
        for ingrediente in tmp.ingrediente:
            label += " " + ingrediente + ","
        label = label[:-1]
        label+= "}|{Tiempo de orden: " + str(tmp.tiempo) + " mins" + "}|{Tiempo en cola: " + str(tmp.espera) + " mins}"
        actual = s.node(tmp.cliente + str(tmp.tiempo),label)
        if ant == None:
            ant = tmp.cliente +str(tmp.tiempo)
        else:
            s.attr("edge",arrowhead="vee", arrowtail="inv", arrowsize=".7", color="maroon", fontsize="10",
          fontcolor="navy")
            s.edge(ant,tmp.cliente +str(tmp.tiempo))
            ant = tmp.cliente +str(tmp.tiempo)
        label = "Tiempo Total restante en cola: " + str(tmp.espera+tmp.tiempo) + " mins"
        s.node("final", label)
        tmp = tmp.sig
    s.edge(ant,"final")
    s.view()

def despachar():
    tmp = cola_de_pedidos.dequeue()
    j = gp.Digraph("pedido despachado", filename = 'despache.gv',
               node_attr={'shape': 'record'})
    j.attr(rankdir='LR', size='8,5')
    label = ""
    label += "{Nombre: " + tmp.cliente + "}|{Ingredientes:"
    for ingrediente in tmp.ingrediente:
        label += " " + ingrediente + ","
    label = label[:-1]
    label+= "}|{Tiempo de orden: " + str(tmp.tiempo) + " mins" + "}"
    j.node(tmp.cliente + str(tmp.tiempo),label)
    j.view()
    
while opcion != 4:
    print("""########## Menú ##########
# 1.- Poner orden        #
# 2.- Ver ordenes        #
# 3.- Despachar orden    #
# 4.- Salir              #
##########################""")

    opcion = input("selecciona una opcion: ")

    if opcion == "1":
        ponerOrden()
        ver_orden()
    elif opcion == "2":
        ver_orden()
    elif opcion == "3":
        despachar()
        ver_orden()
    elif opcion == "4":
        input("Nos vemos!")
    else:
        print("no se ha seleccionado una opcion correcta")

       
    
        
        
        
    
        

    

    
