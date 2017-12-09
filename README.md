# FreeSpeak Natural Language Interpreter
Minimally structured English language that is interpreted to x86 syntax assembly. Code refactored to a Python Flask application and live version hosted on nginx using uwsgi.
___

### Change Log:
####    12/8
* Fixed string escaping problems
* Added singular variable declarations
* Added ability to modify variables
* Added repeat functionality to emulate looping
* Fixed box subroutine so that it works with non-string types
* Added copy to clipboard button
* Added "Show Internal Interpretation" button to show debugging info

####    11/29
* HTTPS certificate signed by LetsEncrypt
* Firewalls configured on Live Server
* Secure html escaped strings sent to freespeak engine
* Jinja templating engine used for dynamic page generation instead of Python constantly returning raw HTML
* Default POST requests instead of GET with plain text query strings
* Application served with uwsgi
* Switched from Apache to Nginx web server
* Ported to Python Flask micro-framework from raw Python CGI

#### Current Features:
* Fully functional frontend
* ~~Python CGI handles all queries~~
* ###### Refactored Flask Application
* Optimized addition, subtraction, multiplication and division that can evaluate before being sent to the NASM interpreter
* Dynamically sized arrays
* Type can either be directly specified, or if it is left off, the highest precedented type is assumed for all items in an array.
* Support for integers, floats, strings and booleans.
* Box structure that stores all parameters in an asterisk box
* Print feature that (currently only) prints the first element of a string array
* Random access selector that can be combined with the print feature to print the 0th - nth specified structure (also understands the term "this")
* Supports multiple sentences and multiple tasks in a single sentence.
* Automatically allocates space for array using either malloc or a fixed section .data label depending on item type.
* Maintains a list of all open registers it can use for arrays and pushes and pops all in use registers before and after function call.
* Super advanced error handling (if something breaks it won't tell you and doesn't print the output box below the text field)

___
#### In Development:
* Better context error handling
* More sophisticated print function
* Inner-array accessor functions
* Stand alone (non-array) values
* Ability to perform non pre-optimized mathematical operations that are shown in outputted assembly.
* Adding support for:
  * conditional statements
  * A(n) [OBJECT] is ... style function declarations

#### Reach/Future Goals:
* Speech to text
* Complete code refactoring to utilize a supervised machine learning algorithm, possibly with TensorFlow
* Ability to pass the so-called Turing test for esoteric languages

#### Example Usages:
* ***"Build a box with the text "This is a box.". Then, print this box."***

* ***"Construct an array with the values "cat", "dog", 3.10 * 0.55 + 0.3, 5, 1 through 5 incrementing by 1."***

* ***"Create a matrix of booleans with 1.2, True, False, 0, 1, and 2 - 5."***

* ***"Make an array of values with "cat", "dog", "monkey", 123, 1.23, True, then create another array of strings with the values "cat", "big dog", 1 through 3 incrementing by 0.5. Finally, construct another array of values "test", "testing test test", and 1.2345. Print the 2nd array."***

* ***"Make a box with "test1". Then make a box with "test2". Lastly, make a box with "test3". Print the 2nd box, print the 1st box, and then print the 3rd box."***

* ***"Make a box with "test" and print this. repeat this 3 times."***

* ***"Store 3 in a variable called apples. Store apples in a variable named oranges.Add 1 to oranges and then make a box with oranges and then print this. Repeat this 6 more times. Make a box with apples and print this."***

#### Installation:
##### Python Flask Implementation:
make sure you have python3 and install the following dependencies using pip:
```
pip3 install flask numpy
```
Now clone the repository and navigate to *FreeSpeak_NLP/freespeak* in a terminal window. From this directory, type the following commands to configure the Flask App:
```
export FLASK_APP=run.py
```
Finally, just type:
```
flask run
```
and the flask application should start running on localhost port 5000.

##### Python CGI Implementation (deprecated):
Configure a simple apache server on the OS of your choice, clone this repo and make the "docs" folder your DocumentRoot, cd into the "backend" folder and run the (linux) commands or their equivalent:
```
chmod g+rw wordcache
chmod g+rw wordcache/*
chgrp www-data wordcache
chgrp www-data wordcache/*
```
Next, get the apache server to accept Python CGI by including the following in the same config file that DocumentRoot was changed in:
```
<Directory "/var/www/html/FreeSpeak_NLP/cgi-bin">
        Options ExecCGI
        SetHandler cgi-script
</Directory>

<Directory "/var/www/html">
        Options +ExecCGI
        AddHandler cgi-script .py
</Directory>
```
Then simply start the apache server and go to localhost:8080 or whichever port was configured in the main/virtualhost config file.

___
   **https://www.freespeak.network (http://45.55.89.112/)**
