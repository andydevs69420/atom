#! comment
#! another comment!

import[std];

struct Pet 
{
    name:str;
    dob:str;
}

fun[int] main(_args:array[str])
{   
    print(true || 3);

    let x = false;

    switch (x || 3) 
    {
        case !true, false: print("asdasd");
    }

    return 0b0000011;
}