#! comment
#! another comment!

import [std, stringstd, stringstd, integerstd, floatstd];


fun[int] main(_args:array[str])
{   
    print(_args);
    print(tohexstring([255, 159, 152, 128]));
    print(fromcharcodepoints([240, 159, 152, 128]));
    print(atoi("100")   + 2);
    print(atof("200.2") * 1);
    print(atof("100"));
    print(itoa(100) + "hola!");
    print(ftoa(2.2) + "2");
    return 0xc0ffee;
}