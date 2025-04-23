from app import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(
        host=app.config.get("IP_HOST", "localhost"),
        port=app.config.get("PORT_HOST", 8000),
        debug=app.config.get("DEBUG", True),
        use_reloader=False,
    )
