[![Unitary Fund](https://img.shields.io/badge/Supported%20By-UNITARY%20FUND-brightgreen.svg?style=for-the-badge)](http://unitary.fund)
# QuNetSim 

![QuNetSim Tests](https://github.com/tqsd/QuNetSim/workflows/QuNetSim%20Tests/badge.svg)

QuNetSim is a quantum-enabled network simulator that adds common quantum networking tasks like teleportation, superdense coding, sharing EPR pairs, etc. With QuNetSim, one can design and test robust quantum network protocols under various network conditions.

## Installation and Documentation

See https://tqsd.github.io/QuNetSim/ for documentation. To install the latest release via pip:
```
pip install qunetsim
```

## Quick Start Guide

### Templater

The QuNetSim pip package comes with a templater. After installing the library, simply type `template` and follow the instructions. A template QuNetSim example will be generated. 

### Quick Example

```python
from qunetsim.components import Host, Network

network = Network.get_instance()
network.start()

alice = Host('Alice')
bob = Host('Bob')

alice.add_connection(bob.host_id)
bob.add_connection(alice.host_id)

alice.start()
bob.start()

network.add_hosts([alice, bob])

# Block Alice to wait for qubit arrive from Bob
alice.send_epr(bob.host_id, await_ack=True)
q_alice = alice.get_epr(bob.host_id)
q_bob = bob.get_epr(alice.host_id)

print("EPR is in state: %d, %d" % (q_alice.measure(), q_bob.measure()))
network.stop(True)
```

### Quick Example: generate a network from a string 

```python
from qunetsim.generator import network_generate
from qunetsim.objects import Qubit

# Initialize the network and hosts
# Note: we use 'A<==>B' to represent a classical and quantum connection
#       we use 'A<-->B' to represent a classical only connection
#       we use 'A<~~>B' to represent a quantum only connection
#       All connections are added uni-directionally, so '<' and '>'
#       represent the direction of the flow of traffic.
network, hosts = network_generate("Alice<=>Bob<~>Eve<=>Dean<->Alice")

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
```



## Contributing 

Feel free to contribute by adding Github issues and pull requests. Adding test cases for any contributions is a requirement for any pull request to be merged. 

## Citation
```bibtex
@article{diadamo2020qunetsim,
  title={QuNetSim: A Software Framework for Quantum Networks},
  author={DiAdamo, Stephen and N{\"o}tzel, Janis and Zanger, Benjamin and Be{\c{s}}e, Mehmet Mert},
  journal={IEEE Transactions on Quantum Engineering},
  year={2021},
  doi={10.1109/TQE.2021.3092395}
}
```
