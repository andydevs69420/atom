




from std import [print];

import [integerstd];


fun[void] test_import()
{
    integerstd.itoa(100);
    print(  "Hello World!"  );
    print(  integerstd.itoa(69420) );
}



fun[void] test_all()
{
    test_import();

}