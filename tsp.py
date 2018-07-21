

import numpy as np
import itertools
import random
#from sympy import *
#from sympy.combinatorics import Permutation
global generation
generation = 1
population = 500
evolution_times = 200
bestroute=[]
N = 100   #elite_space

dimension = int(input("dimension of the matrix: "))  #input the dimension of the matrix

range_min = int(input("type the minimum value: "))

range_max = int(input("type the maximum value: "))   #define the range

distance_non_sym = (np.random.randint(range_min,range_max,size=(dimension,dimension)))

for i in range(dimension):
    distance_non_sym[i][i] = 0

distance_sym = np.tril(distance_non_sym) + np.tril(distance_non_sym, -1).T     #set the cost bewtween two places identical
print(distance_non_sym,'\n',distance_sym)
print(distance_non_sym[0][1])




cities = set()
for i in range(dimension):
   cities.add(i)

def get_route(city):
   t=[]
   start = first(city)
   for rest in itertools.permutations(city - {start}):
       if len(t)>=population:
           break
       else:
           t = t + [[start]+ tour(rest)]
   return t

def first(collection):
   return next(iter(collection))

tour = list

#route_list here is the first generation
route_list = get_route(cities)

print(route_list)

#calculate the cost of every route


def route_cost(path):
    return sum(cost(path[i], path[i-1])
               for i in range(len(path)))

def cost(a,b):
    return distance_sym[a][b]

def all_cost(routes):
    route_cost_list = []
    for i in range(len(routes)):
        route_cost_list.append(route_cost(routes[i]))
    return route_cost_list



def selection(pop):
    sorted_index = np.argsort(all_cost(pop))
    selected=[]
    for index in sorted_index:
        if len(selected)<N:
            selected.append(pop[index])
        else:
            break
    return selected



#mutation function
def mutation(gene):
    gene_temp = gene[:]
    index1 = random.randint(0,dimension-1)
    index2 = random.randint(0,dimension-1)
    while index2==index1:
        index2 = random.randint(0,dimension-1)
    gene_temp[index1],gene_temp[index2]=gene_temp[index2],gene_temp[index1]
    return gene_temp



#use cycle crossover here

def crossover(gene1,gene2):
    child = gene1[:]
    while child == gene1:
        cycleindices = []
        index_gene1 = random.randint(0,len(gene1)-1)
        cycleindices.append(index_gene1)
        city_gene2 = gene2[index_gene1]
        index_gene1 = gene1.index(city_gene2)
        while index_gene1 != cycleindices[0]:
            cycleindices.append(index_gene1)
            city_gene2 = gene2[index_gene1]
            index_gene1 = gene1.index(city_gene2)
            for index in cycleindices:
                child[index] = gene2[index]

    #while child == gene2:
     #   index_gene11
    return child

#special case
#a = [1,2,3,4]
#b = [3,4,2,1]
#c = crossover(a,b)
#print(a,b,c)


crossover_rate = 0.3
mutation_rate = 0.3

def generate(candidate1):
    candidate = candidate1[:]
    parent1 = random.choice(candidate)

    #if crossover
    if random.random() < crossover_rate:
        parent2 = random.choice(candidate)
        while parent2 == parent1:
            parent2 = random.choice(candidate)
        child = crossover(parent1,parent2)
    else:
        child = parent1

    #if mutation
    if random.random() < mutation_rate:
        child = mutation(child)

    return child

def next_gen():
    new_gen=[]
    bestroutelist = selection(route_list)
    while len(new_gen)<len(route_list):
        t = generate(bestroutelist)
        if (t in new_gen) == False:
            new_gen.append(t)
    return new_gen




count = 0
while count < evolution_times:
    bestroute = selection(route_list)[0]
    print(generation,bestroute,route_cost(bestroute))
    generation += 1
    next_gen()
    route_list=next_gen()
    count += 1


def findbest(dd):
    route_list1 = selection(dd)[0]
    value = route_cost(route_list1)
    return value

print(findbest(get_route(cities)))
