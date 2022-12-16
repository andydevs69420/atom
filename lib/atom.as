#! comment
#! another comment!

define fun[int] _obj:int add(_n:int) _obj + _n;

struct Person {
    name:str;
}



fun[int] main(_args:array[str])
{   
    2 + 2;
    print(2!add(4));

    print(Person("Philipp"));

    print(add(1,2));

    return 0;
}

native::std
fun[void] print(_object:any);

