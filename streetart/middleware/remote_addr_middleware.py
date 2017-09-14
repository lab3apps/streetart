from django.http import HttpResponse

class RemoteAddrMiddleware(object):
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		return self.get_response(request)

	def process_exception(self, request, exception): 
		return HttpResponse("in exception")

	def process_request(self, request):
		if 'HTTP_X_FORWARDED_FOR' in request.META:
			ip = request.META['HTTP_X_FORWARDED_FOR'].split(',')[0].strip()
			request.META['REMOTE_ADDR'] = ip