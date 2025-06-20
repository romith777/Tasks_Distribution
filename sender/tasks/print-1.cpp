#include <iostream>

class Greeter {
public:
    void sayHello() {
        std::cout << "This is file 1 cpp" << std::endl;
    }
};

int main() {
    Greeter myGreeter;
    myGreeter.sayHello();
    return 0;
}