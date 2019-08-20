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

    # GET /inner?type=ReloadConfig HTTP/1.1
    s_initialize(name="req_inner")
    with s_block("req_block_inner"):
        s_string("GET", name="method_get")
        s_delim(" ", name="space")
        s_static("/inner")
        s_delim("?", name="question_mark")
        s_string("type")
        s_delim("=", name='equal_mark')
        s_group("inner_type", ['ReloadConfig', 'GetStatus', 'GetConfig'])
        s_delim(" ")
        s_string('HTTP/1.1', name='http_version')
        s_static("\r\n")
    s_static("\r\n")

    # GET /?action=healthCheck HTTP/1.1
    # action list:
    # hexdump
    # getLog
    # healthCheck
    # listDir
    # tailFile
    # cleanCache
    # traceCall
    # listMetrics
    # getMetrics
    s_initialize(name="req_action")
    with s_block("req_block_reloadconfig"):
        s_string("GET", name="method_get")
        s_delim(" ", name="space")
        s_delim("/")
        s_delim("?", name="question_mark")
        s_static("action")
        s_delim("=", name='equal_mark')
        s_group("action_value", ['healthCheck', 'GetStatus', 'GetConfig'])
        s_delim(" ")
        s_string('HTTP/1.1', name='http_version')
        s_static("\r\n")
    s_static("\r\n")

    session.connect(s_get("req_inner"))
    session.connect(s_get("req_inner"), s_get("req_action"))
    session.fuzz()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Command Usages')
    parser.add_argument("-P", "--web_port", type=int, default=26002, help="port number")
    args = parser.parse_args()
    main(args.web_port)
    main()
