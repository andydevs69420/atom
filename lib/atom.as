#! comment
#! another comment!


struct Person {
    name:str;
    nage:int;
    eat:fn[int](str);
}

fun[void] eat(_food:str) {
    print(_food);
    return 0;
}

enum xx {
    x = 2 << 3
}


fun[int] main(_args:array[str])
{   
    2 + 2;
    print(2!add(4));

    const x = Person("Philipp", 0, eat);

    let i = 0;
    for (; i < 10; i += 1)
        print(i);

    print(x.name = "ada");

    print(x.nage += 2);
    print(x);

    print(add(1, 2));
    print(xx.x);
    print(xx);
    x.eat("diaper");

    return 0;
}

native::std
fun[void] print(_object:any);


define fun[int] _obj:int add(_n:int) _obj + _n;
