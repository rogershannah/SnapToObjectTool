# SnapToSurfaceTool

![image](https://user-images.githubusercontent.com/43558247/166723846-5958a5f0-7d41-4ff2-8ac2-df19fa51051d.png)


Snap to surface tool allows the user to select objects and align them to the center of a selected plane in either the X, Y, or Z direction. Optionally, the user can rotate the objects in the direction of the plane.


## Installation and Use
1. Download the files in zip folder

 ![image](https://user-images.githubusercontent.com/43558247/167177306-5ab39e56-b74f-4053-b145-b50ae849affc.png)
 
2. Extract the miles and move them drag into the scripts Maya folder (ex. `...\maya\2022\scripts`)
3. Open "execute_tool.py" in the Maya script editor and run the script ![image](https://user-images.githubusercontent.com/43558247/167178537-72ccf865-25b9-426c-bdac-55db39bf828f.png)
  a. ctrl + Enter to run
4. Select a plane to set the snap destination
5. Select objects to move
6. Optionally: 
  a. Sort the objects based on their X, Y, or Z value
  b. convert the curve to a plane
  c. adjust the plane's size (default is 1, minimum is .001)
  d. add a plane depth to convert the plane to a poly object
