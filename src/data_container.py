from src.events import Events

global containerized_events
containerized_events = Events()


def set_containerized_events(events):
    global containerized_events
    containerized_events = events


def get_containerized_events():
    global containerized_events
    return containerized_events
