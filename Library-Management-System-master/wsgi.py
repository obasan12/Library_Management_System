#!/bin/env python
"""
This script runs the Library_Management_System application using a development server.
"""

import os
from Library_Management_System import create_app

application = create_app()  # Create the app instance

if __name__ == "__main__":
    application.run(debug=True)
