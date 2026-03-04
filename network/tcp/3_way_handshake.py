from scapy.all import *
from scapy.layers.inet import IP, TCP

target_ip = "104.18.27.120"  # example.com
target_port = 80

# === STEP 1: Send SYN ===
ip = IP(dst=target_ip)
src_port = RandShort()
tcp_syn = TCP(sport=src_port, dport=target_port, flags='S', seq=1000)
syn_packet = ip / tcp_syn

print("=== STEP 1: Sending SYN ===")
print(f"Seq: 1000, Flags: S")

synack = sr1(syn_packet, timeout=5, verbose=0)

if synack and synack[TCP].flags == 'SA':
    print("\n=== STEP 2: Received SYN-ACK ===")
    server_seq = synack[TCP].seq
    server_ack = synack[TCP].ack
    print(f"Server Seq: {server_seq}, Server Ack: {server_ack}, Flags: SA")

    # === STEP 3: Send ACK ===
    tcp_ack = TCP(
        sport=src_port,
        dport=target_port,
        flags='A',
        seq=1001,  # Our seq + 1
        ack=server_seq + 1  # Acknowledge server's SYN
    )
    ack_packet = ip / tcp_ack

    send(ack_packet, verbose=0)
    print("\n=== STEP 3: Sent ACK ===")
    print(f"Seq: 1001, Ack: {server_seq + 1}, Flags: A")
    print("\n✓ TCP Handshake Complete!")
else:
    print("No SYN-ACK received")
