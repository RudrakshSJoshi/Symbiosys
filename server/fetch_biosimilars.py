import asyncio
from typing import List
from fastapi import HTTPException

async def generate_biosimilars_async(
    model_loader,  # Just add this parameter
    fold_sequence: str,
    num_return_sequences: int = 2,
    max_length: int = 150,
    top_k: int = 950,
    repetition_penalty: float = 1.2,
    eos_token_id: int = 0,
) -> List[str]:
    """
    Asynchronously generate protein sequences using the pre-loaded ProtGPT2 model.
    """

    def _run_generation():
        """Synchronous function to run the model generation."""
        if not model_loader.is_loaded:
            raise HTTPException(status_code=500, detail="Model not loaded")
        
        # Preprocess the input sequence to follow FASTA format
        # Remove any existing newlines and format with 60 amino acids per line
        processed_sequence = preprocess_sequence(fold_sequence)
        
        # Generate sequences using the pre-loaded model
        sequences = model_loader.protgpt2(
            processed_sequence,
            max_length=max_length,
            do_sample=True,
            top_k=top_k,
            repetition_penalty=repetition_penalty,
            num_return_sequences=num_return_sequences,
            eos_token_id=eos_token_id
        )
        
        # Extract just the generated text and remove newlines
        return [clean_generated_sequence(seq['generated_text']) for seq in sequences]
    
    # Run the synchronous generation function in a thread pool
    loop = asyncio.get_event_loop()
    results = await loop.run_in_executor(None, _run_generation)
    
    return results


def preprocess_sequence(sequence: str) -> str:
    """
    Preprocess the input sequence to follow FASTA format with 60 amino acids per line.
    Adds <|endoftext|> tokens and formats with newlines every 60 characters.
    """
    # Remove any existing whitespace and newlines
    clean_seq = ''.join(sequence.split())
    
    # Format with newlines every 60 amino acids
    formatted_seq = ''
    for i in range(0, len(clean_seq), 60):
        formatted_seq += clean_seq[i:i+60] + '\n'
    
    # Add the special tokens
    processed_sequence = f"<|endoftext|>\n{formatted_seq}<|endoftext|>"
    
    return processed_sequence


def clean_generated_sequence(generated_text: str) -> str:
    """
    Clean the generated sequence by removing newlines and special tokens.
    Returns a clean amino acid sequence without formatting.
    """
    # Remove all newlines and whitespace
    clean_seq = ''.join(generated_text.split())
    
    # Remove the special tokens if they exist
    clean_seq = clean_seq.replace('<|endoftext|>', '')
    
    return clean_seq