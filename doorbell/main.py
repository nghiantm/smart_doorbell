import logging
from doorbell_camera import Doorbell

if __name__ == "__main__":
    # set up logging
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    doorbell = Doorbell()
    doorbell.run()