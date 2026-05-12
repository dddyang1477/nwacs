import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    import nwacs_server_v3
    msg = 'IMPORT OK'
except Exception as e:
    msg = 'IMPORT ERROR: ' + str(e)
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_test_out.txt'), 'w') as f:
    f.write(msg)