class Direction:
    """
    Enumeration for the direction of the connection.
    """
    UNIDIRECTIONAL_A_B = 1   # A --> B
    UNIDIRECTIONAL_B_A = 2   # A <-- B
    BIDIRECTIONAL = 3        # A <-> B

    @staticmethod
    def get_direction(string):
        """
        Get the direction from the string.

        Args:
            string (str): The string representing the connection.

        Returns:
            Direction: The direction.
        """
        start = string[0] == '<'
        end = string[-1] == '>'

        if not (start ^ end):
            return Direction.BIDIRECTIONAL
        elif start:
            return Direction.UNIDIRECTIONAL_B_A
        else:
            return Direction.UNIDIRECTIONAL_A_B
