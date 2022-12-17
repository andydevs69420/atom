#! comment
#! another comment!

import [stringstd];



fun[void] eat(_food:str) 
{
    print(_food);
    return null;
}

enum xx {
    x = 2 << 3
}

fun[int] main(_args:array[str])
{   
    print(typeof main);

    return 0;
}

native::std
fun[void] print(_object:any);


define fun[int] _obj:int add(_n:int) _obj + _n;
