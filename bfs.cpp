#include "astar.hpp"

void astar_lib::read_from_file(const string& filename){
    vect.clear();
    ifstream input(filename);
    input>>py>>px>>by>>bx>>height;

    for (int i=0;i<height;++i){
        string t_string;
        input>>t_string;
        vect_.push_back(t_string);
    }

}