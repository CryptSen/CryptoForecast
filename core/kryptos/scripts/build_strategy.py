import json
import time
import requests

from flask.helpers import get_debug_flag

import click
import logbook
from flask_jsonrpc.proxy import ServiceProxy
import pandas as pd

from kryptos.strategy import Strategy
from kryptos.data.manager import AVAILABLE_DATASETS
from kryptos import setup_logging
from kryptos.utils.outputs import in_docker
from kryptos.utils.load import get_strat


log = logbook.Logger("Platform")
setup_logging()

REMOTE_API_URL = 'http://kryptos.produvia.com/api'
LOCAL_API_URL = "http://web:5000/api" if in_docker() else 'http://0.0.0.0:5000/api'



@click.command()
@click.option(
    "--market-indicators",
    "-ta",
    multiple=True,
    help="Market Indicators listed in order of priority",
)
@click.option(
    "--machine-learning-models",
    "-ml",
    multiple=True,
    help="Machine Learning Models",
)
@click.option(
    "--dataset", "-d", type=click.Choice(AVAILABLE_DATASETS), help="Include asset in keyword list"
)
@click.option("--columns", "-c", multiple=True, help="Target columns for specified dataset")
@click.option("--data-indicators", "-i", multiple=True, help="Dataset indicators")
@click.option("--json-file", "-f")
@click.option("--python-script", "-p")
@click.option("--paper", is_flag=True, help="Run the strategy in Paper trading mode")
@click.option("--rpc", is_flag=True, help="Run the strategy via JSONRPC")
@click.option("--hosted", "-h", is_flag=True, help="Run via rpc using remote server")
def run(market_indicators, machine_learning_models, dataset, columns, data_indicators, json_file, python_script, paper, rpc, hosted):

    strat = Strategy()

    if python_script is not None:
        strat = get_strat(python_script)

    columns = list(columns)

    for i in market_indicators:
        strat.add_market_indicator(i.upper())

    for i in machine_learning_models:
        strat.add_ml_models(i.upper())

    # currently assigns -i indicator to the column provided at the same index
    if dataset is not None:
        strat.use_dataset(dataset, columns)
        for i, ind in enumerate(data_indicators):
            strat.add_data_indicator(dataset, ind.upper(), col=columns[i])

    if json_file is not None:
        strat.load_json_file(json_file)

    click.secho(strat.serialize(), fg="white")

    if hosted:
        API_URL = REMOTE_API_URL

    else:
        API_URL = LOCAL_API_URL

    if rpc:
        strat_id, queue_name = run_rpc(strat, API_URL, live=paper, simulate_orders=True)
        poll_status(strat_id, queue_name, API_URL)

    else:
        viz = not in_docker()
        strat.run(live=paper, viz=viz)
        result_json = strat.quant_results.to_json()
        display_summary(result_json)


def display_summary(result_json):
    click.secho("\n\nResults:\n", fg="magenta")
    result_dict = json.loads(result_json)
    for k, v in result_dict.items():
        # nested dict with trading type as key
        metric, val = k, v["Backtest"]
        click.secho("{}: {}".format(metric, val), fg="green")


def run_rpc(strat, api_url, live=False, simulate_orders=True):
    click.secho(
        """
        *************
        Running strategy on JSONRPC server at {}
        Visualization will not be shown.
        *************
        """.format(
            api_url
        ),
        fg="yellow",
    )
    rpc_service = ServiceProxy(api_url)
    strat_json = strat.serialize()
    res = rpc_service.Strat.run(strat_json, live, simulate_orders)
    log.info(res)

    if res.get("error"):
        raise Exception(res["error"])

    result = res["result"]
    strat_id = result["data"]["strat_id"]
    queue_name = result["data"]['queue']
    status = result["status"]
    click.secho("Job Started. Strategy job ID: {}".format(strat_id))
    click.secho("status: {}".format(status), fg="magenta")
    return strat_id, queue_name


def poll_status(strat_id, queue_name, api_url):
    rpc_service = ServiceProxy(api_url)
    status = None
    colors = {"started": "green", "failed": "red", "finished": "blue"}
    while status not in ["finished", "failed"]:
        res = rpc_service.Strat.status(strat_id, queue_name)
        status = res["result"]["status"]
        meta = res["result"]["data"]['meta']

        click.secho(json.dumps(meta, indent=2))
        time.sleep(2)

    result_json = res["result"].get("strat_results")
    display_summary(result_json)