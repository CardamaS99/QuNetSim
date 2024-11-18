from qunetsim.components import Host


class ConnType:
    """
    Enumeration for the connection types.
    """
    CLASSICAL_AND_QUANTUM = 1
    CLASSICAL = 2
    QUANTUM = 3

    """
    Function to add the connection between the hosts, depending on the connection type.
    """
    add_connection_function = {
        CLASSICAL_AND_QUANTUM: Host.add_connection,
        CLASSICAL: Host.add_c_connection,
        QUANTUM: Host.add_q_connection
    }

    @staticmethod
    def get_conn_type(string):
        """
        Get the connection type from the string.

        Args:
            string (str): The string representing the connection type.

        Returns:
            ConnType: The connection type.
        """
        if string == '==':
            return ConnType.CLASSICAL_AND_QUANTUM
        elif string == '--':
            return ConnType.CLASSICAL
        elif string == '~~':
            return ConnType.QUANTUM
