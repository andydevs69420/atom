#! comment
#! another comment!


import[std];


enum hello_t {
    a = 2 << 3,
    b = 3 << 2
}

fun[int] main(_args:array[str])
{   
    let x = ~2;
    print(x == -+3);
    print(true != true);
    return 2;
}



