#Import os Library
import os

# Create Directory
os.mkdir("c:/test/w3school")

# Create Directory
os.makedirs("c:/test/w3school")

#print all entries in current directory
print (os.listdir())

#Print current working directory
print("Current directory:" , os.getcwd())

#Create a new directory
os.mkdir("mydir")

#Change current working directory
os.chdir("mydir")

#Print current working directory
print("Current directory now:" , os.getcwd())


#create a new directory
os.mkdir("mydir")

#change the currently running directory
os.chdir("mydir")

#Print the updated directory path
print ("Updated directory:" , os.getcwd())