import re
import subprocess
import tempfile
import os

def interpret(source):
    outputs = []

    # Python segments
    for segment in re.findall(r'<\?py(.*?)\?>', source, re.S):
        code = segment.strip()
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.py') as f:
            f.write(code)
            path = f.name
        res = subprocess.run(['python', path], capture_output=True, text=True)
        outputs.append(res.stdout)
        os.unlink(path)

    # JavaScript segments
    for segment in re.findall(r'<\?js(.*?)\?>', source, re.S):
        code = segment.strip()
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.js') as f:
            f.write(code)
            path = f.name
        res = subprocess.run(['node', path], capture_output=True, text=True)
        outputs.append(res.stdout)
        os.unlink(path)

    # PHP segments
    for segment in re.findall(r'<\?php(.*?)\?>', source, re.S):
        code = segment.strip()
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.php') as f:
            f.write("<?php\n" + code + "\n?>")
            path = f.name
        res = subprocess.run(['php', path], capture_output=True, text=True)
        outputs.append(res.stdout)
        os.unlink(path)

    # CSS segments (print as message, not executed)
    for segment in re.findall(r'<\?css(.*?)\?>', source, re.S):
        css = segment.strip()
        outputs.append(f"[CSS Styling Loaded]\n{css}\n")

    # C# segments (assumes csc installed)
    for segment in re.findall(r'<\?cs(.*?)\?>', source, re.S):
        code = segment.strip()
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.cs') as f:
            f.write(f"using System; class Program {{ static void Main() {{ {code} }} }}")
            path = f.name
        exe_path = path.replace('.cs', '.exe')
        compile_res = subprocess.run(['csc', '/nologo', '/out:' + exe_path, path], capture_output=True, text=True)
        if os.path.exists(exe_path):
            run_res = subprocess.run([exe_path], capture_output=True, text=True)
            outputs.append(run_res.stdout)
            os.unlink(exe_path)
        os.unlink(path)

    # C++ segments (assumes g++ installed)
    for segment in re.findall(r'<\?cpp(.*?)\?>', source, re.S):
        code = segment.strip()
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.cpp') as f:
            f.write(f"#include <iostream>\nusing namespace std;\nint main() {{ {code} return 0; }}")
            path = f.name
        exe_path = path.replace('.cpp', '')
        compile_res = subprocess.run(['g++', path, '-o', exe_path], capture_output=True, text=True)
        if os.path.exists(exe_path):
            run_res = subprocess.run([exe_path], capture_output=True, text=True)
            outputs.append(run_res.stdout)
            os.unlink(exe_path)
        os.unlink(path)

    # Print combined output
    print(''.join(outputs))
