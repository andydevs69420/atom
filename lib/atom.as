#! comment
#! another comment!

import [std, stringstd];



fun[int] main(_args:array[str])
{   
    print(_args);
    print(tohexstring([240, 159, 152, 128]));
    print(fromcharcodepoints([240, 159, 152, 128]));
    print(parsestring("\xff\x9f\x98\x80"));

    return 0xc0ffee;
}