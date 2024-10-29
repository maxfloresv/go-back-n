echo "[TEST] 256 KB file. host=localhost. window_size variable. pack_size=1444."
python3 go_back_n.py 1444 10 localhost 1818 < ./files/256KB.txt > OUT &
time wait
python3 go_back_n.py 1444 50 localhost 1818 < ./files/256KB.txt > OUT &
time wait
python3 go_back_n.py 1444 100 localhost 1818 < ./files/256KB.txt > OUT &
time wait
python3 go_back_n.py 1444 500 localhost 1818 < ./files/256KB.txt > OUT &
time wait
python3 go_back_n.py 1444 1000 localhost 1818 < ./files/256KB.txt > OUT &
time wait
python3 go_back_n.py 1444 2500 localhost 1818 < ./files/256KB.txt > OUT &
time wait


echo "[TEST] 1 MB file. host=localhost. window_size variable. pack_size=1444."
python3 go_back_n.py 1444 10 localhost 1818 < ./files/1MB.txt > OUT &
time wait
python3 go_back_n.py 1444 50 localhost 1818 < ./files/1MB.txt > OUT &
time wait
python3 go_back_n.py 1444 100 localhost 1818 < ./files/1MB.txt > OUT &
time wait
python3 go_back_n.py 1444 500 localhost 1818 < ./files/1MB.txt > OUT &
time wait
python3 go_back_n.py 1444 1000 localhost 1818 < ./files/1MB.txt > OUT &
time wait
python3 go_back_n.py 1444 2500 localhost 1818 < ./files/1MB.txt > OUT &
time wait

echo "[TEST] 5 MB file. host=localhost. window_size variable. pack_size=1444."
python3 go_back_n.py 1444 10 localhost 1818 < ./files/5MB.txt > OUT &
time wait
python3 go_back_n.py 1444 50 localhost 1818 < ./files/5MB.txt > OUT &
time wait
python3 go_back_n.py 1444 100 localhost 1818 < ./files/5MB.txt > OUT &
time wait
python3 go_back_n.py 1444 500 localhost 1818 < ./files/5MB.txt > OUT &
time wait
python3 go_back_n.py 1444 1000 localhost 1818 < ./files/5MB.txt > OUT &
time wait
python3 go_back_n.py 1444 2500 localhost 1818 < ./files/5MB.txt > OUT &
time wait

echo "[TEST] 10 MB file. host=localhost. window_size variable. pack_size=1444."
python3 go_back_n.py 1444 10 localhost 1818 < ./files/10MB.txt > OUT &
time wait
python3 go_back_n.py 1444 50 localhost 1818 < ./files/10MB.txt > OUT &
time wait
python3 go_back_n.py 1444 100 localhost 1818 < ./files/10MB.txt > OUT &
time wait
python3 go_back_n.py 1444 500 localhost 1818 < ./files/10MB.txt > OUT &
time wait
python3 go_back_n.py 1444 1000 localhost 1818 < ./files/10MB.txt > OUT &
time wait
python3 go_back_n.py 1444 2500 localhost 1818 < ./files/10MB.txt > OUT &
time wait