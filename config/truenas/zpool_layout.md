# TrueNAS SCALE ZFS Storage & Ingest Architecture

## Host Details
* **Hostname**: `truenas.local` (IP: `192.168.0.47`)
* **OS & Kernel**:
```text
Linux truenas 6.18.23-production+truenas #1 SMP PREEMPT_DYNAMIC Tue Jun 16 15:04:36 UTC 2026 x86_64 GNU/Linux
```

## ZFS Pools & Datasets
```text
NAME        SIZE  ALLOC   FREE  CKPOINT  EXPANDSZ   FRAG    CAP  DEDUP    HEALTH  ALTROOT
boot-pool    39G  17.5G  21.5G        -         -    34%    44%  1.00x    ONLINE  -
pool1       992G   641G   351G        -         -    14%    64%  1.00x    ONLINE  /mnt

pool: boot-pool
 state: ONLINE
  scan: scrub repaired 0B in 00:02:25 with 0 errors on Tue Sep  1 03:47:27 2026
config:

	NAME        STATE     READ WRITE CKSUM
	boot-pool   ONLINE       0     0     0
	  sda3      ONLINE       0     0     0

errors: No known data errors

  pool: pool1
 state: ONLINE
status: Some supported and requested features are not enabled on the pool.
	The pool can still be used, but some features are unavailable.
action: Enable all features using 'zpool upgrade'. Once this is done,
	the pool may no longer be accessible by software that does not support
	the features. See zpool-features(7) for details.
  scan: scrub repaired 0B in 01:45:37 with 0 errors on Sun Aug 23 01:45:39 2026
config:

	NAME                                      STATE     READ WRITE CKSUM
	pool1                                     ONLINE       0     0     0
	  mirror-0                                ONLINE       0     0     0
	    ce9964bc-247a-4655-b413-204983b1318b  ONLINE       0     0     0
	    44825693-5e55-477d-b108-4ea7da9fd499  ONLINE       0     0     0

errors: No known data errors

NAME                                                                                             USED  AVAIL  REFER  MOUNTPOINT
boot-pool                                                                                       17.5G  20.3G    96K  none
boot-pool/.system                                                                               25.4M  20.3G   112K  legacy
boot-pool/.system/configs-ae32c386e13840b2bf9c0083275e7941                                       256K  20.3G   256K  legacy
boot-pool/.system/cores                                                                           96K  1024M    96K  legacy
boot-pool/.system/netdata-ae32c386e13840b2bf9c0083275e7941                                      24.6M  20.3G  24.6M  legacy
boot-pool/.system/nfs                                                                            116K  20.3G   116K  legacy
boot-pool/.system/samba4                                                                         168K  20.3G   168K  legacy
boot-pool/.system/vm                                                                              96K  20.3G    96K  legacy
boot-pool/ROOT                                                                                  17.5G  20.3G    96K  none
boot-pool/ROOT/25.10.1                                                                          3.09G  20.3G   104M  legacy
boot-pool/ROOT/25.10.1/audit                                                                     232K  20.3G  52.0M  /audit
boot-pool/ROOT/25.10.1/conf                                                                     7.53M  20.3G  7.53M  /conf
boot-pool/ROOT/25.10.1/data                                                                       88K  20.3G   280K  /data
boot-pool/ROOT/25.10.1/etc                                                                      7.50M  20.3G  6.45M  /etc
boot-pool/ROOT/25.10.1/home                                                                        0B  20.3G   124K  /home
boot-pool/ROOT/25.10.1/mnt                                                                        96K  20.3G    96K  /mnt
boot-pool/ROOT/25.10.1/opt                                                                      4.65M  20.3G  4.65M  /opt
boot-pool/ROOT/25.10.1/root                                                                        8K  20.3G   160K  /root
boot-pool/ROOT/25.10.1/usr                                                                      2.88G  20.3G  2.88G  /usr
boot-pool/ROOT/25.10.1/var                                                                      89.0M  20.3G  5.86M  /var
boot-pool/ROOT/25.10.1/var/ca-certificates                                                        96K  20.3G    96K  /var/local/ca-certificates
boot-pool/ROOT/25.10.1/var/lib                                                                  31.1M  20.3G  28.4M  /var/lib
boot-pool/ROOT/25.10.1/var/lib/incus                                                            2.40M  20.3G  2.40M  /var/lib/incus
boot-pool/ROOT/25.10.1/var/log                                                                  51.1M  20.3G  24.8M  /var/log
boot-pool/ROOT/25.10.1/var/log/journal                                                          50.7M  20.3G  50.7M  /var/log/journal
boot-pool/ROOT/25.10.2.1                                                                        3.12G  20.3G   104M  legacy
boot-pool/ROOT/25.10.2.1/audit                                                                   216K  20.3G  53.7M  /audit
boot-pool/ROOT/25.10.2.1/conf                                                                   7.72M  20.3G  7.72M  /conf
boot-pool/ROOT/25.10.2.1/data                                                                     88K  20.3G   288K  /data
boot-pool/ROOT/25.10.2.1/etc                                                                    7.43M  20.3G  6.48M  /etc
boot-pool/ROOT/25.10.2.1/home                                                                      0B  20.3G   124K  /home
boot-pool/ROOT/25.10.2.1/mnt                                                                     104K  20.3G   104K  /mnt
boot-pool/ROOT/25.10.2.1/opt                                                                    4.65M  20.3G  4.65M  /opt
boot-pool/ROOT/25.10.2.1/root                                                                      8K  20.3G   200K  /root
boot-pool/ROOT/25.10.2.1/usr                                                                    2.94G  20.3G  2.94G  /usr
boot-pool/ROOT/25.10.2.1/var                                                                    56.1M  20.3G  5.27M  /var
boot-pool/ROOT/25.10.2.1/var/ca-certificates                                                      96K  20.3G    96K  /var/local/ca-certificates
boot-pool/ROOT/25.10.2.1/var/lib                                                                31.1M  20.3G  28.3M  /var/lib
boot-pool/ROOT/25.10.2.1/var/lib/incus                                                          2.55M  20.3G  2.55M  /var/lib/incus
boot-pool/ROOT/25.10.2.1/var/log                                                                18.8M  20.3G  24.9M  /var/log
boot-pool/ROOT/25.10.2.1/var/log/journal                                                        18.4M  20.3G  18.4M  /var/log/journal
boot-pool/ROOT/25.10.3                                                                          3.15G  20.3G   104M  legacy
boot-pool/ROOT/25.10.3/audit                                                                     216K  20.3G   158M  /audit
boot-pool/ROOT/25.10.3/conf                                                                     7.72M  20.3G  7.72M  /conf
boot-pool/ROOT/25.10.3/data                                                                       88K  20.3G   280K  /data
boot-pool/ROOT/25.10.3/etc                                                                      7.44M  20.3G  6.48M  /etc
boot-pool/ROOT/25.10.3/home                                                                        0B  20.3G   132K  /home
boot-pool/ROOT/25.10.3/mnt                                                                       104K  20.3G   104K  /mnt
boot-pool/ROOT/25.10.3/opt                                                                      4.65M  20.3G  4.65M  /opt
boot-pool/ROOT/25.10.3/root                                                                        8K  20.3G   200K  /root
boot-pool/ROOT/25.10.3/usr                                                                      2.94G  20.3G  2.94G  /usr
boot-pool/ROOT/25.10.3/var                                                                      84.9M  20.3G  5.24M  /var
boot-pool/ROOT/25.10.3/var/ca-certificates                                                        96K  20.3G    96K  /var/local/ca-certificates
boot-pool/ROOT/25.10.3/var/lib                                                                  29.3M  20.3G  28.2M  /var/lib
boot-pool/ROOT/25.10.3/var/lib/incus                                                             888K  20.3G   888K  /var/lib/incus
boot-pool/ROOT/25.10.3/var/log                                                                  49.4M  20.3G  26.1M  /var/log
boot-pool/ROOT/25.10.3/var/log/journal                                                          49.0M  20.3G  49.0M  /var/log/journal
boot-pool/ROOT/26.0.0-BETA.1                                                                    3.78G  20.3G   115M  legacy
boot-pool/ROOT/26.0.0-BETA.1/audit                                                               288K  20.3G   262M  /audit
boot-pool/ROOT/26.0.0-BETA.1/conf                                                               9.14M  20.3G  9.14M  /conf
boot-pool/ROOT/26.0.0-BETA.1/data                                                                 88K  20.3G   300K  /data
boot-pool/ROOT/26.0.0-BETA.1/etc                                                                8.08M  20.3G  6.90M  /etc
boot-pool/ROOT/26.0.0-BETA.1/home                                                                  0B  20.3G   132K  /home
boot-pool/ROOT/26.0.0-BETA.1/mnt                                                                 112K  20.3G   112K  /mnt
boot-pool/ROOT/26.0.0-BETA.1/opt                                                                4.84M  20.3G  4.84M  /opt
boot-pool/ROOT/26.0.0-BETA.1/root                                                                  0B  20.3G   200K  /root
boot-pool/ROOT/26.0.0-BETA.1/usr                                                                3.55G  20.3G  3.55G  /usr
boot-pool/ROOT/26.0.0-BETA.1/var                                                                93.3M  20.3G  5.53M  /var
boot-pool/ROOT/26.0.0-BETA.1/var/ca-certificates                                                  96K  20.3G    96K  /var/local/ca-certificates
boot-pool/ROOT/26.0.0-BETA.1/var/lib                                                            31.3M  20.3G  31.0M  /var/lib
boot-pool/ROOT/26.0.0-BETA.1/var/log                                                            55.4M  20.3G  34.7M  /var/log
boot-pool/ROOT/26.0.0-BETA.1/var/log/journal                                                    55.1M  20.3G  55.1M  /var/log/journal
boot-pool/ROOT/26.0.0-BETA.2                                                                    4.33G  20.3G   116M  legacy
boot-pool/ROOT/26.0.0-BETA.2/audit                                                               487M  20.3G  93.2M  /audit
boot-pool/ROOT/26.0.0-BETA.2/conf                                                               9.07M  20.3G  9.07M  /conf
boot-pool/ROOT/26.0.0-BETA.2/data                                                               1.30M  20.3G   328K  /data
boot-pool/ROOT/26.0.0-BETA.2/etc                                                                7.98M  20.3G  6.91M  /etc
boot-pool/ROOT/26.0.0-BETA.2/home                                                                428K  20.3G   132K  /home
boot-pool/ROOT/26.0.0-BETA.2/mnt                                                                 112K  20.3G   112K  /mnt
boot-pool/ROOT/26.0.0-BETA.2/opt                                                                4.84M  20.3G  4.84M  /opt
boot-pool/ROOT/26.0.0-BETA.2/root                                                                568K  20.3G   200K  /root
boot-pool/ROOT/26.0.0-BETA.2/usr                                                                3.57G  20.3G  3.57G  /usr
boot-pool/ROOT/26.0.0-BETA.2/var                                                                 154M  20.3G  5.49M  /var
boot-pool/ROOT/26.0.0-BETA.2/var/ca-certificates                                                  96K  20.3G    96K  /var/local/ca-certificates
boot-pool/ROOT/26.0.0-BETA.2/var/lib                                                            31.1M  20.3G  30.8M  /var/lib
boot-pool/ROOT/26.0.0-BETA.2/var/log                                                             117M  20.3G  30.5M  /var/log
boot-pool/ROOT/26.0.0-BETA.2/var/log/journal                                                    29.1M  20.3G  29.1M  /var/log/journal
boot-pool/grub                                                                                  9.03M  20.3G  9.03M  legacy
pool1                                                                                            641G   320G  4.66M  /mnt/pool1
pool1/.ix-virt                                                                                   323M   320G    96K  /mnt/pool1/.ix-virt
pool1/.ix-virt/buckets                                                                            96K   320G    96K  legacy
pool1/.ix-virt/containers                                                                         96K   320G    96K  /mnt/pool1/.ix-virt/containers
pool1/.ix-virt/custom                                                                             96K   320G    96K  legacy
pool1/.ix-virt/deleted                                                                           322M   320G    96K  legacy
pool1/.ix-virt/deleted/buckets                                                                    96K   320G    96K  legacy
pool1/.ix-virt/deleted/containers                                                                 96K   320G    96K  legacy
pool1/.ix-virt/deleted/custom                                                                     96K   320G    96K  legacy
pool1/.ix-virt/deleted/images                                                                    322M   320G    96K  legacy
pool1/.ix-virt/deleted/images/0a8e52b0db63ba53ac844681a74395ef4e150d0e498bb8702a2b53b19c113435   322M   320G   322M  legacy
pool1/.ix-virt/deleted/virtual-machines                                                           96K   320G    96K  legacy
pool1/.ix-virt/images                                                                             96K   320G    96K  legacy
pool1/.ix-virt/virtual-machines                                                                   96K   320G    96K  legacy
pool1/.system                                                                                   3.25G   320G  2.08G  legacy
pool1/.system/configs-ae32c386e13840b2bf9c0083275e7941                                          18.1M   320G  18.1M  legacy
pool1/.system/cores                                                                              120K  1024M   120K  legacy
pool1/.system/netdata-ae32c386e13840b2bf9c0083275e7941                                           349M   320G   349M  legacy
pool1/.system/nfs                                                                                120K   320G   120K  legacy
pool1/.system/samba4                                                                             256K   320G   256K  legacy
pool1/.system/truesearch                                                                         834M   320G   834M  legacy
pool1/.system/vm                                                                                  96K   320G    96K  legacy
pool1/.system/webshare                                                                           136K   320G   136K  legacy
pool1/.truenas_containers                                                                        304K   320G   104K  /mnt/.truenas_containers/pool1
pool1/.truenas_containers/containers                                                             104K   320G   104K  /mnt/.truenas_containers/pool1/containers
pool1/.truenas_containers/images                                                                  96K   320G    96K  /mnt/.truenas_containers/pool1/images
pool1/ix-apps                                                                                   7.86G   320G   164K  /mnt/.ix-apps
pool1/ix-apps/app_configs                                                                        700K   320G   564K  /mnt/.ix-apps/app_configs
pool1/ix-apps/app_mounts                                                                        84.0M   320G   104K  /mnt/.ix-apps/app_mounts
pool1/ix-apps/app_mounts/bookshelf                                                              1.88M   320G    96K  /mnt/.ix-apps/app_mounts/bookshelf
pool1/ix-apps/app_mounts/bookshelf/config                                                       1.78M   320G  1.76M  /mnt/.ix-apps/app_mounts/bookshelf/config
pool1/ix-apps/app_mounts/odoo                                                                   81.9M   320G   104K  /mnt/.ix-apps/app_mounts/odoo
pool1/ix-apps/app_mounts/odoo/addons                                                              96K   320G    96K  /mnt/.ix-apps/app_mounts/odoo/addons
pool1/ix-apps/app_mounts/odoo/data                                                              19.0M   320G  19.0M  /mnt/.ix-apps/app_mounts/odoo/data
pool1/ix-apps/app_mounts/odoo/postgres_data                                                     62.7M   320G  62.7M  /mnt/.ix-apps/app_mounts/odoo/postgres_data
pool1/ix-apps/docker                                                                            7.37G   320G  7.37G  /mnt/.ix-apps/docker
pool1/ix-apps/truenas_catalog                                                                    412M   320G   412M  /mnt/.ix-apps/truenas_catalog
pool1/share01                                                                                    630G   320G   630G  /mnt/pool1/share01
pool1/share02                                                                                   31.2M   320G  31.1M  /mnt/pool1/share02
pool1/share02/newstore                                                                            96K   320G    96K  /mnt/pool1/share02/newstore
```

## Storage Usage & Directory Hierarchy
```text
Filesystem      Size  Used Avail Use% Mounted on
pool1           321G  4.8M  321G   1% /mnt/pool1

Network Traffic Ingest Hierarchy:
total 39K
drwxrwxrwx 432 truenas_admin truenas_admin  432 Sep  2 09:39 devices
-rwxrwxrwx   1 truenas_admin truenas_admin  14K Sep  2 09:39 dns_cache.json
drwxrwxrwx   2 truenas_admin truenas_admin    3 Sep  2 08:37 logs
drwxrwxrwx   2 truenas_admin truenas_admin    3 Sep  2 09:39 raw_pcaps
drwxrwxrwx   2 truenas_admin truenas_admin    5 Sep  2 09:05 scripts
-rwxrwxrwx   1 truenas_admin truenas_admin 7.8K Sep  2 09:39 subnet_summary.csv
```
