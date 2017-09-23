def import_xl(file_path):
    df = pd.read_excel(file_path,header = None)
    df = df.values
    return df

def export_xl(file_path,sheets):
    writer = pd.ExcelWriter(file_path)
    for sheet,name in sheets.items():
        df = pd.DataFrame(name)
        df.to_excel(writer,sheet)
    writer.save()

#Henter ut en kolonne
def column(matrix, i):
    return [row[i] for row in matrix]

#Henter ut en rad
def row(matrix, i):
    return [column[i] for column in matrix]

#Selection sort O(n2)        
def selection_sort(array):
    n = len(array)
    for i in range(0,n):
        smallest = i
        for j in range(i,n):
            if array[j]<array[smallest]:
                smallest = j
        copy = array[i]
        array[i] = array[smallest]
        array[smallest] = copy
    return array

#Leser om to lister inneholder minst ett felles tall
def common_node(array_1,array_2):
    x = selection_sort(array_1)
    y = selection_sort(array_2)
    i = 0
    j = 0
    share = 0
    stop = max([len(x),len(y)])-1
    while min([i,j])< stop:
        if x[i]>y[j]:
            j+=1
        elif x[i]<y[j]:
            i+=1
        else:
            share = 1
            j = 10**6
            i = 10**6
    return share

def common_node_count(array_1,array_2):
    x = selection_sort(array_1)
    y = selection_sort(array_2)
    i = 0
    j = 0
    share = 0
    while i < len(x) and j < len(y):
        if x[i]>y[j]:
            j+=1
        elif x[i]<y[j]:
            i+=1
        else:
            share += 1
            j +=1
            i +=1
    return share

#KORTERSTE RUTE FUNKSJONER

#Lager en graf fra lenke-liste
def make_graph(array):
    #nodes = common_node_count(column(array,0),column(array,1))
    nodes = 35
    matrix = np.full((nodes,nodes),10**6) #Lager matrise med store tall som byttes
    for i in range(0,len(array)): #Hovedloop
        #Trekker fra en for sammenlignbarhet med python-arrays
        matrix[array[i][1]-1][array[i][0]-1] = array[i][2]
        matrix[array[i][0]-1][array[i][1]-1] = array[i][2]
    np.fill_diagonal(matrix, 0)
    return matrix

#Lager lengdematrise n x n
def floyd_warshall(array):
    matrix = make_graph(array)
    #nodes = common_node_count(column(array,0),column(array,1))
    nodes = 35
    pred = np.full((nodes,nodes),-1)

    for i in range(0,nodes):
        for j in range(0,nodes):
            if i != j:
                pred[i][j] = i
    
    for k in range(0,nodes):
        for i in range(0,nodes):
            for j in range(0,nodes):
                if matrix[i][j] > matrix[i][k] +  matrix[k][j]:
                    matrix[i][j] = matrix[i][k] +  matrix[k][j]
                    pred[i][j] = pred[k][j]
    return matrix,pred

#Laster inn data fra en csv fil til et nettverksarray
def get_network(net_csv):
    graf = open(net_csv,'r')
    lenker=0
    for line in graf:
        lenker+=1
    graf_edit = np.full((lenker, 3),0)
    graf = open(net_csv,'r')
    k = 0
    for line in graf:
        stuff = line.split(";")
        graf_edit[k][0] = float(stuff[0])
        graf_edit[k][1] = float(stuff[1])
        temp = stuff[2].split('\n')[0]
        graf_edit[k][2] = float(temp)
        k+=1
    return graf_edit

#Lager en path-vektor
def path(p,i,j,path_vec):
    if i == j:
        path_vec.append(i) 
    else:
        path(p, i, p[i][j],path_vec)
        path_vec.append(j)
        
#Henter en spesifikk path
def get_path(p,i,j):
    #j = j + 1
    path_vec=[]
    path(p,i,j,path_vec)
    #for i in range(1,len(path_vec)):
    #    path_vec[i] = path_vec[i] - 1
    return path_vec

#Lager adjecency-matrise (ikke ferdig)
def build_adj(pred):
    
    adj_mat = np.zeros((len(pred),len(pred)))
    array_a = []
    array_b = []
    for i in range(1,len(pred)):
        for j in range(1,len(pred)):
            array_a = get_path(pred,i,j)
            print array_a
            array_b = get_path(pred,2,10)
            print array_b
            try:
                adj_mat[1][j] = common_node(array_a,array_b)
            except:
                adj_mat[1][j] = 0
                
            print adj_mat[1][j]
            
    return adj_mat


#Nettverkslaster
#Argumenter: (1) Forgjenger-matrise (2) antall noder (3) nettverksfil (4) od-matrise
def network_loader(graf,net,od,pred):

    #Antall noder
    n = len(od)-1

    #Redigering
    for k in range(0,len(net)):
        net[k][3]=0 #Nulllstiller antall reiser
        net[k][2]=graf[k][2] #Legger inn oppdaterteavstander fra grafen        

    #Legger ut reiser paa nettet
    for i in range(0,n):
        for j in range(0,n):
            path = get_path(pred,i,j)
            len_path=get_len_path(path)
            for h in range(0,len_path):
                for k in range(0,len(net)):
                    if net[k][0] == path[h]+1 and net[k][1] == path[1+h]+1:
                        net[k][3] += int(od[i][j])
                    elif net[k][1] == path[h]+1 and net[k][0] == path[1+h]+1:
                        net[k][3] += int(od[i][j])
    return net

#a=get_path(pred,5,12)

#GRAVITASJONSFUNKSJONER
def deter_mat_make(length_mat):
    
    deter_mat = np.zeros((len(length_mat),len(length_mat)))
    for i in range(0,len(length_mat)):
        for j in range(0,len(length_mat)):
            deter_mat[i][j] = deter(length_mat[i][j])
    return deter_mat
    
def deter(length):
    return 2.71**(beta*length)

def sumproduct(list1,list2):
    
    sums = 0
    for i in range(0,len(list1)):
        sums += list1[i]*list2[i]
    return sums
        
def gravity(origin, destination, length_mat):
    
    #Initialization
    deter_mat = deter_mat_make(length_mat) #Lager matrise med forvitring
    dimension = len(origin) #Henter ut matrisedimensjonene
    alpha = [1]*(dimension) #Intitierer alpha-vektor
    beta = [1]*(dimension)  #Intitierer beta-vektor
    largest = 10**6         #Intitierer storste avvik
    alpha_last = alpha      #Intitierer alpha -1
    beta_last = beta        #Intitierer beta -1
    k = 0                   #Intitierer tellevariabler for iterasjoner
    iterasjoner = []
    
    #Hovedlokke
    while largest > .00001:
        
        #Oppdaterer faktorene
       for p in range(0,dimension):
          alpha[p] = origin[p]/(sumproduct(beta_last,column(deter_mat,p)))
          beta[p] = destination[p]/(sumproduct(alpha,row(deter_mat,p)))
          largest = 0
          
        #Looper for aa finne storste element
       for j in range(0,dimension):
           current = alpha[j]*sumproduct(beta,column(deter_mat,j))-origin[j]
           if current>largest:
               largest = current
               
        #Setter forrige beta
       beta_last = beta
       iterasjoner.append(largest)
       #Legger til en iterasjon
       k+=1
       print "Konvergens, Gravitasjonsmodell", largest
       if k == maxiter:
           largest = 0
       
    return alpha,beta,k,iterasjoner

def create_od(origin,destination, length_mat):
    
    alpha,beta,k,iterasjoner = gravity(origin, destination, length_mat)
    deter_mat = deter_mat_make(length_mat)
    od = np.zeros((len(origin),len(origin)))
    
    for i in range(0,len(origin)):
        for j in range(0,len(origin)):
            od[i][j] = alpha[i]*beta[j]*deter_mat[i][j]
    return od,alpha,beta,k,iterasjoner

def calc_pt_matrix(od,length_mat):
    out_od = np.zeros((len(od),len(od)))
    for i in range(0,len(od)):
        for j in range(0,len(od)):
            out_od[i][j] = int(out_od[i][j])*length_mat[i][j]
    return out_od

def get_min(net):
    smallest = 10**6
    smallest_id = 10**6
    for i in range(0,len(net)):
        if net[i][3]/net[i][2]<smallest and net[i][5]==0:
            smallest = net[i][3]/net[i][2]
            smallest_id = i
    return smallest_id,smallest
 

def change_graph(graph,net):
    graph_out = graph
    for i in range(0,len(net)):
        if net[i][5]==1:
            graph_out[i][2]=k_just*graph_out[i][2]
    return graph_out

def production(net):
    sumcost = 0
    for i in range(0,len(net)):
        if net[i][5]!=1:
            sumcost += (net[i][3]/capacity)*net[i][2]
    return sumcost

def sum_pass(net):
    sumpass = 0
    for i in range(0,len(net)):
        sumpass+=net[i][3]
    return sumpass

def get_len_path(path):
    len_path = 0
    if len(path) < 3:
        len_path = 0
    elif len(path) == 3:
        len_path = 2
    else:
        len_path=int(len(path)/2)+int(len(path)%2)+1
    return len_path

def obj(od,length_mat,net,prodgoal):
    return (production(net)*kmk*dogn-prodgoal)**2*(k_just-1)*capacity/.9+time_cost(od,length_mat)
    
def time_cost(od,length_mat):
    cost = 0
    for i in range(0,len(od)-1):
        for j in range(0,len(od)-1):
            cost += od[i][j]*length_mat[i][j]
    return cost

def get_zero_net(net):
    zero_net = np.zeros((len(net),6))
    for i in range(0,len(net)):
        zero_net[i][2] = net[i][2]
        zero_net[i][3] = net[i][3]
        zero_net[i][5] = net[i][5]
    return zero_net

def update_zero_net(net,zero_net):
    for i in range(0,len(net)):
        zero_net[i][5] = net[i][5]
    return zero_net
