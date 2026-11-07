from ytagent.cli import build_report, main


def test_report_for_eligible_channel():
    assert build_report(1500, 4200) == "Eligible for the YouTube Partner Program."


def test_report_includes_gap_and_estimate():
    report = build_report(710, 2500, subs_per_day=22.5, hours_per_day=40)
    assert "290 needed" in report
    assert "Estimated days: 38" in report


def test_report_handles_stalled_growth():
    assert "never" in build_report(500, 100, subs_per_day=5, hours_per_day=0)


def test_main_prints_report(capsys):
    assert main(["900", "4000"]) == 0
    assert "100 needed" in capsys.readouterr().out
