py_arris_exporter
===============
This is a python script, installed into Docker, which facilitates scraping Arris SB6183 cablemodems for their relevant RF data and surfacing that to prometheus.

![Screenshot of grafana dashboard](/doc/ae-screenshot.png?raw=true "Screenshot")

## How to use
There are three methods one could use to run this software:

  * [Run the script on a machine locally](#local)
  * [Run the docker container on a docker host](#docker)
  * [Deploy to Kubernetes via Helm](#helm)

## local
One can install this app by running `pip install .` in the source directory.  If you're curious about prerequisites, check setup.py.  Once installed, executing `py_arris_exporter` will start a python webserver on port 9393.  Any request uri to the service will return a set of prometheus metrics.

## docker
You can also run this app as a docker container by executing `docker run -d -p9393:9393 petergrace/arris_exporter` which will spawn a container and daemonize, exposing the port on your local system at port 9393.  This is better if you don't want to commingle your python environment installs.

## helm
If you are leveraging kubernetes, there is a helm chart under the helm/ subdirectory of this repository where you can deploy petergrace/arris_exporter directly to your kubernetes cluster.  It will create a service called `arris-exporter` on a ClusterIP that you can then target with your prometheus install.


## prometheus configuration
Here's a snippet of my scrape config for prometheus inside of my kubernetes environment:

```
- job_name: 'arris'
  static_configs:
    - targets: ['arris-exporter:9393']
```

As you can see, it doesn't have many bells or whistles; it just reports the data I wanted to see to prometheus.

## grafana config
In the grafana/ subdirectory, I have included my grafana dashboard json that I use to query the datapoints from prometheus, to make the screenshot shown above.
