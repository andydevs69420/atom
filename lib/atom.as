#! comment
#! another comment!


fun[void] eat(_food:str) 
{
    print(_food);
    return null;
}

native::std
fun[void] print(_object:any);


fun[int] main(_args:array[str])
{   
    print(eat("ginamos"));
    return 0;
}


