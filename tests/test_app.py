import unittest
from unittest.mock import patch, MagicMock
import os  # Add this import
import logging  # Add this import
from collections import defaultdict
import app as app_module  # Import the app module
from app import app, generate_metrics, periodic_metrics_generation, display_top_apps
from metrics_manager import MetricsManager
from config import *  # Import all configurations
import threading
import importlib

class TestApp(unittest.TestCase):
    def setUp(self):
        # Create a test client for the Flask app
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Create a new MetricsManager instance for the test
        self.metrics_manager = MetricsManager()

    def tearDown(self):
        """Reset the metrics_manager state after each test."""
        self.metrics_manager.metrics_history.clear()
        self.metrics_manager.exceedance_count.clear()

    def test_metrics_endpoint(self):
        """Test the /metrics endpoint."""
        response = self.client.get('/metrics')
        self.assertEqual(response.status_code, 200)
        self.assertIn(METRIC_NAME.encode(), response.data)

    def test_metrics_endpoint_no_metrics(self):
        """Test the /metrics endpoint when no metrics are available."""
        # Clear the metrics history
        self.metrics_manager.metrics_history.clear()

        # Access the /metrics endpoint
        response = self.client.get('/metrics')

        # Verify the response
        self.assertEqual(response.status_code, 200)
        self.assertIn(METRIC_NAME.encode(), response.data)

        # Verify that the logger was called
        with self.assertLogs(logger='app', level='INFO') as log:
            self.client.get('/metrics')
            self.assertIn("INFO:app:Serving metrics in Prometheus format", log.output)

    @patch('app.generate_metrics')  # Mock generate_metrics to return fixed values
    def test_metrics_endpoint_with_metrics(self, mock_generate_metrics):
        """Test the /metrics endpoint when metrics are available."""
        # Mock generate_metrics to return fixed metrics
        mock_generate_metrics.return_value = {"app1": 1000, "app2": 2000}

        # Simulate metrics in the metrics_manager
        self.metrics_manager.store_metrics({"app1": 1000, "app2": 2000})

        # Access the /metrics endpoint
        response = self.client.get('/metrics')

        # Verify the response
        self.assertEqual(response.status_code, 200)
        self.assertIn(f'{METRIC_NAME}{{app_name="app1"}} 1000'.encode(), response.data)  # Use METRIC_NAME
        self.assertIn(f'{METRIC_NAME}{{app_name="app2"}} 2000'.encode(), response.data)  # Use METRIC_NAME

    @patch('app.random.randint')  # Mock random.randint to return fixed values
    def test_generate_metrics(self, mock_randint):
        """Test the generate_metrics function."""
        # Mock random.randint to return fixed values
        mock_randint.return_value = RANDOM_METRIC_MIN  # All metrics will be RANDOM_METRIC_MIN (1)

        # Generate metrics
        metrics = generate_metrics()

        # Verify the metrics
        self.assertIsInstance(metrics, dict)
        self.assertEqual(len(metrics), NUM_APPS)
        for key, value in metrics.items():
            self.assertTrue(key.startswith('app'))
            self.assertEqual(value, RANDOM_METRIC_MIN)  # All values should be RANDOM_METRIC_MIN (1)

    @patch('app.time.sleep')  # Mock time.sleep to avoid waiting
    @patch('app.generate_metrics')  # Mock generate_metrics to control output
    @patch('app.metrics_manager')  # Mock the metrics_manager used in app
    def test_periodic_metrics_generation(self, mock_metrics_manager, mock_generate_metrics, mock_sleep):
        """Test the periodic_metrics_generation function."""
        # Mock generate_metrics to return a fixed set of metrics
        mock_generate_metrics.return_value = {"app1": THRESHOLD + 1, "app2": THRESHOLD - 1}

        # Mock the metrics_manager instance and its methods
        mock_metrics_manager.exceedance_count = defaultdict(int)
        mock_metrics_manager.process_metrics = lambda metrics, threshold: (
            mock_metrics_manager.exceedance_count.update(
                {app_name: mock_metrics_manager.exceedance_count[app_name] + 1 
                 for app_name, value in metrics.items() if value > threshold}
            )
        )

        # Mock get_top_exceedance_apps to return a valid list of tuples
        mock_metrics_manager.get_top_exceedance_apps.return_value = [("app1", 1)]

        # Temporarily set LOG_TO_CONSOLE_ONLY_EXCEEDINGS to False for this test
        from config import LOG_TO_CONSOLE_ONLY_EXCEEDINGS
        original_setting = LOG_TO_CONSOLE_ONLY_EXCEEDINGS
        LOG_TO_CONSOLE_ONLY_EXCEEDINGS = False

        # Call the function with a limited number of iterations
        periodic_metrics_generation(max_iterations=1)

        # Restore the original setting
        LOG_TO_CONSOLE_ONLY_EXCEEDINGS = original_setting

        # Ensure time.sleep was called
        mock_sleep.assert_called()

        # Ensure generate_metrics was called
        mock_generate_metrics.assert_called()

        # Verify the exceedance_count is updated
        self.assertEqual(mock_metrics_manager.exceedance_count["app1"], 1)
        self.assertEqual(mock_metrics_manager.exceedance_count.get("app2", 0), 0)

        # Verify that the logger was called
        with self.assertLogs(logger='app', level='INFO') as log:
            # Temporarily set LOG_TO_CONSOLE_ONLY_EXCEEDINGS to False for this test
            from config import LOG_TO_CONSOLE_ONLY_EXCEEDINGS
            original_setting = LOG_TO_CONSOLE_ONLY_EXCEEDINGS
            LOG_TO_CONSOLE_ONLY_EXCEEDINGS = False

            periodic_metrics_generation(max_iterations=1)
            self.assertIn("INFO:app:Iteration 0: Metrics processed and logged.", log.output)

            # Restore the original setting
            LOG_TO_CONSOLE_ONLY_EXCEEDINGS = original_setting
        
    @patch('app.metrics_manager')  # Mock the metrics_manager used by the Flask app
    @patch('app.DISPLAY_MODE', 'page')  # Set DISPLAY_MODE to 'page' for this test
    def test_exceeding_endpoint(self, mock_metrics_manager):
        """Test the /exceeding endpoint."""
        # Simulate exceedance counts in the mocked metrics_manager
        mock_metrics_manager.exceedance_count = {"app1": 5, "app2": 3, "app3": 2}
        mock_metrics_manager.get_top_exceedance_apps.return_value = [("app1", 5), ("app2", 3), ("app3", 2)]

        # Access the /exceeding endpoint
        response = self.client.get('/exceeding')

        # Verify the response
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Top 3 Apps Exceeding Threshold', response.data)
        self.assertIn(b'app1', response.data)
        self.assertIn(b'app2', response.data)
        self.assertIn(b'app3', response.data)

    @patch('app.metrics_manager')  # Mock the metrics_manager used by the Flask app
    @patch('app.DISPLAY_MODE', 'invalid')  # Mock DISPLAY_MODE to an invalid value
    def test_exceeding_endpoint_invalid_display_mode(self, mock_metrics_manager):
        """Test the /exceeding endpoint when DISPLAY_MODE is invalid."""
        # Simulate exceedance counts in the mocked metrics_manager
        mock_metrics_manager.exceedance_count = {"app1": 5, "app2": 3, "app3": 2}
        mock_metrics_manager.get_top_exceedance_apps.return_value = [("app1", 5), ("app2", 3), ("app3", 2)]

        # Access the /exceeding endpoint
        response = self.client.get('/exceeding')

        # Verify the response
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Display mode is not set to \'page\' or \'both\'.', response.data)

    @patch('app.DISPLAY_MODE', 'console')  # Mock DISPLAY_MODE to 'console'
    @patch('builtins.print')  # Mock print to test console output
    def test_display_top_apps_console(self, mock_print):
        """Test the display_top_apps function in console mode."""
        top_apps = [("app1", 5), ("app2", 3)]
        display_top_apps(top_apps)
        mock_print.assert_called_with(f"Top {TOP_X_APPS} apps exceeding threshold: {top_apps}")

    @patch('app.DISPLAY_MODE', 'page')  # Mock DISPLAY_MODE to 'page'
    def test_display_top_apps_page_mode(self):
        """Test the display_top_apps function in page mode."""
        top_apps = [("app1", 5), ("app2", 3)]
        display_top_apps(top_apps)
        # No assertion needed since the function only contains a pass statement

    @patch('app.DISPLAY_MODE', 'both')  # Mock DISPLAY_MODE to 'both'
    @patch('builtins.print')  # Mock print to test console output
    def test_display_top_apps_both_mode(self, mock_print):
        """Test the display_top_apps function in both mode."""
        top_apps = [("app1", 5), ("app2", 3)]
        display_top_apps(top_apps)
        mock_print.assert_called_with(f"Top {TOP_X_APPS} apps exceeding threshold: {top_apps}")

    @patch('os.makedirs')  # Mock os.makedirs to avoid creating directories
    @patch('builtins.open', new_callable=unittest.mock.mock_open)  # Mock open to avoid file operations
    def test_write_exceedings_to_file_configuration(self, mock_open, mock_makedirs):
        """Test the WRITE_EXCEEDINGS_TO_FILE configuration."""
        top_apps = [("app1", 5), ("app2", 3)]

        # Mock LOG_TO_FILE to False to prevent the logger from creating directories
        with patch('config.LOG_TO_FILE', False):
            # Test WRITE_EXCEEDINGS_TO_FILE = True
            with patch('config.WRITE_EXCEEDINGS_TO_FILE', True):
                importlib.reload(app_module)  # Reload the app module to apply the new configuration
                app_module.log_exceedings(top_apps)
                mock_makedirs.assert_called_once_with(os.path.dirname(app_module.EXCEEDINGS_FILE_PATH), exist_ok=True)
                mock_open.assert_called_once_with(app_module.EXCEEDINGS_FILE_PATH, "a")
                mock_open().write.assert_called()  # Ensure the file is written to

            # Reset the mock for the next test
            mock_makedirs.reset_mock()
            mock_open.reset_mock()

            # Test WRITE_EXCEEDINGS_TO_FILE = False
            with patch('config.WRITE_EXCEEDINGS_TO_FILE', False):
                importlib.reload(app_module)  # Reload the app module to apply the new configuration
                app_module.log_exceedings(top_apps)
                mock_makedirs.assert_not_called()  # Ensure no directories are created
                mock_open.assert_not_called()  # Ensure no file operations are performed

    def test_log_to_console_configuration(self):
        """Test the LOG_TO_CONSOLE configuration."""
        # Reset the logger's handlers and close any open file handlers
        for handler in app_module.logger.handlers[:]:
            if isinstance(handler, logging.FileHandler):
                handler.close()  # Close the file handler to avoid ResourceWarning
            app_module.logger.removeHandler(handler)

        # Test LOG_TO_CONSOLE = True
        with patch('config.LOG_TO_CONSOLE', True):
            importlib.reload(app_module)  # Reload the app module to apply the new configuration
            self.assertTrue(app_module.LOG_TO_CONSOLE)
            self.assertTrue(any(isinstance(handler, logging.StreamHandler) for handler in app_module.logger.handlers))

        # Reset the logger's handlers and close any open file handlers
        for handler in app_module.logger.handlers[:]:
            if isinstance(handler, logging.FileHandler):
                handler.close()  # Close the file handler to avoid ResourceWarning
            app_module.logger.removeHandler(handler)
        
    def test_log_to_file_configuration(self):
        """Test the LOG_TO_FILE configuration."""
        # Reset the logger's handlers
        app_module.logger.handlers.clear()

        # Test LOG_TO_FILE = True
        with patch('config.LOG_TO_FILE', True):
            importlib.reload(app_module)  # Reload the app module to apply the new configuration
            self.assertTrue(app_module.LOG_TO_FILE)
            self.assertTrue(any(isinstance(handler, logging.FileHandler) for handler in app_module.logger.handlers))

        # Reset the logger's handlers
        app_module.logger.handlers.clear()

        # Test LOG_TO_FILE = False
        with patch('config.LOG_TO_FILE', False):
            importlib.reload(app_module)  # Reload the app module to apply the new configuration
            self.assertFalse(app_module.LOG_TO_FILE)
            self.assertFalse(any(isinstance(handler, logging.FileHandler) for handler in app_module.logger.handlers))

    @patch('app.threading.Thread')  # Mock threading.Thread to avoid starting a new thread
    @patch('app.app.run')  # Mock app.run to avoid running the Flask app
    def test_main(self, mock_app_run, mock_thread):
        """Test the main block when the script is run as the main program."""
        # Import the app module
        import app

        # Simulate running the script as the main program
        with patch('app.__name__', '__main__'):
            # Call the main function directly
            app.main()

        # Verify that threading.Thread was called
        mock_thread.assert_called_with(target=app.periodic_metrics_generation, daemon=True)
        mock_thread.return_value.start.assert_called()

        # Verify that app.run was called
        mock_app_run.assert_called_with(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    unittest.main()