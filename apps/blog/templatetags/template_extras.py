from django import template
from urlobject import URLObject
from apps.blog.models import Tag

register = template.Library()

@register.simple_tag(name='add_tag', takes_context=True)
def add_tag(context, tagname):

	# Current url
	url = URLObject(context.request.get_full_path())
	url = url.add_query_param('tag', tagname)

	return url

@register.simple_tag(name='remove_tag', takes_context=True)
def remove_tag(context, tagname):

	# Current url
	url = URLObject(context.request.get_full_path())

	# Dictionary of tags in current url
	tagdict = url.query.multi_dict
	tagvalues = tagdict['tag']
	print(tagdict)
	print(tagvalues)


	# Remove the value of to be removed tagname
	tagvalues.remove(tagname)
	print(tagvalues)

	# Make clean url
	url = url.del_query_param('tag')

	# Add only the remaining tags to the new url
	for stay_tag in tagvalues:
		url = url.add_query_param('tag', stay_tag)

	return url

@register.simple_tag(name='go_to_page', takes_context=True)
def go_to_page(context, pagenumber):
	url = URLObject(context.request.get_full_path())
	url = url.set_query_param('page', pagenumber)
	return url