import investigator.log_tools as log_tools

def test_search_logs(tmp_path, monkeypatch):

    fake_log = tmp_path / "app.log"

    fake_log.write_text(
        "INFO | Login Successful\n"
        "ERROR | Database timed out\n"
        "ERROR | Connection pool exhausted\n",
        encoding="utf-8"
    )

    monkeypatch.setattr(log_tools, "LOG_FILE", fake_log)

    result = log_tools.search_logs("timed out")

    assert "Database timed out" in result
    assert "Connection pool exhausted" not in result
    assert "Login successful" not in result