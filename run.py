import subprocess
import os
from pathlib import Path
import sys
from src.utils.logger import setup_logger

def run_pipeline():
    """Run the end-to-end pipeline."""
    logger = setup_logger("config/config.yaml")
    logger.info("Starting end-to-end pipeline")
    
    # Set project root as working directory
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # Add project root to sys.path
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    # Define script paths
    scripts = [
        project_root / "src" / "ingestion" / "ingestion.py",
        project_root / "src" / "preprocessing" / "preprocess.py",
        project_root / "src" / "model" / "pricing_model.py",
        project_root / "src" / "genai" / "insights.py",
        project_root / "src" / "api" / "serve.py",
        project_root / "frontend" / "app.py"
    ]
    
    try:
        for i, script in enumerate(scripts):
            if not script.exists():
                logger.error(f"Script not found: {script}")
                raise FileNotFoundError(f"Script not found: {script}")
            
            logger.info(f"Executing script: {script}")
            if i in [1, 4, 5]:  # Preprocessing, API, and frontend run as servers
                subprocess.Popen(["python", str(script)])
            else:  # Ingestion, model, and GenAI run once
                subprocess.run(["python", str(script)], check=True)
    
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        raise

if __name__ == "__main__":
    run_pipeline()