    Efficient Processing:

        Uses a deque for the buffer with O(1) append/pop operations

        Maintains a running weighted sum to avoid recalculating from scratch each time

    Correct Weight Application:

        The current input x always gets weight w[0]

        Previous values shift to use weights w[1], w[2], etc.

    Handles Initial Buffer:

        Initializes buffer with zeros

        Correctly processes values even before buffer is full

    Comprehensive Testing:

        Tests the exact example from the problem

        Tests with all weights = 1 (moving average filter)

        Tests with a sine wave as suggested

        Tests custom scenarios

    Algorithm Details:

        When a new value arrives, it removes the contribution of the oldest value

        Shifts the weights for all intermediate values

        Adds the contribution of the new value with weight w[0]

        Updates the buffer with the new value at position 0

The implementation correctly handles the requirement that "index 0 in x is the current entry" by always placing new values at position 0 in the buffer and shifting older values to the right.
