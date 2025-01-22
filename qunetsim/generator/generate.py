from qunetsim.components import Host, Network
from .connection import Connection

import re


def get_connections(hosts: dict[str, Host], string: str) -> list[Connection]:
    """
    Get the connections from the string.

    Args:
        hosts (dict[str, Host]): The dictionary of hosts.
        string (str): The string representing the connections.

    Returns:
        list[Connection]: The list of connections.
    """
    # Use the regular expression to get the connections
    regex = r'(\{(?:\w+,)*\w+\}|\w+)(<{0,1}(?:==|--|~~)>{0,1})(\{(?:\w+,)*\w+\}|\w+)'

    connections = []
    start = 0

    while True:
        match = re.search(regex, string[start:])
        if not match:
            break

        # Get the hosts from the left and right side
        hosts_left = get_hosts(match.group(1))
        hosts_right = get_hosts(match.group(3))
        connection_type = match.group(2)

        print(f"Match 1: {match.group(1)}, Match 2: {match.group(2)}, Match 3: {match.group(3)}")

        print(f"Hosts left: {hosts_left}")
        print(f"Hosts right: {hosts_right}")

        # Append the new connections
        for host_left in hosts_left:
            for host_right in hosts_right:
                host1 = hosts[host_left]
                host2 = hosts[host_right]
                connections.append(Connection(host1, host2, connection_type))

                print(f"Connection between {host1} and {host2} of type {connection_type}")

        # Update the start index
        start += match.start(3)

    # Remove the duplicates
    connections = list(dict.fromkeys(connections))

    return connections


def get_hosts(string: str) -> list[str]:
    """
    Get the hosts from the string.

    Args:
        string (str): The string representing the hosts.

    Returns:
        list[str]: The list of hosts.
    """
    # Use the regular expression (\w+)
    regex = r'(\w+)'

    hosts = []

    for match in re.finditer(regex, string):
        hosts.append(match.group())

    # remove the duplicates
    hosts = list(dict.fromkeys(hosts))

    return hosts


def array_to_host(array):
    """
    Convert the array of host string to a host object.

    Args:
        array (list): The array representing the host.

    Returns:
        list (Host): The list with the host objects.
    """

    # Create one host object for each host in the array
    hosts = {host: Host(host) for host in array}

    return hosts


def network_parser(string) -> tuple[dict[str, Host], list[Connection]]:
    """
    Parse the network string and return the network object.

    Args:
        string (str): The string representing the network.

    Returns:
        tuple[dict[str, Host], list[Connection]]: The hosts and connections.
    """
    # Remove the spaces and line breaks
    string = string.replace(' ', '')

    # Get the hostnames
    string_hosts = get_hosts(string)

    # Create the host objects
    hosts = array_to_host(string_hosts)

    # Get the connections
    connections = get_connections(hosts, string)

    return hosts, connections


def network_generate(string : str) -> tuple[Network, dict[str, Host]]:
    """
    Generate the network from the string.

    Args:
        string (str): The string representing the network.

    Returns:
        tuple[Network, dict[str, Host]]: The network and the hosts.
    """
    network = Network.get_instance()
    hosts, connections = network_parser(string)

    for connection in connections:
        connection.add_connection()

    # Append the hosts to the network
    for host in hosts.values():
        network.add_host(host)

    return network, hosts
