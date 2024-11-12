import zipfile
import os
import io
import unittest
from unittest.mock import patch, MagicMock
from main import open_zip, ls, cd  # Импортируем функции из main.py

class TestZipfileFunctions(unittest.TestCase):
    def setUp(self):
        # Создаем виртуальный zip-файл для тестов
        self.test_zip_path = "test.zip"
        self.zip_data = io.BytesIO()
        with zipfile.ZipFile(self.zip_data, 'w') as zip_file:
            zip_file.writestr("test_dir/test_file.txt", "Sample content")
            zip_file.writestr("test_dir/another_file.txt", "Another sample")

    @patch("zipfile.ZipFile")
    def test_open_zip_success(self, MockZipFile):
        """Test opening a valid zip file successfully."""
        # Настраиваем макет (mock) для успешного открытия zip-файла
        MockZipFile.return_value = zipfile.ZipFile(self.zip_data)
        zip_fs = open_zip(self.test_zip_path)
        
        # Проверяем, что zip_fs не является None, что означает успешное открытие
        self.assertIsNotNone(zip_fs)

    def test_open_zip_failure(self):
        """Test handling a bad zip file."""
        with patch("zipfile.ZipFile", side_effect=zipfile.BadZipFile):
            zip_fs = open_zip("bad_zip_path.zip")
            self.assertIsNone(zip_fs)

    def test_ls_success(self):
        """Test listing files in a directory successfully."""
        with zipfile.ZipFile(self.zip_data, 'r') as zip_fs:
            with patch("builtins.print") as mock_print:
                ls(zip_fs, "test_dir/")
                mock_print.assert_any_call("test_file.txt")
                mock_print.assert_any_call("another_file.txt")

    def test_ls_empty_directory(self):
        """Test listing files in an empty directory."""
        with zipfile.ZipFile(self.zip_data, 'r') as zip_fs:
            with patch("builtins.print") as mock_print:
                ls(zip_fs, "non_existent_dir/")
                mock_print.assert_called_with("Содержимое non_existent_dir/:")
