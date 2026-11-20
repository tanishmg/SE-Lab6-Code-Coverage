import pytest
from pet_walking_service import process_walking_routes, inspect_gps_collars


def route(session="standard_30", walks=None, confirmed=True, weekend=False):
    return {"route_confirmed": confirmed, "session_type": session,
            "walks": [] if walks is None else walks, "is_weekend": weekend}


def walk(pets=1, aggression=False, meds=False):
    return {"num_pets": pets, "aggression_alert": aggression, "needs_meds": meds}


def test_standard_30():
    assert process_walking_routes([route(walks=[walk()])], 5) == {"total_revenue": 27.0, "status": "COMPLETED"}


def test_standard_60_and_meds():
    assert process_walking_routes([route("standard_60", [walk(2, meds=True)])], 5)["total_revenue"] == 51.0


def test_express_and_large_group():
    assert process_walking_routes([route("express_15", [walk(4)])], 5)["total_revenue"] == 41.4


def test_unconfirmed_and_unknown_session_are_skipped():
    result = process_walking_routes([route(confirmed=False, walks=[walk()]), route("premium", [walk()])], 5)
    assert result == {"total_revenue": 0.0, "status": "ZERO_EARNINGS"}


def test_invalid_pet_count_records_incident():
    result = process_walking_routes([route(walks=[walk(0)])], 5)
    assert result["status"] == "ZERO_EARNINGS"


def test_aggression_on_sixty_minute_route_cancels_route():
    result = process_walking_routes([route("standard_60", [walk(), walk(aggression=True), walk(2)])], 5)
    assert result["total_revenue"] == 0.0


def test_aggression_on_other_route_does_not_add_earnings_for_that_walk():
    result = process_walking_routes([route("standard_30", [walk(aggression=True), walk(2)])], 5)
    assert result["total_revenue"] == 32.0


def test_weekend_transport_fee():
    result = process_walking_routes([route(walks=[walk()], weekend=True)], 7)
    assert result["total_revenue"] == 34.0


def test_more_than_four_incidents_triggers_audit():
    result = process_walking_routes([route(walks=[walk(0)] * 5)], 5)
    assert result["status"] == "INCIDENT_AUDIT"


def test_route_validation():
    with pytest.raises(ValueError):
        process_walking_routes("not-a-list", 5)
    with pytest.raises(ValueError):
        process_walking_routes([], -1)


def test_gps_no_data_and_online():
    assert inspect_gps_collars([]) == "NO_DATA"
    assert inspect_gps_collars([[20, 19, 20, 18]]) == "ONLINE"


def test_gps_lost_signal_streak():
    assert inspect_gps_collars([[10, 19]]) == "LOST_SIGNAL_ALERT"
