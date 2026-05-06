# FastAPI Wrapper for Meeting Ticket Extractor

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from modules.basic_processor import BasicMeetingProcessor
from utils.config import configure_lm, load_environment
import os
import time
import logging
from fastapi.middleware.cors import CORSMiddleware

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment
load_environment()

app = FastAPI(
    title="Meeting Ticket Extractor API",
    description="API for extracting actionable tickets from meeting notes",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class MeetingNotesRequest(BaseModel):
    notes: str
    model: Optional[str] = "mistral-tiny"
    use_optimized: Optional[bool] = False

class Ticket(BaseModel):
    title: str
    description: Optional[str] = None
    assignee: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[str] = None
    confidence: Optional[float] = None

class ProcessResponse(BaseModel):
    tickets: List[Ticket]
    processing_time: float
    model_used: str
    status: str

class HealthCheckResponse(BaseModel):
    status: str
    model_configured: bool
    available_models: List[str]

# Initialize processor
def get_processor(model_name="mistral-tiny", use_optimized=False):
    """Get processor instance"""
    try:
        # Configure LM
        configure_lm("mistral", model=model_name)
        
        # Create processor
        processor = BasicMeetingProcessor()
        
        # Load optimized version if available and requested
        if use_optimized and os.path.exists("optimized_processor.json"):
            try:
                processor.load("optimized_processor.json")
                logger.info("Loaded optimized processor")
            except Exception as e:
                logger.warning(f"Could not load optimized processor: {e}")
        
        return processor
    except Exception as e:
        logger.error(f"Failed to initialize processor: {e}")
        raise HTTPException(status_code=500, detail=f"Processor initialization failed: {e}")

@app.on_event("startup")
async def startup_event():
    """Startup event to initialize resources"""
    logger.info("Starting Meeting Ticket Extractor API...")
    
    # Test basic processor initialization
    try:
        test_processor = get_processor()
        logger.info("✅ Basic processor initialized successfully")
        
        # Check if optimized processor is available
        if os.path.exists("optimized_processor.json"):
            logger.info("✅ Optimized processor available")
        else:
            logger.info("ℹ️  No optimized processor found")
            
    except Exception as e:
        logger.error(f"❌ Failed to initialize processor: {e}")

@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint"""
    try:
        # Test processor initialization
        test_processor = get_processor()
        
        return {
            "status": "healthy",
            "model_configured": True,
            "available_models": ["mistral-tiny", "mistral-small", "mistral-medium"]
        }
    except Exception as e:
        return {
            "status": "degraded",
            "model_configured": False,
            "available_models": [],
            "error": str(e)
        }

@app.post("/process", response_model=ProcessResponse)
async def process_meeting_notes(request: MeetingNotesRequest):
    """Process meeting notes and extract tickets"""
    start_time = time.time()
    
    try:
        logger.info(f"Processing meeting notes with model: {request.model}")
        
        # Get processor
        processor = get_processor(request.model, request.use_optimized)
        
        # Process notes
        result = processor(request.notes)
        
        # Parse tickets
        tickets = result.tickets if hasattr(result, 'tickets') else []
        
        # Ensure tickets is a list
        if isinstance(tickets, str):
            import json
            try:
                tickets = json.loads(tickets)
            except:
                tickets = []
        elif not isinstance(tickets, list):
            tickets = [tickets] if tickets else []
        
        # Convert to response format
        response_tickets = []
        for ticket in tickets:
            response_ticket = Ticket(
                title=ticket.get('title', 'Untitled'),
                description=ticket.get('description'),
                assignee=ticket.get('assignee'),
                priority=ticket.get('priority'),
                due_date=ticket.get('due_date'),
                confidence=ticket.get('confidence')
            )
            response_tickets.append(response_ticket)
        
        processing_time = time.time() - start_time
        
        logger.info(f"Processed {len(response_tickets)} tickets in {processing_time:.2f}s")
        
        return {
            "tickets": response_tickets,
            "processing_time": processing_time,
            "model_used": request.model,
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"Processing failed: {e}")
        raise HTTPException(status_code=500, detail=f"Processing failed: {e}")

@app.post("/batch-process", response_model=List[ProcessResponse])
async def batch_process_notes(requests: List[MeetingNotesRequest]):
    """Process multiple meeting notes in batch"""
    results = []
    
    for i, request in enumerate(requests):
        try:
            logger.info(f"Processing batch item {i+1}/{len(requests)}")
            result = await process_meeting_notes(request)
            results.append(result)
        except Exception as e:
            logger.error(f"Batch item {i+1} failed: {e}")
            results.append({
                "tickets": [],
                "processing_time": 0,
                "model_used": request.model,
                "status": f"error: {e}"
            })
    
    return results

@app.get("/models")
async def get_available_models():
    """Get available models"""
    return {
        "models": [
            {
                "name": "mistral-tiny",
                "description": "Fast, cost-effective model",
                "recommended_for": "Quick testing and development"
            },
            {
                "name": "mistral-small",
                "description": "Balanced performance model",
                "recommended_for": "Production use with good accuracy"
            },
            {
                "name": "mistral-medium",
                "description": "Higher quality model",
                "recommended_for": "High accuracy requirements",
                "note": "Requires higher tier API access"
            }
        ]
    }

@app.get("/optimize-info")
async def get_optimization_info():
    """Get optimization status"""
    info = {
        "optimized_processor_available": os.path.exists("optimized_processor.json"),
        "optimization_methods": ["bootstrap", "mirov2"],
        "recommendation": "Use --use_optimized=true for better accuracy if available"
    }
    
    if info["optimized_processor_available"]:
        info["recommendation"] = "Optimized processor is available and recommended for production use"
    
    return info

if __name__ == "__main__":
    import uvicorn
    
    # Check if API key is available
    mistral_key = os.getenv("MISTRAL_API_KEY")
    if not mistral_key or mistral_key == "your-mistral-api-key-here":
        logger.warning("⚠️  Mistral API key not configured. API will run in degraded mode.")
        logger.warning("Please set MISTRAL_API_KEY in .env file")
    else:
        logger.info("✅ Mistral API key configured")
    
    # Run the API
    logger.info("Starting API server on http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Additional utility functions for API

def create_api_client():
    """Create a simple API client for testing"""
    import requests
    import json
    
    class MeetingTicketClient:
        def __init__(self, base_url="http://localhost:8000"):
            self.base_url = base_url
        
        def process_notes(self, notes, model="mistral-tiny", use_optimized=False):
            """Process meeting notes"""
            url = f"{self.base_url}/process"
            payload = {
                "notes": notes,
                "model": model,
                "use_optimized": use_optimized
            }
            
            try:
                response = requests.post(url, json=payload)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                logger.error(f"API client error: {e}")
                return {"error": str(e)}
        
        def health_check(self):
            """Check API health"""
            url = f"{self.base_url}/health"
            try:
                response = requests.get(url)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                return {"status": "error", "error": str(e)}
    
    return MeetingTicketClient()

if __name__ == "__main__":
    # The uvicorn.run() call above will block, so this is just for documentation
    pass