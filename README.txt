0. Chase O'Donnell- cco49 ////Sieg Alejandro-ska89

1. We implemented a sequential querey in order to find out which TS reponded to our client query. Our program uses the socket class
and it's settimeout() function in order to implement the timeout. Because it's sequential, it is easy to determine which ts responded

2. There are no known issues with the attached code

3. One problem we encountered was finding out the best way to implement the timeout and whether or not we wanted the 5 second delay to occur on the TS or not.
We ended up deciding that we wouldn't force a 5 second wait() but instead just not response or do anything at all and the ls will have a timeeout instead. 


4. We gained a comprehensive understanding of how Load-Balancing DNS is able to reduce the server load by distributing the records among different top level servers. The parallelism speeds up the process and the timeout avoids the TS needing to clog the network by sending back an NS.


