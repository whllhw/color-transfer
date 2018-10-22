#include <iostream>
#include <string>
using namespace std;
typedef struct StructTest
{
    char* name;
    int age;
    int score[3];
}StructTest, *StructPtr;
class TestLib
{
    public:
        int passInt(int a);
        double passDouble(double d);
        char passChar(char c);
        char* passString(char* s);
        StructTest passStruct(StructTest st);
        StructPtr passStructPtr(StructPtr p);
        StructPtr passStructArray(StructTest vst[], int size);
};
int TestLib::passInt(int a) {
    cout << a << " in c++" << endl;
    return a;
}
double TestLib::passDouble(double d) {
    cout << d << " in c++" << endl;
    return d;
}
char TestLib::passChar(char c) {
    cout << c << " in c++" << endl;
    return c;
}
char* TestLib::passString(char* s) {
    cout << s << " in c++" << endl;
    return s;
}
StructTest TestLib::passStruct(StructTest st) {
    cout << st.name << " " << st.age << " " << st.score[2] << " in c++" << endl;
    return st;
}
StructPtr TestLib::passStructPtr(StructPtr p) {
    cout << p->name << " " << p->age << " " << p->score[2] << " in c++" << endl;
    return p;
}
StructPtr TestLib::passStructArray(StructTest vst[], int size) {
    cout << vst[0].name << " in c++" << endl;
    cout << vst[1].name << " in c++" << endl;
    return &vst[0];
}
extern "C" {
    TestLib obj;
    int passInt(int a) {
        return obj.passInt(a);
    }
    double passDouble(double d){
        return obj.passDouble(d);
    }
    char passChar(char c) {
        return obj.passChar(c);
    }
    char* passString(char* s){
        return obj.passString(s);
    }
    StructTest passStruct(StructTest st){
        return obj.passStruct(st);
    }
    StructPtr passStructPtr(StructPtr p){
        return obj.passStructPtr(p);
    }
    StructPtr passStructArray(StructTest vst[], int size){
        return obj.passStructArray(vst, size);
    }
}
// generate it into lib
// g++ -o libTest.so -shared -fPIC cppLib.cpp
