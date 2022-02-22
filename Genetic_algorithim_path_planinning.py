import random as ran
import tempfile as TP
from math import *
import numpy as np
import matplotlib.pyplot as mp

generation_home_land=TP.NamedTemporaryFile(delete=False)
generation_house=generation_home_land.name+".npz"

smallest_gene_land=TP.NamedTemporaryFile(delete=False)
smallest_gene_house=smallest_gene_land.name+".npz"

no_of_child=0
generation=0

def distance_measuring(genome,no_of_points):
    '''
    measuring total eculadian distance for each genom

    Argument
    -----------
    genome: dictionary with string key and 2d array
    no_of_points: now of goals in the map

    Return
    -----------
    distance list contain total eculdian distance for each genome
    '''
    i=0
    j=1
    total_distance=[]
    key=list(dict(genome))
    while(i<len(key)):
        sum_of_distance=0
        while(j<no_of_points-1):
            x1=float(genome[key[i]][j][0])
            x2=float(genome[key[i]][j+1][0])
            y1=float(genome[key[i]][j][1])
            y2=float(genome[key[i]][j+1][1])
            sum_of_distance+=sqrt(pow((x1-x2),2)+(pow((y1-y2),2)))
            j+=1
        j=0
        total_distance.append(sum_of_distance)
        i+=1
    i=0
    return total_distance

def shuffle_2D_matrix(matrix, axis = 0):
    """
    Shuffle 2D matrix by column or row.
    
    Arguments:
    matrix: 2D matrix to be shuffled
    seed  : seed of numpy.random
    axis  : zero - by column, non-zero - by row
    
    Returns:
    shuffled_matrix: shuffled matrix
    """
    np.random.seed()
    
    if axis == 0: # by column
        m = matrix.shape[1]
        permutation = list(np.random.permutation(m))
        shuffled_matrix = matrix[:, permutation]
    else:          # by row
        m = matrix.shape[0]
        permutation = list(np.random.permutation(m))
        shuffled_matrix = matrix[permutation, :]

    return shuffled_matrix

def first_creation(waypoints,no_of_parents):
    """
    create the first n chromosome to begin 
    the algorithim 
    
    Arguments:
        way points: 2D matrix of points to make the chromosome
        no of parents : how many chromosome you want to produce
    
    Returns:
        none
    save the dictionary into temporary file 
    """
    i=0
    dict={}
    dict.update({"genom_"+str(i):waypoints})
    i+=1
    waypoints=np.delete(waypoints,0,axis=0)
    while(i<no_of_parents):
        parent_n=shuffle_2D_matrix(waypoints,1)
        parent_n=np.append(parent_n,np.array([[0,0]]),axis=0)
        parent_n=np.flip(parent_n)
        parent_n=np.fliplr(parent_n)
        dict['genom_'+str(i)]=parent_n
        i+=1
    np.savez(generation_house,**dict)
    
def cross_over(genoms,row):
    """
        crossing over two genoms and produce new genoms
    Arguments:
        generation_genoms: presverve generation geneoms 
        row: no of cordinate that genom had 
    Returns:
        none
    save modified gene
    """
    #defination of dictionary where genoms will be preserved
    parent_genes=dict(genoms) #where original genom preserved
    name_of_parents=list(parent_genes.keys()) #preserve name of parents key
    hospital={} #where produced children is preserved until it will be given to parents
    to_parents={} #where all children is given to parent
    male=0 
    female=0
    global no_of_child

    #crossover part
    while(male<len(name_of_parents)):#a loop that make single gene crossed with all other gene
        female=male+1
        while(female<len(name_of_parents)):#other gene
            #print(name_of_parents[male]+" married to "+name_of_parents[female])
            endpoint=ran.randint(1,(row-5))
            child=parent_genes[name_of_parents[female]][0:int(row/2)]
            row_child,col_child=np.shape(child)
            parent=parent_genes[name_of_parents[male]]
            parent_counter=0 #loop through parent loop that carry the parent genes to prevent same goal
            duplicate_counter=0 #count duplicate points
            while(parent_counter<row):
                child_gene_counter=0 #loop through child loop that have the gene
                child=np.resize(child,(row_child,2))

                #comparison for repeated element
                while(child_gene_counter<row_child):
                    if(bool(np.all(parent[parent_counter]==child[child_gene_counter]))): #there are same goal on booth so dont transfer
                        duplicate_counter=1
                        break  #if it find duplictae imdiatly exit the loop
                    child_gene_counter+=1

                if(duplicate_counter==0):
                    fianl_birth=np.append(child,parent[parent_counter])
                    child=fianl_birth
                    row_child+=1
                    if(row_child==(row)):
                        hospital.update({("child_"+str(no_of_child)):np.resize(fianl_birth,(row,2))})
                        no_of_child+=1
                        break
                duplicate_counter=0 #reset counter of duplicate element
                parent_counter+=1
            female+=1
        male+=1

    to_parents.update(genoms)
    to_parents.update(hospital)
    np.savez(generation_house,**to_parents)
    
def mutation(genoms,row):
    """
    mutation function that change the order of points in same genome and save in temporary file
    Arguments:
        genome: contain generation geneoms 
        no_of_points : number of goals
    Returns:
        none
    """
    i=0  #no of itration for each geneom
    j=0
    genes=dict(genoms)#tansform each generation into dictionary 
    genoms_key=list(genes.keys())#list that preserve the name of each genom
    while(i<len(genoms_key)):

        #the following list generating random list for mutation DNA selection
        mutated_gene_no=ran.randint(1,row-1)#determine the degree of mutation in the genes
        row1_list=ran.sample(range(1,row),mutated_gene_no)
        row2_list=ran.sample(range(1,row),mutated_gene_no)
        #end of generating 

        #print("mutation_no: "+str(mutated_gene_no))

        while(j<mutated_gene_no-1):
            genes[genoms_key[i]][[row1_list[j],row2_list[j+1]]]=genes[genoms_key[i]][[row2_list[j+1],row1_list[j]]]
            j+=1
        j=0
        i+=1
    i=0
    np.savez(generation_house,**genes)

def fitness(genome,distance_list,biggest_acceptable_distance):
    """
    fitness function that test which geneome has the shortest distance
    and get its index to enter it in fuction to be deleted
    
    Arguments:
        genome: presverve generation geneoms 
        no_of_points : number of goals cordinate in the map
        biggest_acceptable_distance=if the geneome distance is bigger than will be eleminated
    Returns:
        list contain key no .of eleminated genes
    """
    i=0
    j=1
    y=0
    total_distance=[]
    total_distance=distance_list
    genome_to_be_deleted=[]
    key=list(dict(genome))

    while(y<len(total_distance)):
        if(total_distance[y] > float(biggest_acceptable_distance)):
            genome_to_be_deleted.append(y)
        y+=1
    y=0
    return genome_to_be_deleted

def elemination(generation_genoms,key_name):
    """
        elemintaed the genes that that exceed maximum acceptable distance
    Arguments:
        generation_genoms: presverve generation geneoms 
        key_name: list contain genes name that will be  deleted
        biggest_acceptable_distance=if the geneome distance is bigger than will be eleminated
    Returns:
        none
    save modified gene
    """
    test={}
    test=dict(generation_genoms)
    key_g=list(test.keys())
    key_no=key_name
    i=0
    while (i<len(key_name)):
        del test[key_g[key_no[i]]] 
        i+=1
    np.savez(generation_house,**test)

def best_of_best_saver(genome,distance_list):
    """
        measuring total distance for each gene in final generation and select the best genoms
    Arguments:
        genoms: presverve generation geneoms 
        no of points: no of goals cordintae
    Returns:
        none
    """
    i=0
    j=1
    key=list(dict(genome))
    total_distance=[]
    total_distance.append(distance_list)
    minimum=min(total_distance) #search for the minimum distance in list
    index_minimum=total_distance.index(minimum) # determine where the gene name taht has the smallest total distance
    smallest_distance_gene={"smallest_one":genome[key[index_minimum]]}
    np.savez(smallest_gene_house,**smallest_distance_gene)

waypoint =  np.array([           [0.,0.],
                        [ 114.28714842,   41.98759603],
                        [  62.47783741,  -10.16037304],
                        [  24.5058101 ,  179.34217451],
                        [  -9.51912637,   86.66461683],
                        [-107.49794568,   23.53735607],
                        [  91.98201947,  153.39087436],
                        [ 130.74459844,   95.76204485],
                        [ 100.11681872,   -9.67705624],
                        [ -97.97803427, -116.85725875],
                        [  12.76266999,  200.86528354],
                        [  35.42322761,  -86.24626489],
                        [ -15.17293957,  -39.18455774],
                        [  50.71204359,  -43.96724648],
                        [-165.73686143,  -40.45509785],
                        [ -59.11389879,  -75.68251789],
                        [ -65.86307249,  -51.20886232],
                        [-118.65056562,   58.30787596],
                        [   0.25090536,   49.73685338],
                        [  95.02087717,   63.66352072]])

row,col=waypoint.shape

first_creation(waypoint,8) #begin of generating the parents
generation_gnenome=np.load(generation_house,allow_pickle=False)

'''
start of the genetic algorithm
'''
no_of_generation=1 #count no of generation
every_genereation_check=1 #pass n generation then check there fitnes

now_best=0

best_of_best=500000000

wait_to_exit=0 #how many times should the best distance be repeated  to exit the main loop

exit_threshold=1000#limit of repeated best distance 

while(1):
    cross_over(generation_gnenome,row)
    generation_gnenome=np.load(generation_house,allow_pickle=False)
    mutation(generation_gnenome,row)
    generation_gnenome=np.load(generation_house,allow_pickle=False)
    distance=distance_measuring(generation_gnenome,row)
    now_best=min(distance)

    if(now_best==best_of_best or best_of_best<now_best):
        #print("condition happened")
        wait_to_exit+=1

    elif(now_best < best_of_best ):
        best_of_best=now_best
        best_of_best_saver(generation_gnenome,row)
        best_best_genes=np.load(smallest_gene_house,allow_pickle=False)

    if(no_of_generation%every_genereation_check==0):
        child_to_be_eliminated=fitness(generation_gnenome,distance,biggest_acceptable_distance=(now_best*1.15))# the child that will be eleminated it if it bigger than acceptable distance
        elemination(generation_gnenome,child_to_be_eliminated)
        generation_gnenome=np.load(generation_house,allow_pickle=False)

    if(len(generation_gnenome)==1):
        first_creation(best_best_genes["smallest_one"],8) #begin of generating the parents at case of eleminating all children
        generation_gnenome=np.load(generation_house,allow_pickle=False)

    print("generation "+str(no_of_generation)+ " | precentage to reach to the best = "+str((1180/best_of_best)*100)+str("%"))

    if(wait_to_exit==exit_threshold):
        break
    
    no_of_generation+=1
    
beeest_dict=dict(best_best_genes)
print("\nbest \n",str(dict(best_best_genes)))
mp.plot(beeest_dict["smallest_one"][:,0],beeest_dict["smallest_one"][:,1])
mp.scatter(waypoint[:,0],waypoint[:,1])
mp.show()
