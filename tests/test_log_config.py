import unittest
from unittest.mock import patch, MagicMock
import logging
import os
from src.log_config import setup_logging, MaxLevelFilter


class TestLogConfig(unittest.TestCase):
    """
    Unit tests for the logging configuration and custom logging filters.

    This class contains tests for verifying the correct setup of logging handlers, 
    log levels, and the behavior of the `MaxLevelFilter`. It ensures that the logging 
    system behaves as expected when `setup_logging` is called, and that custom 
    filtering mechanisms operate correctly.

    Methods:
    --------
    setUp():
        Resets the logging configuration before each test to ensure a clean environment.
        Clears any existing handlers to simulate a fresh logger state.

    test_setup_logging_sets_correct_handlers():
        Tests that the `setup_logging` function properly configures two handlers:
        - A DEBUG level handler that logs detailed debugging information.
        - An ERROR level handler that logs error messages only.
        Also checks that each handler is correctly assigned a formatter and 
        added to the logger.

    test_max_level_filter():
        Verifies the behavior of the `MaxLevelFilter`, ensuring it filters log records 
        based on their log level.
        - Allows log messages at levels DEBUG, INFO, and WARNING.
        - Blocks log messages at levels above WARNING (e.g., ERROR).

    Usage:
    ------
    Run this test suite using a unittest-compatible test runner to verify 
    the behavior of the logging configuration.

    Dependencies:
    -------------
    - `unittest`: Python's built-in unit testing framework.
    - `unittest.mock`: Provides the ability to mock objects for testing.
    - `logging`: Python's logging module for log configuration.
    - `os`: Used for filesystem operations in the logging setup.

    Example:
    --------
    To run the tests, use the following command:
        >>> python -m unittest test_log_config.py

    Notes:
    ------
    - This test suite ensures that the `setup_logging` function adheres to 
      best practices by correctly configuring log handlers, levels, and formatters.
    - The `MaxLevelFilter` is tested to ensure it restricts logging messages 
      to the specified maximum level.
    - Mocking is extensively used to simulate file and logger operations without 
      affecting the actual filesystem or logger behavior.

    Raises:
    -------
    AssertionError:
        - If the expected log handlers are not set up correctly.
        - If the log levels and filtering do not match the specified criteria.
    """
    def setUp(self):
        """
        Set up a clean logger state before each test.

        This ensures the logger is reset, with no handlers,
        simulating a fresh logging environment for each test case.
        """
        # Reset any logging configuration before each test
        logger = logging.getLogger()
        logger.handlers = []  # Clear all handlers to simulate a fresh logger

    @patch("os.makedirs")
    @patch("os.path.exists")
    @patch("logging.FileHandler")
    @patch("logging.getLogger")
    def test_setup_logging_sets_correct_handlers(
        self, mock_getLogger, mock_FileHandler, mock_exists, mock_makedirs
    ):
        """
        Test that setup_logging correctly configures logging handlers.

        This verifies that:
        - Two handlers (DEBUG and ERROR) are added to the logger.
        - The DEBUG handler logs at the DEBUG level.
        - The ERROR handler logs at the ERROR level.
        - Each handler has a formatter assigned.
        """
        # Mock log directory doesn't exist
        mock_exists.return_value = False

        # Mock the logger and file handler
        mock_logger = MagicMock()
        mock_logger.hasHandlers.return_value = (
            False  # Ensure that handlers are not reported as existing
        )

        # Simulate a real list for handlers, instead of the default MagicMock list
        mock_logger.handlers = []

        # Manually simulate addHandler behavior
        def add_handler_side_effect(handler):
            mock_logger.handlers.append(handler)

        mock_logger.addHandler.side_effect = add_handler_side_effect

        mock_getLogger.return_value = mock_logger
        mock_debug_handler = MagicMock()
        mock_error_handler = MagicMock()
        mock_FileHandler.side_effect = [mock_debug_handler, mock_error_handler]

        # Call setup_logging
        setup_logging()

        # Ensure the logger's addHandler method is called twice (once for each handler)
        self.assertEqual(mock_logger.addHandler.call_count, 2)

        # Ensure the handlers have correct logging levels
        mock_debug_handler.setLevel.assert_called_once_with(logging.DEBUG)
        mock_error_handler.setLevel.assert_called_once_with(logging.ERROR)

        # Ensure the formatter is set for both handlers
        mock_debug_handler.setFormatter.assert_called_once()
        mock_error_handler.setFormatter.assert_called_once()

        # Now, since we manually appended the handlers, we can check if they were added
        self.assertIn(mock_debug_handler, mock_logger.handlers)
        self.assertIn(mock_error_handler, mock_logger.handlers)

    def test_max_level_filter(self):
        """
        Test the behavior of MaxLevelFilter for filtering log messages by level.

        This checks that:
        - Messages at or below the max level (WARNING) are allowed.
        - Messages above the max level (ERROR) are blocked.
        """
        max_level = logging.WARNING
        log_filter = MaxLevelFilter(max_level)

        # Create mock log records with different levels
        record_debug = MagicMock(levelno=logging.DEBUG)
        record_info = MagicMock(levelno=logging.INFO)
        record_warning = MagicMock(levelno=logging.WARNING)
        record_error = MagicMock(levelno=logging.ERROR)

        # Assertions for the filter behavior
        self.assertTrue(log_filter.filter(record_debug))
        self.assertTrue(log_filter.filter(record_info))
        self.assertTrue(log_filter.filter(record_warning))
        self.assertFalse(log_filter.filter(record_error))
