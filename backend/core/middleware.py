from .models import Organization

class OrganizationMiddleware:
    def __init__(self, get_response):
        # get_response = the next middleware or view function in Django's request chain
        self.get_response = get_response

    def __call__(self, request):
        # This makes the middleware "callable" - Django calls this method for each request
        
        slug = request.headers.get("X-ORG")
        # Extract the "X-ORG" header value from the HTTP request
        # Returns None if header doesn't exist
        
        request.organization = (
            Organization.objects.filter(slug=slug).first()
            # Query database for Organization with matching slug
            # .first() returns the first match or None if not found
            if slug else None
        )
        
        return self.get_response(request)
        # Call the next middleware/view and return its response
        # This passes the request onwards in the Django chain