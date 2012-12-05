@echo on
python b.py %1 %1_out.txt
python a.py %1_out.txt
python c.py %1_out.txt %1_out_c.txt
