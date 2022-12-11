#! comment
#! another comment!

import [std, stringstd];

wrapper fun _string:str toLowerCase() strtolower(_string);


fun[int] main(_args:array[str])
{   
    2 + 2;
    print(charcodepoints("😀大"));
    let i = 0;
    for (; i < 10; i += 1)
        print(strlen("hello") + i);
    

    #! ε大😀ε大😀ε大😀ε大😀ε大😀ε大😀ε大😀ε大😀ε大😀ε大😀ε大

    print(strtolower("FOOOC"));
    print("FOOOC"!toLowerCase());
    print(strsplit("asda|sd", "|"));
    print(strreverse("hola"));
    print(strrepeat("a", 50));
    print(fromcharcodepoints([240, 159, 152, 128]));

    "\u041"; #! 1_114_111 | 0x10ffff
    "\x41" ;

    print(tohexstring([240, 159, 152, 128]));

    return 0xc0ffee;
}