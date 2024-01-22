# Currency App Tool

Monitor currency, price and manipulating

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [Frontend](#frontend)
  - [Backend](#backend)
- [Configuration](#configuration)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

Integrated with 3rd API to get the info and analyze the price

## Features

Highlight the key features of your project.

- Fetch API
- Visualize data
- Automation via CRON

## Prerequisites

Prerequisites need to have installed:

- Node.js and npm (for React frontend)
- Python and Django (for backend)

## Getting Started

Read below to start the intallation:

### Frontend

1. Navigate to the `frontend` directory:

```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the server
``` bash
npm start
```

The React app should now be running on http://localhost:3000.

### Backend

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies using a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```

3. Apply migrations:
```bash
python manage.py migrate
```

4. Start the Django development server:
```bash
python manage.py runserver
```

The Django backend should now be running on http://localhost:8000.
