#! comment
#! another comment!

import [std, ooplike];

wrap _array:array[str] push(_element:str) _array + _element ;



fun[int] main(_args:array[str])
{   
    let x = 200;

    x = 200000;

    print(x);
    print(_args);

    let v = 2;

    print(v);

    v = 10;
    print(v);

    x[2] = 2;

    return 0;
}



