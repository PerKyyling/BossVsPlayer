#include <iostream>
#include <fstream>
#include <chrono>
#include <string>

#include <windows.h>
#include <psapi.h>
#pragma comment(lib, "psapi.lib")

#include "astar1.hpp"

const int NUMTR = 25;

using clocks = std::chrono::high_resolution_clock;
using nanoseconds = std::chrono::nanoseconds;
using namespace std;

size_t get_current_memory_kb() {
    PROCESS_MEMORY_COUNTERS pmc;
    if (GetProcessMemoryInfo(GetCurrentProcess(), &pmc, sizeof(pmc))) {
        return pmc.WorkingSetSize / 1024;
    }
    return 0;
}

// Функция получения пикового использования памяти (в КБ)
size_t get_peak_memory_kb() {
    PROCESS_MEMORY_COUNTERS pmc;
    if (GetProcessMemoryInfo(GetCurrentProcess(), &pmc, sizeof(pmc))) {
        return pmc.PeakWorkingSetSize / 1024;
    }
    return 0;
}

void astar_memory_test() {
    ofstream out_file("C:\\c++\\hse\\A-star\\astar_memory_dsu.csv");
    out_file << "height" << ";memory_before" << ";peak" << ";growth" << endl;
    
    size_t initial_peak = get_peak_memory_kb();

    for (int i = 0; i < 1100; i += 5) {
        astar_lib astr;
        astr.read_from_file("C:\\c++\\hse\\A-star\\labgen\\tests_dsu\\" + to_string(i));
        int height = astr.get_height();

        size_t mem_before = get_current_memory_kb();

        string ans = astr.astar();

        size_t current_peak = get_peak_memory_kb();
        size_t delta = current_peak - initial_peak;
        
        initial_peak = current_peak;

        out_file << height << ";"
                 << mem_before << ";"
                 << current_peak << ";"
                 << delta << endl;
    }
}

void astar_time_test_dsu(){
    ofstream out("C:\\c++\\hse\\A-star\\astar_2000_tupoi_lb.csv");
    out << "Height";
    for (int i = 1; i <= NUMTR; ++i) {
        out << ";" << to_string(i);
    }
    out << endl;
    for (int i = 0; i < 1100; i += 3) {
        astar_lib astr;
        astr.read_from_file("C:\\c++\\hse\\A-star\\tupoi_labitint\\tests\\" + to_string(i));
        int height = astr.get_height();
        out << height;
        for (int j = 0; j < NUMTR; ++j) {
            auto start = clocks::now();
            string ans = astr.astar();
            auto elapsed = clocks::now() - start;
            long long nanosec = std::chrono::duration_cast<nanoseconds>(elapsed).count();
            out << ";" << nanosec;
        }
        out << endl;
    }
}

void bfs_time_test(){
    ofstream out("C:\\c++\\hse\\A-star\\bfs_2000_snake.csv");
    out << "Height";
    for (int i = 1; i <= NUMTR; ++i) {
        out << ";" << to_string(i);
    }
    out << endl;
    for (int i = 0; i < 1100; i += 5) {
        Bfs astr;
        astr.read_from_file("C:\\c++\\hse\\A-star\\snake_labirinth\\tests\\" + to_string(i));
        int height = astr.get_height();
        out << height;
        for (int j = 0; j < NUMTR; ++j) {
            auto start = clocks::now();
            string ans = astr.bfs();
            auto elapsed = clocks::now() - start;
            long long nanosec = std::chrono::duration_cast<nanoseconds>(elapsed).count();
            out << ";" << nanosec;
        }
        out << endl;
    }
}




int main() {
    astar_memory_test();
}
