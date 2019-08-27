from boofuzz import *
import argparse

def check_logagent_status(target, fuzz_data_logger, session, sock):
    fuzz_data_logger.log_info("[MD] Check logagent status.")

def main(web_port):
    target_ip = "127.0.0.1"
    start_cmd = ['/home/staragent/plugins/logagent/logagent-collector', '--pull-mode']
    sess = Session(
        target=Target(
            connection=SocketConnection(target_ip, 8182, proto='tcp'),
            procmon=pedrpc.Client(target_ip, web_port),
            procmon_options={"start_commands": [start_cmd]}
        ),
       sleep_time=1,
       # post_test_case_callbacks = [check_logagent_status]
    )

    # register post_test_case_callbacks
    sess.register_post_test_case_callback(check_logagent_status)


    # with s_block("supported_file_path"):
    #     s_group('', ["/alidata/", "/apsara/", "/disk1/", "/home/", "/usr/"])


    # GET /inner?type=ReloadConfig HTTP/1.1
    s_initialize(name="req_inner")
    with s_block("req_block_inner"):
        s_string("GET", name="method_get")
        s_delim(" ", name="space")
        s_delim("/")
        s_static("inner")
        s_delim("?", name="question_mark")
        s_static("type")
        s_delim("=", name='equal_mark')
        s_group("inner_type", ['ReloadConfig', 'GetStatus', 'GetConfig'])
        s_static(" ") # space is necessary
        s_string('HTTP/1.1', name='http_version')
        s_static("\r\n")
    s_static("\r\n")

    # GET /get?file=/home/staragent/plugins/logagent/local_data/monitor-2019-06-07T21-33-38.267.log&begin=0&end=200 HTTP/1.1
    s_initialize(name="req_get")
    with s_block("req_block_get"):
        s_string("GET", name="method_get")
        s_delim(" ", name="space")
        s_delim("/")
        s_static("get")
        s_delim("?", name="question_mark")
        s_static("file")
        s_delim("=", name='equal_mark')
        s_group('supportted_root_dir', ["/alidata/", "/apsara/", "/disk1/", "/home/", "/usr/"])
        s_string('filename')
        s_delim("&")
        s_static("begin=")
        s_int(0)
        s_delim("&")
        s_static("end=")
        s_int(200)
        s_static(" ") # space is necessary
        s_string('HTTP/1.1', name='http_version')
        s_static("\r\n")
    s_static("\r\n")

    # GET /size?file=/home/staragent/plugins/logagent/local_data/monitor-2019-06-07T21-33-38.267.log HTTP/1.1
    s_initialize(name="req_size")
    with s_block("req_block_size"):
        s_string("GET", name="method_get")
        s_delim(" ", name="space")
        s_delim("/")
        s_static("size")
        s_delim("?", name="question_mark")
        s_static("file")
        s_delim("=", name='equal_mark')
        s_group('supportted_root_dir', ["/alidata/", "/apsara/", "/disk1/", "/home/", "/usr/"])
        s_string('filename')
        s_delim(" ")
        s_string('HTTP/1.1', name='http_version')
        s_static("\r\n")
    s_static("\r\n")
    
    # GET /tail?file=/home/staragent/plugins/logagent/local_data/monitor-2019-06-07T21-33-38.267.log&task_id=001 HTTP/1.1

    s_initialize(name="req_tail")
    with s_block("req_block_tail"):
        s_string("GET", name="method_get")
        s_delim(" ", name="space")
        s_delim("/")
        s_static("tail")
        s_delim("?", name="question_mark")
        s_static("file")
        s_delim("=", name='equal_mark')
        s_group('supportted_root_dir', ["/alidata/", "/apsara/", "/disk1/", "/home/", "/usr/"])
        s_string('filename')
        s_delim("&")
        s_static("task_id=")
        s_int(0)
        s_static(" ") # space is necessary
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
    s_initialize(name="req_action_healthcheck")
    with s_block("req_block_healthcheck"):
        s_string("GET", name="method_get")
        s_delim(" ", name="space")
        s_delim("/")
        s_delim("?", name="question_mark")
        s_static("action")
        s_delim("=", name='equal_mark')
        s_group("action_value", ['healthCheck', 'cleanCache', 'listMetrics', 'getMetrics'])
        s_static(" ") # space is necessary
        s_string('HTTP/1.1', name='http_version')
        s_static("\r\n")
    s_static("\r\n")

    # GET /?action=hexdump&file=/etc/shadow,0,200 HTTP/1.1
    s_initialize(name="req_action_hexdump")
    with s_block("req_block_hexdump"):
        s_string("GET", name="method_get")
        s_delim(" ", name="space")
        s_delim("/")
        s_delim("?", name="question_mark")
        s_static("action")
        s_delim("=", name='equal_mark')
        s_static("hexdump")
        s_delim("&")
        s_static("file=")
        s_static("/home/dupei/github/boofuzz/fuzzer/testcase.hexdump")
        s_delim(",")
        s_int(0)
        s_delim(",")
        s_int(200)
        s_static(" ") # space is necessary
        s_string('HTTP/1.1', name='http_version')
        s_static("\r\n")
    s_static("\r\n")

    #
    sess.connect(s_get("req_inner"))
    sess.connect(s_get("req_get"))
    sess.connect(s_get("req_size"))
    sess.connect(s_get("req_tail"))
    sess.connect(s_get("req_action_healthcheck"))
    sess.connect(s_get("req_action_hexdump"))

    sess.fuzz()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Command Usages')
    parser.add_argument("-P", "--web_port", type=int, default=26002, help="port number")
    args = parser.parse_args()
    main(args.web_port)
