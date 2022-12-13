#! comment
#! another comment!

import [std, stringstd];


fun[int] main(_args:array[str])
{   
    print(_args);
    print(tohexstring([240, 159, 152, 128]));
    print(fromcharcodepoints([240, 159, 152, 128]));

    print(atoi("100") + 2);

    print(atof("200") * 1);

    return 0xc0ffee;
}