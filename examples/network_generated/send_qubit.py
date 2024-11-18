from qunetsim.generator import network_generate
from qunetsim.objects import Qubit

network, hosts = network_generate("Alice<==>Bob<~~>Eve<==>Dean<-->Alice")

network.draw_quantum_network()
network.draw_classical_network()

network.start(list(hosts.keys()))

# Initialize the hosts
for host in hosts.values():
    host.start()

for _ in range(10):
    # Create a qubit owned by Alice
    q = Qubit(hosts['Alice'])
    # Put the qubit in the excited state
    q.H()
    # Send the qubit and await an ACK from Dean
    q_id, ack_arrived = hosts['Alice'].send_qubit('Dean', q, await_ack=True)

    # Get the qubit on Dean's side from Alice
    q_rec = hosts['Dean'].get_qubit('Alice', q_id, wait=0)

    # Ensure the qubit arrived and then measure and print the results.
    if q_rec is not None:
        m = q_rec.measure()
        print("Results of the measurements for q_id are ", str(m))
    else:
        print('Qubit did not arrive.')

network.stop(stop_hosts=True)
