from django import forms

from django.core.exceptions import ValidationError


class ListTextWidget(forms.TextInput):
	def __init__(self, data_list, name, *args, **kwargs):
		super(ListTextWidget, self).__init__(*args, **kwargs)
		self._name = name
		self._list = data_list
		self.attrs.update({'list':'list__%s' % self._name})

	def render(self, name, value, attrs=None):
		text_html = super(ListTextWidget, self).render(name, value, attrs=attrs)
		data_list = '<datalist id="list__%s">' % self._name
		
		for item in self._list:
			data_list += '<option value="%s">' % item
		data_list += '</datalist>'

		return (text_html + data_list)


	def getDataList():
		volunteer_group_list = ('Christ Church in Short Hills', 
			'Newark Academy', 
			'Newcomer\'s Short Hills', 
			'Worldwide Orphans', 
			'Investors Savings Bank', 
			'Summit Medical Group Foundation',
			'Freewalkers',
			'Winston School',
			'JAG Physical Therapy',
			'Seton Hall Nursing Students', 
			'Junior League of Oranges Short Hills', 
			'Sisterhood of Salaam Shalom',
			'Carpenter\'s Club', 
			'Clarity Refractive Services', 
			'Arturo\'s',
			'Temple Sharey Tefilo-Israel',
			'Congregation Beth El',
			'TBJ')

		return sorted(volunteer_group_list)

	def get_choices_list():
		l = [""] + ListTextWidget.getDataList()
		r = ['Other'] + ListTextWidget.getDataList()
		return list(zip(l,r))


#Another option for DataFields
class OptionalChoiceWidget(forms.MultiWidget):
    def decompress(self,value):
        #this might need to be tweaked if the name of a choice != value of a choice
        if value: #indicates we have a updating object versus new one
            if value in [x[0] for x in self.widgets[0].choices]:
                 return [value,""] # make it set the pulldown to choice
            else:
                 return ["",value] # keep pulldown to blank, set freetext
        return ["",""] # default for new object

class OptionalChoiceField(forms.MultiValueField):
    def __init__(self, choices, max_length=80, *args, **kwargs):
        """ sets the two fields as not required but will enforce that (at least) one is set in compress """
        fields = (forms.ChoiceField(choices=choices,required=False),
                  forms.CharField(required=False))
        self.widget = OptionalChoiceWidget(widgets=[f.widget for f in fields])
        super(OptionalChoiceField,self).__init__(required=False,fields=fields,*args,**kwargs)
    def compress(self,data_list):
        """ return the choicefield value if selected or charfield value (if both empty, will throw exception """
        if not data_list:
            raise ValidationError('If Other, please enter how you heard of the food pantry in the text box to the right')
        return data_list[0] or data_list[1]