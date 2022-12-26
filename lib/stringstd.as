#! STRING STANDARD LIB
#! author: andydevs69420
#! date: December 10 2022

native::stringstd
function strlen(__string__:str) -> int;

native::stringstd
function strtoupper(__string__:str) -> str;

native::stringstd
function strtolower(__string__:str) -> str;

native::stringstd
function strsplit(__string__:str, __delimeter__:str) -> array[str];

native::stringstd
function strreverse(__string__:str) -> str;

native::stringstd
function strrepeat(__string__:str, __times__:int) -> str;

native::stringstd
function charcodepoints(__string__:str) -> array[int];

native::stringstd
function fromcharcodepoints(__codepoints__:array[int]) -> str;

native::stringstd
function tohexstring(__codepoints__:array[int]) -> str;

native::stringstd
function atoi(__string__:str) -> int;

native::stringstd
function atof(__string__:str) -> float;

native::stringstd
function strformat(__format:str, _format_list:array[any]) -> str;
