#include "astar.hpp"

void Bfs::read_from_file(const string& filename){
    vect_.clear();
    ifstream input(filename);
    input >> py >> px >> by >> bx >> height;

    for (int i = 0; i < height; ++i){
        string t_string;
        input >> t_string;
        vect_.push_back(t_string);
    }

    if (!vect_.empty()) {
        normalVector_.resize(vect_.size());
        for (auto& row : normalVector_) {
            row.assign(vect_[0].size(), 0);
        }
        createNormalVector();
    }
}

void Bfs::createNormalVector() {  // Убрать параметры, использовать члены класса
    for (int j = 0; j < vect_.size(); j++) {
        for (int i = 0; i < vect_[0].size(); i++) {
            if (vect_[j][i] == '1') {
                normalVector_[j][i] = 1;  // Исправить normalVector -> normalVector_
            }
            else {
                normalVector_[j][i] = 0;
            }
        }
    }
}

std::string Bfs::bfs() {
    std::vector<int> this_point = {py, px};
    std::stringstream ss;
    ss << py << "," << px;
    vector_.push(this_point);
    vectIsVisited_.insert(ss.str());
    
    while (!vector_.empty()) {
        int y = vector_.front()[0];
        int x = vector_.front()[1];
        
        if ((y == by) && (x == bx)) {
            std::vector<std::vector<int>> data;
            int j = y;
            int i = x;
            data.push_back({j, i});
            
            while ((j != py) || (i != px)) {
                std::string key = std::to_string(j) + "," + std::to_string(i);
                auto it = map_.find(key);
                if (it == map_.end() || it->second.empty()) break;
                auto parent = it->second;
                // ИСПРАВИТЬ: parent - это vector<vector<int>>, берём последнего родителя
                j = parent.back()[0];  // parent.back() - это vector<int>{y, x}
                i = parent.back()[1];
                data.push_back({j, i});
            }
            
            if (data.size() < 2) return "";
            
            int delta_y = (data[data.size() - 2][0] - data[data.size() - 1][0]);
            int delta_x = (data[data.size() - 2][1] - data[data.size() - 1][1]);
            
            if (delta_y < 0) return "U";
            else if (delta_y > 0) return "D";
            else if (delta_x < 0) return "L";
            else return "R";
        }
        
        // Проверка ширины поля (исправить normalVector_[0].size())
        int field_width = normalVector_.empty() ? 0 : normalVector_[0].size();
        
        // Вверх
        if (y - 1 >= 0 && normalVector_[y - 1][x] != 1) {
            std::vector<int> next_point = {y - 1, x};
            std::string key = std::to_string(y - 1) + "," + std::to_string(x);
            if (vectIsVisited_.find(key) == vectIsVisited_.end()) {
                vectIsVisited_.insert(key);
                map_[key] = {vector_.front()};
                vector_.push(next_point);
            }
        }
        
        // Вниз
        if (y + 1 < normalVector_.size() && normalVector_[y + 1][x] != 1) {
            std::vector<int> next_point = {y + 1, x};
            std::string key = std::to_string(y + 1) + "," + std::to_string(x);
            if (vectIsVisited_.find(key) == vectIsVisited_.end()) {
                vectIsVisited_.insert(key);
                map_[key] = {vector_.front()};
                vector_.push(next_point);
            }
        }
        
        // Влево
        if (x - 1 >= 0 && normalVector_[y][x - 1] != 1) {
            std::vector<int> next_point = {y, x - 1};
            std::string key = std::to_string(y) + "," + std::to_string(x - 1);
            if (vectIsVisited_.find(key) == vectIsVisited_.end()) {
                vectIsVisited_.insert(key);
                map_[key] = {vector_.front()};
                vector_.push(next_point);
            }
        }
        
        // Вправо (использовать field_width)
        if (x + 1 < field_width && normalVector_[y][x + 1] != 1) {
            std::vector<int> next_point = {y, x + 1};
            std::string key = std::to_string(y) + "," + std::to_string(x + 1);
            if (vectIsVisited_.find(key) == vectIsVisited_.end()) {
                vectIsVisited_.insert(key);
                map_[key] = {vector_.front()};
                vector_.push(next_point);
            }
        }
        
        vector_.pop();
    }
    
    return "";
}