# fastapi_app.py
from fastapi import FastAPI, UploadFile, File
import pandas as pd
from pydantic import BaseModel, ValidationError
import io

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str
    price: float


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Check if the uploaded file is a CSV
    if file.filename.endswith(".csv"):
        contents = await file.read()
        # Convert bytes to file-like object
        csv_file = io.BytesIO(contents)
        
        # Parse the CSV file
        df = pd.read_csv(csv_file)
        print(df)
        # Validate and cleanse data
        try:
            items = df.to_dict(orient="records")
            validated_items = [Item(**item) for item in items]
            # Perform any data cleansing operations here
            # For example, removing duplicates, fixing errors, etc.
            cleansed_items = validated_items
            # Convert float values to strings
            cleansed_items = [{k: str(v) if isinstance(v, float) else v for k, v in item.items()} for item in cleansed_items]
            return {"items": cleansed_items}
        except ValidationError as e:
            return {"error": "Validation error", "details": e.errors()}
    else:
        return {"error": "Uploaded file is not a CSV"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
