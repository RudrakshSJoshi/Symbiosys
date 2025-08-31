# model_loader.py
import os
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

class ModelLoader:
    def __init__(self):
        self.protgpt2 = None
        self.is_loaded = False
    
    def load_model(self, model_dir: str = "model_data", model_id: str = "nferruz/ProtGPT2"):
        """Load the model once at application startup"""
        if self.is_loaded:
            return self.protgpt2
        
        # Check if model files exist in the specified directory
        model_path = os.path.join(model_dir, model_id.replace("/", "--"))
        
        # Check for common model files to determine if model is cached
        model_files_exist = (
            os.path.exists(model_path) and 
            any(fname.endswith(('.bin', '.pth', '.h5', '.json', '.txt', '.safetensors')) 
                for fname in os.listdir(model_path))
        )
        
        # If model exists locally, use local path with local_files_only
        if model_files_exist:
            print(f"Loading model from local cache: {model_path}")
            # Load model and tokenizer separately with local_files_only
            model = AutoModelForCausalLM.from_pretrained(
                model_path,
                local_files_only=True
            )
            tokenizer = AutoTokenizer.from_pretrained(
                model_path,
                local_files_only=True
            )
            
            # Create pipeline with loaded model and tokenizer
            self.protgpt2 = pipeline(
                'text-generation', 
                model=model,
                tokenizer=tokenizer
            )
        else:
            print(f"Model not found in {model_dir}, downloading from HuggingFace...")
            self.protgpt2 = pipeline(
                'text-generation', 
                model=model_id,
                cache_dir=model_dir
            )
        
        self.is_loaded = True
        print("Model loaded successfully!")
        return self.protgpt2

# Global instance
model_loader = ModelLoader()