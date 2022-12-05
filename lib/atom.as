#! comment
#! another comment!

import [std, ooplike];


wrap _array:array[str] push(_element:str) _array + _element ;

fun[int] add(_a:int, _b:int) 
{
    return _a + _b;
}

fun[int] main(_args:array[str])
{   
    const y = {};
    print(y);
    print(add(1, 3));
    print(  _args  );
    return 0x0;
}


