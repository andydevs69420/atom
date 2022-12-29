
from std import [printf, print];
import [stringstd];


function none() -> void {
    
    return null;
}

function main(_args:array[str]) -> int
{
    let x;
    let y = x;

    for (x = 0; x < 2000; x += 1) none();
    
    print(x);
    print(y);

    assert y == null -> "Nah!!!";

    return 0;
}


