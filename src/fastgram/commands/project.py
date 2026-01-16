import typer
from pathlib import Path
from rich.console import Console


"""
fastgram - A modern CLI tool for FastAPI developers

This module provides commands for initializing FastAPI projects
and managing development servers.

Usage:
    fastgram init <project_name>    - Create new FastAPI project structure
    fastgram help                   - Show available commands
"""


console_router = typer.Typer()
console = Console()


FOLDERS = [
    "service",
    "core",
    "database",
    "schema",
    "api",
    "views",
    "middleware",
]


@console_router.command("init")
def init_command(
    name: str = typer.Argument(
        "backend",
        help="Project folder name (default: backend)"
    ),
):
    project_dir = Path(name)

    if project_dir.exists():
        console.print(
            f"❌ Directory '{name}' already exists",
            style="bold red"
        )
        raise typer.Exit(code=1)

    console.print(f"🚀 Initializing FastAPI project: [bold]{name}[/bold]")

    project_dir.mkdir()

    for folder in FOLDERS:
        folder_path = project_dir / folder
        folder_path.mkdir(parents=True)
        (folder_path / "__init__.py").touch()

    main_py = project_dir / "main.py"
    main_py.write_text(
        '''"""FastAPI application module.

This module contains the main FastAPI application instance and all
registered routes. The application is created using FastAPI framework
with automatic OpenAPI documentation generation.

To run the application:
    python manage.py runserver

The application will be available at http://127.0.0.1:8000
API documentation: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc
"""
from fastapi import FastAPI

from middleware.loader import load_middlewares


app = FastAPI(
    title="FastAPI Project",
    description="A modern FastAPI application",
    version="1.0.0",
)
load_middlewares(app)


@app.get("/")
async def root():
    return {"status": "ok", "message": "Welcome to FastAPI"}
'''
    )

    manage_py = project_dir / "manage.py"
    manage_py.write_text(
        '''
"""
Script for FastAPI projects.

This utility provides a set of commands to help you manage your FastAPI
application during development.

Usage:
    python manage.py <command> [options]

Available commands:
    runserver    Start the development server
    migrate      Create database tables
    startapp     Create a new application
    help         Show this help message

Options for runserver:
    --host HOST     Bind to this host (default: 127.0.0.1)
    --port PORT     Bind to this port (default: 8000)
    --noreload      Disable auto-reload

Options for startapp:
    <name>        Name of the application to create
"""

import sys
import uvicorn
from settings import HOST, PORT, RELOAD


def main():
    """Run administrative tasks."""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]

    host = HOST
    port = PORT
    reload = RELOAD

    i = 0
    while i < len(args):
        if args[i] == "--host" and i + 1 < len(args):
            host = args[i + 1]
            i += 2
        elif args[i] == "--port" and i + 1 < len(args):
            port = int(args[i + 1])
            i += 2
        elif args[i] == "--noreload":
            reload = False
            i += 2
        else:
            i += 1

    if command == "runserver":
        print(f"🚀 Starting server at http://{host}:{port}")
        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            reload=reload,
        )

    elif command == "migrate":
        print("🗄️  Running database migrations...")
        import asyncio
        from fastgram.database import init_db

        async def run_migrate():
            try:
                print("📊 Checking database connection...")
                await init_db()
                print("✅ Database tables created successfully!")
                print("🎉 Migration completed!")
            except Exception as e:
                print(f"❌ Migration failed: {e}")
                sys.exit(1)
        asyncio.run(run_migrate())

    elif command == "help":
        print(__doc__)
    else:
        print(f"Unknown command: {command}")
        print("Run 'python manage.py help' for usage information.")
        sys.exit(1)


if __name__ == "__main__":
    main()
'''
    )

    middleware_dir = project_dir / "middleware"

    (middleware_dir / "cors.py").write_text(
        '''"""CORS Middleware for FastAPI.

Provides Cross-Origin Resource Sharing (CORS) support
to allow cross-origin requests.
"""
from starlette.middleware.cors import CORSMiddleware


class CORSMiddleware(CORSMiddleware):
    """Custom CORS Middleware with permissive settings."""

    def __init__(self, app):
        super().__init__(
            app,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )
'''
    )

    (middleware_dir / "request_id.py").write_text(
        '''"""Request ID Middleware for FastAPI.

Adds a unique request ID to each incoming request
and includes it in the response headers.
"""
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Middleware that assigns a unique ID to each request."""

    async def dispatch(self, request: Request, call_next):
        request_id = uuid.uuid4().hex
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response
'''
    )

    (middleware_dir / "logging.py").write_text(
        '''"""Logging Middleware for FastAPI.

Logs incoming HTTP requests with method and URL.
"""
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware that logs basic request information."""

    async def dispatch(self, request: Request, call_next):
        print(f"[REQ] {request.method} {request.url}")
        return await call_next(request)
'''
    )

    (middleware_dir / "rate_limit.py").write_text(
        '''"""Rate Limit Middleware for FastAPI.

Limits the number of requests from a single IP address.
Uses in-memory storage by default.
"""
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from fastapi import status

from settings import RATE_LIMIT_LIMIT


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware that rate limits requests by IP address."""

    def __init__(self, app):
        super().__init__(app)
        limit, window = RATE_LIMIT_LIMIT.split("/")
        self.limit = int(limit)
        self.window_seconds = 1 if window == "second" else 60
        self.requests: dict[str, list[float]] = {}

    async def dispatch(self, request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()

        if client_ip in self.requests:
            self.requests[client_ip] = [
                t for t in self.requests[client_ip]
                if now - t < self.window_seconds
            ]
        else:
            self.requests[client_ip] = []

        if len(self.requests[client_ip]) >= self.limit:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={"error": "Too Many Requests"},
            )

        self.requests[client_ip].append(now)

        return await call_next(request)
'''
    )

    (middleware_dir / "loader.py").write_text(
        '''"""Middleware loader utility.

Automatically loads all middlewares defined in settings.MIDDLEWARE
and applies them to the FastAPI application.
"""
import importlib

from fastapi import FastAPI

from settings import MIDDLEWARE


def load_middlewares(app: FastAPI) -> None:
    """Load and register all middlewares from settings."""
    for dotted_path in MIDDLEWARE:
        module_path, class_name = dotted_path.rsplit(".", 1)
        module = importlib.import_module(module_path)
        middleware_class = getattr(module, class_name)
        app.add_middleware(middleware_class)
'''
    )

    settings_py = project_dir / "settings.py"

    # Generate a secure secret key for this project
    import secrets
    secret_key = secrets.token_urlsafe(32)

    settings_py.write_text(
        f'''"""Application settings.

Contains configuration for the FastAPI application,
including middleware registration and server settings.
"""


# Server settings
HOST = "127.0.0.1"
PORT = 8000
RELOAD = True

# Database settings
DB_URL = "sqlite+aiosqlite:///./db.sqlite3"

# Rate limit settings
RATE_LIMIT_LIMIT = "5/second"


SECRET_KEY = "{secret_key}"

# Middleware registration
# Order matters: middlewares are applied from top to bottom
MIDDLEWARE = [
    "middleware.rate_limit.RateLimitMiddleware",
    "middleware.logging.LoggingMiddleware",
    "middleware.cors.CORSMiddleware",
    "middleware.request_id.RequestIDMiddleware",
]
'''
    )

    # === Database setup (imported directly from fastgram.database) ===
    # No need to create database.py - use fastgram.database directly

    console.print("✅ Project structure created successfully!",
                  style="bold green")
    console.print(
        f"👉 Next steps:\n"
        f"✅ cd {name}"
    )
