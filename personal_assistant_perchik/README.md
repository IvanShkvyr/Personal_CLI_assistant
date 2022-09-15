Personal assistant  
====================
 *** 
The assistant could:  
* save contacts with names, addresses, phone numbers, email and birthdays to the contact book;  
* display a list of contacts whose birthday is a specified number of days from the current date;  
* check the correctness of the entered phone number and email when creating or editing a record and notify the user in case of incorrect entry;  
* search for contacts from the contact book;  
* edit and delete entries from the contact book;  
* save notes with text information;  
* search for notes;  
* edit and delete notes;  
* add "tags" to notes, keywords describing the topic and subject of the record;  
* search and sort notes by keywords (tags);  
* sort files in the specified folder by category (images, documents, videos, etc.);  
* the bot must analyze the entered text and try to guess what the user wants from it and suggest the closest command to execute.  

 *** 

This is a package to make your folder clear and structured. 
Worked under Python 3.10  

You just need to install this package with command:  
```
pip install -i https://test.pypi.org/simple/ personal-assistant-perchik==1.0.2  
```
or from folder with setup.py file:  
```
python install .  
```
 *** 

To start the program, you must perform one of the following actions:  
* to call the file sorter in a folder, call the command line in the corresponding folder and run the command:  
```
clean-folder  
```
* to call the personal assistant, call the command line and run the command:  
```
personal-assistant  
```