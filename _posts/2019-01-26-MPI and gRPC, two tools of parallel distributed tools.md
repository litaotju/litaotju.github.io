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

## Resources
gRPC C++ quick start:
[https://grpc.io/docs/quickstart/cpp.html#whats-next](https://grpc.io/docs/quickstart/cpp.html#whats-next)
[ihttps://github.com/grpc/grpc](https://github.com/grpc/grpc)

## What's RPC/gRPC

RPC is for remote process call, means you can all a remote function like it's running in local process.
Normally it has RPC server and RPC clients, the RPC server provides functions as a service to the clients,
and clients can call the function into server by RPC protocol. 
The RPC server and RPC clients are just processes, they can run on same machine and also on different machine.
gRPC is a very popular RPC implementaion, which has many language bindings.

### Compare gRPC/MPI

* Compared with MPI, the RPC is relatively high level APIs.
    In MPIs, messges need to convert to POD (plain old data) before sending it, and the receriver also only receives POD data.
    So if you need to send some high level langunage abstract objects like C++ Objects, you need to convert it to POD data firstly.

    But in gRPC, the requests and response (messages) are defined by proto buffers, the gRPC infratructure take care of serialization and deserialzation of the messages,   the user(client/server) can use high level accessors and setters, as the abstract object.

* gRPC has server/client structure, which normally has a clearly defination. And a server may be called by many clients. But MPI parallel do not have a normally pattern of different processes, you can custom the collective pattern of different processes as your need.  MPI is a set of tightly coupled processes to achive a computing goal together, user need to define the compute goals and collective pattern clearly when desiging MPI program.   But gRPC can be not that tightly coupled, the clients may have very different shape/purpose, which the server do not need to consider

* MPI programm is differet instance processes of same program code, the `mpirun` is responsible to invoke and manage the processes on machines. But the gRPC server and client normally do not need same code, the just share the minial part of stub code/protocal code generated by gRPC tools. The server and client can be developed seperately, the client only needs like some headers to use the service.

* MPI program runs on a set of very similar computers, which should share some envs, like comman storage, common user login info, the cluster normally connected by high bandwidth LAN. But the gRPC prosseses can run on very different machines, the do not need to share same envs, as MPI does, the gRPC may run on data center server, and the client may run on edge devices, like user's desktop/laptop or mobile phones. The server is unlikely to know the platform where the clients runs, and it does not care. So MPI is normally only used on HPC clusters, and but the gRPC can used to provide severices over internet.

* gRPC is based on HTTP/2 protocal.

* Normally we use C/C++/Fortan for MPI, but gRPC has many popular language, like Jave/Python/Php/JS...

* MPI is more on parallel computing, gRPC is more service/client structure.

# Reference and further reading
> [http://mpitutorial.com/tutorials/mpi-introduction/](http://mpitutorial.com/tutorials/mpi-introduction/)  
> [How Can MPI Fit Into Today's Big Computing](https://ljdursi.github.io/EuroMPI2016/#1)  
> [HPC is dying, and MPI is killing it](https://www.dursi.ca/post/hpc-is-dying-and-mpi-is-killing-it.html)