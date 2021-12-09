
based on jumpcloud system_id, we are now collecting telemetry data on most systems.  this data is collected into a round robin database https://en.wikipedia.org/wiki/RRDtool

to view the trending data (data is collected and averaged over 5 min intervals)
we have a script interface that generates .png files on the fly
for example, db01
5e47200b39d027716364c7da "db01" (db01) Ubuntu 16.04 x86_64

to view all graphs at once (default goes back 7 days)
https://monitor.nationsinfocorp.com/plot?system_id=5e47200b39d027716364c7da

now that we have a quick view at each server via server_id,
visually we can start to identify trends and analysis. 
ie.  "ps defunct" jumped out at me for db01.  defunct processes are unusual
using the plotter.py (btw, this code is at https://bitbucket.org/itninfo/jumpcloud.git) we can view isolated occurances of rrd (round robin database) and its data source (aka DS) like so...
https://monitor.nationsinfocorp.com/plot?system_id=5e47200b39d027716364c7da&rrd=ps&ds=defunct

I will write an alert for the "ps defunct" that captures the defunct process and sends an alert much in the same regard are mysql async slave replication failure alerts

the plotter tool has other features that allow one to visually inspect
go back in time one day (24 hours),
https://monitor.nationsinfocorp.com/plot?system_id=5e47200b39d027716364c7da&back=1

go back in time 3 hours,
https://monitor.nationsinfocorp.com/plot?system_id=5e47200b39d027716364c7da&scale=hour&back=3

go back in time and view a certain time frame, yyyy-mm-ddTHH:MM:ss
https://monitor.nationsinfocorp.com/plot?system_id=5e47200b39d027716364c7da&start=2020-03-11T16:45:00&end=2020-03-12T16:45:00








