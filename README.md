
<p align="center">
    <img src="https://icons.iconarchive.com/icons/papirus-team/papirus-apps/128/atom-beta-icon.png"/>
    <!-- copyright papirus icon -->
</p>

# ATOM-PROTOTYPE-V1 ⚡
<p>
    Atom prototype programming language project proposal.
    The final implementation will be transpiled/compiled to C using TCC by Fabrice Bellard, as for the moment it uses virtual machine which is also implemented in python3.11 and it uses mark/sweep and compact GC on a linear(single) memory model.
</p>

**SAMPLE CODE SNIPPETS**
```python
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
```

**SYNTAX**
```python
#! import statement

import [std];
from integerstd import [itoa];

function main(_args:array[str]) -> int {
    std.print("Hello World!");
    let string_num = itoa(69420) + " -> string";
    return 0;
}
```

```python
#! enum declairation

enum STATE {
    OK  = 0x01,
    BAD = 0x02
}

function main(_args:array[str]) -> int {
    std.printf("STATE::OK  = {}\n", [STATE.OK ]);
    std.printf("STATE::BAD = {}\n", [STATE.BAD]);
    return 0;
}
```

```python
#! struct declairation

struct Person, Employee {
    name:str;
    age:int;
}

function main(_args:array[str]) -> int {
    std.print(Person("andy404", 23));
    return 0;
}
```

```python
#! implements declairation

struct Person, Employee {
    name:str;
    age:int;
}

implements Person {

    function getName(&self) -> str {
        return self.name;
    }
}

function main(_args:array[str]) -> int {
    std.print(Person("andy404", 23).getName());
    return 0;
}
```

```python
#! function declairation

function _func_name(_param0:int, _param1:int) -> void {
    #! statements here!
}
```

```python
#! function wrapper declairation

define function _param0:int plus(_param1:int) -> int _param0 + _param1 ;
#! to call: 2!plus(5);
#! same as: plus(2, 5);
```

```python
#! variable declairation

#! global variable
var _x = 2;

#! global constant
const _y = 3;

function main(_args:array[str]) -> int {
    
    #! local variable
    let _x = 2;

    #! local constant
    const _y = 3;

    return 0;
}
```

```python
#! if statement

if (0xc0ffee == 12648430)
    std.print("value of hex 0xc0ffee is 12648430");
#! else if (true) print("reachable as always!");
else 
    std.print("Nah!!!");
```

```python
#! switch statement

switch("Hello"[1]) {

    case "a", "b", "c": std.print("Found at case 1");
    case "e": std.print("Found at case 2");
    else:
        std.print("Ooops, not found!");

}
```

```python
#! for loop/statement

let _i;
for (_i = 0; _i < 5; _i += 1) {

    std.printf("{}, ", [_i]);

    #! other statements!
}
```

```python
#! while loop/statement

let _i;
while (_i < 5) {

    std.printf("{}, ", [_i]);

    _i += 1;
}
```

```python
#! do_while loop/statement

let _i;
do {

    std.printf("{}, ", [_i]); _i += 1;

} while(_i < 5)
```

```python
#! operation

function main(_args:array[str]) -> int
{
    #! int
    2 + 2 * (5 + 1 * 2);

    #! float
    4 / 2;

    #! int
    4 % 2;

    #! float
    4 % 2.0;

    #! compile time zero division
    100 / 0;

    #! runtime zero division
    let _divisor = 0;
    100 / _divisor;

    #! str
    "Hello" + " " + "World!";

    #! bool
    !false == !("fooc" == "yeah!");

    #! null
    null;

    #! int array append -> arary
    [1, 2] + 3;

    #! str array append -> arary
    ["a", "b"] + "c";

    #! array extend -> arary
    [1,2,3] + [4,5,6];

    #! array push: <array[T]>[1,2,3].push(4) -> where T is the element type
    #! returns null
    [1,2,3].push(4);

    #! array pop: <array[T]>[1,2,3].pop() -> where T is the element type
    #! removes top element and return|throws index error if array is empty
    #! returns top element where type is T
    [1,2,3].pop();

    #! array peek: <array[T]>[1,2,3].peek() -> where T is the element type
    #! look-up top element and return|throws index error if array is empty
    #! returns top element where type is T
    [1,2,3].peek();

    #! array size: [1,2,3].size()
    #! returns number of items inside array
    [1,2,3].peek();

    #! array subscript
    let _arr = [1,2,3]; #! <array[T]> where T is int
        std.print(_arr[1]);
        _arr[1] += 2;
    
    #! array unpack
    let _unpack = [*[1,2,3], 4,5,6]; #! -> let _unpack = [1,2,3,4,5,6];

    #! map merge -> map
    {"pork": "hub"} + {"hub": "pork"};
    
    #! map keys -> <array[K]> where K is key type
    
    

    return 0;
}
```