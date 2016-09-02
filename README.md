# CSLab: Anomaly Alarm
The purpose of this project is to study and implement network anomaly detection algorithms using Python, SQL, and the [Toa Network Flow Data Monitoring System](https://github.com/cslab-uprrp/toa) as tools to gather and analyze data. This will be integrated into Toa as an automatic anomaly detection system that will generate alarms and alerts for system administrators.

#### Modules:
1. `dataquery.py`: Handles connections to the database and the queries used to extract the network flow data from the database.

2. `anomalyAlgorithms.py`: Implementation of the algorithms, and any extra data manipulation.

3. `client.py`: Gathers the data sets and runs the algorithms.

4. `graph.py`: Takes care of generating graphs to visualize the data using `chart.js`.

Currently, It's set up to work as a cron job to gather data for tests:
```
*/5 * * * * ../../usr/bin/python /home/user/client.py time.md ID
*/5 * * * * ../../usr/bin/python /home/user/updateTime.py
```
This can be set up with the `crontab -e` command. Setup your desired start time using the `time.md` file:

```
DD/MM/YYYY 00:00:00
```

### Setup:
Set your database credentials within a `credentials.py` file, as seen in the `credentialstemplate.py` file example:

```python
login = {
	'user' : "username",
	'password': "password",
	'db': "database",
	'host': "hostname"
	'port': "port"
}
```

The `requirements.txt` file includes all of the dependencies, which can easily be installed using `pip`:

```
$ pip install -r requirements.txt
```

Use of a virtual environment is recommended. Run with:

```
$ python app.py
```
