from apps.blog.models import Tag

def base(request):
	'''
	View that is inherited everywhere (for base template)
	'''
	return {'tags': Tag.objects.all()}