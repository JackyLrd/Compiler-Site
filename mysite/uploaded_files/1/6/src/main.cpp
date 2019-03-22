#include <iostream>
#include "test.h"

using namespace std;

int main()
{
    cout << "Hello World!" << endl;
    auto A = foo(1, 2);
    A.func();
}