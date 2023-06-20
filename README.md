<img width="100" alt="ouster-os1-rev7" src="https://github.com/pjoneja/viam-ouster-lidar/assets/6338447/ebe63242-9824-47ef-82b9-01cfbd476925">

# viam-ouster-lidar
A demo integrating Ouster lidar as a custom component in [Viam](https://www.viam.com). My aim is to see a 3D point cloud and 2D image captured by an Ouster lidar sensor streaming to Viam's app. This demo is written in Python using the [viam-sdk](https://docs.viam.com/program/sdks/) and [ouster-sdk](https://ouster.com/developers/ouster-sdk/).

<img width="1312" alt="Screen Shot 2023-06-20 at 5 13 19 AM 1" src="https://github.com/pjoneja/viam-ouster-lidar/assets/6338447/658fb58c-1830-4867-bf29-7428cd8166d1">

This repo contains two custom components: one named `ouster_lidar` and the other named `simple`. The simple one really should be called a mock, it just sends a pre-existing image and pcd and doesn't use any hardware. I wrote the simple/mock one first to figure out how to write a custom component. Then I extended what I learned to write the ouster_lidar component.

I followed the [examples included in Viam's SDK](https://github.com/viamrobotics/viam-python-sdk/tree/main/examples) to learn how to do this. My main idea is to inherit from the existing Camera class and reuse the associated client and gRPC service. 

## Setup
Install the python packages specified in [requirements.txt](https://github.com/pjoneja/viam-ouster-lidar/blob/main/requirements.txt). I tested on Python 3.10 on MacOS.

```shell
cd path/to/this/directory
python3 -m pip install requirements.txt
```

## Testing
To test my work outside of Viam's app, I run `server.py` as a standalone gRPC server. At the same time, I separately run the client in `test/connect.py` to check that the outputs. This part works great!


## Integrating with Viam's app
Use this config on app.viam.com to run this demo. You may need to modify some paths.

```json
{
  "components": [
    {
      "attributes": {},
      "depends_on": [],
      "model": "pj:demo:mysimple",
      "name": "simple-component",
      "namespace": "pj",
      "type": "simple"
    },
    {
      "attributes": {
        "sensor_hostname": "os-122247000765.local"
      },
      "depends_on": [],
      "model": "pj:demo:myousterlidar",
      "name": "ouster-lidar-component",
      "namespace": "pj",
      "type": "ouster-lidar"
    }
  ],
  "modules": [
    {
      "executable_path": "/Users/pranav.joneja/code/viam/ouster-lidar-demo/run_module.sh",
      "name": "demo-module"
    }
  ],
  "processes": [
    {
      "args": [
        "/Users/pranav.joneja/code/viam/ouster-lidar-demo/server.py"
      ],
      "id": "python",
      "log": true,
      "name": "python3"
    }
  ],
  "remotes": [
    {
      "address": "localhost:9090",
      "insecure": true,
      "name": "python-server"
    }
  ],
  "services": [
    {
      "attributes": {
        "capture_dir": "",
        "sync_interval_mins": 0.1,
        "tags": []
      },
      "name": "data",
      "type": "data_manager"
    }
  ]
}
```

## Run the viam-server
With everything set up, run the server to start the demo!

```shell
viam-server -config <path/to/viam-robot-config.json>
```

Check the 'Control' tab on app.viam.com to see the images obtained from the mock camera and Ouster lidar.

# TODOs
- Fix the pcd MIME type to correctly send 3D point clouds
- What belongs in the driver.py vs model.py? Why are they different?
- Figure out how to use the component config attributes to get the sensor hostname and other sensor-specific values.
- Automatically configure the lidar sensor on startup. Check that the sensor is running and the robot is receiving data.

Here's what the 3D point cloud from the Ouster lidar should look like:
<img width="912" alt="Screen Shot 2023-06-20 at 2 10 06 AM" src="https://github.com/pjoneja/viam-ouster-lidar/assets/6338447/c253b74d-6d03-4348-9a38-5109690bb0c6">
