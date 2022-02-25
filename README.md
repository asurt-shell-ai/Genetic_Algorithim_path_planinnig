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

# Dependencies
```
pip3 install numpy
pip3 install matplotlib
pip3 install sklearn
```
# ScreenShot 
