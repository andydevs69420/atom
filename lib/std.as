#! STANDARD LIBRARY FOR ATOM
#! author: andydevs69420
#! date: December 2 2022

const STDOUTID = 0x00;
const STDERRID = 0x01;
const STDINID  = 0x02;

#! printf function.
#! syntax: printf("Hello {0}, I'm {0}", ["World", "andydevs69420"]);
native::std
function printf(_string:str, _fmt_args:array[any]) -> void;

#! print function
#! syntax: print("Hello World!");
native::std
function print(_str:any) -> void;

#! readline function.
#! syntax: const input = readl("input:>>");
native::std 
function readl(_message:str) -> str;

#! var x = test_import("asdasd");

