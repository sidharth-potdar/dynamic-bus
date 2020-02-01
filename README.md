# CX4230

## Structure 

Have one process (Engine) that is constantly running and executing events, and managing the queue. Have a second 
process (Simulation) that generates events from distributions and sends them to the Engine. We can send them over in batch. 

Maybe another process for long-running event logic 

shared dictionary, simulation process can monitor shared dict to generate more events 

