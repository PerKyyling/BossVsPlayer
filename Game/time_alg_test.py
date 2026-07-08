from algor import *
from time import *
import os

len_tests = 25


with open("dsu_2000_timetest.csv", "w", encoding="utf-8") as res_file:

    hd = ['height'] + [str(x) for x in range(1, len_tests + 1)]
    res_file.write(";".join(hd) + "\n")

    for i in range(0,2000,5):

        map = []
        base_path=r"C:\c++\hse\A-star\labgen\tests_dsu"
        file_name = os.path.join(base_path, str(i))
        with open(file_name, "r", encoding="utf-8") as file:

            py, px, by, bx, len_map = file.readline().strip().split()
            for line in file:

                cleaned_line = line.strip()

                if cleaned_line:
                    map.append(cleaned_line)

        py, px, by, bx, len_map = int(py), int(px), int(by), int(bx), int(len_map)

        file_results = []

        for _ in range(len_tests):
            start_time = perf_counter()
            boss_path = to_inst(map, py, px, by, bx)
            end_time = perf_counter()

            ans = round((end_time - start_time) * 10 ** 9)

            file_results.append(ans)


        ans_new = [str(len_map)] + [str(ans) for ans in file_results]

        string_results = ";".join(ans_new)

        res_file.write(f"{string_results}\n")

        print(f"тест {i}...")









