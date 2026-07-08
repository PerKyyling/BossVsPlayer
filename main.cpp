#include "astar.hpp"
#include <iostream>
#include <fstream>
#include <chrono>
#include <string>
const int NUMTR=5;

using clocks = std::chrono::high_resolution_clock;
using nanoseconds = std::chrono::nanoseconds;
using namespace std;



int main(){
    ofstream out("C:\\c++\\hse\\A-star\\astar.csv");
    out<<"Height"<<";1"<<";2"<<";3"<<";4"<<";5"<<endl;
    for (int i=0;i<100;++i){
        astar_lib astr;
        astr.read_from_file("C:\\c++\\hse\\A-star\\tests\\"+to_string(i));
        int height=astr.get_height();
        out<<height;
        for (int j=0;j<NUMTR;++j){
            auto start=clocks::now();
            string ans=astr.astar();
            auto elapsed = clocks::now()-start;
            long long nanosec = std::chrono::duration_cast<nanoseconds>(elapsed).count();
            out<<";"<<nanosec;
        }
        out<<endl;
    }
}