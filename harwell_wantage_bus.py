import requests
import json
import re
import pprint

api_secrets_file = 'transportapi_secrets.json'

transport_api_url_base = "https://transportapi.com/v3/uk/"
bus_stop_atocode = "340000368SHE"
wanted_direction = 'Wantage'

def print_json(json_data):

    pprint.PrettyPrinter().pprint(json_data)

def load_api_secrets(filename):

    try:
        with open(filename, 'r') as fp:
            api_params = json.load(fp)
    except Exception as e:
        print('Failed to load API secrets key: {}'.format(e))
        api_params = None

    return api_params


def main():

    api_params = load_api_secrets(api_secrets_file)

    stop_url = transport_api_url_base + 'bus/stop/{}/live.json'.format(bus_stop_atocode)
    stop_params = {
        'group': 'route',
        'nextbuses': 'no',
    }
    request_params = dict(api_params, **stop_params)

    try:
        response = requests.get(stop_url, params=request_params)
        response.raise_for_status()
    except Exception as e:
        print("Failed to retrieve API data: {}".format(e))
        return

    dest_re = re.compile('{}'.format(wanted_direction), re.IGNORECASE)

    live_data = response.json()
    for (route, departures) in live_data['departures'].items():
        for departure in departures:
            if dest_re.search(departure['direction']):
                print(route, departure['direction'], departure['aimed_departure_time'], departure['best_departure_estimate'])


if __name__ == '__main__':

    main()
