import os

target_dirs = [
    "contabilidad/perseo", "contabilidad/contifico", "contabilidad/invoka",
    "contabilidad/factuplan", "contabilidad/facturasoft", "pagos/payphone",
    "pagos/kushki", "pagos/datafast", "pagos/pagomedios"
]

old_log = """logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)"""

new_log = """logging.basicConfig(
    level=logging.INFO,
    format='{"time":"%(asctime)s", "level":"%(levelname)s", "name":"%(name)s", "message":"%(message)s"}',
)"""

for d in target_dirs:
    py_path = f"/root/mcphub/{d}/server.py"
    if os.path.exists(py_path):
        with open(py_path, 'r') as f:
            content = f.read()
        if old_log in content:
            content = content.replace(old_log, new_log)
            with open(py_path, 'w') as f:
                f.write(content)
            print(f"Updated logging in {py_path}")
        else:
            print(f"Old logging format not found in {py_path}")
    else:
        print(f"File not found: {py_path}")
