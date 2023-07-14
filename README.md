# Automated Greenhouse Warning Systems (GWS)

The GWS is a smart way to monitor and take care of your plants using only python, a raspberry pi, and a handful of sensors. 

GWS has two modes of operations, either through a cronjob that executes the monitoring script every predetermined (by the user) time period, or through running a dashboard that visualizes the values for the user. In both cases, the user is notified immediately through telegram in case the plant needs you attention. If the soil is dry, an automatic irrigation system is set up to take care of watering the plant.

Please refer to usage to see how to execute either of the modes of operation.  
 
## Installation

To start using GWS, simply clone this folder somewhere into your system. Make sure you have all dependencies installed and the raspberry pi connected to start using the scripts.

```bash
git clone https://github.com/zahiTouqan/GreenhouseCPS.git
```
For the connection of the raspberry pi, please follow the documentation provided in our project presentation.
## Usage
### Modes of Operation:
* Cronjob:
First open the crontab using
```bash
user@desktop:~/GreenhouseCPS/grove.py$ crontab -e 
```
Then refer to this [tutorial](https://www.adminschoice.com/crontab-quick-reference) to set up the cronjob.

* Dashboard: Ensure that you have streamlit installed on your raspberry pi, then simply run this command on the folder containing dashboard.py. 
 
```bash
user@desktop:~/GreenhouseCPS/grove.py$ streamlit run dashboard.py 
```

Streamlit will also set up a link to view the dashboard using other devices connected to the network.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

[The Greenhouse Initiative Team](https://github.com/zahiTouqan)
