echo "[TEST] 256 KB. Stop-and-Wait with pack_size=1500 in host=localhost."
python3 go_back_n.py 1500 1 localhost 1818 < ./files/256KB.txt > OUT &
time wait
echo "[TEST] 256 KB. Go-Back-N with N=50 and pack_size=1500 in host=localhost."
python3 go_back_n.py 1500 50 localhost 1818 < ./files/256KB.txt > OUT &
time wait

echo "[TEST] 1 MB. Stop-and-Wait with pack_size=1500 in host=localhost."
python3 go_back_n.py 1500 1 localhost 1818 < ./files/1MB.txt > OUT &
time wait
echo "[TEST] 1 MB. Go-Back-N with N=50 and pack_size=1500 in host=localhost."
python3 go_back_n.py 1500 50 localhost 1818 < ./files/1MB.txt > OUT &
time wait

echo "[TEST] 5 MB. Stop-and-Wait with pack_size=1500 in host=localhost."
python3 go_back_n.py 1500 1 localhost 1818 < ./files/5MB.txt > OUT &
time wait
echo "[TEST] 5 MB. Go-Back-N with N=50 and pack_size=1500 in host=localhost."
python3 go_back_n.py 1500 50 localhost 1818 < ./files/5MB.txt > OUT &
time wait

echo "[TEST] 10 MB. Stop-and-Wait with pack_size=1500 in host=localhost."
python3 go_back_n.py 1500 1 localhost 1818 < ./files/10MB.txt > OUT &
time wait
echo "[TEST] 10 MB. Go-Back-N with N=50 and pack_size=1500 in host=localhost."
python3 go_back_n.py 1500 50 localhost 1818 < ./files/10MB.txt > OUT &
time wait