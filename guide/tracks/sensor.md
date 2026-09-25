---
name: Sensor rig
does: Something that measures
lede: >-
  The fastest route to a credible result. There are no moving parts to crash, and the proof is
  data anyone can check.
first: A sensor node that records one quantity for a week without a gap, and shows it on a live dashboard.
examples:
  - Soil moisture along a garden bed, logged every ten minutes (agriculture)
  - A balcony solar panel's output against the weather (energy)
  - Vibration and temperature on a delivery trolley over a day (logistics)
budget: Under €250
time: 2–6 weeks
hardest: Running unattended. Power, Wi-Fi and enclosures fail long before the sensor does.
---

## Plan

One quantity, one place, and one question the data should answer.

- "Does the soil dry out faster at the south end of the bed?" beats "monitor the garden".
- Decide how often to measure, and for how long, before choosing the parts.

## Simulate

Wire and code the circuit in [[Wokwi]] before the parts arrive, and build the dashboard against
made-up data.

- Move to [[PlatformIO]] once the Arduino IDE gets in the way.
- A dashboard that already works with fake data is ready the day real data arrives.

## Parts

An ESP32 or [[Arduino]] board, the sensor, a power supply and an enclosure, from [[BerryBase]]
or [[reichelt elektronik]].

- [[ESPHome]] — Turns an ESP32 into a networked sensor from a short YAML file.
- [[Raspberry Pi]] — When the node needs a camera or heavier processing.

## Build

Get one reading on the bench, then leave it running on your desk for 24 hours before it goes
anywhere else.

- Send readings to [[Grafana]], or at least to a CSV file, from the first one.
- When a sensor bus misbehaves, a cheap logic analyser with [[sigrok]] shows what is actually on
  the wire.

## Test

Install it where it will stay, and leave it alone: a week without a gap is the bar.

- Check power and Wi-Fi at the installation spot first. The corner that needs the sensor is
  rarely where the router is.
- Compare against a reference where one exists, such as [[DWD Open Data]] for the weather.

## Show

Publish the week of data and the dashboard, not a screenshot of them.

- Share the dashboard or a [[Streamlit]] page so others can explore the data themselves.
- Archive the dataset on [[Zenodo]], so it can be cited.
