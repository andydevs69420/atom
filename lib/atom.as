#! comment
#! another comment!

import [integerstd, stringstd, floatstd];
from std import [scan, readFile, writeFile, printf, print];

function fact(_n:int) -> int 
{   return (_n == 1)? 1 : _n * fact(_n - 1);   }

function non_rec_fact(_n:int) -> int 
{
    let _res = 1;

    for(; _n > 1; _n -= 1) _res *= _n;

    return _res;
}

struct Person, Employee
{
    name:str;
}

function sequence(_a:int, _b:int) -> void {
    print(_a);
    print(_b);
    print(_a != _b);
   
}



function main(_args:array[str]) -> int
{   
    tests();
    print(Person("Andy"));
    print(2!add(3));
    print(integerstd);
    print("age: " + integerstd.itoa(100));
    print(stringstd.atof("125") * 2);
    
    let x = 5;

    print(fact(x));
    print(non_rec_fact(x));
    print([].peek);
    print({}.keys);
    
    sequence(100,200);

    let vv = Person("Andy");
        vv.eat("Diaper");
        vv.lobbster();
    
    let b = [1, 2, 3];

    b.push(3);

    print(b);

    print(b.peek());
    print(b);

        b.pop();

    print(b.size());
    print(b.size);
    print({"Hello": "World"}.keys());
    let hola = {"world": "Hello"};
    print(hola.values()[0] + " " + "World");

    printf("adsasd {} {} {} {} {} {}", [1, 2, 3, b, {"Hello": 69420}, vv]);
    print(stringstd.strformat("Hello {} {}!", ["World", 69420]) + "hola");

    let xx = 0;

    for(; xx < 1000; xx += 1)
        printf("num: {}", [xx]);

    print(2 != 2);

    "Hello"[3];

    [2][0] = 2;

    let v = {"hola": 2};

    print(typeof main);

    return 0;
}

implements Person
{
    function lobbster(&self) -> void 
    {
        "" + "adsasd";
    }

    function eat(&self, _food:str) -> void 
    {
        print("Eating " + _food);
    }
}

function tests() -> int
{
    let v = 1232132323233232323223323235;
    v + v;
    return v;
}

struct Dog
{
    name:str;
    dob:int;
}

define function _int:int add(_rhs:int) -> int _int * _rhs;

