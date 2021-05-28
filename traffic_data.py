from herepy import (
    TrafficApi,
    IncidentsCriticalityStr,
    IncidentsCriticalityInt,
    FlowProximityAdditionalAttributes,
)

traffic_api = TrafficApi(api_key="ENTER-API-KEY")


def get_incident_count(latitude, longitude):
    response = traffic_api.incidents_via_proximity(
        latitude=latitude,
        longitude=longitude,
        radius=15000,
        criticality=[
            IncidentsCriticalityInt.critical,
            IncidentsCriticalityInt.major,
        ],
    )
    response_dict = response.as_dict()

    incident_count = len(response_dict["TRAFFICITEMS"]["TRAFFICITEM"])

    return incident_count
