#! comment
#! another comment!



import[std];


enum hello_t {
    a = 2 << 3,
    b = 3 << 2
}


if (true && 2 != 2)
    print("FOOOOOC");
else if(true && !true)
    print("true");
else
    print("false");


if (3 != 3)
    print("YES!!!");
else if (!true)
    print("OFC!!");
else
    print("No");


wrap _str:str println() print(_str);
wrap _arr:array[int] push(_element:int) _arr + _element;

switch(100) 
{
    case 1,2,3, 50 + 25 + 26: 
        print("100 found at case 1");

    case 100:
        print("100 found at case 2");

    else:
        print("100 not found!");
}

struct Person, Employee, Tao
{   
    name:str;
    age:int;
}

enum myenum {
    a = 1,
    b = 0x02,
    c = 0o03,
    d = 0b011
}

fun[int] main(_args:array[str])
{   
    const p1 = Person("Andy", 404);
    const e1 = Employee("Marielle", 23);
    const e2 = Employee("Mark", 50);
    print(p1);
    print(e1);

    const arr = [
        p1, e1
    ];

    print(arr);

    arr + Tao("Josh", 100);

    print(arr);

    print(myenum);
    print(myenum.a);
    print(myenum.b);

    return 2;
}



