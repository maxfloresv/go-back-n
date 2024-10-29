echo "[TEST] 256 KB file. host=localhost. window_size=50. pack_size variable."
python3 go_back_n.py 150 50 localhost 1818 < ./files/256KB.txt > OUT &
time wait
python3 go_back_n.py 500 50 localhost 1818 < ./files/256KB.txt > OUT &
time wait
python3 go_back_n.py 1000 50 localhost 1818 < ./files/256KB.txt > OUT &
time wait
python3 go_back_n.py 1444 50 localhost 1818 < ./files/256KB.txt > OUT &
time wait

echo "[TEST] 1 MB file. host=localhost. window_size=50. pack_size variable."
python3 go_back_n.py 150 50 localhost 1818 < ./files/1MB.txt > OUT &
time wait
python3 go_back_n.py 500 50 localhost 1818 < ./files/1MB.txt > OUT &
time wait
python3 go_back_n.py 1000 50 localhost 1818 < ./files/1MB.txt > OUT &
time wait
python3 go_back_n.py 1444 50 localhost 1818 < ./files/1MB.txt > OUT &
time wait

echo "[TEST] 5 MB file. host=localhost. window_size=50. pack_size variable."
python3 go_back_n.py 150 50 localhost 1818 < ./files/5MB.txt > OUT &
time wait
python3 go_back_n.py 500 50 localhost 1818 < ./files/5MB.txt > OUT &
time wait
python3 go_back_n.py 1000 50 localhost 1818 < ./files/5MB.txt > OUT &
time wait
python3 go_back_n.py 1444 50 localhost 1818 < ./files/5MB.txt > OUT &
time wait

echo "[TEST] 10 MB file. host=localhost. window_size=50. pack_size variable."
python3 go_back_n.py 150 50 localhost 1818 < ./files/10MB.txt > OUT &
time wait
python3 go_back_n.py 500 50 localhost 1818 < ./files/10MB.txt > OUT &
time wait
python3 go_back_n.py 1000 50 localhost 1818 < ./files/10MB.txt > OUT &
time wait
python3 go_back_n.py 1444 50 localhost 1818 < ./files/10MB.txt > OUT &
time wait