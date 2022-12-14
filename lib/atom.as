#! comment
#! another comment!

import [std, stringstd, stringstd];



fun[int] main(_args:array[str])
{   
    print(_args);
    print(tohexstring([255, 159, 152, 128]));
    print(fromcharcodepoints([240, 159, 152, 128]));
    print(atoi("100s")   + 2);
    print(atof("200.2") * 1);
    return 0xc0ffee;
}