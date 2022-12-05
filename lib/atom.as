#! comment
#! another comment!

import [std, ooplike];

wrap _array:array[str] push(_element:str) _array + _element ;

fun[int] main(_args:array[str])
{   
    let x = 100;
        x = 900;

    print(x);
    print(_args);

    const v = 2;

    print(v);

    v =  100;
    print(v);

    [1,2,3][2] = "asdasd";

    return 0;
}



