from pet_walking_service import process_walking_routes, inspect_gps_collars
from CodeCoverageTest_PES2UG24AM169_application import route, walk

# Branch-focused cases deliberately exercise both outcomes of each decision.
def test_all_session_type_branches():
    routes = [route("standard_60", [walk(1)]), route("standard_30", [walk(1)]),
              route("express_15", [walk(1)]), route("unknown", [walk(1)])]
    result = process_walking_routes(routes, 4)
    assert result["total_revenue"] == 86.0


def test_confirmed_and_unconfirmed_routes():
    result = process_walking_routes([route(confirmed=False), route(walks=[walk()])], 5)
    assert result["total_revenue"] == 27


def test_pet_count_and_aggression_branches():
    routes = [route("standard_30", [walk(0), walk(1, aggression=True), walk(4), walk(3)])]
    result = process_walking_routes(routes, 5)
    assert result["total_revenue"] == 85.6


def test_standard_sixty_aggression_break_branch():
    result = process_walking_routes([route("standard_60", [walk(1), walk(1, aggression=True), walk(3)])], 5)
    assert result["total_revenue"] == 0


def test_medication_and_weekend_true_false():
    routes = [route(walks=[walk(1, meds=True)], weekend=True), route(walks=[walk(1)], weekend=False)]
    assert process_walking_routes(routes, 5)["total_revenue"] == 65.0


def test_incident_audit_and_completed_and_zero_statuses():
    assert process_walking_routes([route(walks=[walk(0)] * 5)], 1)["status"] == "INCIDENT_AUDIT"
    assert process_walking_routes([route(walks=[walk()])], 1)["status"] == "COMPLETED"
    assert process_walking_routes([], 1)["status"] == "ZERO_EARNINGS"


def test_gps_empty_outer_and_empty_inner_lists():
    assert inspect_gps_collars([]) == "NO_DATA"
    assert inspect_gps_collars([[]]) == "ONLINE"


def test_gps_low_signal_streak_resets_and_alerts():
    assert inspect_gps_collars([[10, 20, 10]]) == "ONLINE"
    assert inspect_gps_collars([[20, 19, 19]]) == "LOST_SIGNAL_ALERT"


def test_invalid_routes_and_negative_fee_validation_branches():
    import pytest
    with pytest.raises(ValueError):
        process_walking_routes(None, 5)
    with pytest.raises(ValueError):
        process_walking_routes([], -0.01)
