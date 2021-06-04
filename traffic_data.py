from herepy import (
    TrafficApi,
    IncidentsCriticalityInt,
)

traffic_api = TrafficApi(api_key="MY_API_KEY")


def get_incident_count(latitude, longitude):

    # make request to HERE Traffic API
    response = traffic_api.incidents_via_proximity(
        latitude=latitude,
        longitude=longitude,
        radius=15000,
        criticality=[
            IncidentsCriticalityInt.critical,
            IncidentsCriticalityInt.major,
        ],
    )

    # convert response to dictionary
    response_dict = response.as_dict()

    # count number of incidents
    incident_count = len(response_dict["TRAFFICITEMS"]["TRAFFICITEM"])

    return incident_count
