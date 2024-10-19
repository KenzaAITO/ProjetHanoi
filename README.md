## Introduction


## Features

- **Real-time tracking:** Track the location of objects or people in real-time within a defined area.
- **Scalability:** The system supports multiple nodes, allowing for the tracking of multiple targets simultaneously.
- **Low-cost solution:** Utilize affordable Arduino boards and compatible wireless communication modules for cost-effective implementation.
- **Customizability:** The project provides a flexible framework that can be adapted to different use cases and requirements.
- **Arduino compatibility:** Designed to work with various Arduino boards and compatible hardware, providing a wide range of options for hardware selection.

## Prerequisites


## Libraries


## Dependencies

List any Python dependencies here that need to be installed.


## Getting Started

### Setup

1. **Install MQTT Broker:** 


2. **Run the Project:**
    ```bash
    poetry run python main.py
    ```

### Visualization

The visualization code focuses on plotting the latest positions of the tags without printing updates. The plot should update with the latest positions received from the MQTT messages.

1. **Set up distances between anchors:** Ensure the distances are correctly set in `constants.py` and the tag's code.

2. **Run the visualization code:**
    ```bash
    python3 main.py
    ```
3. **Access the visualization:** Dash is running on `http://127.0.0.1:8050/`.

## Architecture


## Structure diagram 

graph TD;


## Devices


- **Robot:** An MQTT server to receive all the position data from the tags. Note: The default configuration may not allow you to correctly receive the tag's position.

- **Python Visualization:** Subscribes to the MQTT broker and visualizes the position data.

## Sequence Diagram: 


## Algoritm


## Future Enhancements

