import investigator.code_tools as code_tools

def test_list_directory(tmp_path, monkeypatch):

    (tmp_path / "app.py").write_text("Hello")
    (tmp_path / "database.py").write_text("Database")

    (tmp_path / "logs").mkdir()

    monkeypatch.setattr(code_tools, "WORKING_DIR", tmp_path )

    result = code_tools.list_directory()

    assert "Files" in result
    assert "Folders" in result

    assert "app.py" in result["Files"]
    assert "database.py" in result["Files"]
    assert "logs" in result["Folders"]

def test_read_file(tmp_path, monkeypatch):

    fake_file = tmp_path / "database.py"

    fake_file.write_text(
        "def connect_to_database():\n"
        "   return True\n",
        encoding="utf-8"
    )

    monkeypatch.setattr(code_tools, "WORKING_DIR", tmp_path)

    result = code_tools.read_file("database.py")

    assert isinstance(result, str)
    assert "def connect_to_database()" in result
    assert "return True" in result

def test_read_file_access_denied(tmp_path, monkeypatch):

    allowed_dir = tmp_path / "sample_app"
    allowed_dir.mkdir()

    secret_file = tmp_path / ".env"
    secret_file.write_text(
        "GEMINI_API_KEY=fake_api_key",
        encoding="utf-8"
    )

    monkeypatch.setattr(code_tools, "WORKING_DIR", allowed_dir)

    result = code_tools.read_file("../.env")

    assert result == "Access denied"