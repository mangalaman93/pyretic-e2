Pyretic-e2
==========

E2 framework implementation using pyretic

### Installation
Make sure you are using `python2` (not `python3`). Install dependencies as follows -
```
sudo apt-get install python-dev python-pip python-netaddr screen hping3 ml-lpt graphviz ruby1.9.1-dev libboost-dev libboost-test-dev libboost-program-options-dev libevent-dev automake libtool flex bison pkg-config g++ libssl-dev python-all python-all-dev python-all-dbg
sudo pip install networkx bitarray netaddr ipaddr pytest ipdb sphinx pyparsing==1.5.7 yappi
```

Install following for generating http traffic -
```
apt-get install nmap
```

### How to Run (examples)
```
python pyretic.py pyretic.e2-examples.pipelet_test
```

### TODO
* Update README

### References
* [networkx tutorial](https://networkx.github.io/documentation/latest/tutorial/tutorial.html)
* [Install pyretic VM](https://github.com/frenetic-lang/pyretic/wiki/Building-the-Pyretic-VM)
* [Running pyretic](https://github.com/frenetic-lang/pyretic/wiki/running-pyretic)
* [Mininet](https://github.com/mininet/mininet/wiki/Introduction-to-Mininet)
