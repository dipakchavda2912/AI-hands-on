from ast import List
import json
import re

class ParseUtils:
    # Extract and parse the JSON from the response
    def extract_json_from_response(self, message) -> list:
        """Extract JSON array from AIMessage content"""
        content = message.strip()
        
        # Remove markdown code blocks
        match = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', content, re.DOTALL)
        print("match:", match)
        if match:
            json_str = match.group(1).strip()
        else:
            json_str = content

        # Parse JSON
        return json.loads(json_str)
        
    def parse(self, response) -> list[dict]:
        response = response.strip()
        parsed_response = self.extract_json_from_response(response)
        content = []
        for item in parsed_response:
            content.append({"file": item, "content": item})
        print(f"Parsing Response: {content}")