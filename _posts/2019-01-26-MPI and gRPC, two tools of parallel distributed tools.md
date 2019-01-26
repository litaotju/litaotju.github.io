---
layout: post
title: MPI and gRPC, two tools of parallel distributed tools
description: 
category: 
tags: 
---
{% include JB/setup %}


# MPI

MPI is short for Message Passing Interface, widely adoption at HPC for parallel computing.
But it's relatively low level APIs.
Here is an example of MPI tutorial website, http://mpitutorial.com/tutorials/mpi-introduction/

You can install open-mpi development enviroment by 
```bash
sudo apt install libopenmpi-dev
```

## MPI Hello World
This example shows an basic examples of how to write/compile/run the helloworld mpi example, which do not use any message sending/receving between processes.


### Code
```c++
#include "mpi.h"
#include <cstdio>

int main(int argc, char ** argv)
{
    MPI_Init(&argc, &argv);

    int world_size;
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);
    

    int world_rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

    char processor_name[MPI_MAX_PROCESSOR_NAME];
    int name_len;
    MPI_Get_processor_name(processor_name, &name_len);

    printf("Hello world from processor %s, rank %d of %d processors\n",
            processor_name, world_rank, world_size);

    MPI_Finalize();
}
```

### Compile
After saving the above code as helloworld.cpp, you could compile it with the mpi compiler by following line:
```bash
mpic++ helleworld.cpp -o helloworld.exe
```

### Run on single machine
After compiled the mpi code as helloworld.exe, you could invoke the program by mpirun command, and specify the any nummber of processes to run the command.
```bash
mpirun -n 4 ./helloworld.exe
```
The `-n 4` option is to specify the number of parallel process to 4. You could change it to `-n 20` if you need 20 process to run it.
After running with 4 process, the output will be like the following:
```
Hello world from processor deep, rank 0 of 4 processors
Hello world from processor deep, rank 3 of 4 processors
Hello world from processor deep, rank 1 of 4 processors
Hello world from processor deep, rank 2 of 4 processors
```
When you run a second time, most likely the output will change, because there is no gurantee of the order/speed of the processes.

```
Hello world from processor deep, rank 1 of 4 processors
Hello world from processor deep, rank 3 of 4 processors
Hello world from processor deep, rank 0 of 4 processors
Hello world from processor deep, rank 2 of 4 processors
```

### Run on an MPI clusters.
To run the MPI process of different computers (clusters), first you need to configure the clusters.
The main point of configuring the clusters varies based on your system, but the main point is to share some user login so `mpirun` can login to other worker machine from the master machine which your command is issued, and also to share same storage env, so after the `mpirun` login to remote worker machine, it could find the **binaries and lib** and other dependency it needs. From this helloworld program view, it does not load any data from file system, the share filesystem setup is only to share the helloworld.exe on remote machine. You could also manually copy the programm to remote host, but it's not convient.

[Here](http://mpitutorial.com/tutorials/running-an-mpi-cluster-within-a-lan/) You can find a tutorial of set up MPI clusters over LAN 

After you configure the clusters on serveral host/nodes, you could run the MPI helloworld as follows depends on your needs
```
# Run 10 process on `master` node
mpirun -n 10  --hosts master ./helloworld.exe

# Run totally 10 process on `master, host1, host2` nodes
mpirun -n 10 --hosts master,host1,host2 ./helloworld.exe

##One thing to notice is that, you always need to add the `master` node(your currently login machine, where you issue the command) to the host lists
## The following command will failed if you only use a remote machine 
mpirun -n 10 --hosts host1 ./helloworld.exe

```

You could also saved the host list and the number of procssor it has in a file, and then use the `-f` option of `mpirun` to specify the hosts.
Like followng hostfile

```
>>> cat host_file
cetus1:2
cetus2:2
cetus3:2
cetus4:2
```
To run with the above nodes:
```
mpirun -n 8 -f hostfile ./hello_world.exe
```

## MPI send/receving example
http://mpitutorial.com/tutorials/mpi-send-and-receive/

# gRPC



# Reference
> http://mpitutorial.com/tutorials/mpi-introduction/
>