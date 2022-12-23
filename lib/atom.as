#! comment
#! another comment!

from test import [print];
import [integerstd, stringstd];
from std import [test_all];

var x   = [1,2,3];
const y = [1,2,3, x], z = 2;

enum a {
    y = 2
}

const v = test;

function fact(_n:int) -> int {

    return (_n == 1)? 1 : _n * fact(_n - 1);
}

function non_rec_fact(_n:int) -> int {

    let _res = 1;

    for(; _n > 1; _n -= 1)
    {
        _res *= _n;
    }

    return _res;
}

function main(_args:array[str]) -> int
{   
    tests();
    print(y);
    print(Person("Andy"));
    print(2!add(3));
    print(integerstd);
    print("age: " + integerstd.itoa(100));
    print(stringstd.atof("125") * 2);
    print(v);
    print(typeof v);

    let x = 15;

    print(fact(x));
    print(non_rec_fact(x));

    test_all();

    return 0;
}

function tests() -> int
{
    let v = 123213232323323232322332323;
    v + v;
    return v;
}

struct Person, Employee
{
    name:str;
}

struct Dog {
    name:str;
}

define function _int:int add(_rhs:int) -> int _int * _rhs; 

