from typing import Dict, Optional
from pydantic import BaseModel, ValidationError
import json

class Response(BaseModel):
    title: str
    topic: str
    summary: str
    content: str

    def model_dump(self) -> Dict[str, str]:
        return {
            "title": self.title,
            "topic": self.topic,
            "summary": self.summary,
            "content": self.content
        }

def clean_and_parse_response(response) -> Optional[Response]:
    try:
        # Clean the response string
        response_str = response.content.strip()
        
        # Remove markdown code block indicators if exist
        if response_str.startswith("```json"):
            response_str = response_str[7:]
        if response_str.endswith("```"):
            response_str = response_str[:-3]
        
        # Parse JSON
        parsed_json = json.loads(response_str)
        
        # Validate JSON
        validated_response = Response.model_validate(parsed_json)
        return validated_response
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None
    except ValidationError as e:
        print(f"Validation error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error in parsing response: {e}")
        return None