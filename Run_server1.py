import socket
import subprocess
import time
import os

MODEL_PATH = r#Replace this path with the path to the GGUF model you want to run. This is an example path."C:\Users\Name\LLMs and stuff\LLM.gguf"
SERVER_PATH = r#Once you moved the folder to its permanent spot, open the folder, go to where this says, "New folder\llama.cpp\build\bin\Release\llama-server.exe" and update this with the new path of the LlamaServer.exe
PORT = 8080

def is_port_open(host, port):
    """Check if a port is open on a host."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        try:
            s.connect((host, port))
            return True
        except (OSError, ConnectionRefusedError):
            return False

def start_llm_server():
    if not os.path.exists(MODEL_PATH):
        print(f"Model not found: {MODEL_PATH}")
        return
    if not os.path.exists(SERVER_PATH):
        print(f"Server executable not found: {SERVER_PATH}")
        return

    print("Starting llama.cpp server on GPU")

    cmd = [SERVER_PATH, "--model", MODEL_PATH, "-c", "2048", "-ngl", "100", "--port", str(PORT)]

    try:
        subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
    except Exception as e:
        print(f"Failed {e}")
        return

    print("Waiting for server")
    timeout = 180
    start_time = time.time()
    while not is_port_open("127.0.0.1", PORT):
        if time.time() - start_time > timeout:
            print("Server did not start within 3 minutes.")
            return
        time.sleep(2)

    print("LLM server is ready")

if __name__ == "__main__":
    start_llm_server()
