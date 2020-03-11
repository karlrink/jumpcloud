
```
<html>
<img src="http://127.0.0.1:8001/plot?host=sdbc10-ca4-01&rrd=ps&ds=procs&display=img">
<img src="http://127.0.0.1:8001/plot?host=sdbc10-ca4-01&rrd=ps&ds=defunct&display=img">
<img src="http://127.0.0.1:8001/plot?host=sdbc10-ca4-01&rrd=sbm&ds=sbm&back=1&scale=hour&display=img">
<img src="http://127.0.0.1:8001/plot?host=sdbc10-ca4-01&rrd=mysql&ds=InnoBufPoolPgsData&back=1&scale=hour&display=img">
</html>
```

<!--

display embeded image... use &display=img

an RRD is the round robin data base file
an RRD file can contain multiple data sources (DS)

for example, the ps.rrd file contains two DS, procs and defunct
  /plot?host=sdbc10-ca4-01&rrd=ps&ds=procs&display=img
  /plot?host=sdbc10-ca4-01&rrd=ps&ds=defunct&display=img

while the sbm.rrd only has a single DS (because this is and was the first i made and was working with...).
  /plot?host=sdbc10-ca4-01&rrd=sbm
so, to embed:
  /plot?host=sdbc10-ca4-01&rrd=sbm&ds=sbm&display=img

I quickly discovered that DS can be stored as 1 to 19 characters [a-zA-Z0-9_].
most programs out there are storing the DS as [0], [1], etc... and using external programming to match DS [0] to a textual display.  They
are doing this to keep the .rrd file to a minumum size.

however, with our setup, the plotter can automatically gen the DS header and display w/o keep track of what DS [2] may or may not be,
and the .rrd file is still pretty small.  1.2 mb for mysql and mysql has 48 DS's
ie...
    cmdline += ' DS:AbortedClients:GAUGE:600:U:U '
    cmdline += ' DS:AbortedConnects:GAUGE:600:U:U '
    cmdline += ' DS:AccessDeniedErrors:GAUGE:600:U:U '
    cmdline += ' DS:BytesReceived:GAUGE:600:U:U '
    cmdline += ' DS:BytesSent:GAUGE:600:U:U '
    cmdline += ' DS:Connections:GAUGE:600:U:U '
    cmdline += ' DS:CreatedTMPFiles:GAUGE:600:U:U '
    cmdline += ' DS:InnoBufPoolPgsData:GAUGE:600:U:U '
    cmdline += ' DS:InnoBufPoolBytsData:GAUGE:600:U:U '
    ...

so, i like the notion of not keeping an index of DS[0], DS[1], ... And just empeding the DS header in the .rrd file.
this allows us to simply read the .rrd file and dispaly ie.

  /plot?host=sdbc10-ca4-01&rrd=mysql
  /plot?host=sdbc10-ca4-01&rrd=mysql&ds=AbortedClients
  /plot?host=sdbc10-ca4-01&rrd=mysql&ds=InnoBufPoolPgsData&display=img


-->

