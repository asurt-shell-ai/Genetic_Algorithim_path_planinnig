# Genetic Algorithim path planinnig
Developing the genetic algorthim to solve a "Travel salesman problem" </br> 
# Mechanism of working
it intially produce a shuffled matrices from given numpy 2d array of waypoint cordinates </br>
the function used :
```
first_creation(waypoints,no_of_parents)
#waypoint : is the N X 2 numpy 2d matrix
#no_of_parents : is the number of intial chromsome for reproduction 
#save the produced parent into temporary file
```
second step is crossover prouduce children = (1.5 x no of given parents) depend O2X crossover technique
```
cross_over(genoms,row)
#genome : dictionary that contain chromosome of child or parent with value N X 2 numpy 2d araay 
#row : number of goals cordinates
#save the produced parent into temporary file
```
mutation phase which happen after crossover that make mutation to random goals cordinate 
```
mutation(genoms,row)
#genome : dictionary that contain chromosome of child or parent with value N X 2 numpy 2d araay 
#row : number of goals cordinates
#save the produced parent/children into temporary file
```
last phase is classifictaion phase which eliminate the biggest distance children and select only the smallest children in generation
```
fitness(genome,distance_list,no_of_best_children)
# genome : dictionary that contain chromosome of child or parent with value N X 2 numpy 2d araay  
# distance_list : take the list of distance for each chromosome
# no_of_best_children : how many children you want to select to continue generation
# Non-return function 
```
and another function is distance measuring that measure distance for each generation 
```
distance_measuring(genome):
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
 ```
# Dependencies
```
pip3 install numpy
pip3 install matplotlib
pip3 install sklearn
```
# ScreenShot 
![download](https://user-images.githubusercontent.com/81301684/155792995-11cdd46f-906f-45e1-aaaa-9b48bf284dd4.png)

![download (1)](https://user-images.githubusercontent.com/81301684/155795104-a71b5550-8c4f-40c3-9646-9ce539cacda7.png)
