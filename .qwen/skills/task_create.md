# Add Task Skill

**Purpose**: Create a new task for the user.

**Endpoint/Call**: `POST /api/tasks`

**Parameters**:
- `title`: str (required) - The title of the task (1-200 characters)
- `description`: str (optional) - The description of the task (up to 1000 characters)

**Headers**:
- `Authorization`: Bearer token (required for authentication)

**Returns**:
```json
{
  "id": int,
  "user_id": str,
  "title": str,
  "description": str,
  "completed": bool,
  "created_at": datetime,
  "updated_at": datetime
}
```

**Behavior**: 
- Creates a new task record in the tasks table associated with the authenticated user
- Validates that the title is between 1-200 characters
- Validates that the description is less than 1000 characters if provided
- Sets the completion status to false by default
- Returns the newly created task object with all details

**Example Request**:
```bash
curl -X POST "http://localhost:8000/api/tasks" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project proposal",
    "description": "Finish writing the project proposal document and submit for review"
  }'
```

**Example Response**:
```json
{
  "id": 123,
  "user_id": "user_abc123",
  "title": "Complete project proposal",
  "description": "Finish writing the project proposal document and submit for review",
  "completed": false,
  "created_at": "2023-10-27T10:00:00",
  "updated_at": "2023-10-27T10:00:00"
}
```