#! comment
#! another comment!

import[std];



struct Pet 
{
    name:str;
    dob :str;
}



fun[i8] add(_a:i8, _b:i8) { return _a * _b; }

fun[i8] main(_args:array[str])
{   
    print(Pet("Milo", "Jun"));
    add(6, 127);
    return 0b0000011;
}