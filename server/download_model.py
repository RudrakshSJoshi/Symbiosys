from transformers import AutoModelForCausalLM, AutoTokenizer
import os

def download_model(model_id: str = "nferruz/ProtGPT2", model_dir: str = "model_data"):
    """
    Download the ProtGPT2 model and tokenizer to the specified directory.
    
    Args:
        model_id: HuggingFace model identifier
        model_dir: Directory to save the model
    """
    print(f"Downloading model {model_id} to {model_dir}...")
    
    # Create directory if it doesn't exist
    os.makedirs(model_dir, exist_ok=True)
    
    try:
        # Download and save tokenizer
        print("Downloading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(model_id, cache_dir=model_dir)
        tokenizer.save_pretrained(os.path.join(model_dir, model_id.replace("/", "--")))
        
        # Download and save model
        print("Downloading model...")
        model = AutoModelForCausalLM.from_pretrained(model_id, cache_dir=model_dir)
        model.save_pretrained(os.path.join(model_dir, model_id.replace("/", "--")))
        
        print("✅ Download completed successfully!")
        print(f"Model saved to: {os.path.join(model_dir, model_id.replace('/', '--'))}")
        
    except Exception as e:
        print(f"❌ Error downloading model: {e}")

if __name__ == "__main__":
    # Download the model to your model_data directory
    download_model(model_id="nferruz/ProtGPT2", model_dir="model_data")