from std import [print, printf, scan, readFile, writeFile];
import [stringstd];


function main(_args:array[str]) -> int {

    print("Hola!");
    print(fact(5));
    print(non_recursive_fact(5));
    run()? print("All test passed!") : "Failed!";
    return 0;
}

function rec() -> void {
    rec();
}

#! factorial

function fact(_n:int) -> int {
    #! uses recursion
    return (_n <= 1)? 1 : _n * fact(_n - 1);
}


function non_recursive_fact(_n:int) -> int {
    #! non recursive factorial
    let _res = 1;
    
    for (; _n >=1; _n -= 1) {
        _res *= _n;
    }

    return _res;
}

function run() -> bool
{
    test_import();
    test_if_stmnt();
    test_switch_stmnt();
    test_for_loop();
    test_while();
    test_dowhile();
    test_enum();
    test_struct();
    test_impements();
    test_arithmetic();
    test_ternary();
    test_function_wrapper();
    #! success tests!
    return true;
}

function test_import() -> void
{
    std.printf("From printf access: {} {}!\n", ["Hello", "World"]);
    print("Hello World!");
    printf("Hello {}!\n", ["World"]);
    const _input = scan("message ::> ");
    printf("inputed: {}\n", [_input]);
    writeFile("lib/written.txt", _input, true);
    print(readFile("lib/written.txt"));
}

function test_if_stmnt() -> void
{
    if ((3 > 2) && (3 < 2))
    {
        #! false
        print("unreachable!!");
    }
    else if ((3 > 2) || (3 < 2))
    {
        #! true
        print("OK!!!");
    }

    return null;
}

function test_switch_stmnt() -> void
{
    switch("Hello" + " " + "World")
    {
        case "1", "2", "3": print("Found at case 1");
        case "Hello World":
            print("Found at case 2");
        else:
            print("Not found!");
    }
}

function test_for_loop() -> void
{
    print("for");
    let _i;
    for (_i = 0; _i < 10; _i += 1)
        printf("{}, ", [_i]);
    
    print("");

    _i = 0;
    for (;;)
    {
        printf("{}, ", [_i]);

        if (_i >= 10) break;
        _i += 1;
    }

    print("");
}

function test_while() -> void 
{
    print("while");
    let _i = 0;

    while (_i < 5)
    {
        printf("{}, ", [_i]);
        _i += 1;
    }

    print("");
}

function test_dowhile() -> void
{
    print("do while");

    let _i = 0;
    do {

        printf("{}, ", [_i]);
        _i += 1;

    } while(_i < 5)

    print("");
}

enum STATE
{
    OK  = 0,
    BAD = 1
}

function test_enum() -> void
{
    print(STATE);
    printf("STATE::OK  = {}\n", [STATE.OK ]);
    printf("STATE::BAD = {}\n", [STATE.BAD]);
}


struct Person 
{
    _name:str;
    _age:int;
}



function test_struct() -> void
{
    const _p1 = Person("Philipp", 23);
    print(_p1);
    printf("Person::name = {}\n", [_p1._name]);
    printf("Person::age  = {}\n", [_p1._age ]);
}

implements Person
{
    function speak(&self, _msg:str) -> void
    {
        print(_msg);
    }

    function walk(&self) -> void
    {
        print("walking...");
        self.speak("Foooooc");
    }
}


function test_impements() -> void
{
    const _p1 = Person("Philipp", 23);
    printf("{} says ", [_p1._name]); _p1.speak("Hello");

    _p1.walk();
}

function test_arithmetic() -> void
{
    print(2 * 2 + 3 / 2 % 1 ^^ 2);
    print("Hello" + "World");
    print([] + [1, 2, 3]);
    print({} + {"Hola": 2} + {"World": 3});
    test_arithmetic_with_error();
}

function test_arithmetic_with_error() -> void
{
    #! print(3 << 2.2);    #! type error
    #! print(100 / 0);     #! zero division error
    #! print("Hello" + 2); #! type error
}


function test_ternary() -> void 
{
    return (3 > 2 && 2 < 3)? print("condition true!") : print("condtion false!");
}


define function _arr:array[int] printArray() -> void printf("Array: {}\n", [_arr]);

function test_function_wrapper() -> void
{
    [1, 2, 3]!printArray();
}

