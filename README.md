# FreeSpeak Natural Language Interpreter
Raw English language interpreted to NASM based on Natural Language Processing techniques.

___
#### Current Features:
* Fully functional frontend
* Python CGI handles all queries
* Sentences are stripped of superfluous words and the important words are classified with labels
* Words are kept in order and stored inside a sentence container so that context can be derived
* Labeled words are sent to the NASM interpret module that simply goes through the words and constructs what the labels say
* NASM interpretter module currently only supports the creation of arrays

___
#### In Development:
* Working on adding better multi-sentence support
* Handling multiple tasks in one sentence
* Better error handling
* Adding support for: 
  * conditional statements
  * loops
  * basic mathematics
  * various specified types

___
   **http://www.freespeak.network**
