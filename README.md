# Fiscalização Checklist System

## Overview

This project provides a webhook-based automation system that processes planning checklists from Way-V and automatically creates execution checklists. The system acts as a bridge between planning and execution phases by automating the workflow.

![Project Workflow](https://via.placeholder.com/800x400?text=Webhook+Processing+Flow)

## Features

- **Webhook Processing**: Automatically receives and processes checklist planning data
- **Item Filtering**: Identifies enabled items from different checklist types (FA, FT, FO, GC, VC)
- **Automatic Checklist Creation**: Creates execution checklists based on webhook data
- **Form Template Cache**: Maintains a local cache of form templates for faster processing
- **Static ngrok Domain**: Uses a reserved domain for consistent webhook endpoint access

## Installation

### Requirements

- Python 3.8+
- pip (Python package manager)

### Dependencies

```
pip install fastapi nest-asyncio pyngrok uvicorn requests
```

## Configuration

1. **ngrok Authentication**

   Update the ngrok auth token in `main.py`:

   ```python
   # In main.py, find the configurar_ngrok function
   def configurar_ngrok():
       try:
           auth_token = "YOUR_NGROK_AUTH_TOKEN_HERE"
           conf.get_default().auth_token = auth_token
           print("✅ ngrok configurado com sucesso!")
           return True
       except Exception as e:
           print(f"❌ Erro ao configurar ngrok: {e}")
           return False
   ```

2. **Static Domain Setup**

   Update your static domain in `main.py`:

   ```python
   # In main.py, find the main function
   public_url = criar_tunel_ngrok(8000, "YOUR-STATIC-DOMAIN.ngrok-free.app")
   ```

## Running the Application

### Standard Mode

Start the application server:

```bash
python main.py
```

### Test Mode

Run a quick system test without starting the server:

```bash
python main.py --teste
```

## How It Works

1. **Webhook Receives Planning Data**: External system sends planning data with enabled items
2. **Template Cache Update**: System refreshes template cache for latest data
3. **Item Processing**: System extracts details for enabled items from templates
4. **Checklist Creation**: Creates an execution checklist with all enabled items
5. **Response**: Returns status information and checklist ID

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/webhook` | POST | Main webhook endpoint for receiving planning data |
| `/itens-habilitados` | GET | Returns enabled items from last webhook |
| `/recarregar-cache` | GET | Force reload of the forms cache |
| `/status-cache` | GET | Check cache status and age |
| `/ultimo-checklist` | GET | Returns the ID of the most recently created checklist |

## Component Descriptions

- **main.py**: Main orchestration file that configures the system and starts the server
- **webhook.py**: Processes webhook data and extracts relevant information
- **GET.py**: Handles template retrieval and caching
- **POST.py**: Creates new checklists through the API

## Debugging

- The system creates a `cache_formularios.json` file for caching templates
- The last webhook data is saved to `ultimo_webhook.json` for debugging

## Troubleshooting

1. **ngrok Errors**: 
   - Verify your authentication token is correct and has sufficient permissions
   - Check if the static domain is correctly registered with your account

2. **Cache Issues**:
   - Delete `cache_formularios.json` and restart to force a fresh cache

3. **Duplicate Webhooks**:
   - The system includes deduplication to prevent double-processing

## Further Assistance

For questions or issues with this system, please contact the developer.
