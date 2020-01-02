Use cases
=========

Now, imagine if from your PC at your work, or when you go to support one of your customers, in a couple of minutes
you can perform all of the following basics out of the box procedures, they will see you as a hero!

You could even redirect the logging of several network devices to your PC while you are working in order to see them
with a syslog server on your PC, or only with the Salt event-bus, and after the jobs is done, revert the syslog
change in seconds.

All this examples are running against a GNS3 virtual lab in my PC, you can do the same with the VM or installing it
following the install guides. I am only running legacy IOS but they support others OS via NAPALM, and of course, regular
server operating system.

Some tips before we start:

**netor scripts**

In time i will create *netor*-x style script just as a mask of the following commands, and again, ir order to try to
make it easier to start using Ansible ans Salt. And i will had a simple command to update the /bin folder.


**Ansible:**

* I am providing a couple of playbook, some parses, and scripts for you to experiment.
* You might see some warning related to Python2 getting to end of support, and some other pieces of code about to get deprecated. Typical linux style, letting you know about thing that are about to change.
* you con limit the devices to execute a playbook by adding ``-l xxx``. Where xxx is regEx filter.
* you can add ``--check --diff`` to check commands before applying and to show the differences to apply.
* you can send information from the playbook to a parser to crop information and/or to script to do something else, this means that there is communication between to move information and act accordingly.
* ``ansible-playbook`` is the command to execute playbooks, you have to cd to the playbooks directory
* Ansible is kind of static, because it only do something when you enter a command. If you want to trigger actions you have to use an external tool, like Nagios. If Nagios detects something execute this Ansible playbook.

**Salt:**

* what it super cool about Salt is the even if the commands are weird at the beginning, all of the modules/functions have a help right at the command line, i will show you how.
* ``salt`` is for execution online commands against the devices
* ``salt-run`` is for executing commands with information that Salt already
* to every command you can add at the end ``-l debug`` to check what is going on.
* it has incredible ``net.bgp`` module to check for information, to configure and potentially react.
* Salt has a cache database with information gathered by runners, the cool thing about this is that you don't need to install and maintain a separate DB to store information like regular network management software requires.
* Salt has an event bus, which you can see with ``salt-run state.event pretty=True``, the amazing thing about this is that you can start thinking in **Orchestration**, or in other words, define a reactor to an event when some message gets to the event bus. You can even attach a chat bot.


Ansible examples
****************

From easy to hard

**Make a backup**

::

    *adrian@adrian-VirtualBox:~/netor/netor/ansible/playbooks$ ansible-playbook backup.yml -l c1*

    PLAY [Backup devices configs] *************************************************************************************************

    TASK [Read IOS configs] *******************************************************************************************************

    ok: [c1_s1_cpe]

    ok: [c1_s1_co-1]

    ok: [c1_s1_ua-1]

    TASK [Save IOS config] ********************************************************************************************************
    changed: [c1_s1_cpe]
    changed: [c1_s1_ua-1]
    changed: [c1_s1_co-1]

    PLAY RECAP ********************************************************************************************************************
    c1_s1_co-1                 : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
    c1_s1_cpe                  : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
    c1_s1_ua-1                 : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

    adrian@adrian-VirtualBox:~/netor/netor/ansible/playbooks$ ls -la ../backup/
    total 160
    drwxr-xr-x 2 adrian adrian 4096 Nov 15 22:49 .
    drwxr-xr-x 6 adrian adrian 4096 Nov 15 22:47 ..
    -rw-rw-r-- 1 adrian adrian 3428 Nov 15 22:49 show_run_c1_s1_co-1.txt
    -rw-rw-r-- 1 adrian adrian 2262 Nov 15 22:49 show_run_c1_s1_cpe.txt
    -rw-rw-r-- 1 adrian adrian 3082 Nov 15 22:49 show_run_c1_s1_ua-1.txt
    adrian@adrian-VirtualBox:~/netor/netor/ansible/playbooks$


**show arp tables**

::

    adrian@adrian-VirtualBox:~/netor/netor/ansible/playbooks$ ansible-playbook show-arp.yml -l c1_s1_cpe

    PLAY [Show IP ARP] ************************************************************************************************************

    TASK [Show IP ARP] ************************************************************************************************************

    ok: [c1_s1_cpe]

    TASK [debug] ******************************************************************************************************************
    ok: [c1_s1_cpe] => {
        "list_of_ip_arp.stdout_lines": [
            [
                "Protocol  Address          Age (min)  Hardware Addr   Type   Interface",
                "Internet  10.0.12.1              68   c201.375c.0001  ARPA   FastEthernet0/0",
                "Internet  10.0.12.2               -   c202.5d80.0000  ARPA   FastEthernet0/0",
                "Internet  10.100.12.1             -   c202.5d80.0001  ARPA   FastEthernet0/1",
                "Internet  10.100.12.2            68   c204.5f8c.0000  ARPA   FastEthernet0/1"
            ]
        ]
    }

    PLAY RECAP ********************************************************************************************************************
    c1_s1_cpe                  : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0


**gather-facts, which is the device basic information**

::

    adrian@adrian-VirtualBox:~/netor/netor/ansible/playbooks$ ansible-playbook gather-facts.yml -l c1_s1_cpe

    PLAY [Gather IOS facts] *******************************************************************************************************

    TASK [gather all facts] *******************************************************************************************************

    ok: [c1_s1_cpe]

    TASK [Display the OS version] *************************************************************************************************
    ok: [c1_s1_cpe] => {
        "msg": "The hostname is r2 and the OS is 12.4(15)T13"
    }

    TASK [Display config] *********************************************************************************************************
    ok: [c1_s1_cpe] => {
        "msg": {
            "ansible_facts": {
                "ansible_net_api": "cliconf",
                "ansible_net_config": "!\nversion 12.4\nno service pad\nservice tcp-keepalives-in\nservice tcp-keepalives-out\nservice timestamps debug datetime msec localtime show-timezone\nservice timestamps log datetime msec localtime show-timezone\nservice password-encryption\n!\nhostname r2\n!\nboot-start-marker\nboot-end-marker\n!\nlogging buffered 32000\nno logging console\nenable secret 5 $1$QAh2$FiUShFDsaikloAgWmKsW1.\n!\naaa new-model\n!\n!\naaa authentication login default local-case\naaa authorization exec default local \n!\n!\naaa session-id common\nmemory-size iomem 5\nno ip source-route\nip options drop\nip cef\n!\n!\nip dhcp bootp ignore\n!\n!\nno ip domain lookup\nip domain name quadrant.edu\n!\nmultilink bundle-name authenticated\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\nfile prompt quiet\nusername cisco privilege 15 secret 5 $1$OKM5$WoIzwQQ6Xrlt3ymrIH8VE/\narchive\n log config\n  hidekeys\n! \n!\n!\n!\nip ssh version 2\nip scp server enable\n!\n!\n!\n!\ninterface FastEthernet0/0\n description to_r1\n ip address 10.0.12.2 255.255.255.0\n no ip redirects\n no ip proxy-arp\n duplex auto\n speed auto\n!\ninterface FastEthernet0/1\n description to_inside\n ip address 10.100.12.1 255.255.255.0\n no ip redirects\n no ip proxy-arp\n duplex auto\n speed auto\n!\ninterface FastEthernet1/0\n no ip address\n shutdown\n duplex auto\n speed auto\n!\nrouter eigrp 1\n network 10.0.0.0\n no auto-summary\n!\nip forward-protocol nd\nip route 0.0.0.0 0.0.0.0 10.0.12.1\n!\n!\nno ip http server\nno ip http secure-server\n!\nip sla 1\n udp-echo 10.0.12.1 999\n timeout 4000\n tag probe1_test2\n frequency 5\n history lives-kept 1\n history buckets-kept 3\n history filter all\nip sla 2\n icmp-echo 10.0.12.1\n tag probe1_test1\n history lives-kept 1\n history filter all\nsnmp-server community snmpCommunity RW\nsnmp-server community read_only RO\nsnmp-server community read_write RW\n!\n!\n!\n!\n!\n!\ncontrol-plane\n!\n!\n!\n!\n!\n!\n!\n!\n!\nbanner login ^C\n\nUnauthorized access is prohibited!\n\n^C\n!\nline con 0\n exec-timeout 20 0\n logging synchronous\nline aux 0\n exec-timeout 0 1\n no exec\n transport output none\nline vty 0 4\n exec-timeout 20 0\n logging synchronous\n transport input ssh\n transport output ssh\nline vty 5 15\n exec-timeout 20 0\n logging synchronous\n transport input ssh\n transport output ssh\n!\nntp server 10.0.0.2\n!\nend",
                "ansible_net_gather_network_resources": [],
                "ansible_net_gather_subset": [
                    "default",
                    "config"
                ],
                "ansible_net_hostname": "r2",
                "ansible_net_image": "tftp://255.255.255.255/unknown",
                "ansible_net_iostype": "IOS",
                "ansible_net_model": "3725",
                "ansible_net_python_version": "2.7.15+",
                "ansible_net_serialnum": "FTX0945W0MY",
                "ansible_net_system": "ios",
                "ansible_net_version": "12.4(15)T13",
                "ansible_network_resources": {},
                "discovered_interpreter_python": "/usr/bin/python"
            },
            "changed": false,
            "failed": false,
            "warnings": [
                "default value for \`gather_subset` will be changed to \`min` from \`!config` v2.11 onwards",
                "Platform linux on host c1_s1_cpe is using the discovered Python interpreter at /usr/bin/python, but future installation of another Python interpreter could change this. See https://docs.ansible.com/ansible/2.9/reference_appendices/interpreter_discovery.html for more information."
            ]
        }
    }

    PLAY RECAP ********************************************************************************************************************
    c1_s1_cpe                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0


**add a regular show command at 'cmd='**

::

    adrian@adrian-VirtualBox:~/netor/netor/ansible/playbooks$ ansible-playbook ios-show-cmd.yml -e cmd="'run | inc snmp'" -l c1_s1

    PLAY [IOS show cmd] ***********************************************************************************************************

    TASK [IOS show cmd] ***********************************************************************************************************

    ok: [c1_s1_cpe]

    ok: [c1_s1_co-1]

    ok: [c1_s1_ua-1]

    TASK [debug] ******************************************************************************************************************
    ok: [c1_s1_co-1] => {
        "output.stdout_lines": [
            [
                "snmp-server community snmpCommunity RW"
            ]
        ]
    }
    ok: [c1_s1_ua-1] => {
        "output.stdout_lines": [
            [
                "snmp-server community snmpCommunity RW"
            ]
        ]
    }
    ok: [c1_s1_cpe] => {
        "output.stdout_lines": [
            [
                "snmp-server community snmpCommunity RW",
                "snmp-server community read_only RO",
                "snmp-server community read_write RW"
            ]
        ]
    }

    PLAY RECAP ********************************************************************************************************************
    c1_s1_co-1                 : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
    c1_s1_cpe                  : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
    c1_s1_ua-1                 : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0


::

    adrian@adrian-VirtualBox:~/netor/netor/ansible/playbooks$ ansible-playbook ios-show-cmd.yml -e "cmd='ip int bri'" -l c1_s1

    PLAY [IOS show cmd] ***********************************************************************************************************

    TASK [IOS show cmd] ***********************************************************************************************************

    ok: [c1_s1_cpe]

    ok: [c1_s1_co-1]

    ok: [c1_s1_ua-1]

    TASK [debug] ******************************************************************************************************************
    ok: [c1_s1_cpe] => {
        "output.stdout_lines": [
            [
                "Interface                  IP-Address      OK? Method Status                Protocol",
                "FastEthernet0/0            10.0.12.2       YES NVRAM  up                    up      ",
                "FastEthernet0/1            10.100.12.1     YES NVRAM  up                    up      ",
                "FastEthernet1/0            unassigned      YES NVRAM  administratively down down"
            ]
        ]
    }
    ok: [c1_s1_co-1] => {
        "output.stdout_lines": [
            [
                "Interface                  IP-Address      OK? Method Status                Protocol",
                "FastEthernet0/0            10.100.12.2     YES NVRAM  up                    up      ",
                "FastEthernet0/1            unassigned      YES unset  administratively down down    ",
                "FastEthernet1/0            unassigned      YES unset  up                    up      ",
                "FastEthernet1/1            unassigned      YES unset  up                    down    ",
                "FastEthernet1/2            unassigned      YES unset  up                    down    ",
                "FastEthernet1/3            unassigned      YES unset  up                    down    ",
                "FastEthernet1/4            unassigned      YES unset  up                    down    ",
                "FastEthernet1/5            unassigned      YES unset  up                    down    ",
                "FastEthernet1/6            unassigned      YES unset  up                    down    ",
                "FastEthernet1/7            unassigned      YES unset  up                    down    ",
                "FastEthernet1/8            unassigned      YES unset  up                    down    ",
                "FastEthernet1/9            unassigned      YES unset  up                    down    ",
                "FastEthernet1/10           unassigned      YES unset  up                    down    ",
                "FastEthernet1/11           unassigned      YES unset  up                    down    ",
                "FastEthernet1/12           unassigned      YES unset  up                    down    ",
                "FastEthernet1/13           unassigned      YES unset  up                    down    ",
                "FastEthernet1/14           unassigned      YES unset  up                    down    ",
                "FastEthernet1/15           unassigned      YES unset  up                    down    ",
                "Vlan1                      unassigned      YES NVRAM  administratively down down    ",
                "Vlan10                     10.100.200.1    YES NVRAM  up                    up"
            ]
        ]
    }
    ok: [c1_s1_ua-1] => {
        "output.stdout_lines": [
            [
                "Interface                  IP-Address      OK? Method Status                Protocol",
                "FastEthernet0/0            unassigned      YES NVRAM  administratively down down    ",
                "FastEthernet0/1            unassigned      YES NVRAM  administratively down down    ",
                "FastEthernet1/0            unassigned      YES unset  up                    up      ",
                "FastEthernet1/1            unassigned      YES unset  up                    up      ",
                "FastEthernet1/2            unassigned      YES unset  up                    up      ",
                "FastEthernet1/3            unassigned      YES unset  up                    down    ",
                "FastEthernet1/4            unassigned      YES unset  up                    down    ",
                "FastEthernet1/5            unassigned      YES unset  up                    down    ",
                "FastEthernet1/6            unassigned      YES unset  up                    down    ",
                "FastEthernet1/7            unassigned      YES unset  up                    down    ",
                "FastEthernet1/8            unassigned      YES unset  up                    down    ",
                "FastEthernet1/9            unassigned      YES unset  up                    down    ",
                "FastEthernet1/10           unassigned      YES unset  up                    down    ",
                "FastEthernet1/11           unassigned      YES unset  up                    down    ",
                "FastEthernet1/12           unassigned      YES unset  up                    down    ",
                "FastEthernet1/13           unassigned      YES unset  up                    down    ",
                "FastEthernet1/14           unassigned      YES unset  up                    down    ",
                "FastEthernet1/15           unassigned      YES unset  up                    down    ",
                "Vlan1                      unassigned      YES NVRAM  administratively down down    ",
                "Vlan10                     10.100.200.2    YES NVRAM  up                    up"
            ]
        ]
    }

    PLAY RECAP ********************************************************************************************************************
    c1_s1_co-1                 : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
    c1_s1_cpe                  : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
    c1_s1_ua-1                 : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0


::

    adrian@adrian-VirtualBox:~/netor/netor/ansible/playbooks$ ansible-playbook ios-show-cmd.yml -e "cmd='ip arp'" -l c1_s1

    PLAY [IOS show cmd] ***********************************************************************************************************

    TASK [IOS show cmd] ***********************************************************************************************************

    ok: [c1_s1_cpe]

    ok: [c1_s1_co-1]

    TASK [debug] ******************************************************************************************************************
    ok: [c1_s1_co-1] => {
        "output.stdout_lines": [
            [
                "Protocol  Address          Age (min)  Hardware Addr   Type   Interface",
                "Internet  10.100.12.1            75   c202.5d80.0001  ARPA   FastEthernet0/0",
                "Internet  10.100.12.2             -   c204.5f8c.0000  ARPA   FastEthernet0/0",
                "Internet  10.100.200.1            -   c204.5f8c.0000  ARPA   Vlan10",
                "Internet  10.100.200.2           75   c206.1b68.0000  ARPA   Vlan10"
            ]
        ]
    }
    ok: [c1_s1_cpe] => {
        "output.stdout_lines": [
            [
                "Protocol  Address          Age (min)  Hardware Addr   Type   Interface",
                "Internet  10.0.12.1              75   c201.375c.0001  ARPA   FastEthernet0/0",
                "Internet  10.0.12.2               -   c202.5d80.0000  ARPA   FastEthernet0/0",
                "Internet  10.100.12.1             -   c202.5d80.0001  ARPA   FastEthernet0/1",
                "Internet  10.100.12.2            75   c204.5f8c.0000  ARPA   FastEthernet0/1"
            ]
        ]
    }

    PLAY RECAP ********************************************************************************************************************
    c1_s1_co-1                 : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
    c1_s1_cpe                  : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0


**show interfaces**

This playbook is using the ansible network engine role and/with a parser, which means that the standard output is
being send to an external script to crop that output and give back the results to Ansible to show it.

You can still get the same info in a simpler way, the interesting part here is to show the power of roles, parses, and
scripts, in order to process the regular output.

::

    adrian@adrian-VirtualBox:~/netor/netor/ansible/playbooks$ ansible-playbook ne-showintf.yml -l c1_s1

    PLAY [GENERATE A REPORT] ******************************************************************************************************

    TASK [CAPTURE SHOW IP INTERFACE] **********************************************************************************************

    ok: [c1_s1_cpe]

    ok: [c1_s1_co-1]

    TASK [PARSE THE RAW OUTPUT] ***************************************************************************************************

    ok: [c1_s1_cpe]
    ok: [c1_s1_co-1]

    TASK [Display the data] *******************************************************************************************************
    ok: [c1_s1_cpe] => {
        "interface_facts": {
            "FastEthernet0/0": {
                "config": {
                    "description": "to_r1",
                    "mtu": "1500",
                    "name": "FastEthernet0/0",
                    "type": null
                }
            },
            "FastEthernet0/1": {
                "config": {
                    "description": "to_inside",
                    "mtu": "1500",
                    "name": "FastEthernet0/1",
                    "type": "AmdFE"
                }
            }
        }
    }
    ok: [c1_s1_co-1] => {
        "interface_facts": {
            "FastEthernet0/0": {
                "config": {
                    "description": "to_inet",
                    "mtu": "1500",
                    "name": "FastEthernet0/0",
                    "type": null
                }
            },
            "FastEthernet1/0": {
                "config": {
                    "description": null,
                    "mtu": "1500",
                    "name": "FastEthernet1/0",
                    "type": null
                }
            },
            "FastEthernet1/1": {
                "config": {
                    "description": null,
                    "mtu": "1500",
                    "name": "FastEthernet1/1",
                    "type": null
                }
            },
            "FastEthernet1/10": {
                "config": {
                    "description": null,
                    "mtu": "1500",
                    "name": "FastEthernet1/10",
                    "type": null
                }
            },
            "FastEthernet1/11": {
                "config": {
                    "description": null,
                    "mtu": "1500",
                    "name": "FastEthernet1/11",
                    "type": null
                }
            },
            "FastEthernet1/12": {
                "config": {
                    "description": null,
                    "mtu": "1500",
                    "name": "FastEthernet1/12",
                    "type": null
                }
            },
            "FastEthernet1/13": {
                "config": {
                    "description": null,
                    "mtu": "1500",
                    "name": "FastEthernet1/13",
                    "type": null
                }
            },
            "FastEthernet1/14": {
                "config": {
                    "description": null,
                    "mtu": "1500",
                    "name": "FastEthernet1/14",
                    "type": null
                }
            },
            "FastEthernet1/15": {
                "config": {
                    "description": null,
                    "mtu": "1500",
                    "name": "FastEthernet1/15",
                    "type": "EtherSVI"
                }
            },
            "FastEthernet1/2": {
                "config": {
                    "description": null,
                    "mtu": "1500",
                    "name": "FastEthernet1/2",
                    "type": null
                }
            },
            "FastEthernet1/3": {
                "config": {
                    "description": null,
                    "mtu": "1500",
                    "name": "FastEthernet1/3",
                    "type": null
                }
            },
            "FastEthernet1/4": {
                "config": {
                    "description": null,
                    "mtu": "1500",
                    "name": "FastEthernet1/4",
                    "type": null
                }
            },
            "FastEthernet1/5": {
                "config": {
                    "description": null,
                    "mtu": "1500",
                    "name": "FastEthernet1/5",
                    "type": null
                }
            },
            "FastEthernet1/6": {
                "config": {
                    "description": null,
                    "mtu": "1500",
                    "name": "FastEthernet1/6",
                    "type": null
                }
            },
            "FastEthernet1/7": {
                "config": {
                    "description": null,
                    "mtu": "1500",
                    "name": "FastEthernet1/7",
                    "type": null
                }
            },
            "FastEthernet1/8": {
                "config": {
                    "description": null,
                    "mtu": "1500",
                    "name": "FastEthernet1/8",
                    "type": null
                }
            },
            "FastEthernet1/9": {
                "config": {
                    "description": null,
                    "mtu": "1500",
                    "name": "FastEthernet1/9",
                    "type": null
                }
            },
            "Vlan10": {
                "config": {
                    "description": "LAN",
                    "mtu": "1500",
                    "name": "Vlan10",
                    "type": "EtherSVI"
                }
            }
        }
    }

    PLAY RECAP ********************************************************************************************************************
    c1_s1_co-1                 : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
    c1_s1_cpe                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0


** Another example of parsers to show ip interface brief**

::

    adrian@adrian-VirtualBox:~/netor/netor/ansible/playbooks$ ansible-playbook ne-showipintf.yml -l c1_s1

    PLAY [GENERATE A REPORT] ******************************************************************************************************

    TASK [CAPTURE SHOW IP INTERFACE] **********************************************************************************************

    ok: [c1_s1_cpe]

    ok: [c1_s1_co-1]


    TASK [PARSE THE RAW OUTPUT] ***************************************************************************************************

    ok: [c1_s1_co-1]
    ok: [c1_s1_ua-1]
    ok: [c1_s1_cpe]

    TASK [DISPLAY THE DATA] *******************************************************************************************************
    ok: [c1_s1_cpe] => {
        "ip_interface_facts": [
            {
                "FastEthernet0/0": {
                    "data": {
                        "admin_state": "up",
                        "ip": "10.0.12.2",
                        "name": "FastEthernet0/0",
                        "protocol_state": "up"
                    }
                }
            },
            {
                "FastEthernet0/1": {
                    "data": {
                        "admin_state": "up",
                        "ip": "10.100.12.1",
                        "name": "FastEthernet0/1",
                        "protocol_state": "up"
                    }
                }
            }
        ]
    }
    ok: [c1_s1_co-1] => {
        "ip_interface_facts": [
            {
                "FastEthernet0/0": {
                    "data": {
                        "admin_state": "up",
                        "ip": "10.100.12.2",
                        "name": "FastEthernet0/0",
                        "protocol_state": "up"
                    }
                }
            },
            {
                "Vlan10": {
                    "data": {
                        "admin_state": "up",
                        "ip": "10.100.200.1",
                        "name": "Vlan10",
                        "protocol_state": "up"
                    }
                }
            }
        ]
    }

    PLAY RECAP ********************************************************************************************************************
    c1_s1_co-1                 : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
    c1_s1_cpe                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0


**this example send the output to a python script which proceses the data and returns a dictornary to Ansible in order
to format the output**

::

    adrian@adrian-VirtualBox:~/netor/netor/ansible/playbooks$ ansible-playbook ne-show-ver.yml -l c1_s1

    PLAY [Show Cisco HW, SN, and SW version] **************************************************************************************

    TASK [Show version] ***********************************************************************************************************

    ok: [c1_s1_cpe]

    ok: [c1_s1_co-1]

    ok: [c1_s1_ua-1]

    TASK [PARSE THE RAW OUTPUT] ***************************************************************************************************

    ok: [c1_s1_ua-1]
    ok: [c1_s1_co-1]
    ok: [c1_s1_cpe]

    TASK [execute python script] **************************************************************************************************
    changed: [c1_s1_co-1 -> localhost]
    changed: [c1_s1_ua-1 -> localhost]
    changed: [c1_s1_cpe -> localhost]

    TASK [debug] ******************************************************************************************************************
    ok: [c1_s1_co-1] => {
        "output.stdout_lines": [
            "Hostname: c1_s1_co-1",
            "Serial_Number: FTX0945W0MY",
            "Software_Release: fc3",
            "Hardware_Version: 3725",
            "Software_Version: 12.4(15)T13",
            "Software_Image: C3725-ADVENTERPRISEK9-M"
        ]
    }
    ok: [c1_s1_cpe] => {
        "output.stdout_lines": [
            "Hostname: c1_s1_cpe",
            "Serial_Number: FTX0945W0MY",
            "Software_Release: fc3",
            "Hardware_Version: 3725",
            "Software_Version: 12.4(15)T13",
            "Software_Image: C3725-ADVENTERPRISEK9-M"
        ]
    }
    ok: [c1_s1_ua-1] => {
        "output.stdout_lines": [
            "Hostname: c1_s1_ua-1",
            "Serial_Number: FTX0945W0MY",
            "Software_Release: fc3",
            "Hardware_Version: 3725",
            "Software_Version: 12.4(15)T13",
            "Software_Image: C3725-ADVENTERPRISEK9-M"
        ]
    }

    PLAY RECAP ********************************************************************************************************************
    c1_s1_co-1                 : ok=4    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
    c1_s1_cpe                  : ok=4    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
    c1_s1_ua-1                 : ok=4    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0


**example on how to set up snmp**

In this case, the configuration was applied to two devices, because the 3rd one already had it. Look for the word "changed"

::

    adrian@adrian-VirtualBox:~/netor/netor/ansible/playbooks$ ansible-playbook set-snmp.yml -l c1_s1

    PLAY [Set SNMP] ***************************************************************************************************************

    TASK [Configure SNMP comminities on devices] **********************************************************************************

    ok: [c1_s1_cpe]

    changed: [c1_s1_co-1]

    changed: [c1_s1_ua-1]

    PLAY RECAP ********************************************************************************************************************
    c1_s1_co-1                 : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
    c1_s1_cpe                  : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
    c1_s1_ua-1                 : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

    adrian@adrian-VirtualBox:~/netor/netor/ansible/playbooks$ ansible-playbook ios-show-cmd.yml -e "cmd='run | inc snmp'" -l c1_s1

    PLAY [IOS show cmd] ***********************************************************************************************************

    TASK [IOS show cmd] ***********************************************************************************************************

    ok: [c1_s1_cpe]

    ok: [c1_s1_co-1]

    ok: [c1_s1_ua-1]

    TASK [debug] ******************************************************************************************************************
    ok: [c1_s1_cpe] => {
        "output.stdout_lines": [
            [
                "snmp-server community snmpCommunity RW",
                "snmp-server community read_only RO",
                "snmp-server community read_write RW"
            ]
        ]
    }
    ok: [c1_s1_co-1] => {
        "output.stdout_lines": [
            [
                "snmp-server community snmpCommunity RW",
                "snmp-server community read_only RO",
                "snmp-server community read_write RW"
            ]
        ]
    }
    ok: [c1_s1_ua-1] => {
        "output.stdout_lines": [
            [
                "snmp-server community snmpCommunity RW",
                "snmp-server community read_only RO",
                "snmp-server community read_write RW"
            ]
        ]
    }

    PLAY RECAP ********************************************************************************************************************
    c1_s1_co-1                 : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
    c1_s1_cpe                  : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
    c1_s1_ua-1                 : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0


**another case of show arp**

::

    adrian@adrian-VirtualBox:~/netor/netor/ansible/playbooks$ ansible-playbook show-arp.yml -l c1_s1

    PLAY [Show IP ARP] ************************************************************************************************************

    TASK [Show IP ARP] ************************************************************************************************************

    ok: [c1_s1_cpe]

    ok: [c1_s1_co-1]

    ok: [c1_s1_ua-1]

    TASK [debug] ******************************************************************************************************************
    ok: [c1_s1_co-1] => {
        "list_of_ip_arp.stdout_lines": [
            [
                "Protocol  Address          Age (min)  Hardware Addr   Type   Interface",
                "Internet  10.100.12.1            78   c202.5d80.0001  ARPA   FastEthernet0/0",
                "Internet  10.100.12.2             -   c204.5f8c.0000  ARPA   FastEthernet0/0",
                "Internet  10.100.200.1            -   c204.5f8c.0000  ARPA   Vlan10",
                "Internet  10.100.200.2           78   c206.1b68.0000  ARPA   Vlan10"
            ]
        ]
    }
    ok: [c1_s1_ua-1] => {
        "list_of_ip_arp.stdout_lines": [
            [
                "Protocol  Address          Age (min)  Hardware Addr   Type   Interface",
                "Internet  10.100.200.1           78   c204.5f8c.0000  ARPA   Vlan10",
                "Internet  10.100.200.2            -   c206.1b68.0000  ARPA   Vlan10"
            ]
        ]
    }
    ok: [c1_s1_cpe] => {
        "list_of_ip_arp.stdout_lines": [
            [
                "Protocol  Address          Age (min)  Hardware Addr   Type   Interface",
                "Internet  10.0.12.1              78   c201.375c.0001  ARPA   FastEthernet0/0",
                "Internet  10.0.12.2               -   c202.5d80.0000  ARPA   FastEthernet0/0",
                "Internet  10.100.12.1             -   c202.5d80.0001  ARPA   FastEthernet0/1",
                "Internet  10.100.12.2            78   c204.5f8c.0000  ARPA   FastEthernet0/1"
            ]
        ]
    }

    PLAY RECAP ********************************************************************************************************************
    c1_s1_co-1                 : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
    c1_s1_cpe                  : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
    c1_s1_ua-1                 : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0


**getting better, this one checks if an ACL is already there, and if not it will apply it**

::

    adrian@adrian-VirtualBox:~/netor/netor/ansible/playbooks$ ansible-playbook check-acl.yml -l c1_s1 --check

    PLAY [Check or create exact ACL order] ****************************************************************************************

    TASK [Check or create exact ACL order] ****************************************************************************************

    changed: [c1_s1_cpe]

    changed: [c1_s1_co-1]

    changed: [c1_s1_ua-1]

    PLAY RECAP ********************************************************************************************************************
    c1_s1_co-1                 : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
    c1_s1_cpe                  : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
    c1_s1_ua-1                 : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

    adrian@adrian-VirtualBox:~/netor/netor/ansible/playbooks$ ansible-playbook check-acl.yml -l c1_s1 --check --diff

    PLAY [Check or create exact ACL order] ****************************************************************************************

    TASK [Check or create exact ACL order] ****************************************************************************************

    changed: [c1_s1_cpe]

    changed: [c1_s1_co-1]

    changed: [c1_s1_ua-1]

    PLAY RECAP ********************************************************************************************************************
    c1_s1_co-1                 : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
    c1_s1_cpe                  : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
    c1_s1_ua-1                 : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0


Salt examples
*************

From easy to hard

**basic to test the connection between Salt and the devices**

::

    adrian@adrian-VirtualBox:~$ sudo salt 'c1_s1*' test.ping
    c1_s1_ua-1:
        True
    c1_s1_co-1:
        True
    c1_s1_cpe:
        True


**you can also add the ``-l debug`` flag**

::

    adrian@adrian-VirtualBox:~$ sudo salt 'c1_s1*' test.ping -l debug
    [DEBUG   ] Reading configuration from /etc/salt/master
    [DEBUG   ] Using cached minion ID from /etc/salt/minion_id: adrian-VirtualBox
    [DEBUG   ] Missing configuration file: /home/adrian/.saltrc
    [DEBUG   ] Configuration file path: /etc/salt/master
    [WARNING ] Insecure logging configuration detected! Sensitive data may be logged.
    [DEBUG   ] Reading configuration from /etc/salt/master
    [DEBUG   ] Using cached minion ID from /etc/salt/minion_id: adrian-VirtualBox
    [DEBUG   ] Missing configuration file: /home/adrian/.saltrc
    [DEBUG   ] MasterEvent PUB socket URI: /var/run/salt/master/master_event_pub.ipc
    [DEBUG   ] MasterEvent PULL socket URI: /var/run/salt/master/master_event_pull.ipc
    [DEBUG   ] Initializing new AsyncZeroMQReqChannel for ('/home/adrian/netor-master/netor/salt/config/pki/master', 'adrian-VirtualBox_master', 'tcp://127.0.0.1:4506', 'clear')
    [DEBUG   ] Connecting the Minion to the Master URI (for the return server): tcp://127.0.0.1:4506
    [DEBUG   ] Trying to connect to: tcp://127.0.0.1:4506
    [DEBUG   ] Closing AsyncZeroMQReqChannel instance
    [DEBUG   ] LazyLoaded local_cache.get_load
    [DEBUG   ] Reading minion list from /var/cache/salt/master/jobs/ba/6ceb1709725e52888fafec43611acca92cb7287fe14f0aab323f7711bbc3f0/.minions.p
    [DEBUG   ] get_iter_returns for jid 20191116123204208193 sent to {'c1_s1_cpe', 'c1_s1_co-1', 'c1_s1_ua-1'} will timeout at 12:32:09.226416
    [DEBUG   ] jid 20191116123204208193 return from c1_s1_ua-1
    [DEBUG   ] return event: {'c1_s1_ua-1': {'ret': True, 'retcode': 0, 'jid': '20191116123204208193'}}
    [DEBUG   ] LazyLoaded nested.output
    c1_s1_ua-1:
        True
    [DEBUG   ] jid 20191116123204208193 return from c1_s1_cpe
    [DEBUG   ] return event: {'c1_s1_cpe': {'ret': True, 'retcode': 0, 'jid': '20191116123204208193'}}
    [DEBUG   ] LazyLoaded nested.output
    c1_s1_cpe:
        True
    [DEBUG   ] jid 20191116123204208193 return from c1_s1_co-1
    [DEBUG   ] return event: {'c1_s1_co-1': {'ret': True, 'retcode': 0, 'jid': '20191116123204208193'}}
    [DEBUG   ] LazyLoaded nested.output
    c1_s1_co-1:
        True
    [DEBUG   ] jid 20191116123204208193 found all minions {'c1_s1_cpe', 'c1_s1_ua-1', 'c1_s1_co-1'}
    [DEBUG   ] Closing IPCMessageSubscriber instance
    adrian@adrian-VirtualBox:~$


**this is i think the coolest and easiest function of Salt**

The **net.find** module allows you to search in 3 seconds information gathered by mining.
Lets look for IP address, MACs, interface descriptions, vlan, etc. configured on the devices.

::

    adrian@adrian-VirtualBox:~/netor/netor/salt$ sudo salt-run net.find 10.0.0.0/8 best=False
    Details for all interfaces that include network 10.0.0.0/8

        ------------------------------------------------------------------------------------------------------------------------------
        |   Device   |    Interface    | Interface Description |   IP Addresses  | Enabled |  UP  |    MAC Address    | Speed [Mbps] |
        ------------------------------------------------------------------------------------------------------------------------------
        | c1_s1_co-1 | FastEthernet0/0 |        to_inet        |  10.100.12.2/24 |   True  | True | C2:04:5F:8C:00:00 |      10      |
        ------------------------------------------------------------------------------------------------------------------------------
        | c1_s1_co-1 |      Vlan10     |          LAN          | 10.100.200.1/24 |   True  | True | C2:04:5F:8C:00:00 |     100      |
        ------------------------------------------------------------------------------------------------------------------------------
        | c1_s1_cpe  | FastEthernet0/0 |         to_r1         |   10.0.12.2/24  |   True  | True | C2:02:5D:80:00:00 |      10      |
        ------------------------------------------------------------------------------------------------------------------------------
        | c1_s1_cpe  | FastEthernet0/1 |       to_inside       |  10.100.12.1/24 |   True  | True | C2:02:5D:80:00:01 |      10      |
        ------------------------------------------------------------------------------------------------------------------------------
        | c1_s1_ua-1 |      Vlan10     |         user1         | 10.100.200.2/24 |   True  | True | C2:06:1B:68:00:00 |     100      |
        ------------------------------------------------------------------------------------------------------------------------------
        | c2_s1_co-1 | FastEthernet0/0 |        to_inet        |  10.101.23.2/24 |   True  | True | C2:05:48:3C:00:00 |      10      |
        ------------------------------------------------------------------------------------------------------------------------------
        | c2_s1_co-1 |      Vlan10     |          LAN          | 10.101.201.1/24 |   True  | True | C2:05:48:3C:00:00 |     100      |
        ------------------------------------------------------------------------------------------------------------------------------
        | c2_s1_cpe  | FastEthernet0/0 |         to_r1         |   10.0.13.2/24  |   True  | True | C2:03:29:20:00:00 |      10      |
        ------------------------------------------------------------------------------------------------------------------------------
        | c2_s1_cpe  | FastEthernet0/1 |       to_inside       |  10.101.23.1/24 |   True  | True | C2:03:29:20:00:01 |      10      |
        ------------------------------------------------------------------------------------------------------------------------------
        | c2_s1_ua-1 |      Vlan10     |         user1         | 10.101.201.2/24 |   True  | True | C2:07:61:70:00:00 |     100      |
        ------------------------------------------------------------------------------------------------------------------------------
    None


::

    adrian@adrian-VirtualBox:~/netor/netor/salt$ sudo salt-run net.find Vlan10
    Pattern "Vlan10" found in the description of the following interfaces
    Details for interface Vlan10

        ------------------------------------------------------------------------------------------------------------------------
        |   Device   | Interface | Interface Description |   IP Addresses  | Enabled |  UP  |    MAC Address    | Speed [Mbps] |
        ------------------------------------------------------------------------------------------------------------------------
        | c1_s1_ua-1 |   Vlan10  |         user1         | 10.100.200.2/24 |   True  | True | C2:06:1B:68:00:00 |     100      |
        ------------------------------------------------------------------------------------------------------------------------
        | c2_s1_ua-1 |   Vlan10  |         user1         | 10.101.201.2/24 |   True  | True | C2:07:61:70:00:00 |     100      |
        ------------------------------------------------------------------------------------------------------------------------
    Details for all interfaces on device Vlan10
    Pattern "Vlan10" found in one of the following LLDP details
    LLDP Neighbors for interface Vlan10
    LLDP Neighbors for all interfaces on device Vlan10
    MAC Address(es) on device Vlan10
    MAC Address(es) on interface Vlan10
    ARP Entries on device Vlan10
    ARP Entries on interface Vlan10

        ---------------------------------------------------------------------
        |  Age  |   Device   | Interface |      IP      |        MAC        |
        ---------------------------------------------------------------------
        | 108.0 | c1_s1_ua-1 |   Vlan10  | 10.100.200.1 | C2:04:5F:8C:00:00 |
        ---------------------------------------------------------------------
        |  0.0  | c1_s1_ua-1 |   Vlan10  | 10.100.200.2 | C2:06:1B:68:00:00 |
        ---------------------------------------------------------------------
        | 108.0 | c2_s1_ua-1 |   Vlan10  | 10.101.201.1 | C2:05:48:3C:00:00 |
        ---------------------------------------------------------------------
        |  0.0  | c2_s1_ua-1 |   Vlan10  | 10.101.201.2 | C2:07:61:70:00:00 |
        ---------------------------------------------------------------------


::

    adrian@adrian-VirtualBox:~/netor/netor/salt$ sudo salt-run net.find to_inside
    Pattern "to_inside" found in the description of the following interfaces

        ----------------------------------------------------------------------------------------------------------------------------
        |   Device  |    Interface    | Interface Description |  IP Addresses  | Enabled |  UP  |    MAC Address    | Speed [Mbps] |
        ----------------------------------------------------------------------------------------------------------------------------
        | c1_s1_cpe | FastEthernet0/1 |       to_inside       | 10.100.12.1/24 |   True  | True | C2:02:5D:80:00:01 |      10      |
        ----------------------------------------------------------------------------------------------------------------------------
    Details for interface to_inside
    Details for all interfaces on device to_inside
    Pattern "to_inside" found in one of the following LLDP details
    LLDP Neighbors for interface to_inside
    LLDP Neighbors for all interfaces on device to_inside
    MAC Address(es) on device to_inside
    MAC Address(es) on interface to_inside
    ARP Entries on device to_inside
    ARP Entries on interface to_inside
    None


::

    adrian@adrian-VirtualBox:~/netor/netor/salt$ sudo salt-run net.find 10.100.12.1
    Details for all interfaces that include network 10.100.12.1/32 - only best match returned

        ----------------------------------------------------------------------------------------------------------------------------
        |   Device  |    Interface    | Interface Description |  IP Addresses  | Enabled |  UP  |    MAC Address    | Speed [Mbps] |
        ----------------------------------------------------------------------------------------------------------------------------
        | c1_s1_cpe | FastEthernet0/1 |       to_inside       | 10.100.12.1/24 |   True  | True | C2:02:5D:80:00:01 |      10      |
        ----------------------------------------------------------------------------------------------------------------------------
    ARP Entries for IP 10.100.12.1

        -----------------------------------------------------------------------
        | Age |   Device  |    Interface    |      IP     |        MAC        |
        -----------------------------------------------------------------------
        | 0.0 | c1_s1_cpe | FastEthernet0/1 | 10.100.12.1 | C2:02:5D:80:00:01 |
        -----------------------------------------------------------------------
    IP Address 10.100.12.1 is set for interface FastEthernet0/1, on c1_s1_cpe

        ----------------------------------------------------------------------------------------------------------------------------
        |   Device  |    Interface    | Interface Description |  IP Addresses  | Enabled |  UP  |    MAC Address    | Speed [Mbps] |
        ----------------------------------------------------------------------------------------------------------------------------
        | c1_s1_cpe | FastEthernet0/1 |       to_inside       | 10.100.12.1/24 |   True  | True | C2:02:5D:80:00:01 |      10      |
        ----------------------------------------------------------------------------------------------------------------------------
    LLDP Neighbors for interface FastEthernet0/1 on device c1_s1_cpe
    None


::

    adrian@adrian-VirtualBox:~/netor/netor/salt$ sudo salt-run net.find C2:02:5D:80:00:01
    MAC Address(es)
    ARP Entries for MAC C2:02:5D:80:00:01

        --------------------------------------------------------------------------
        |  Age  |   Device   |    Interface    |      IP     |        MAC        |
        --------------------------------------------------------------------------
        | 114.0 | c1_s1_co-1 | FastEthernet0/0 | 10.100.12.1 | C2:02:5D:80:00:01 |
        --------------------------------------------------------------------------
    LLDP Neighbors for all interfaces having Chassis ID C2:02:5D:80:00:01
    Interface FastEthernet0/1 on c1_s1_cpe has the physical address (C2:02:5D:80:00:01)

        ----------------------------------------------------------------------------------------------------------------------------
        |   Device  |    Interface    | Interface Description |  IP Addresses  | Enabled |  UP  |    MAC Address    | Speed [Mbps] |
        ----------------------------------------------------------------------------------------------------------------------------
        | c1_s1_cpe | FastEthernet0/1 |       to_inside       | 10.100.12.1/24 |   True  | True | C2:02:5D:80:00:01 |      10      |
        ----------------------------------------------------------------------------------------------------------------------------
    LLDP Neighbors for interface FastEthernet0/1 on device c1_s1_cpe
    None


**States, great concept!**

It is getting better...

Salt define a **sate** in a file in which you can define attributes (like ntp in this example), and later you can
apply that state/attribute to any OS. Yes it will figure out what commands to execute depending on the OS.

Read about this state ntp.sls file at the ``netor/salt/config/pillar/states`` folder.

::

    adrian@adrian-VirtualBox:~/netor/netor/salt$ sudo salt 'c1_s1_cpe' state.apply ntp
    c1_s1_cpe:
    ----------
              ID: netntp
        Function: netntp.managed
          Result: True
         Comment: Device configured properly.
         Started: 23:44:39.097859
        Duration: 1629.019 ms
         Changes:

    Summary for c1_s1_cpe
    ------------
    Succeeded: 1
    Failed:    0
    ------------
    Total states run:     1
    Total run time:   1.629 s
    adrian@adrian-VirtualBox:~/netor/netor/salt$


    adrian@adrian-VirtualBox:~/netor/netor/salt$ more ./config/pillar/states/ntp.sls
    netntp:
      netntp.managed:
        - servers:
          - 10.0.0.2
    adrian@adrian-VirtualBox:~/netor/netor/salt$


**this is how you can view the event bus**

You will see what happens when you apply the **state**

::

    adrian@adrian-VirtualBox:~/netor/netor/salt$ sudo salt-run state.event pretty=True
    20191115234741088036	{
        "_stamp": "2019-11-15T22:47:41.088306",
        "minions": [
            "c1_s1_cpe"
        ]
    }
    salt/job/20191115234741088036/new	{
        "_stamp": "2019-11-15T22:47:41.088725",
        "arg": [
            "ntp"
        ],
        "fun": "state.apply",
        "jid": "20191115234741088036",
        "minions": [
            "c1_s1_cpe"
        ],
        "missing": [],
        "tgt": "c1_s1_cpe",
        "tgt_type": "glob",
        "user": "sudo_adrian"
    }
    minion/refresh/c1_s1_cpe	{
        "Minion data cache refresh": "c1_s1_cpe",
        "_stamp": "2019-11-15T22:47:41.300837"
    }
    salt/job/20191115234741088036/ret/c1_s1_cpe	{
        "_stamp": "2019-11-15T22:47:43.462567",
        "cmd": "_return",
        "fun": "state.apply",
        "fun_args": [
            "ntp"
        ],
        "id": "c1_s1_cpe",
        "jid": "20191115234741088036",
        "out": "highstate",
        "retcode": 0,
        "return": {
            "netntp_-netntp_-netntp_-managed": {
                "__id__": "netntp",
                "__run_num__": 0,
                "__sls__": "ntp",
                "changes": {},
                "comment": "Device configured properly.",
                "duration": 2026.341,
                "name": "netntp",
                "result": true,
                "start_time": "23:47:41.424906"
            }
        },
        "success": true
    }


**how to use the online help of the commands**

In this case the mine function/module

::

    adrian@lmint2:~$ sudo salt-run mine
    mine.get:

            Gathers the data from the specified minions' mine, pass in the target,
            function to look up and the target type

            CLI Example:

                salt-run mine.get '*' network.interfaces

    mine.update:

            New in version 2017.7.0

            Update the mine data on a certain group of minions.

            tgt
                Which minions to target for the execution.

            tgt_type: ``glob``
                The type of ``tgt``.

            clear: ``False``
                Boolean flag specifying whether updating will clear the existing
                mines, or will update. Default: ``False`` (update).

            mine_functions
                Update the mine data on certain functions only.
                This feature can be used when updating the mine for functions
                that require refresh at different intervals than the rest of
                the functions specified under ``mine_functions`` in the
                minion/master config or pillar.

            CLI Example:

                salt-run mine.update '*'
                salt-run mine.update 'juniper-edges' tgt_type='nodegroup'

    ... continue


**wait you can do a simulation with the "test=True" option**

::

    adrian@lmint2:~$ sudo salt 'c1_s1_cpe' state.apply sla test=True
    c1_s1_cpe:
    ----------
              ID: rpmprobes
        Function: probes.managed
          Result: None
         Comment: Testing mode: configuration was not changed!
         Started: 10:37:24.816077
        Duration: 1648.158 ms
         Changes:
                  ----------
                  added:
                      ----------
                      probe_name1:
                          ----------
                          probe1_test1:
                              ----------
                              probe_type:
                                  icmp-ping
                              target:
                                  10.0.12.1
                          probe1_test2:
                              ----------
                              probe_count:
                                  3
                              probe_type:
                                  udp-ping
                              source:
                                  10.100.12.1
                              target:
                                  10.0.12.1
                              test_interval:
                                  5
                  removed:
                      None
                  updated:
                      None

    Summary for c1_s1_cpe
    ------------
    Succeeded: 1 (unchanged=1, changed=1)
    Failed:    0
    ------------
    Total states run:     1
    Total run time:   1.648 s


**check a running configuration**

This command will take 3 second since you can have a proxy minion with a session already established with the device

::

    adrian@lmint2:~$ sudo salt 'c1_s1_cpe' net.config source='running'
    c1_s1_cpe:
        ----------
        comment:
        out:
            ----------
            candidate:
            running:
                Building configuration...

                Current configuration : 2202 bytes
                !
                version 12.4
                no service pad
                service tcp-keepalives-in
                service tcp-keepalives-out
                service timestamps debug datetime msec localtime show-timezone
                service timestamps log datetime msec localtime show-timezone
                service password-encryption
                !
                hostname r2
                !
                boot-start-marker
                boot-end-marker
                !
                logging buffered 32000
                no logging console
                enable secret 5 $1$QAh2$FiUShFDsaikloAgWmKsW1.
                !
                aaa new-model
                !
                !
                aaa authentication login default local-case
                aaa authorization exec default local
                !
                !
                aaa session-id common
                memory-size iomem 5
                no ip source-route
                ip options drop
                ip cef
                !
                !
                ip dhcp bootp ignore
                !
                !
                no ip domain lookup
                ip domain name quadrant.edu
                !
                multilink bundle-name authenticated
    ... continue

**of course you can add a simple 'grep'**

::

    adrian@lmint2:~$ sudo salt 'c1_s1_cpe' net.config source='running' | grep snmp
                snmp-server community snmpCommunity RW
                snmp-server community read_only RO
                snmp-server community read_write RW


** do a simple ping from several devices to check for problems**

You could try this for ping from several countries/sites to 1 server/service inside/outside of the network.

::

    adrian@adrian-VirtualBox:~$ sudo salt 'c1_s1_*' network.ping 10.0.12.2
    c1_s1_ua-1:
        PING 10.0.12.2 (10.0.12.2) 56(84) bytes of data.
        64 bytes from 10.0.12.2: icmp_seq=1 ttl=253 time=31.9 ms
        64 bytes from 10.0.12.2: icmp_seq=2 ttl=253 time=324 ms
        64 bytes from 10.0.12.2: icmp_seq=3 ttl=253 time=21.4 ms
        64 bytes from 10.0.12.2: icmp_seq=4 ttl=253 time=103 ms

        --- 10.0.12.2 ping statistics ---
        4 packets transmitted, 4 received, 0% packet loss, time 3003ms
        rtt min/avg/max/mdev = 21.461/120.435/324.668/122.081 ms
    c1_s1_cpe:
        PING 10.0.12.2 (10.0.12.2) 56(84) bytes of data.
        64 bytes from 10.0.12.2: icmp_seq=1 ttl=253 time=41.7 ms
        64 bytes from 10.0.12.2: icmp_seq=2 ttl=253 time=344 ms
        64 bytes from 10.0.12.2: icmp_seq=3 ttl=253 time=52.1 ms
        64 bytes from 10.0.12.2: icmp_seq=4 ttl=253 time=124 ms

        --- 10.0.12.2 ping statistics ---
        4 packets transmitted, 4 received, 0% packet loss, time 3003ms
        rtt min/avg/max/mdev = 41.770/140.752/344.745/121.997 ms
    c1_s1_co-1:
        PING 10.0.12.2 (10.0.12.2) 56(84) bytes of data.
        64 bytes from 10.0.12.2: icmp_seq=1 ttl=253 time=44.9 ms
        64 bytes from 10.0.12.2: icmp_seq=2 ttl=253 time=359 ms
        64 bytes from 10.0.12.2: icmp_seq=3 ttl=253 time=66.6 ms
        64 bytes from 10.0.12.2: icmp_seq=4 ttl=253 time=148 ms

        --- 10.0.12.2 ping statistics ---
        4 packets transmitted, 4 received, 0% packet loss, time 3005ms
        rtt min/avg/max/mdev = 44.999/155.004/359.790/124.385 ms


**if the have a route to a destination**

::

    adrian@lmint2:~$ sudo salt '*' route.show 192.168.201.3
    c1_s1_co-1:
        ----------
        comment:
        out:
            ----------
            192.168.201.3:
        result:
            True
    c2_s1_ua-1:
        ----------
        comment:
        out:
            ----------
            192.168.201.3:
        result:
            True
    c1_s1_cpe:
        ----------
        comment:
        out:
            ----------
            192.168.201.3:
        result:
            True
    c2_s1_cpe:
        ----------
        comment:
        out:
            ----------
            192.168.201.3:
        result:
            True


**a simple ping with True or False if it was successful**

::

    adrian@lmint2:~$ sudo salt 'c1_s1*' net.ping 192.168.201.3
    c1_s1_ua-1:
        ----------
        comment:
        out:
            ----------
        result:
            True
    c1_s1_cpe:
        ----------
        comment:
        out:
            ----------
        result:
            True


**a traceroute showing the latency**

::

    adrian@lmint2:~$ sudo salt 'c1_s1_cpe' net.traceroute 192.168.201.3
    c1_s1_cpe:
        ----------
        comment:
        out:
            ----------
            success:
                ----------
                0:
                    ----------
                    probes:
                        ----------
                        1:
                            ----------
                            host_name:
                                10.0.12.1
                            ip_address:
                                10.0.12.1
                            rtt:
                                208.0
                        2:
                            ----------
                            host_name:
                                10.0.12.1
                            ip_address:
                                10.0.12.1
                            rtt:
                                32.0
                        3:
                            ----------
                            host_name:
                                10.0.12.1
                            ip_address:
                                10.0.12.1
                            rtt:
                                24.0
                1:
                    ----------
                    probes:
                        ----------
                        1:
                            ----------
                            host_name:
                                10.0.12.1
                            ip_address:
                                10.0.12.1
                            rtt:
                                28.0
                        2:
                            ----------
                            host_name:
                                10.0.12.1
                            ip_address:
                                10.0.12.1
                            rtt:
                                32.0
                        3:
                            ----------
                            host_name:
                                10.0.12.1
                            ip_address:
                                10.0.12.1
                            rtt:
                                32.0
                2:
                    ----------
                    probes:
                        ----------
                        1:
                            ----------
                            host_name:
                                10.0.0.1
                            ip_address:
                                10.0.0.1
                            rtt:
                                36.0
                        2:
                            ----------
                            host_name:
                                10.0.0.1
                            ip_address:
                                10.0.0.1
                            rtt:
                                40.0
                        3:
                            ----------
                            host_name:
                                10.0.0.1
                            ip_address:
                                10.0.0.1
                            rtt:
                                36.0
                3:
                    ----------
                    probes:
                        ----------
                        1:
                            ----------
                            host_name:
                                192.168.201.3
                            ip_address:
                                192.168.201.3
                            rtt:
                                40.0
                        2:
                            ----------
                            host_name:
                                192.168.201.3
                            ip_address:
                                192.168.201.3
                            rtt:
                                36.0
                        3:
                            ----------
                            host_name:
                                192.168.201.3
                            ip_address:
                                192.168.201.3
                            rtt:
                                40.0
        result:
            True


**another kind ok ping**

::

    adrian@adrian-VirtualBox:~$ sudo salt 'c1_s1_cpe' net.ping 10.0.12.2
    c1_s1_cpe:
        ----------
        comment:
        out:
            ----------
            success:
                ----------
                packet_loss:
                    0
                probes_sent:
                    5
                results:
                    |_
                      ----------
                      ip_address:
                          10.0.12.2
                      rtt:
                          0.0
                    |_
                      ----------
                      ip_address:
                          10.0.12.2
                      rtt:
                          0.0
                    |_
                      ----------
                      ip_address:
                          10.0.12.2
                      rtt:
                          0.0
                    |_
                      ----------
                      ip_address:
                          10.0.12.2
                      rtt:
                          0.0
                    |_
                      ----------
                      ip_address:
                          10.0.12.2
                      rtt:
                          0.0
                rtt_avg:
                    3.0
                rtt_max:
                    4.0
                rtt_min:
                    1.0
                rtt_stddev:
                    0.0
        result:
            True


**check the information about the devices**

::

    adrian@lmint2:~$ sudo salt 'c1_s1_cpe' net.facts
    c1_s1_cpe:
        ----------
        comment:
        out:
            ----------
            fqdn:
                r2.quadrant.edu
            hostname:
                r2
            interface_list:
                - FastEthernet0/0
                - FastEthernet0/1
                - FastEthernet1/0
            model:
                3725
            os_version:
                3700 Software (C3725-ADVENTERPRISEK9-M), Version 12.4(15)T13, RELEASE SOFTWARE (fc3)
            serial_number:
                FTX0945W0MY
            uptime:
                38160
            vendor:
                Cisco
        result:
            True


**this is interesting, you can format the output**

Salt has several out formatters, like table, json, etc

::

    adrian@lmint2:~$ sudo salt 'c1_s1_cpe' net.arp --out=table
    c1_s1_cpe:
    ----------
        comment:
        ----------
        out:
        ----------
            -------------------------------------------------------------
            |  Age  |    Interface    |      Ip     |        Mac        |
            -------------------------------------------------------------
            | 126.0 | FastEthernet0/0 |  10.0.12.1  | C2:01:37:5C:00:01 |
            -------------------------------------------------------------
            |  0.0  | FastEthernet0/0 |  10.0.12.2  | C2:02:5D:80:00:00 |
            -------------------------------------------------------------
            |  0.0  | FastEthernet0/1 | 10.100.12.1 | C2:02:5D:80:00:01 |
            -------------------------------------------------------------
            | 149.0 | FastEthernet0/1 | 10.100.12.2 | C2:04:5F:8C:00:00 |
            -------------------------------------------------------------


**check arp entries**

::

    adrian@lmint2:~$ sudo salt 'c1_s1_cpe' net.arp
    c1_s1_cpe:
        ----------
        comment:
        out:
            |_
              ----------
              age:
                  126.0
              interface:
                  FastEthernet0/0
              ip:
                  10.0.12.1
              mac:
                  C2:01:37:5C:00:01
            |_
              ----------
              age:
                  0.0
              interface:
                  FastEthernet0/0
              ip:
                  10.0.12.2
              mac:
                  C2:02:5D:80:00:00
            |_
              ----------
              age:
                  0.0
              interface:
                  FastEthernet0/1
              ip:
                  10.100.12.1
              mac:
                  C2:02:5D:80:00:01
            |_
              ----------
              age:
                  150.0
              interface:
                  FastEthernet0/1
              ip:
                  10.100.12.2
              mac:
                  C2:04:5F:8C:00:00
        result:
            True


**check interfaces**

::

    adrian@lmint2:~$ sudo salt 'c1_s1_cpe' net.interfaces
    c1_s1_cpe:
        ----------
        comment:
        out:
            ----------
            FastEthernet0/0:
                ----------
                description:
                    to_r1
                is_enabled:
                    True
                is_up:
                    True
                last_flapped:
                    -1.0
                mac_address:
                    C2:02:5D:80:00:00
                mtu:
                    1500
                speed:
                    10
            FastEthernet0/1:
                ----------
                description:
                    to_inside
                is_enabled:
                    True
                is_up:
                    True
                last_flapped:
                    -1.0
                mac_address:
                    C2:02:5D:80:00:01
                mtu:
                    1500
                speed:
                    10
            FastEthernet1/0:
                ----------
                description:
                is_enabled:
                    False
                is_up:
                    False
                last_flapped:
                    -1.0
                mac_address:
                    C2:02:5D:80:00:10
                mtu:
                    1500
                speed:
                    100
        result:
            True


**check ip addresses of interfaces**

::

    adrian@lmint2:~$ sudo salt 'c1_s1_cpe' net.ipaddrs
    c1_s1_cpe:
        ----------
        comment:
        out:
            ----------
            FastEthernet0/0:
                ----------
                ipv4:
                    ----------
                    10.0.12.2:
                        ----------
                        prefix_length:
                            24
            FastEthernet0/1:
                ----------
                ipv4:
                    ----------
                    10.100.12.1:
                        ----------
                        prefix_length:
                            24
        result:
            True


**check arp entries**

::

    adrian@lmint2:~$ sudo salt 'c1_s1_cpe' net.arp
    c1_s1_cpe:
        ----------
        comment:
        out:
            |_
              ----------
              age:
                  130.0
              interface:
                  FastEthernet0/0
              ip:
                  10.0.12.1
              mac:
                  C2:01:37:5C:00:01
            |_
              ----------
              age:
                  0.0
              interface:
                  FastEthernet0/0
              ip:
                  10.0.12.2
              mac:
                  C2:02:5D:80:00:00
            |_
              ----------
              age:
                  0.0
              interface:
                  FastEthernet0/1
              ip:
                  10.100.12.1
              mac:
                  C2:02:5D:80:00:01
            |_
              ----------
              age:
                  153.0
              interface:
                  FastEthernet0/1
              ip:
                  10.100.12.2
              mac:
                  C2:04:5F:8C:00:00
        result:
            True


**check the same arp entries but with an "table" output formatter**

::

    adrian@lmint2:~$ sudo salt 'c1_s1_cpe' net.arp --out=table
    c1_s1_cpe:
    ----------
        comment:
        ----------
        out:
        ----------
            -------------------------------------------------------------
            |  Age  |    Interface    |      Ip     |        Mac        |
            -------------------------------------------------------------
            | 130.0 | FastEthernet0/0 |  10.0.12.1  | C2:01:37:5C:00:01 |
            -------------------------------------------------------------
            |  0.0  | FastEthernet0/0 |  10.0.12.2  | C2:02:5D:80:00:00 |
            -------------------------------------------------------------
            |  0.0  | FastEthernet0/1 | 10.100.12.1 | C2:02:5D:80:00:01 |
            -------------------------------------------------------------
            | 154.0 | FastEthernet0/1 | 10.100.12.2 | C2:04:5F:8C:00:00 |
            -------------------------------------------------------------
        result:
        ----------


**or with json formatter**

::

    adrian@lmint2:~$ sudo salt 'c1_s1_cpe' net.arp --out=json
    {
        "c1_s1_cpe": {
            "out": [
                {
                    "interface": "FastEthernet0/0",
                    "mac": "C2:01:37:5C:00:01",
                    "ip": "10.0.12.1",
                    "age": 130.0
                },
                {
                    "interface": "FastEthernet0/0",
                    "mac": "C2:02:5D:80:00:00",
                    "ip": "10.0.12.2",
                    "age": 0.0
                },
                {
                    "interface": "FastEthernet0/1",
                    "mac": "C2:02:5D:80:00:01",
                    "ip": "10.100.12.1",
                    "age": 0.0
                },
                {
                    "interface": "FastEthernet0/1",
                    "mac": "C2:04:5F:8C:00:00",
                    "ip": "10.100.12.2",
                    "age": 154.0
                }
            ],
            "result": true,
            "comment": ""
        }
    }


**send messages with slack**

Edit and try the playbook "backup-msg-slack.yml". After the backup you will receive a message in Slack telling you so.
This is just an example of what you can do with chatOps.


Finally, check the respective project pages because this is only an intro... there are thousands of cool stuff to do.