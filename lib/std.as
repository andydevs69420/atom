#! STANDARD LIBRARY FOR ATOM
#! author: andydevs69420
#! date: December 2 2022

const STDOUTID = 0x00;
const STDERRID = 0x01;
const STDINID  = 0x02;

#! printf function.
#! usage: printf("Hello {}, I'm {}", ["World", "andydevs69420"]);
native::std
function printf(_string:str, _fmt_args:array[any]) -> void;

#! print function
#! usage: print("Hello World!");
native::std
function print(_str:any) -> void;

#! scan function.
#! usage: const input = scan("input:>>");
native::std 
function scan(_message:str) -> str;

#! readFile function.
#! usage: const content = readFile("path/to/file.extension");
native::std 
function readFile(_path:str) -> str;

#! writeFile function.
#! usage: const content = writeFile("path/to/file.extension", "somedata to write", false);
native::std 
function writeFile(_path:str, _data:str, _append:bool) -> void;

