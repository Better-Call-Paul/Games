

/*
template metaprograming and object pool

*/

#include <iostream>

using namespace std;

template<int A, int B>
struct GCD {
    static constexpr int value = GCD<B, A % B>::value;
};

template<int A>
struct GCD<A, 0> {
    static constexpr int value = A;
};


int main() {

    constexpr int result = GCD<48, 18>::value;
    cout << result << "\n";

    return 0;
}