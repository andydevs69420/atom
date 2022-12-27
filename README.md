
<p align="center">
    <img src="https://icons.iconarchive.com/icons/papirus-team/papirus-apps/512/atom-beta-icon.png"/>
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
    let _res = 0;
    
    for (; _n > 1; _n -= 1) {
        _res *= _n;
    }

    return _n;
}
```

