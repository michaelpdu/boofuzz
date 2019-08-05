import os
import sys
fuzzer_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(fuzzer_dir)
sys.path.append(root_dir)

from boofuzz import *

def main():
    target_ip = "127.0.0.1"
    port_num = 8901
    start_cmd = ['/home/dupei/github/boofuzz/vul_server/vul_server']
    session = Session(
        target=Target(
            connection=SocketConnection(target_ip, port_num, proto='tcp'),
            procmon=pedrpc.Client(target_ip, 26002),
            procmon_options={"start_commands": [start_cmd]}
        ),
       sleep_time=1,
    )

    s_initialize(name="Request")
    with s_block("Request-Line"):
        s_string("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", name='Request-URI')
    s_static('\n')

    session.connect(s_get("Request"))
    session.fuzz()

if __name__ == "__main__":
    main()
