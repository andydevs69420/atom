
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