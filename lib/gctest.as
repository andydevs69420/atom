
from std import [print];
from releasetest import [run];

struct Person
{
    _name:str;
}

implements Person
{
    function speak(&self, _msg:str) -> void
    {

    }
}



function main(_args:array[str]) -> int 
{
    const _res = run();

    if (_res) print("All test passed!!!");

    let LOCK = 3;

    let KEY = 3;

    assert KEY == LOCK -> "Oppps! invalid house key :(";

    print("Welcome!!");
    print(_args.size());
    return 0;
}

