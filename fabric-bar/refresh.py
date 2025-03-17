import os, psutil, signal

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

def refresh():
    BAR_SCRIPT_PATH = "$HOME/dotfiles/fabric-bar/fabric_bar.py"
    # Find and terminate the existing bar process
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if "python" in proc.info['name'] and "fabric_bar.py" in " ".join(proc.info['cmdline']):
            print(proc.info)
            os.kill(proc.info['pid'], signal.SIGTERM)
    
    print("Bar process terminated")
    # Restart the bar
    # os.system(f"python3 {BAR_SCRIPT_PATH} &")


if __name__ == "__main__":
    refresh()