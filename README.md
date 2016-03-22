# CSLab: Anomaly Alarm
The purpose of this project is to study and implement network anomaly detection algorithms using Python, SQL, and the [Toa Network Flow Data Monitoring System](https://github.com/cslab-uprrp/toa) as tools to gather and analyze data. Eventually, the aim is to integrate this Anomaly Detection system into Toa.

####Modules:
1. `dataquery.py` - Queries used to extract the network flow data from the database.
2. `anomalyAlgorithms.py` - Implementation of the algorithms, and any extra data manipulation.
3. `client.py` - Client that brings it all together.
	* Currently needs a lot of work.
		* Refactor out the CSV file generator, for data gathering and analysis.
		* Refactor out the graph generator, and expand it.
		* Add tests for new algorithms.
4. `graph.py` - Takes care of generating graphs to visualize the data.
	* The output is the graph.js file that will be used to chart, with graph.js.
	* This will be improved with a dashboard application that will graph according to input.


Currently, It's set up to work as a cron job to gather data for tests:

```
*/5 * * * * ../../usr/bin/python /home/user/client.py time.md ID
*/5 * * * * ../../usr/bin/python /home/user/updateTime.py
```

This can be set up with the `crontab -e` command.

####Coming soon:
1. Implement and test new algorithms:
	* K-Nearest Neighbor - Implemented, not tested as of yet.
	* Linear Regresion
	* Moving Average
2. There's always room for code improvement...
3. Visualization dashboard.
4. Voting system for the algorithms (only generate alarm when most algorithms detect an anomaly).