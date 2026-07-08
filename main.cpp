#include "astar.hpp"
#include <iostream>
#include <fstream>
#include <chrono>
#include <string>
const int NUMTR=25;

using clocks = std::chrono::high_resolution_clock;
using nanoseconds = std::chrono::nanoseconds;
using namespace std;


void astar_time_test_dsu(){
    ofstream out("C:\\c++\\hse\\A-star\\astar_2000_dsu.csv");
    out<<"Height";
    for (int i=1;i<=NUMTR;++i){
        out<<";"<<to_string(i);
    }
    out<<endl;
    for (int i=0;i<2000;i++){
        astar_lib astr;
        astr.read_from_file("C:\\c++\\hse\\A-star\\labgen\\tests_dsu\\"+to_string(i));
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


int main(){
    astar_time_test_dsu();
}