from subprocess import Popen, PIPE

def call_mwfn(inp_fn, stdin):
    mwfn_cmd = ["Multiwfn", inp_fn]
    proc = Popen(mwfn_cmd, universal_newlines=True,
                 stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = proc.communicate(stdin)
    proc.terminate()
    return stdout, stderr
