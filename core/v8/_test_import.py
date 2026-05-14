import sys
import os
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_import_result.txt')

try:
    import nwacs_server_v3
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write('OK: nwacs_server_v3 imported successfully\n')
        f.write(f'Has main: {hasattr(nwacs_server_v3, "main")}\n')
        f.write(f'Has NWACSHandler: {hasattr(nwacs_server_v3, "NWACSHandler")}\n')
except Exception as e:
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write(f'ERROR: {e}\n')
        traceback.print_exc(file=f)