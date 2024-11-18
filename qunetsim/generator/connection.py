from qunetsim.components import Host
from .conn_type import ConnType
from .direction import Direction

class Connection:
    """
    Class representing a connection between two hosts.
    """

    def __init__(self, hostA: Host, hostB: Host, connection_string: str):
        """
        Initialize the connection.

        Args:
            hostA (Host): The first host.
            hostB (Host): The second host.
            connection_string (str): The string representing the connection.
        """
        self.hostA = hostA
        self.hostB = hostB
        
        self.direction = Direction.get_direction(connection_string)

        if connection_string[0] == '<':
            connection_string = connection_string[1:]
        if connection_string[-1] == '>':
            connection_string = connection_string[:-1]

        self.type = ConnType.get_conn_type(connection_string)

    def add_connection(self):
        """
        Add the connection between the hosts.
        """
        if self.direction == Direction.UNIDIRECTIONAL_A_B:
            ConnType.add_connection_function[self.type](self.hostA, self.hostB.host_id)
        elif self.direction == Direction.UNIDIRECTIONAL_B_A:
            ConnType.add_connection_function[self.type](self.hostB, self.hostA.host_id)
        else:
            ConnType.add_connection_function[self.type](self.hostA, self.hostB.host_id)
            ConnType.add_connection_function[self.type](self.hostB, self.hostA.host_id)

    def __str__(self):
        """
        Get the string representation of the connection.

        Returns:
            str: The string representation of the connection.
        """
        # Direction to str
        start = ''
        end = ''
        connection_type = ''
        if self.direction == Direction.UNIDIRECTIONAL_A_B:
            end = '>'
        elif self.direction == Direction.UNIDIRECTIONAL_B_A:
            start = '<'
        else:
            start = '<'
            end = '>'

        # Connection type to str
        if self.type == ConnType.CLASSICAL_AND_QUANTUM:
            connection_type = '=='
        elif self.type == ConnType.CLASSICAL:
            connection_type = '--'
        else:
            connection_type = '~~'

        return f'{self.hostA.host_id} {start}{connection_type}{end} {self.hostB.host_id}'