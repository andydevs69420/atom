#! STANDARD LIBRARY FOR ATOM
#! author: andydevs69420
#! date: December 2 2022

const STDOUTID = 0x00;
const STDERRID = 0x01;
const STDINID  = 0x02;

#! printf function.
#! syntax: printf("Hello {0}, I'm {0}", ["World", "andydevs69420"]);
native::std
fun[void] printf(_string:str, _fmt_args:array[any]);

#! print function
#! syntax: print("Hello World!");
native::std
fun[void] print(_str:any);

#! readline function.
#! syntax: const input = readl("input:>>");
native::std 
fun[str] readl(_message:str);

#! read file content.
#! syntax: const filec = readfile("/abspath/file.*");
#! native::std
#! fun[str] readfile(_file_to_path:str);

#! itoa - convert integer to string.
#! syntax: const tostr = itoa(10000);
#! native::std
#! fun[std] itoa(_int:int);

#! atoi - convert string to int.
#! syntax: const toint = atoi("123");
#! native::std
#! fun[std] itoa(_int:int);


