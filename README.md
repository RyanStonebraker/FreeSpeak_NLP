# FreeSpeak Natural Language Interpreter
Raw English language that is interpreted to NASM Assembly using Python CGI with minimal external library usage and with intelligent task handling that has the ability the find whether an unknown word is a synonym for a known element.

___
#### Current Features:
* Fully functional frontend
* Python CGI handles all queries
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
* More sophisticated print function
* Inner-array accessor functions 
* Stand alone (non-array) values
* Ability to perform non pre-optimized mathematical operations that are shown in NASM.
* More external view controls (Make font bigger, show output, Copy everything to clipboard, etc.)
* Adding support for:
  * conditional statements
  * loops
  * A(n) [OBJECT] is ... style function declarations

___
   **http://www.freespeak.network**
