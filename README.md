# ProjectManagement
This program searches for the critical path for a project with a given number of work required.

The configuration of the program, the available jobs and their parameters are set in the "Configuration" file in the format:
<Job ID> - <duration>: <not earlier than> <...> <...> -> <not later than> <...> <...>

Job ID -- Free name, user selectable;
duration -- duration of work.
Dependencies "not earlier than" and "not later than" are specified by work numbers separated by spaces without punctuation marks.
