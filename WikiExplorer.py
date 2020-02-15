import wikipedia
import random as rdm
import networkx as nx
import matplotlib.pyplot as plt

# First, we create a dictionnary that'll store previously visited links
class dico:
    def __init__(self):
        self.dico=[]
    
    #We add a few basic functions
    def len(self):
        return len(self.dico)

    def isin(self,obj):
        n=self.len()
        i=0
        while i<n:
            if self.dico[i]==obj:
                return True
            else:
                i+=1
        return False

    def add(self,obj):
        if not(self.isin(obj)):
            self.dico.append(obj)
    
    def pos(self,obj):
        n=self.len()
        i=0
        while i<n:
            if self.dico[i]==obj:
                return i
            else:
                i+=1
        return False
    
    def ajoutmultiple(self,liste):
        for e in liste:
            self.add(e)
    
    def stock(self,ind):
        return self.dico[ind]
    
    def list(self):
        return self.dico

#Then we create the Graphs objects
class graph:
    def __init__(self,limit,trees):
        self.body=[]
        self.limit=limit
        self.dico = dico()
        self.trees=trees
    
    def next(self,sommet):
        try:
            #This could be a lot faster, but... 
            allinall = wikipedia.page(sommet).links
            rdm.shuffle(allinall)
            successeurs = allinall[0:rdm.randint(1,self.trees)]
            self.dico.ajoutmultiple(successeurs)
            i=self.dico.pos(sommet)
            for e in successeurs:
                print(e)
                j=self.dico.pos(e)
                self.body.append((i,j))
                if self.dico.len()<self.limit:
                    self.next(e)
        #Sometimes, it doesn't work properly, so we fix it by skipping problematic nodes
        except wikipedia.exceptions.PageError:
            print("• Invalid ID")
        except wikipedia.exceptions.DisambiguationError:
            print("• Ambiguous")
        
    
    def explo(self,init):
        self.dico.add(init)
        self.next(init)
    
    def plot(self):
        G=nx.Graph()
        G.add_nodes_from([i for i in range(self.dico.len())])
        G.add_edges_from(self.body)
        mapping = dict(zip(G, self.dico.list()))
        G = nx.relabel_nodes(G, mapping)
        remove = [node for node,degree in dict(G.degree()).items() if degree == 1]  #Remove this if you want to see all the nodes
        G.remove_nodes_from(remove)
        plt.figure(figsize=[self.limit/30,self.limit/30], facecolor='#333333')
        nx.draw_kamada_kawai(G, node_color='skyblue', alpha=0.5, edge_color='blue', with_labels=True, font_size=9)
        plt.savefig("Graph.png", format="PNG",dpi=300)
        print("---------------------")
        print("Done")

#This is the main function : Dora, the explorer
#Dora("Reddit",1000,10) means that it'll store about 1000 links, and that approximatly 10 links we'll be stored each time we stumble upon a page, starting with the page named "Reddit"
def dora(st,limit,trees):
    G=graph(limit,trees)
    G.explo(st)
    G.plot()