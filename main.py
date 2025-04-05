from scripts.api import price, images
from scripts.constants import verbose
from scripts.scanner import run
import os

if verbose:
    print("[main::verbose] deleting cache...")

list( map( os.unlink, (os.path.join("sources", f) for f in os.listdir("sources")) ) )

code = input("input set code (OP10): ")
interface = input("interface (0): ")
if (interface == ""):
    interface = 0
else:
    interface = int(interface)
    
print("[main::verbose] getting source images")
images(code.strip())
print("[main::verbose] getting market prices...")
price(code.strip())
run(interface)