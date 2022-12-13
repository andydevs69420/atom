#! STRING STANDARD LIB
#! author: andydevs69420
#! date: December 10 2022

native::stringstd
fun[int] strlen(__string__:str);

native::stringstd
fun[str] strtoupper(__string__:str);

native::stringstd
fun[str] strtolower(__string__:str);

native::stringstd
fun[array[str]] strsplit(__string__:str, __delimeter__:str);

native::stringstd
fun[str] strreverse(__string__:str);

native::stringstd
fun[str] strrepeat(__string__:str, __times__:int);

native::stringstd
fun[array[int]] charcodepoints(__string__:str);

native::stringstd
fun[str] fromcharcodepoints(__codepoints__:array[int]);

native::stringstd
fun[str] tohexstring(__codepoints__:array[int]);

native::stringstd
fun[int] atoi(__string__:str);

native::stringstd
fun[float] atof(__string__:str);

