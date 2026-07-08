#include <iostream>
#include <vector>
#include <string>
#include <numeric>
#include <algorithm>
#include <random>
#include <fstream>

using namespace std;

struct DSU {
    vector<int> parent;
    vector<int> rank;

    DSU(int n) {
        parent.resize(n);
        iota(parent.begin(), parent.end(), 0);
        rank.assign(n, 0);
    }
    
    int find(int i) {
        if (parent[i] == i) {
            return i;
        }
        return parent[i] = find(parent[i]);
    }
    
    bool unite(int a, int b) {
        int fa = find(a);
        int fb = find(b);

        if (fa == fb) { return false; }
        if (rank[fa] < rank[fb]) {
            swap(fa, fb);
        }
        parent[fb] = fa;
        if (rank[fa] == rank[fb]) { rank[fa]++; }
        return true;
    }
};

struct wall {
    int u, v;
};

vector<string> generate(int height, int width) {
    int mheight = height * 2 + 1;
    int mwidth = width * 2 + 1;
    int cell_cou = height * width;

    DSU dsu(cell_cou);
    vector<wall> walls;

    for (int y = 0; y < mheight; ++y) {
        for (int x = 0; x < mwidth; ++x) {
            if (x % 2 == 0 && y % 2 == 1) {
                if (x > 0 && x < mwidth - 1) {
                    int cell1 = (x / 2 - 1) + (y / 2) * width;
                    int cell2 = (x / 2) + (y / 2) * width;
                    walls.push_back({cell1, cell2});
                }
            }
            else if (y % 2 == 0 && x % 2 == 1) {
                if (y > 0 && y < mheight - 1) {
                    int cell1 = (x / 2) + (y / 2 - 1) * width;
                    int cell2 = (x / 2) + (y / 2) * width;
                    walls.push_back({cell1, cell2});
                }
            }
        }
    }

    random_device rd;
    mt19937 g(rd());
    shuffle(walls.begin(), walls.end(), g);
    vector<string> lab(mheight, string(mwidth, '1'));

    for (int y = 0; y < height; ++y) {
        for (int x = 0; x < width; ++x) {
            lab[y * 2 + 1][x * 2 + 1] = '.';
        }
    }

    for (const auto& twall : walls) {
        if (dsu.unite(twall.u, twall.v)) {
            int x1 = 2 * (twall.u % width) + 1;
            int y1 = 2 * (twall.u / width) + 1;
            int x2 = 2 * (twall.v % width) + 1;
            int y2 = 2 * (twall.v / width) + 1;

            lab[(y1 + y2) / 2][(x1 + x2) / 2] = '.';
        }
    }
    return lab;
}

int main() {
    for (int i = 0; i < 2000; ++i) {
        int log_size = 50 + i / 2 + i % 2;
        vector<string> strg = generate(log_size, log_size);
        
        int phys_height = log_size * 2 + 1;
        int phys_width = log_size * 2 + 1;

        ofstream out("C:\\c++\\hse\\A-star\\labgen\\tests_dsu\\" + to_string(i));

        out << 1 << " " << 1 << " " << phys_height - 2 << " " << phys_width - 2 << " "<<phys_width<<endl;
        
        for (const auto& c : strg) {
            out << c << endl;
        }
        
        out.close();
    }
    return 0;
}