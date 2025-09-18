# Opening_Files_Python
A simple Python script to open files from a local folder.

Inputs:
        
   ruta: path to the folder where the files are stored.  
         if the files are stored in the same folder as the  
         program use ''.
              
   patrón: allows you to differentiate files you have in the same  
           directory. For example 'p*.*' would extract the files  
           that start with p. By default this variable is set to  
           '*.*' which means extract all files.
            
 Outputs: 
        
   archivo_ext: It is a dictionary with all the files that match  
                the requested pattern. The names inside the  
                dictionary are the same names as the files  
                including the file type.  
                For example, a file named prueba that is txt would  
                be saved as prueba.txt

