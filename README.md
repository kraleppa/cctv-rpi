# cctv-rpi

## Server run

```
python server.py -p MobileNetSSD_deploy.prototxt -m MobileNetSSD_deploy.caffemodel -mw 2 -mh 2

```

## Client run

```
python client.py --server-ip <exposed one, not localhost>
```
