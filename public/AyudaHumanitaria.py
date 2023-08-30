import pandas as pd
import numpy as np
from collections import defaultdict, deque

import networkx as nx
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('TkAgg')

import tkinter as tk

    
class centro_poblado: #queda
  #clase para guardar los atributos de los centro poblados del csv
  
  def __init__(self, id, dept, prov, dist, ccpp, capital,
               viviendas, habitantes, clas_inei, s_alimentos,
               s_salud, s_serv_basicos, s_transporte ):
    
    self.id = id
    self.departamento = dept
    self.provincia = prov
    self.distrito = dist
    self.nombre_centro = ccpp
    self.capital = capital #dicta si este centro poblado es una capital o no
    self.nro_viviendas = viviendas
    self.nro_habitantes = habitantes
    self.clas_inei = clas_inei #dicta si este centro pobladoes de clsificacion rural o urbano
    self.s_alimentos = s_alimentos       # todos los atributos que comienzen por 's_'
    self.s_salud = s_salud               # son de situacion de cierto aspecto del centro
    self.s_serv_basicos = s_serv_basicos # y se guardan como un valor de char(1)
    self.s_transporte = s_transporte     # 'A' = alto, 'M' = medio, 'B' = bajo
    
  def mostrar_centro(self):
    return str('['+ self.nombre_centro + ', ' + self.distrito + ']')
  
#tratamiento de data
def leer_data_nodos():
  datos_nodos = pd.read_csv('C:/Users/ERICK/Downloads/NODOSCentrosPobladosCSV.csv', sep = ';', header = 0, encoding = 'latin-1') 
  N = np.asarray(datos_nodos) 
  
  centros = [] # se crea una lista para guardar los (objetos) nodos
  
  for centro in N: # para cada entrada de centro # se termina creando la lista de 1500 objetos
    nodo = centro_poblado(centro[0], centro[1], centro[2], centro[3], centro[4],centro[5], centro[6],
                          centro[7], centro[8], centro[9],centro[10], centro[11], centro[12])
    
    centros.append(nodo) # se crearon los objetos de 1500 nodos
    
  return centros

def leer_data_aristas():
  data_aristas = pd.read_csv('C:/Users/ERICK/Downloads/ARISTASCentrosPoblados-DistanciasCSV.csv', sep =";", usecols = range(1, 1501), header = 0)
  A = np.asarray(data_aristas)
  return A

def crear_grafo(centros, aristas, ni, nf):
  grafo = defaultdict(list)
  
  for i in range(ni, nf):
    grafo[centros[i].id] = [] # para cada id (osea por cada nodo) se crea una lista donde se guardaran los id de los nodos a los que tiene aristas
    
    for j in range(ni, nf): #mayor numero que los nodos para los subgrafos
      if(aristas[i, j] > 0 and i<j):
        
        grafo[centros[i].id].append(centros[j].id) #añade el id a la lista del nodo si la arista entre los 2 nodos es mayor a 0
            
  return grafo
  
centros = leer_data_nodos() # se crea la lista de objetos que guardan los atributos de los centros # desde esta se accede a los atributos
aristas = leer_data_aristas() # matriz de aristas (lista de listas)


def ver_subgrafo_LA(ni, nf):
  # Crear subgrafo dirigido - lista de adyacencia
  grafo = crear_grafo(centros, aristas, ni, nf) # diccionario de listas (para cada llave guarda una lista de id de los nodos adyacentes)

  # Mostar subgrafo
  for nodo, vecinos in grafo.items():
    print(f'{nodo}: {centros[nodo].nombre_centro}', end = ' -> ')
    for vecino in vecinos: # ejemplo de uso del grafo
      print(f'{centros[vecino].id, centros[vecino].mostrar_centro()}', end = ' ')

    print('\n')

#ver_subgrafo_LA(0, 25)
#----------------------------------------------------------------------------------------------------------------------------------BFS
def bfs_habitantes(grafo, start):
    visitados = set()  # Conjunto para almacenar los nodos visitados
    cola = deque()  # Cola para realizar el recorrido en amplitud
    cola.append(start)  # Agregar el nodo inicial a la cola
    visitados.add(start)  # Marcar el nodo inicial como visitado

    resultado_aristas = []
    resultado_nodos =[]
    print("Recorrido de busqueda por amplitud: ")

    while cola:
        nodo = cola.popleft()  # Sacar el nodo de la parte frontal de la cola #pop(0)
        print(nodo, "-> ", end="")

        #Si el numero de habitantes es superior a 100
        if(centros[nodo].nro_habitantes > 100):
            resultado_nodos.append(nodo) # si el nodo cumple, se anade al resultado

        # Recorrer los vecinos del nodo actual
        vecinos = grafo[nodo] # llave de los nodos_vecinos
        for vecino in vecinos: # nodos vecinos
            if vecino not in visitados:
                resultado_aristas.append((nodo, vecino)) # arista (nodo, nodo_vecino) agregado al resultado si nodo_vecino no ha sido visitado antes
                cola.append(vecino)  # Agregar vecino a la cola
                visitados.add(vecino)  # Marcar vecino como visitado

    return resultado_aristas, resultado_nodos

def bfs_capital(grafo, start):
    visitados = set()  # Conjunto para almacenar los nodos visitados
    cola = deque()  # Cola para realizar el recorrido en amplitud
    cola.append(start)  # Agregar el nodo inicial a la cola
    visitados.add(start)  # Marcar el nodo inicial como visitado

    resultado_aristas = []
    resultado_nodos =[]
    print("Recorrido de busqueda por amplitud: ")

    while cola:
        nodo = cola.popleft()  # Sacar el nodo de la parte frontal de la cola
        print(nodo, "-> ", end="")

        #Si es capital de una provincia
        if (centros[nodo].capital == 1):
            resultado_nodos.append(nodo) # si el nodo cumple, se anade al resultado

        # Recorrer los vecinos del nodo actual
        vecinos = grafo[nodo] # llave de los nodos_vecinos
        for vecino in vecinos: # nodos vecinos
            if vecino not in visitados:
                resultado_aristas.append((nodo, vecino)) # arista (nodo, nodo_vecino) agregado al resultado si nodo_vecino no ha sido visitado antes
                cola.append(vecino)  # Agregar vecino a la cola
                visitados.add(vecino)  # Marcar vecino como visitado

    return resultado_aristas, resultado_nodos

def bfs_vivienda(grafo, start):
    visitados = set()  # Conjunto para almacenar los nodos visitados
    cola = deque()  # Cola para realizar el recorrido en amplitud
    cola.append(start)  # Agregar el nodo inicial a la cola
    visitados.add(start)  # Marcar el nodo inicial como visitado

    resultado_aristas = []
    resultado_nodos =[]
    print("Recorrido de busqueda por amplitud: ")

    while cola:
        nodo = cola.popleft()  # Sacar el nodo de la parte frontal de la cola
        print(nodo, "-> ", end="")

        #Si el numero de viviendas es superior a 50
        if(centros[nodo].nro_viviendas > 50):
            resultado_nodos.append(nodo) # si el nodo cumple, se anade al resultado

        # Recorrer los vecinos del nodo actual
        vecinos = grafo[nodo] # llave de los nodos_vecinos
        for vecino in vecinos: # nodos vecinos
            if vecino not in visitados:
                resultado_aristas.append((nodo, vecino)) # arista (nodo, nodo_vecino) agregado al resultado si nodo_vecino no ha sido visitado antes
                cola.append(vecino)  # Agregar vecino a la cola
                visitados.add(vecino)  # Marcar vecino como visitado

    return resultado_aristas, resultado_nodos

def bfs_necesidades(grafo, start):
    visitados = set()  # Conjunto para almacenar los nodos visitados
    cola = deque()  # Cola para realizar el recorrido en amplitud
    cola.append(start)  # Agregar el nodo inicial a la cola
    visitados.add(start)  # Marcar el nodo inicial como visitado

    resultado_aristas = []
    resultado_nodos =[]
    print("Recorrido de busqueda por amplitud: ")

    while cola:
        nodo = cola.popleft()  # Sacar el nodo de la parte frontal de la cola
        print(nodo, "-> ", end="")

        #Si el centro tiene necesidades con estado ALTO o MEDIO
        if(centros[nodo].s_alimentos != 'B' and centros[nodo].s_salud != 'B' and centros[nodo].s_serv_basicos != 'B' and centros[nodo].s_transporte !='B'):
            resultado_nodos.append(nodo) # si el nodo cumple, se anade al resultado

        # Recorrer los vecinos del nodo actual
        vecinos = grafo[nodo] # llave de los nodos_vecinos
        for vecino in vecinos: # nodos vecinos
            if vecino not in visitados:
                resultado_aristas.append((nodo, vecino)) # arista (nodo, nodo_vecino) agregado al resultado si nodo_vecino no ha sido visitado antes
                cola.append(vecino)  # Agregar vecino a la cola
                visitados.add(vecino)  # Marcar vecino como visitado

    return resultado_aristas, resultado_nodos

#dibujar bfs                
def crear_grafo_nx(grafo):
  G = nx.Graph()
  
  for nodo, vecinos in grafo.items():
        for vecino in vecinos:

            nodo1 = nodo
            nodo2 = centros[vecino].id

            G.add_edge(nodo1, nodo2)
            
  return G

def dibujarGrafo(G):
  pos = nx.spring_layout(G)
  nx.draw(G, pos, with_labels = True)  # with_labels=true es para mostrar los nodos

  edge_labels = nx.get_edge_attributes(G, 'length')
  nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_labels, font_size = 11)

  return pos
  
  
def probar_bfs_habitantes(ni, nf):
    resultado = ""
    grafo = crear_grafo(centros, aristas, ni, nf)
    G = crear_grafo_nx(grafo)
    pos = dibujarGrafo(G)
    resultado_aristas, resultado_nodos = bfs_habitantes(grafo, ni) # el int que se pasa es el nodo inicial

    # Imprimir el resultado de la busqueda
    resultado += "\n\nCentros poblados con numero de habitantes mayor a 100: \n"
    for i in resultado_nodos:
      resultado += (f"[{i}]{centros[i].nombre_centro}: {centros[i].nro_habitantes} habitantes \n")

    # Dibujar el BFS
    for arista in resultado_aristas:
         if (arista[0], arista[1]) in G.edges():
             nx.draw_networkx_edges(G, pos, edgelist = [(arista[0], arista[1])],
                                    width = 2.0, alpha = 0.6, edge_color = 'orange') #si es parte del resultado, se pinta la arista
    for nodo in resultado_nodos:
        if nodo in G.nodes():
              nx.draw_networkx_nodes(G, pos, nodelist = [nodo], node_color = '#ff8000') #si cumplio con la condicion, se pinta el nodo
    
    #plt.show() en la ventana
    return resultado
    
def probar_bfs_capital(ni, nf):
    resultado = ""
    grafo = crear_grafo(centros, aristas, ni, nf)
    G = crear_grafo_nx(grafo)
    pos = dibujarGrafo(G)
    resultado_aristas, resultado_nodos = bfs_capital(grafo, ni) # el int que se pasa es el nodo inicial

    # Imprimir el resultado de la busqueda
    resultado += "\n\nCentros poblados que son capitales de distrito: \n"
    for i in resultado_nodos:
      resultado += (f"[{i}]{centros[i].nombre_centro} es capital de {centros[i].distrito} \n")


    # Dibujar el BFS
    for arista in resultado_aristas:
         if (arista[0], arista[1]) in G.edges():
             nx.draw_networkx_edges(G, pos, edgelist = [(arista[0], arista[1])],
                                    width = 2.0, alpha = 0.6, edge_color = 'orange')
    for nodo in resultado_nodos:
        if nodo in G.nodes():
              nx.draw_networkx_nodes(G, pos, nodelist = [nodo], node_color = '#ff8000')

    return resultado

def probar_bfs_vivienda(ni, nf):
    resultado = ""
    grafo = crear_grafo(centros, aristas, ni, nf)
    G = crear_grafo_nx(grafo)
    pos = dibujarGrafo(G)
    resultado_aristas, resultado_nodos = bfs_vivienda(grafo, ni) # el int que se pasa es el nodo inicial

    # Imprimir el resultado de la busqueda
    resultado += "\n\nCentros poblados con numero de viviendas mayor a 50: \n"
    for i in resultado_nodos:
      resultado += (f"[{i}]{centros[i].nombre_centro}: {centros[i].nro_viviendas} viviendas \n")


    # Dibujar el BFS
    for arista in resultado_aristas:
         if (arista[0], arista[1]) in G.edges():
             nx.draw_networkx_edges(G, pos, edgelist = [(arista[0], arista[1])],
                                    width = 2.0, alpha = 0.6, edge_color = 'orange')
    for nodo in resultado_nodos:
        if nodo in G.nodes():
              nx.draw_networkx_nodes(G, pos, nodelist = [nodo], node_color = '#ff8000')

    return resultado

def probar_bfs_necesidad(ni, nf):
    resultado = ""
    grafo = crear_grafo(centros, aristas, ni, nf)
    G = crear_grafo_nx(grafo)
    pos = dibujarGrafo(G)
    resultado_aristas, resultado_nodos = bfs_necesidades(grafo, ni) # el int que se pasa es el nodo inicial

    # Imprimir el resultado de la busqueda
    resultado += "\n\nCentros poblados con necesidades estado ALTA(A) o MEDIA(M): \n"
    for i in resultado_nodos:
      resultado += (f"[{i}]{centros[i].nombre_centro}: Alimentos ({centros[i].s_alimentos}), Salud ({centros[i].s_salud}), Servicios Basicos ({centros[i].s_serv_basicos}) y Transporte ({centros[i].s_transporte}) \n")

    # Dibujar el BFS
    for arista in resultado_aristas:
         if (arista[0], arista[1]) in G.edges():
             nx.draw_networkx_edges(G, pos, edgelist = [(arista[0], arista[1])],
                                    width = 2.0, alpha = 0.6, edge_color = 'orange')
    for nodo in resultado_nodos:
        if nodo in G.nodes():
              nx.draw_networkx_nodes(G, pos, nodelist = [nodo], node_color = '#ff8000')

    return resultado

#probar_bfs_habitantes(0, 25)
#probar_bfs_vivienda(0, 25)
#probar_bfs_capital(0, 25)
#probar_bfs_necesidades(0, 25)
#plt.show()

#------------------------------------------------------------------------------------------------------------------------------kruskal

# CONECTA CON NUESTRO SUBGRAFO Y CREA EL GRAFO PONDERADO  -----------------------------

def crear_grafoPonderado(subgrafo):
    G = nx.Graph()
    
    for nodo, vecinos in subgrafo.items():
        for vecino in vecinos:

            nodo1 = nodo
            nodo2 = centros[vecino].id #obtiene el id del segundo nodo
            pesoArista = aristas[nodo1][nodo2] #peso de la arista que conecta los 2 nodos

            G.add_edge(nodo1, nodo2, length = pesoArista) #añade la arista al grapo networkx
    return G

# FUNCIONES DE BUSQUEDA ----------------------------------------

def find(padre, i):
    if padre[i] == i:
        return i #retorna el id de la raiz
        
    return find(padre, padre[i])
    
def union(padre, rank, x, y):
    xRaiz = find(padre, x)
    yRaiz = find(padre, y)
        
    #Coloca la raiz del arbol mas pequeño bajo la raiz del arbol más grande
    if rank[xRaiz] < rank[yRaiz]:
        padre[xRaiz] = yRaiz
    elif rank[xRaiz] > rank[yRaiz]:
        padre[yRaiz] = xRaiz
    else:
        padre[yRaiz] = xRaiz
        rank[yRaiz] += 1

# ESCOGER ARISTA CON PESO MENOR  -------------------

def obtenerMinimo(G, visitados):
    menorPesoArista = 10000 
    
    for arista in [(nodo1, nodo2, pesoArista['length']) for nodo1,
                   nodo2, pesoArista in G.edges( data = True) 
                   if 'length' in pesoArista]:

        if visitados[arista] == False and arista[2] < menorPesoArista:
            menorPesoArista = arista[2]
            menor_arista = arista #ovtiene la arista de menor peso entre todas que no esten visitadas
            
    return menor_arista

# ALGORITMO DE KRUSKAL  ----------------------------

def kruskal(G, pos):
    cantNodos = len(G.nodes()) # cantidad de nodos del grafo
    resultado = [] 
    
    visitados = {} 
    for i in [(nodo1, nodo2, pesoArista['length']) for nodo1, 
              nodo2, pesoArista in G.edges(data = True) 
              if 'length' in pesoArista]:

        visitados[i] = False #inicia todas las aristas como no visitadas

    padre = [] 
    rank = []	
    
    for nodo in range(cantNodos): #inicializa el arreglo de padres y el rank
        padre.append(nodo)
        rank.append(0)
    
    #Mientras el número de aristas a tomar es menor que cantNodos -1
    while len(resultado) < cantNodos - 1 :
        
        #Elegimos la arista de peso menor
        aristaActual = obtenerMinimo(G, visitados) 
        visitados[aristaActual] = True 
        
        #Verificar si la arista no genera un ciclo
        #Si es asi, se incluye en el resultado
        # Sino, se descarta e ignora esa arista
        x = find(padre, aristaActual[0])   #nodo1
        y = find(padre, aristaActual[1])   #nodo2
        
        if x != y: #no genera un ciclo
            resultado.append(aristaActual)
            union(padre, rank, x, y)
            
        
    # pintar las aristas del MST de color rojo
    for arista in resultado:
         if (arista[0], arista[1]) in G.edges():
             nx.draw_networkx_edges(G, pos, edgelist = [(arista[0], arista[1])], 
                                    width = 2.5, alpha = 0.6, edge_color = 'r')
    
    return resultado

# DIBUJAR EL GRAFO PONDERADO  ----------------------------

def DibujarGrafoPonderado(G):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels = True)  # with_labels=true es para mostrar los nodos
    
    edge_labels = nx.get_edge_attributes(G, 'length')
    nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_labels, font_size = 11) 
    
    return pos

# PROBAR EL ALGORITMO KRUSKAL  --------------------------
def probar_kruskal(ni, nf):
    subgrafoInicial = crear_grafo(centros, aristas, ni, nf) #crea el grafo como diccionario
    G = crear_grafoPonderado(subgrafoInicial) #crea el grafo ponderado a partir del diccionario
    pos = DibujarGrafoPonderado(G) #lo dibuja y retorna en la variable para mostrarla
    subgrafoFinal = kruskal(G, pos) #realiza el algoritmo y obtiene el MST  partir del grafo

    resultado = ""
    resultado+="\nSUBGRAFO:"
    resultado+="\n[GRAFO INICIAL]\n"

    for nodo, vecinos in subgrafoInicial.items(): #imprime todas las aristas
        for vecino in vecinos:

            nodo1 = nodo
            nodo2 = centros[vecino].id
            pesoArista = aristas[nodo1][nodo2]

            resultado+=f"\n[{nodo1}]{centros[nodo1].nombre_centro} - [{nodo2}]{centros[nodo2].nombre_centro}: {pesoArista}km"

    # Algoritmo Kruskal
    resultado+="\n\n-------------------------------------------------------------"
    resultado+="\nALGORITMO KRUSKAL:"
    resultado+="\nRuta mas corta que conecta a todos los centros poblacionales"
    resultado+="\n[GRAFO FINAL]\n"

    costoTotal=0

    for arista in subgrafoFinal: #imprime las aristas tomadas en el MST
        nodo1 = arista[0]
        nodo2 = arista[1]
        pesoArista = arista[2]

        resultado+=f"\n[{nodo1}]{centros[nodo1].nombre_centro} - [{nodo2}]{centros[nodo2].nombre_centro}: {pesoArista} km"
        costoTotal+=pesoArista #se obtiene el costo total del MST

    resultado+=f"\n\nCantidad de kilometros de la ruta es {costoTotal}"
    return resultado

#-----------------------------------------------------------------------------------------------------------------------Tkinter Menu Principal
menu_p = tk.Tk()
menu_p.geometry("800x600")
menu_p.resizable(False, False)
menu_p.title("Ayuda Humanitaria - Menu Principal")
menu_p.configure(bg='snow1')

TituloK = tk.Label(menu_p, text="Ayuda\nHumanitaria", bg='dark grey', fg="white", font=("Helvetical Bold", 45))
TituloK.place(x=40, y=40)

subtituloK = tk.Label(menu_p, text="Grupo 6 - Complejidad Algoritmica", bg= "snow", fg="black", font=("Helvetical Bold", 15))
subtituloK.place(x=48, y=200)

integrantesK = tk.Label(menu_p, text = "Integrantes del equipo: \n\n-Miguel Ramirez  \n\n-Lucero Obispo  \n\n-Eric Cuevas  ", bg= "snow", fg="black", font=("Helvetical Bold", 20))
integrantesK.place(x=65, y=280)

#elementos bfs-------------------------------------------------------------------------
texto_bfsK = tk.Label(menu_p, text = "Buscar con el algoritmo BFS \ncentros poblados por categorias:", bg= "snow", fg="black", font=("Helvetical Bold", 14))
texto_bfsK.place(x=450, y=40)

# VENTANA BFS HABITANTES ---------------------------------------------------------------------

def ventana_habitantes():
    
    ventana_habitante = tk.Toplevel() #para ventanas adicionales se usa tk.Toplevel()
    ventana_habitante.geometry("900x700")
    ventana_habitante.title("BFS Habitantes")
    ventana_habitante.configure(bg='snow1')

    # Agregar labels en la ventana
    etiquetaH_titulo = tk.Label(ventana_habitante, text="BFS", bg= "snow", fg="black", font="consolas 30 bold")
    etiquetaH_titulo.grid(row=0, column=2, padx=10, pady=10)

    etiqueta_descripcionH = tk.Label(ventana_habitante, 
    text="Halla los centros poblados que tengan como número de habitantes mayor a 100", fg="black", font="consolas 10 bold", bg='snow1')
    etiqueta_descripcionH.grid(row=1, column=1, columnspan=4)

    etiqueta_niH = tk.Label(ventana_habitante, text="Desde: ", fg="black", font="consolas 18 bold", bg='snow1')
    etiqueta_niH.grid(row=2, column=0)

    etiqueta_nfH = tk.Label(ventana_habitante, text="Hasta: ", fg="black", font="consolas 18 bold", bg='snow1')
    etiqueta_nfH.grid(row=2, column=2)

    # Agregar texto con scrollbar
    text_resultado = tk.Text(ventana_habitante, bg='snow1', height=30, width=75)
    text_resultado.grid(row=3, column=1, columnspan=3)

    # Agregar textboxs para que el usuario ingrese datos
    cajaTexto_niH = tk.Entry(ventana_habitante, bg= "snow", font="consolas 18 bold", width=10)
    cajaTexto_niH.grid(row=2,  column=1, padx=10, pady=5)

    cajaTexto_nfH = tk.Entry(ventana_habitante, bg= "snow", font="consolas 18 bold", width=10)
    cajaTexto_nfH.grid(row=2, column=3, padx=10, pady=5)

    def botonKruskal_action():
        if(botonHabitante['text']=='Ejecutar'):
            niH = int(cajaTexto_niH.get())
            nfH = int(cajaTexto_nfH.get())
            if(niH<nfH):
                resultado = probar_bfs_habitantes(niH, nfH)
                text_resultado.insert(tk.END, resultado)
                plt.show() # muestra el grafico de kruskal
                botonHabitante['text']='Clear'

        else:
            cajaTexto_niH.delete(0, "end")
            cajaTexto_nfH.delete(0, "end")
            text_resultado.delete("1.0","end")
            botonHabitante['text']='Ejecutar'

    botonHabitante = tk.Button(ventana_habitante, text="Ejecutar", bg="orange", font="consolas 18 bold", command= botonKruskal_action, width= 10)
    botonHabitante.grid(row=4, column=5,padx=20, pady=10)
    
hacia_bfs_habitantes = tk.Button(menu_p, text="BFS por \n Habitantes", 
bg="light blue", font="Helvetica", width= 16, command= ventana_habitantes) #agregar commands
hacia_bfs_habitantes.place(x=420, y=120)

# VENTANA BFS Capitales ---------------------------------------------------------------------

def ventana_capitales():
    
    ventana_capital = tk.Toplevel() #para ventanas adicionales se usa tk.Toplevel()
    ventana_capital.geometry("900x700")
    ventana_capital.title("BFS Capital")
    ventana_capital.configure(bg='snow1')

    # Agregar labels en la ventana
    etiquetaC_titulo = tk.Label(ventana_capital, text="BFS", bg= "snow", fg="black", font="consolas 30 bold")
    etiquetaC_titulo.grid(row=0, column=2, padx=10, pady=10)

    etiqueta_descripcionC = tk.Label(ventana_capital, 
    text="Halla los centros poblados que sean capital del distrito", fg="black", font="consolas 10 bold", bg='snow1')
    etiqueta_descripcionC.grid(row=1, column=1, columnspan=4)

    etiqueta_niC = tk.Label(ventana_capital, text="Desde: ", fg="black", font="consolas 18 bold", bg='snow1')
    etiqueta_niC.grid(row=2, column=0)

    etiqueta_nfC = tk.Label(ventana_capital, text="Hasta: ", fg="black", font="consolas 18 bold", bg='snow1')
    etiqueta_nfC.grid(row=2, column=2)

    # Agregar texto con scrollbar
    text_resultado = tk.Text(ventana_capital, bg='snow1', height=30, width=75)
    text_resultado.grid(row=3, column=1, columnspan=3)

    # Agregar textboxs para que el usuario ingrese datos
    cajaTexto_niC = tk.Entry(ventana_capital, bg= "snow", font="consolas 18 bold", width=10)
    cajaTexto_niC.grid(row=2,  column=1, padx=10, pady=5)

    cajaTexto_nfC = tk.Entry(ventana_capital, bg= "snow", font="consolas 18 bold", width=10)
    cajaTexto_nfC.grid(row=2, column=3, padx=10, pady=5)

    def botonKruskal_action():
        if(botonCapital['text']=='Ejecutar'):
            niC = int(cajaTexto_niC.get())
            nfC = int(cajaTexto_nfC.get())
            if(niC < nfC):
                resultado = probar_bfs_capital(niC, nfC)
                text_resultado.insert(tk.END, resultado)
                plt.show() # muestra el grafico de kruskal
                botonCapital['text']='Clear'

        else:
            cajaTexto_niC.delete(0, "end")
            cajaTexto_nfC.delete(0, "end")
            text_resultado.delete("1.0","end")
            botonCapital['text']='Ejecutar'

    botonCapital = tk.Button(ventana_capital, text="Ejecutar", bg="orange", font="consolas 18 bold", 
    command= botonKruskal_action, width= 10)
    botonCapital.grid(row=4, column=5,padx=20, pady=10)

hacia_bfs_capital = tk.Button(menu_p, text="BFS por \n Capitales ", 
bg="light blue", font="Helvetica", width= 16, command= ventana_capitales)
hacia_bfs_capital.place(x=620, y=120)

# VENTANA BFS Vivienda ---------------------------------------------------------------------

def ventana_vivienda():
    
    ventana_vivienda = tk.Toplevel() #para ventanas adicionales se usa tk.Toplevel()
    ventana_vivienda.geometry("900x700")
    ventana_vivienda.title("BFS Vivienda")
    ventana_vivienda.configure(bg='snow1')

    # Agregar labels en la ventana
    etiquetaC_titulo = tk.Label(ventana_vivienda, text="BFS", bg= "snow", fg="black", font="consolas 30 bold")
    etiquetaC_titulo.grid(row=0, column=2, padx=10, pady=10)

    etiqueta_descripcionC = tk.Label(ventana_vivienda, 
    text="Halla los centros poblados que tengan como número de viviendas mayor a 50", fg="black", font="consolas 10 bold", bg='snow1')
    etiqueta_descripcionC.grid(row=1, column=1, columnspan=4)

    etiqueta_niC = tk.Label(ventana_vivienda, text="Desde: ", fg="black", font="consolas 18 bold", bg='snow1')
    etiqueta_niC.grid(row=2, column=0)

    etiqueta_nfC = tk.Label(ventana_vivienda, text="Hasta: ", fg="black", font="consolas 18 bold", bg='snow1')
    etiqueta_nfC.grid(row=2, column=2)

    # Agregar texto con scrollbar
    text_resultado = tk.Text(ventana_vivienda, bg='snow1', height=30, width=75)
    text_resultado.grid(row=3, column=1, columnspan=3)

    # Agregar textboxs para que el usuario ingrese datos
    cajaTexto_niC = tk.Entry(ventana_vivienda, bg= "snow", font="consolas 18 bold", width=10)
    cajaTexto_niC.grid(row=2,  column=1, padx=10, pady=5)

    cajaTexto_nfC = tk.Entry(ventana_vivienda, bg= "snow", font="consolas 18 bold", width=10)
    cajaTexto_nfC.grid(row=2, column=3, padx=10, pady=5)

    def botonKruskal_action():
        if(botonCapital['text']=='Ejecutar'):
            niC = int(cajaTexto_niC.get())
            nfC = int(cajaTexto_nfC.get())
            if(niC < nfC):
                resultado = probar_bfs_vivienda(niC, nfC)
                text_resultado.insert(tk.END, resultado)
                plt.show() # muestra el grafico de kruskal
                botonCapital['text']='Clear'

        else:
            cajaTexto_niC.delete(0, "end")
            cajaTexto_nfC.delete(0, "end")
            text_resultado.delete("1.0","end")
            botonCapital['text']='Ejecutar'

    botonCapital = tk.Button(ventana_vivienda, text="Ejecutar", bg="orange", font="consolas 18 bold", 
    command= botonKruskal_action, width= 10)
    botonCapital.grid(row=4, column=5,padx=20, pady=10)

hacia_bfs_vivienda = tk.Button(menu_p, text="BFS por \n Viviendas", 
bg="light blue", font="Helvetica", width= 16, command = ventana_vivienda)
hacia_bfs_vivienda.place(x=420, y=200)

# VENTANA BFS Necesidades ---------------------------------------------------------------------

def ventana_necesidad():
    
    ventana_necesidades = tk.Toplevel() #para ventanas adicionales se usa tk.Toplevel()
    ventana_necesidades.geometry("900x700")
    ventana_necesidades.title("BFS Necesidad")
    ventana_necesidades.configure(bg='snow1')

    # Agregar labels en la ventana
    etiquetaC_titulo = tk.Label(ventana_necesidades, text="BFS", bg= "snow", fg="black", font="consolas 30 bold")
    etiquetaC_titulo.grid(row=0, column=2, padx=10, pady=10)

    etiqueta_descripcionC = tk.Label(ventana_necesidades, 
    text="Halla los centros poblados que tengan mayor necesidad Alta(A) o Media(M)", fg="black", font="consolas 10 bold", bg='snow1')
    etiqueta_descripcionC.grid(row=1, column=1, columnspan=4)

    etiqueta_niC = tk.Label(ventana_necesidades, text="Desde: ", fg="black", font="consolas 18 bold", bg='snow1')
    etiqueta_niC.grid(row=2, column=0)

    etiqueta_nfC = tk.Label(ventana_necesidades, text="Hasta: ", fg="black", font="consolas 18 bold", bg='snow1')
    etiqueta_nfC.grid(row=2, column=2)

    # Agregar texto con scrollbar
    text_resultado = tk.Text(ventana_necesidades, bg='snow1', height=30, width=75)
    text_resultado.grid(row=3, column=1, columnspan=3)

    # Agregar textboxs para que el usuario ingrese datos
    cajaTexto_niC = tk.Entry(ventana_necesidades, bg= "snow", font="consolas 18 bold", width=10)
    cajaTexto_niC.grid(row=2,  column=1, padx=10, pady=5)

    cajaTexto_nfC = tk.Entry(ventana_necesidades, bg= "snow", font="consolas 18 bold", width=10)
    cajaTexto_nfC.grid(row=2, column=3, padx=10, pady=5)

    def botonKruskal_action():
        if(botonCapital['text']=='Ejecutar'):
            niC = int(cajaTexto_niC.get())
            nfC = int(cajaTexto_nfC.get())
            if(niC < nfC):
                resultado = probar_bfs_necesidad(niC, nfC)
                text_resultado.insert(tk.END, resultado)
                plt.show() # muestra el grafico de kruskal
                botonCapital['text']='Clear'

        else:
            cajaTexto_niC.delete(0, "end")
            cajaTexto_nfC.delete(0, "end")
            text_resultado.delete("1.0","end")
            botonCapital['text']='Ejecutar'

    botonCapital = tk.Button(ventana_necesidades, text="Ejecutar", bg="orange", font="consolas 18 bold", 
    command= botonKruskal_action, width= 10)
    botonCapital.grid(row=4, column=5,padx=20, pady=10)

hacia_bfs_necesidades = tk.Button(menu_p, text="BFS por \n necesidades", 
bg="light blue", font="Helvetica", width= 16, command = ventana_necesidad)
hacia_bfs_necesidades.place(x=620, y=200)


#Ventana kruskal---------------------------------------------------------------------
texto_kruskalK = tk.Label(menu_p, text = "Usar el Algoritmo Kruskal \npara encontrar las menores aristas \nentre los centros:", bg= "snow", fg="black", font=("Helvetical Bold", 14))
texto_kruskalK.place(x=450, y=350)

def ventana_kruskal():
    ventanaKruskal = tk.Toplevel() #para ventanas adicionales se usa tk.Toplevel()
    ventanaKruskal.geometry("900x700")
    ventanaKruskal.title("Ayuda Humanitaria")
    ventanaKruskal.configure(bg='snow1')

    # Agregar labels en la ventana
    etiquetaK_titulo = tk.Label(ventanaKruskal, text="KRUSKAL", bg= "snow", fg="black", font="consolas 30 bold")
    etiquetaK_titulo.grid(row=0, column=2, padx=10, pady=10)

    etiqueta_descripcionK = tk.Label(ventanaKruskal, text="Hallar la ruta mas corta en km que te permita movilizarte a todos los centros poblados", fg="black", font="consolas 10 bold", bg='snow1')
    etiqueta_descripcionK.grid(row=1, column=1, columnspan=4)

    etiqueta_niK = tk.Label(ventanaKruskal, text="Desde: ", fg="black", font="consolas 18 bold", bg='snow1')
    etiqueta_niK.grid(row=2, column=0)

    etiqueta_nfK = tk.Label(ventanaKruskal, text="Hasta: ", fg="black", font="consolas 18 bold", bg='snow1')
    etiqueta_nfK.grid(row=2, column=2)

    # Agregar texto con scrollbar
    text_resultado = tk.Text(ventanaKruskal, bg='snow1', height=30, width=75)
    text_resultado.grid(row=3, column=1, columnspan=3)

    # Agregar textboxs para que el usuario ingrese datos
    cajaTexto_niK = tk.Entry(ventanaKruskal, bg= "snow", font="consolas 18 bold", width=10)
    cajaTexto_niK.grid(row=2,  column=1, padx=10, pady=5)

    cajaTexto_nfK = tk.Entry(ventanaKruskal, bg= "snow", font="consolas 18 bold", width=10)
    cajaTexto_nfK.grid(row=2, column=3, padx=10, pady=5)

    def botonKruskal_action():
        if(botonKruskal['text']=='Ejecutar'):
            niK = int(cajaTexto_niK.get())
            nfK = int(cajaTexto_nfK.get())
            if(niK<nfK):
                resultado = probar_kruskal(niK, nfK)
                text_resultado.insert(tk.END, resultado)
                plt.show() # muestra el grafico de kruskal
                botonKruskal['text']='Clear'

        else:
            cajaTexto_niK.delete(0, "end")
            cajaTexto_nfK.delete(0, "end")
            text_resultado.delete("1.0","end")
            botonKruskal['text']='Ejecutar'

    botonKruskal = tk.Button(ventanaKruskal, text="Ejecutar", bg="orange", font="consolas 18 bold", command= botonKruskal_action, width= 10)
    botonKruskal.grid(row=4, column=5,padx=20, pady=10)

hacia_kruskal = tk.Button(menu_p, text="Algoritmo\nKruskal", bg="orange", font="Helvetica", width= 20, command=ventana_kruskal)
hacia_kruskal.place(x=500,  y=450)

#ejecutar
menu_p.mainloop()