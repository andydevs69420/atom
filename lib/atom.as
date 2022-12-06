#! comment
#! another comment!

import [std, ooplike];

wrap _array:array[str] push(_element:str) _array + _element ;

struct Person, Employee
{   
    name:str;
    age:int;
}

struct Boss
{   
    name:str;
    age :int;
}

fun[int] main(_args:array[str])
{   const x = Person  ("Andy"    , 45);
    const y = Employee("Marielle", 23);
    const z = [1, 2, 3, 4];

    const mapp = {z: 2000};
    print(mapp);
    z + 1000;
    print(mapp);
    z[4] = 0;
    print(mapp[z]);

    print(x == x);

    return 2;
}



