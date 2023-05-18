import netflow
import socket
import pandas as pd

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("192.168.88.254", 2073))

df = pd.DataFrame(columns=['INPUT', 'OUTPUT', 'IN_PACKETS', 'IN_OCTETS', 'TCP_FLAGS', 'PROTO', 'TOS', 'SRC_AS', 'DST_AS', 'SRC_MASK', 'DST_MASK'])
try:
    while 1:
        payload, client = sock.recvfrom(4096)
        p = netflow.parse_packet(payload)
        for flow in p.flows:
            item = {
                'INPUT': flow.INPUT, 'OUTPUT': flow.OUTPUT, 
                'IN_PACKETS': flow.IN_PACKETS, 'IN_OCTETS': flow.IN_OCTETS, 
                'TCP_FLAGS': flow.TCP_FLAGS, 'PROTO': flow.PROTO, 
                'TOS': flow.TOS, 'SRC_AS': flow.SRC_AS, 
                'DST_AS': flow.DST_AS, 'SRC_MASK': flow.SRC_MASK, 'DST_MASK': flow.DST_MASK}
            df = df.append(item, ignore_index=True)
except KeyboardInterrupt:
        df.to_csv("gathered.csv")
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)
