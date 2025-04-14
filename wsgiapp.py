
from app import app
from waitress import serve
import platform

if __name__ == "__main__":
    current_os = platform.system()

    if current_os == "Windows":
        print("Running Flask app with Waitress on Windows...")
        serve(app, host="0.0.0.0", port=8000)
    else:
        print("For Linux/macOS, you can run this with Gunicorn:")
        print("  gunicorn wsgi:app")
        from gunicorn.app.base import Application
        from gunicorn import util

        class WSGIApplication(Application):
            def init(self, parser, opts, args):
                self.app_uri = None
                if len(args) > 0:
                    self.cfg.set("default_proc_name", args[0])
                    self.app_uri = args[0]
                if self.app_uri is None:
                    if self.cfg.wsgi_app is not None:
                        self.app_uri = self.cfg.wsgi_app
                    else:
                        raise ConfigError("No application module specified.")

            def load_config(self):
                super().load_config()
                if self.app_uri is None:
                    if self.cfg.wsgi_app is not None:
                        self.app_uri = self.cfg.wsgi_app
                    else:
                        raise ConfigError("No application module specified.")

            def load_wsgiapp(self):
                return util.import_app(self.app_uri)

            def load(self):
                return self.load_wsgiapp()


        WSGIApplication("%(prog)s [OPTIONS] [APP_MODULE]").run()
