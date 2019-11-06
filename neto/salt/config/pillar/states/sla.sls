rpmprobes:
  probes.managed:
    - probes:
        probe_name1:
          probe1_test1:
            target: 10.0.12.1
            probe_type: icmp-ping
          probe1_test2:
            target: 10.0.12.1
            source: 10.100.12.1
            probe_type: udp-ping
            probe_count: 3
            test_interval: 5
