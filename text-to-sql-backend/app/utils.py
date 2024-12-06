import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from typing import Optional

class SQLGenerator:
    def __init__(self, model_path: str):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_path).to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        
    def generate_sql(self, context: str, prompt: str) -> str:
        input_text = f"Context: {context}\nPrompt: {prompt}\nGenerate SQL Query:"
        inputs = self.tokenizer(
            input_text,
            return_tensors="pt",
            max_length=512,
            truncation=True,
            padding=True
        ).to(self.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=128,
                num_beams=5,
                temperature=0.7,
                do_sample=True,
                no_repeat_ngram_size=2,
                early_stopping=True
            )
        
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

def validate_sql(sql: str) -> Optional[str]:
    """
    Basic SQL validation and sanitization
    Returns None if SQL is valid, error message if not
    """
    sql = sql.strip().lower()
    
    # Check for basic SQL injection patterns
    dangerous_keywords = ['drop', 'delete', 'truncate', 'update', 'insert']
    if any(keyword in sql.lower() for keyword in dangerous_keywords):
        return "Unsafe SQL query detected"
    
    # Ensure query starts with SELECT
    if not sql.startswith('select'):
        return "Only SELECT queries are allowed"
    
    return None