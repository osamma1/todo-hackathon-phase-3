# Example curl tests for endpoints

# 1. Test API root endpoint
curl -X GET http://localhost:8000/

# 2. Test getting tasks (requires valid JWT token)
curl -X GET http://localhost:8000/api/tasks \
  -H "Authorization: Bearer YOUR_VALID_JWT_TOKEN_HERE"

# 3. Test getting tasks with filtering and sorting
curl -X GET "http://localhost:8000/api/tasks?status=pending&sort=created" \
  -H "Authorization: Bearer YOUR_VALID_JWT_TOKEN_HERE"

# 4. Test creating a task (requires valid JWT token)
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_VALID_JWT_TOKEN_HERE" \
  -d '{"title": "Test task", "description": "This is a test task"}'

# 5. Test getting a specific task (requires valid JWT token)
curl -X GET http://localhost:8000/api/tasks/1 \
  -H "Authorization: Bearer YOUR_VALID_JWT_TOKEN_HERE"

# 6. Test updating a task (requires valid JWT token)
curl -X PUT http://localhost:8000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_VALID_JWT_TOKEN_HERE" \
  -d '{"title": "Updated task title", "description": "Updated description", "completed": true}'

# 7. Test toggling task completion (requires valid JWT token)
curl -X PATCH http://localhost:8000/api/tasks/1/complete \
  -H "Authorization: Bearer YOUR_VALID_JWT_TOKEN_HERE"

# 8. Test deleting a task (requires valid JWT token)
curl -X DELETE http://localhost:8000/api/tasks/1 \
  -H "Authorization: Bearer YOUR_VALID_JWT_TOKEN_HERE"

# 9. Test invalid token
curl -X GET http://localhost:8000/api/tasks \
  -H "Authorization: Bearer INVALID_TOKEN_HERE"

# 10. Test missing token
curl -X GET http://localhost:8000/api/tasks