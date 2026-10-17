import time
import random
from raft_node import RaftNode, State

def simulate_raft():
    node_ids = [1, 2, 3]
    nodes = [RaftNode(nid, node_ids) for nid in node_ids]

    for step in range(20):
        time.sleep(0.5)
        print(f"\n--- Step {step + 1} ---")

        # Trigger heartbeat dari leader (jika ada)
        leaders = [n for n in nodes if n.state == State.LEADER]
        if leaders:
            leader = random.choice(leaders)
            for node in nodes:
                if node.id != leader.id:
                    node.on_heartbeat(leader.current_term)

        # Leader menambahkan command baru setiap beberapa langkah
        if step % 5 == 0 and leaders:
            leader = random.choice(leaders)
            leader.append_entry(f"command-{step}")

        # Jalankan pengecekan tick pada tiap node
        for node in nodes:
            node.tick()

        # Cetak status node
        for node in nodes:
            print(f"Node {node.id}: {node.state.name} | Term {node.current_term} | Log Len {len(node.log)}")

if __name__ == "__main__":
    print("Simulasi Konsensus Raft Menggunakan Modul Python\n")
    simulate_raft()