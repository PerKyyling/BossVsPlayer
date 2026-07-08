#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <queue>
#include <algorithm>

#include "astar1.hpp"

void Bfs::read_from_file(const std::string& filename){
    vect_.clear();
    std::ifstream input(filename);
    if (!input.is_open()) return;
    
    input >> py >> px >> by >> bx >> height;

    for (int i = 0; i < height; ++i){
        std::string t_string;
        input >> t_string;
        vect_.push_back(t_string);
    }

    if (!vect_.empty()) {
        int rows = vect_.size();
        int cols = vect_[0].size(); 
        
        normalVector_.resize(rows);
        visitedMatrix_.assign(rows, std::vector<bool>(cols, false));
        parentMatrix_.assign(rows, std::vector<Point>(cols, {-1, -1}));
        
        for (auto& row : normalVector_) {
            row.assign(cols, 0);
        }
        createNormalVector();
    }
}

void Bfs::createNormalVector() {  
    for (size_t j = 0; j < vect_.size(); j++) {
        for (size_t i = 0; i < vect_[0].size(); i++) {
            if (vect_[j][i] == '1') {
                normalVector_[j][i] = 1;  
            }
            else {
                normalVector_[j][i] = 0;
            }
        }
    }
}

int Bfs::get_height(){
    return vect_.size();
}

std::string Bfs::bfs() {
    while (!vector_.empty()) vector_.pop();
    
    if (normalVector_.empty()) return "";
    int rows = normalVector_.size();
    int cols = normalVector_[0].size();
    
    for (int y = 0; y < rows; ++y) {
        std::fill(visitedMatrix_[y].begin(), visitedMatrix_[y].end(), false);
    }

    vector_.push({py, px});
    visitedMatrix_[py][px] = true;
    
    while (!vector_.empty()) {
        int y = vector_.front().y;
        int x = vector_.front().x;
        
        if ((y == by) && (x == bx)) {
            std::vector<Point> data;
            int j = y;
            int i = x;
            data.push_back({j, i});
            
            while ((j != py) || (i != px)) {
                Point p = parentMatrix_[j][i];
                j = p.y;
                i = p.x;
                data.push_back({j, i});
            }
            
            if (data.size() < 2) return "";
            
            int delta_y = (data[data.size() - 2].y - data[data.size() - 1].y);
            int delta_x = (data[data.size() - 2].x - data[data.size() - 1].x);
            
            if (delta_y < 0) return "U";
            else if (delta_y > 0) return "D";
            else if (delta_x < 0) return "L";
            else return "R";
        }
        
        if (y - 1 >= 0 && normalVector_[y - 1][x] != 1 && !visitedMatrix_[y - 1][x]) {
            visitedMatrix_[y - 1][x] = true;
            parentMatrix_[y - 1][x] = {y, x};
            vector_.push({y - 1, x});
        }
        if (y + 1 < rows && normalVector_[y + 1][x] != 1 && !visitedMatrix_[y + 1][x]) {
            visitedMatrix_[y + 1][x] = true;
            parentMatrix_[y + 1][x] = {y, x};
            vector_.push({y + 1, x});
        }
        if (x - 1 >= 0 && normalVector_[y][x - 1] != 1 && !visitedMatrix_[y][x - 1]) {
            visitedMatrix_[y][x - 1] = true;
            parentMatrix_[y][x - 1] = {y, x};
            vector_.push({y, x - 1});
        }
        if (x + 1 < cols && normalVector_[y][x + 1] != 1 && !visitedMatrix_[y][x + 1]) {
            visitedMatrix_[y][x + 1] = true;
            parentMatrix_[y][x + 1] = {y, x};
            vector_.push({y, x + 1});
        }
        vector_.pop();
    }
    return "";
}
