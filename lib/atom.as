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
    age :int;
}

enum myenum
{
    a = 1,
    b = 0x02,
    c = 0o03,
    d = 0b100
}

var x = 0;


fun[int] main(_args:array[str])
{   
    let vvv = 0;
    while (!false)
    {   print(vvv);
        vvv = vvv + 1;
        if (vvv >= 2000)
            break;
    }
    print(vvv);
    if (!true) print("hola!");
    return 0b0000011;
}