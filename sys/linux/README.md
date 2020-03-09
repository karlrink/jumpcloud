

```
root@b1c426a893fc:/app# apt-get install -y sysstat
root@b1c426a893fc:/app# mpstat
Linux 4.19.76-linuxkit (b1c426a893fc) 	03/08/20 	_x86_64_	(6 CPU)

02:41:31     CPU    %usr   %nice    %sys %iowait    %irq   %soft  %steal  %guest  %gnice   %idle
02:41:31     all    1.27    0.00    2.96    0.02    0.00    0.05    0.00    0.00    0.00   95.70
root@b1c426a893fc:/app# iostat
Linux 4.19.76-linuxkit (b1c426a893fc) 	03/08/20 	_x86_64_	(6 CPU)

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           1.27    0.00    3.01    0.02    0.00   95.70

Device:            tps    kB_read/s    kB_wrtn/s    kB_read    kB_wrtn
sda              10.37         4.42        43.87     430431    4272180
scd0              0.03         1.84         0.00     178802          0
scd1              0.00         0.00         0.00        132          0
scd2              0.04         2.67         0.00     259756          0

root@b1c426a893fc:/app#
```




