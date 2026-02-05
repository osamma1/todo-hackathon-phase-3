import cohere.errors
try:
    print("Base of BadRequestError:", cohere.errors.BadRequestError.__bases__)
except Exception as e:
    print(e)
