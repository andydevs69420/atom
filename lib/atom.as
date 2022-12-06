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
{   name:str;
    age:int;
}

fun[int] main(_args:array[str])
{   
    const x = Person("Andy", 1000);
    const y = Employee("Marielle", 23);
   
    print(x);
    print(y);

    x.name = y.name;
    y.age  = x.age;

    print(x);
    print(y);

    print({[1,2,3]: 2, [1,2,3,4]: 3, {1:2}:4});

    const z = [1,2,3];

    print(z[2]);

    return 2;
}



