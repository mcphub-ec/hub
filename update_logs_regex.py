import os
import re

target_dirs = [
    "contabilidad/perseo", "contabilidad/contifico", "contabilidad/invoka",
    "contabilidad/factuplan", "contabilidad/facturasoft", "pagos/payphone",
    "pagos/kushki", "pagos/datafast", "pagos/pagomedios"
]

new_log = """logging.basicConfig(
    level=logging.INFO,
    format='{"time":"%(asctime)s", "level":"%(levelname)s", "name":"%(name)s", "message":"%(message)s"}',
)"""

pattern = re.compile(r'logging\.basicConfig\([^)]+\)', re.DOTALL)

for d in target_dirs:
    py_path = f"/root/mcphub/{d}/server.py"
    if os.path.exists(py_path):
        with open(py_path, 'r') as f:
            content = f.read()
        
        new_content = pattern.sub(new_log, content)
        if new_content != content:
            with open(py_path, 'w') as f:
                f.write(new_content)
            print(f"Updated logging in {py_path}")
        else:
            print(f"logging.basicConfig not found in {py_path}")
    else:
        print(f"File not found: {py_path}")
