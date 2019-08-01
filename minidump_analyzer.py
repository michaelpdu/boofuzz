import os
import sys

MINIDUMP_STACKWALK = 'minidump_stackwalk'
if not os.path.exists(MINIDUMP_STACKWALK):
    raise "ERROR: Cannot find minidump_stackwalk!"

class MinidumpAnalyzer:
    def __init__(self):
        self.minidump_stackwalk = MINIDUMP_STACKWALK
        self.msg_map = {}

    def analyze_dump(self, dump_file):
        cmd = '{} {}'.format(self.minidump_stackwalk, dump_file)
        print('CMD:', cmd)
        output = os.popen(cmd).read()
        # Crash reason:  SIGABRT
        # Crash address: 0x3ea00005144
        msg = 'not_found'
        crash_reason = ''
        crash_addr = ''
        for line in output:
            if 'Crash reason:' in line:
                crash_reason = line[15:-1]
                msg = ''
            if 'Crash address:' in line:
                crash_addr = line[15:-1]
                msg = ''
        if crash_reason != '':
            msg = crash_reason
        if crash_addr != '':
            msg = msg + crash_addr
        return msg
    
    def analyze_folder(self, dump_folder):
        for root, _, files in os.walk(dump_folder):
            for name in files:
                dump_file = os.path.join(root, name)
                msg = self.analyze_dump(dump_file)
                if not msg in self.msg_map.keys():
                    self.msg_map[msg] = [name]
                else:
                    self.msg_map[msg].append(name)

    def display_msg_map(self):
        print("Print msg map:")
        for (key, names) in self.msg_map.items():
            print(key, names)
        
    def analyze(self, input):
        if os.path.isdir(input):
            self.analyze_folder(input)
            self.display_msg_map()
        elif os.path.isfile(input):
            msg = self.analyze_dump(input)
            print(input, msg)
        else:
            pass

if __name__ == '__main__':
    analyzer = MinidumpAnalyzer()    
    analyzer.analyze(sys.argv[1])