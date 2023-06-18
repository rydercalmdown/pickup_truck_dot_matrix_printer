# Turning my pickup truck into a dot matrix printer
A machine that attaches to a trailer hitch and writes on roads using water. It's basically a giant water dot matrix printer.

---

## Deploying To Raspberry Pi
To deploy to a pi, copy the src directory to a raspberry pi, and run the following:

```bash
bash install_pi.sh
```

This should take care of installing all base components and python dependencies for the project.

---

## Running
Run the following command to start the application. It will test the relays and then start a webserver accessible on 0.0.0.0:8000.

```bash
python app.py
```

---

## Notes
To adjust GPIO pins, change the order of RelayChannel modules in RelayMasterController.
