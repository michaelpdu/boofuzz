from boofuzz import *
import argparse

def check_logagent_status(target, fuzz_data_logger, session, sock):
    fuzz_data_logger.log_info("[MD] Check logagent status.")

def main(web_port):
    target_ip = "127.0.0.1"
    start_cmd = ['/home/staragent/plugins/logagent/logagent-collector', '--pull-mode']
    session = Session(
        target=Target(
            connection=SocketConnection(target_ip, 8182, proto='tcp'),
            procmon=pedrpc.Client(target_ip, web_port),
            procmon_options={"start_commands": [start_cmd]}
        ),
       sleep_time=1,
       # post_test_case_callbacks = [check_logagent_status]
    )

    # register post_test_case_callbacks
    session.register_post_test_case_callback(check_logagent_status)

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
    parser = argparse.ArgumentParser(description='Command Usages')
    parser.add_argument("-P", "--web_port", type=int, default=26002, help="port number")
    args = parser.parse_args()
    main(args.web_port)
    main()
