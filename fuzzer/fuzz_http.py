from boofuzz import *

def main():
    target_ip = "127.0.0.1"
    start_cmd = ['/home/staragent/plugins/logagent/logagent-collector', '--pull-mode']
    session = Session(
        target=Target(
            connection=SocketConnection(target_ip, 8182, proto='tcp'),
            procmon=pedrpc.Client(target_ip, 26002),
            procmon_options={"start_commands": [start_cmd]}
        ),
       sleep_time=1,
    )

    s_initialize(name="Request")
    with s_block("Request-Line"):
        # s_group("Method", ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE'])
        # s_string("GET", name='method_get')
        # s_delim(" ", name='space-1')
        s_static("GET /inner?type=ReloadConfig", name='Request-URI')
        # s_string("/inner", name='Request-URI')
        # s_delim("?", name='question_mark')
        # s_string("type")
        # s_delim("=", name='equal_mark')
        # s_string("ReloadConfig")
        s_delim(" ", name='space-2')
        # s_string('HTTP/1.1', name='HTTP-Version')
        s_static("\r\n", name="Request-Line-CRLF")
    s_static("\r\n", "Request-CRLF")

    session.connect(s_get("Request"))

    session.fuzz()


if __name__ == "__main__":
    main()
