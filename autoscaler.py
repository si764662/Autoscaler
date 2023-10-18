#! /home/siv/anaconda3/bin/python3.11
'''
Autoscaler script to handle replicase based on cpu utilization
'''
import requests
import logging
import time

logging.basicConfig(
    filename="/home/siv/Autoscaler/app.log",
    filemode="a",
    format="%(asctime)s- %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger()


def scale_up(replicas):
    """
    Module to scale up the replicas if cpu utilization
    crossed the threshold
    """
    try:
        tries = 0
        while tries < 2:
            no_of_replicas = replicas + 3
            url = "http://localhost:8123/app/replicas"
            headers = {"Content-Type": "application/json", "Accept": "application/json"}
            data = {"replicas": no_of_replicas}
            resp = requests.put(url, json=data, headers=headers)
            if resp.status_code == 204:
                logger.info(f"scaled up the no of replicas: {no_of_replicas}")
                break
            else:
                logger.warn("RETRYING !!!! scaling up relicas ")
                time.sleep(2)
                tries += 1

    except requests.exceptions.HTTPError as error:
        logger.error(f"unable to scale up the replicas {error}")


def scale_down(replicas):
    """
    scale down the number of replicas 
    if the cpu utilization is below threshold
    """
    try:
        tries = 0
        while tries < 2:
            no_of_replicas = replicas - 3
            if no_of_replicas < 3:
                logger.info(
                    f"Enough replicas {no_of_replicas} are running hence no scale down required"
                )
                break
            url = "http://localhost:8123/app/replicas"
            headers = {"Content-Type": "application/json", "Accept": "application/json"}
            data = {"replicas": no_of_replicas}
            resp = requests.put(url, json=data, headers=headers)
            if resp.status_code == 204:
                logger.info(f"scaled down the replicas: {no_of_replicas}")
                break
            else:
                logger.warn("RETRYING !!!! scaling down the replicas")
                time.sleep(2)
                tries += 1

    except requests.exceptions.HTTPError as error:
        logger.error(f"unable to scale down the replicas: {error}")


def current_metrics():
    """
    Module to return the current number of replicas
    Returns: no of replicas of the app
    """

    try:
        tries = 0
        while tries < 2:
            url = "http://localhost:8123/app/status"
            headers = {"Accept": "application/json"}
            resp = requests.get(url, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                break
            else:
                time.sleep(2)
                tries += 1
        replicas = data["replicas"]
        cpu_usage = int(data["cpu"]["highPriority"] * 100)

    except requests.exceptions.HTTPError as err:
        logger.error(f"Error while fetching metrics: {err}")
    return replicas, cpu_usage


def main():
    """
    Module checks the current cpu utilization of the app
    and scaleup /scale down the replicas to maintain the usage within 
    the threshold
    """
    replicas, cpu_usage = current_metrics()
    logger.info(f"current replicas: {replicas}")
    logger.info(f"current CPU utilization: {cpu_usage}")
    if cpu_usage > 80:
        logger.info("scalling up the replicas")
        scale_up(replicas)
    elif cpu_usage < 60:
        logger.info("scalling down the replicas")
        scale_down(replicas)
    else:
        logger.info("CPU usage is within threshold")


if __name__ == "__main__":
    main()

