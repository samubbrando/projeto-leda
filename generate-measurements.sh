source config/.env

mkdir measurements

python3 -m src.scripts.linkedlist-measurement.py
python3 -m src.scripts.rbtree-measurement.py
python3 -m src.scripts.skiplist-measurement.py
