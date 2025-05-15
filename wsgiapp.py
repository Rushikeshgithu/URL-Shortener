from app import app
from waitress import serve
import platform

if __name__ == "__main__":
    current_os = platform.system()

    if current_os == "Windows":
        print("Running Flask app with Waitress on Windows...")
        serve(app, host="0.0.0.0", port=8000)
    else:
        print("For Linux/macOS, running with embedded Gunicorn app...")

        from gunicorn.app.base import BaseApplication
        import multiprocessing

        class WSGIApplication(BaseApplication):
            def __init__(self, app, options=None):
                self.application = app
                self.options = options or {}
                super().__init__()

            def load_config(self):
                for key, value in self.options.items():
                    self.cfg.set(key, value)

            def load(self):
                return self.application

        options = {
            "bind": "0.0.0.0:8000",
            "workers": multiprocessing.cpu_count() * 2 + 1,
        }

        WSGIApplication(app, options).run()

